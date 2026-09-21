"""Single-user microphone test, served only on localhost."""
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
import json
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware

import stt
import mock_api
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parent
RECORDINGS = ROOT / 'data' / 'recordings'
gpu_lock = asyncio.Lock()


@asynccontextmanager
async def lifespan(app):
    RECORDINGS.mkdir(parents=True, exist_ok=True)
    app.state.model = await asyncio.to_thread(stt.load_model)
    mock_api.recover()
    worker = asyncio.create_task(mock_api.worker(app.state.model, gpu_lock))
    yield
    worker.cancel()
    try:
        await worker
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=['127.0.0.1', 'localhost'])
app.include_router(mock_api.router)
app.mount('/static', StaticFiles(directory=ROOT / 'static'), name='static')


@app.middleware('http')
async def local_requests(request, call_next):
    if request.method in ['POST', 'PUT', 'DELETE'] and request.headers.get('origin') not in (None, 'http://127.0.0.1:8765', 'http://localhost:8765'):
        from fastapi.responses import JSONResponse
        return JSONResponse({'detail': '허용되지 않은 요청입니다.'}, status_code=403)
    return await call_next(request)


@app.get('/mic')
async def mic():
    return FileResponse(ROOT / 'static/mic.html')


@app.get('/')
async def index():
    return FileResponse(ROOT / 'static/index.html')


@app.get('/api/health')
async def health():
    return {'ready': True, 'model': 'large-v3', 'device': 'cuda'}


@app.post('/api/transcribe')
async def upload(request: Request):
    if request.headers.get('origin') not in (None, 'http://127.0.0.1:8765', 'http://localhost:8765'):
        raise HTTPException(403, '허용되지 않은 요청입니다.')
    mime = request.headers.get('content-type', '').split(';')[0]
    suffix = {'audio/webm': '.webm', 'audio/ogg': '.ogg', 'audio/mp4': '.mp4', 'audio/wav': '.wav'}.get(mime)
    if not suffix:
        raise HTTPException(415, '지원하지 않는 녹음 형식입니다.')
    parts, size = [], 0
    async for chunk in request.stream():
        size += len(chunk)
        if size > 30 * 1024 * 1024:
            raise HTTPException(413, '녹음은 30MB 이하로 보내주세요.')
        parts.append(chunk)
    if size == 0:
        raise HTTPException(400, '빈 녹음입니다.')
    stem = datetime.now().strftime('%Y%m%d-%H%M%S-') + uuid4().hex[:8]
    path = RECORDINGS / (stem + suffix)
    path.write_bytes(b''.join(parts))
    try:
        async with gpu_lock:
            result = await asyncio.to_thread(stt.transcribe, app.state.model, path)
    except Exception as error:
        raise HTTPException(500, f'음성은 {path.name}에 저장했습니다. 전사 실패: {error}') from error
    result['model'] = 'large-v3'
    (RECORDINGS / (stem + '.json')).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return result


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8765)
