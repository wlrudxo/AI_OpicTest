"""Integration checks against the local running server using an existing audio fixture."""
import json
from pathlib import Path
import time
from uuid import uuid4
import requests

BASE = 'http://127.0.0.1:8765/api'
ROOT = Path(__file__).resolve().parents[1]
created = []


def call(path, method='GET', **kwargs):
    response = requests.request(method, BASE+path, timeout=30, **kwargs)
    response.raise_for_status()
    return response.json()


def main():
    topics=['movies','shows','concerts','park','camping','beach','music','cooking','walking','jogging','vacation','travel']
    body={'topics':topics,'level':5,'occupation':'자동 검증', 'student':'아니오','residence':'혼자 거주'}
    assert requests.post(BASE+'/sessions',json={**body,'topics':['movies']}).status_code==400
    s=call('/sessions','POST',json=body);sid=s['id'];created.append(sid);prefix='/sessions/'+sid
    assert len(s['questions'])==15
    s=call(prefix+'/start','POST');assert 2395<s['deadline']-time.time()<=2400
    for _ in range(2):call(prefix+'/play','POST')
    assert requests.post(BASE+prefix+'/play').status_code==409
    fixture=(ROOT/'data/verification/jfk.webm').read_bytes();token=str(uuid4())
    opts={'data':fixture,'headers':{'Content-Type':'audio/webm','X-Answer-Id':token}}
    s=call(prefix+'/answers/q01','POST',**opts);assert s['cursor']==1
    duplicate=call(prefix+'/answers/q01','POST',**opts);assert duplicate['cursor']==1 and len(duplicate['answers'])==1
    assert requests.post(BASE+prefix+'/answers/q03',**{**opts,'headers':{'Content-Type':'audio/webm','X-Answer-Id':str(uuid4())}}).status_code==409
    for i in range(2,8):
        s=call(prefix+f'/answers/q{i:02d}','POST',headers={'Content-Type':'application/x-opic-skip','X-Answer-Id':str(uuid4())})
    before=s['questions'][7]['prompt'];s=call(prefix+'/adjust','POST',json={'choice':'harder'})
    assert s['adjustment']=='harder' and s['questions'][7]['prompt']!=before
    assert requests.post(BASE+prefix+'/adjust',json={'choice':'same'}).status_code==409
    for i in range(8,16):
        s=call(prefix+f'/answers/q{i:02d}','POST',headers={'Content-Type':'application/x-opic-skip','X-Answer-Id':str(uuid4())})
    assert s['status']=='completed' and s['cursor']==15
    for _ in range(30):
        s=call(prefix)
        if s['answers'][0]['stt_status'] not in ['queued','running']:break
        time.sleep(.5)
    a=s['answers'][0];assert a['stt_status']=='completed' and 'fellow Americans' in a['transcript_raw']
    response=requests.get(BASE+prefix+'/audio/'+token);assert response.content==fixture
    raw=a['transcript_raw'];call(prefix+'/answers/'+token,'PUT',json={'text':'Edited test transcript'})
    a=call(prefix)['answers'][0];assert a['transcript_raw']==raw and a['transcript_edited']=='Edited test transcript'
    response=requests.get(BASE+prefix+'/review');assert response.ok and 'Edited test transcript' in response.text
    low=call('/sessions','POST',json={**body,'level':2});created.append(low['id']);assert len(low['questions'])==12
    call('/sessions/'+low['id']+'/finish','POST')
    assert requests.post(BASE+'/sessions',json=body,headers={'Origin':'https://example.com'}).status_code==403
    report={'passed':['survey_validation','15_and_12_questions','40_minute_deadline','two_plays','idempotent_audio_save','question_order','midpoint_adjustment','completion','cuda_transcription','audio_roundtrip','edit_preserves_raw','review_export','origin_check'],'sessions':created}
    (ROOT/'data/verification/mock-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
    # Archive only the synthetic sessions created above, retaining verification evidence.
    destination=ROOT/'data/verification/sessions';destination.mkdir(exist_ok=True)
    for sid in created:
        source=(ROOT/'data/sessions'/sid).resolve();target=(destination/sid).resolve()
        assert source.parent==(ROOT/'data/sessions').resolve() and target.parent==destination.resolve()
        source.rename(target)


if __name__=='__main__':
    main()
