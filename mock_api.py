import asyncio
import json
from pathlib import Path
import re
import time
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, PlainTextResponse
from pydantic import BaseModel, Field

import stt
import tts
from questions import TOPICS, build_questions
from survey import catalog, GROUPS

router = APIRouter(prefix='/api')
ROOT = Path(__file__).resolve().parent / 'data/sessions'
queue = asyncio.Queue()


def folder(sid):
    if not re.fullmatch(r'[0-9a-f]{32}', sid):
        raise HTTPException(404, '세션이 없습니다.')
    return ROOT / sid


def read(sid):
    path = folder(sid) / 'session.json'
    if not path.exists():
        raise HTTPException(404, '세션이 없습니다.')
    return json.loads(path.read_text(encoding='utf-8'))


def save(s):
    directory = folder(s['id'])
    directory.mkdir(parents=True, exist_ok=True)
    temp = directory / 'session.tmp'
    temp.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding='utf-8')
    temp.replace(directory / 'session.json')


def answer(s, aid):
    for item in s['answers']:
        if item['id'] == aid:
            return item
    raise HTTPException(404, '답변이 없습니다.')


async def worker(model, gpu_lock):
    while True:
        sid, aid = await queue.get()
        try:
            s = read(sid)
            a = answer(s, aid)
            a['stt_status'] = 'running'
            save(s)
            async with gpu_lock:
                result = await asyncio.to_thread(stt.transcribe, model, folder(sid) / a['file'])
            s = read(sid)
            a = answer(s, aid)
            a.update(stt_status=result['status'], transcript_raw=result['text'], result=result, error=None)
            save(s)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            s = read(sid)
            answer(s, aid).update(stt_status='failed', error=str(exc))
            save(s)
        finally:
            queue.task_done()


def recover():
    ROOT.mkdir(parents=True, exist_ok=True)
    for path in ROOT.glob('*/session.json'):
        s = json.loads(path.read_text(encoding='utf-8'))
        for a in s['answers']:
            if a['stt_status'] in ['queued', 'running']:
                a['stt_status'] = 'queued'
                queue.put_nowait((s['id'], a['id']))
        save(s)


class Setup(BaseModel):
    topics: list[str]
    level: int = Field(default=5, ge=1, le=6)
    set_number: int = Field(default=1, ge=1, le=3)
    mode: str = 'exam'
    occupation: str = Field(default='직장인', max_length=100)
    student: str = Field(default='아니오', max_length=100)
    residence: str = Field(default='혼자 거주', max_length=100)
    study_type: str = Field(default='', max_length=100)


@router.get('/topics')
async def topics():
    return catalog()


def validate_setup(body):
    keys = {item['id'] for item in catalog()}
    if len(set(body.topics)) < 12 or any(t not in keys for t in body.topics) or body.mode not in ['exam', 'practice']:
        raise HTTPException(400, '설문 항목을 12개 이상 선택해주세요.')
    for group, title, minimum, items in GROUPS:
        if len(set(body.topics) & {i[0] for i in items}) < minimum:
            raise HTTPException(400, f'{title} {minimum}개 이상 선택해주세요.')


@router.post('/speech/prepare')
async def prepare_speech(body: Setup):
    validate_setup(body)
    questions = build_questions(body.topics, body.set_number, body.level)
    tts.prepare(q['prompt'] for q in questions)
    return {'status': 'preparing', 'count': len(questions)}


@router.post('/sessions')
async def create(body: Setup):
    validate_setup(body)
    s = {'id': uuid4().hex, 'setup': body.model_dump(), 'created_at': time.time(), 'started_at': None,
         'deadline': None, 'status': 'ready', 'cursor': 0, 'adjustment': None,
         'questions': build_questions(body.topics, body.set_number, body.level), 'plays': {}, 'answers': []}
    save(s)
    tts.prepare(q['prompt'] for q in s['questions'])
    return s


@router.get('/sessions')
async def history():
    out = []
    for path in ROOT.glob('*/session.json'):
        s = json.loads(path.read_text(encoding='utf-8'))
        out.append({k: s[k] for k in ['id', 'created_at', 'status', 'cursor', 'setup']})
    return sorted(out, key=lambda s: s['created_at'], reverse=True)


@router.get('/sessions/{sid}')
async def get_session(sid: str):
    s = read(sid)
    if s['status'] in ['ready', 'active']:
        tts.prepare(q['prompt'] for q in s['questions'][s['cursor']:])
    feedback = folder(sid) / 'feedback.json'
    s['feedback'] = json.loads(feedback.read_text(encoding='utf-8')) if feedback.exists() else None
    return s


@router.post('/sessions/{sid}/start')
async def start(sid: str):
    s = read(sid)
    if s['status'] == 'ready':
        s.update(status='active', started_at=time.time(), deadline=time.time()+2400)
        save(s)
    return s


def current(s):
    if s['status'] != 'active' or s['cursor'] >= len(s['questions']):
        raise HTTPException(409, '진행 중인 문항이 없습니다.')
    return s['questions'][s['cursor']]


@router.post('/sessions/{sid}/play')
async def play(sid: str):
    s = read(sid)
    q = current(s)
    if time.time() >= s['deadline']:
        raise HTTPException(409, '시험 시간이 종료되었습니다.')
    if s['cursor'] == 7 and s['adjustment'] is None:
        raise HTTPException(409, '먼저 난이도를 다시 선택해주세요.')
    n = s['plays'].get(q['id'], 0)
    if n >= 2 and s['setup']['mode'] == 'exam':
        raise HTTPException(409, '질문은 두 번까지 들을 수 있습니다.')
    s['plays'][q['id']] = n+1
    save(s)
    return {'count': n+1}


class Adjust(BaseModel):
    choice: str


@router.post('/sessions/{sid}/adjust')
async def adjust(sid: str, body: Adjust):
    s = read(sid)
    if s['status'] != 'active' or s['cursor'] != 7 or s['adjustment'] is not None or body.choice not in ['easier', 'same', 'harder']:
        raise HTTPException(409, '난이도 변경 단계가 아닙니다.')
    s['adjustment'] = body.choice
    for q in s['questions'][7:]:
        if body.choice == 'easier':
            q['prompt'] = q['base_prompt'].split('. ')[0] + '.'
        elif body.choice == 'harder':
            q['prompt'] = q['base_prompt'] + ' Explain why, and describe how the situation might have turned out differently.'
    save(s)
    tts.prepare(q['prompt'] for q in s['questions'][7:])
    return s


@router.post('/sessions/{sid}/answers/{qid}')
async def upload_answer(sid: str, qid: str, request: Request):
    token = request.headers.get('x-answer-id', '')
    if not re.fullmatch(r'[a-zA-Z0-9-]{10,64}', token):
        raise HTTPException(400, '답변 식별자가 필요합니다.')
    s = read(sid)
    if any(a['id'] == token for a in s['answers']):
        return s
    if current(s)['id'] != qid:
        raise HTTPException(409, '현재 문항과 일치하지 않습니다.')
    mime = request.headers.get('content-type', '').split(';')[0]
    suffix = {'audio/webm': '.webm', 'audio/ogg': '.ogg', 'audio/mp4': '.mp4', 'audio/wav': '.wav'}.get(mime)
    skipped = mime == 'application/x-opic-skip'
    if not suffix and not skipped:
        raise HTTPException(415, '녹음 형식을 지원하지 않습니다.')
    chunks, size = [], 0
    async for chunk in request.stream():
        size += len(chunk)
        if size > 60 * 1024 * 1024:
            raise HTTPException(413, '녹음 파일이 너무 큽니다.')
        chunks.append(chunk)
    if not size and not skipped:
        raise HTTPException(400, '빈 녹음입니다. 다시 시도해주세요.')
    # Re-read after awaiting upload, so double clicks cannot advance twice.
    s = read(sid)
    if any(a['id'] == token for a in s['answers']):
        return s
    if current(s)['id'] != qid:
        raise HTTPException(409, '이미 저장된 문항입니다.')
    filename = qid + '-' + token + (suffix or '')
    if not skipped:
        (folder(sid) / filename).write_bytes(b''.join(chunks))
    s['answers'].append({'id': token, 'question_id': qid, 'file': None if skipped else filename,
                         'stt_status': 'skipped' if skipped else 'queued', 'transcript_raw': '',
                         'transcript_edited': None, 'saved_at': time.time()})
    s['cursor'] += 1
    if s['cursor'] >= len(s['questions']) or time.time() >= s['deadline']:
        s['status'] = 'completed'
    save(s)
    if not skipped:
        queue.put_nowait((sid, token))
    return s


@router.post('/sessions/{sid}/finish')
async def finish(sid: str):
    s = read(sid)
    s['status'] = 'completed'
    save(s)
    return s


@router.get('/sessions/{sid}/audio/{aid}')
async def audio(sid: str, aid: str):
    a = answer(read(sid), aid)
    if not a['file']:
        raise HTTPException(404, '건너뛴 문항입니다.')
    return FileResponse(folder(sid) / a['file'])


class Edit(BaseModel):
    text: str = Field(max_length=20000)


@router.put('/sessions/{sid}/answers/{aid}')
async def edit(sid: str, aid: str, body: Edit):
    s = read(sid)
    answer(s, aid)['transcript_edited'] = body.text
    save(s)
    return {'saved': True}


@router.post('/sessions/{sid}/answers/{aid}/retry')
async def retry(sid: str, aid: str):
    s = read(sid)
    a = answer(s, aid)
    if not a['file'] or a['stt_status'] in ['queued', 'running']:
        raise HTTPException(409, '재처리할 수 없는 상태입니다.')
    a['stt_status'] = 'queued'
    save(s)
    queue.put_nowait((sid, aid))
    return {'queued': True}


@router.get('/sessions/{sid}/review')
async def review(sid: str):
    s = read(sid)
    lines = [f'# OPIc 모의시험 {sid}', '', f"설정: {s['setup']}", '', '원본 음성을 유지하고 STT 오류를 영어 오류와 구분해 평가하세요.', '']
    for q in s['questions']:
        lines += [f"## {q['order']}. {q['topic']} / {q['type']}", q['prompt'], '']
        matches = [a for a in s['answers'] if a['question_id'] == q['id']]
        if not matches:
            lines += ['미응답', '']
        for a in matches:
            lines += [f"상태: {a['stt_status']}", f"음성: {folder(sid) / a['file'] if a['file'] else '없음'}", f"원본 전사: {a['transcript_raw']}"]
            if a['transcript_edited'] is not None:
                lines += [f"수정 전사: {a['transcript_edited']}"]
            lines += ['']
    text = '\n'.join(lines)
    (folder(sid) / 'review.md').write_text(text, encoding='utf-8')
    return PlainTextResponse(text, headers={'Content-Disposition': 'attachment; filename="review.md"'})
