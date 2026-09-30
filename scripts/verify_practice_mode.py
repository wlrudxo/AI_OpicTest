"""Check practice mode: no deadline, stay on a question after recording, retries and /next."""
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastapi import FastAPI
from fastapi.testclient import TestClient
import mock_api

SELECTION = ['movies', 'shows', 'concerts', 'park', 'gaming', 'reading',
             'jogging', 'walking', 'no_exercise', 'vacation', 'travel', 'travel_abroad']
AUDIO = {'Content-Type': 'audio/webm'}
SKIP = {'Content-Type': 'application/x-opic-skip'}


def upload(client, sid, qid, headers, body=b'fake-webm'):
    r = client.post(f'/api/sessions/{sid}/answers/{qid}', content=body if headers is AUDIO else b'',
                    headers={**headers, 'X-Answer-Id': str(uuid4())})
    assert r.status_code == 200, r.text
    return r.json()


def main():
    app = FastAPI()
    app.include_router(mock_api.router)
    client = TestClient(app)
    with TemporaryDirectory() as directory, patch.object(mock_api, 'ROOT', Path(directory)):
        body = {'topics': SELECTION, 'level': 5, 'set_number': 3, 'mode': 'practice', 'profile_id': 'KT'}
        s = client.post('/api/sessions', json=body).json()
        sid = s['id']
        s = client.post(f'/api/sessions/{sid}/start').json()
        assert s['status'] == 'active' and s['deadline'] is None, 'practice must have no deadline'
        assert client.post(f'/api/sessions/{sid}/play').status_code == 200
        # Recording keeps the cursor on the same question; retries are numbered attempts.
        s = upload(client, sid, 'q01', AUDIO)
        assert s['cursor'] == 0 and s['answers'][-1]['attempt'] == 1
        s = upload(client, sid, 'q01', AUDIO)
        assert s['cursor'] == 0 and s['answers'][-1]['attempt'] == 2
        for _ in range(3):  # play count is unlimited in practice
            assert client.post(f'/api/sessions/{sid}/play').status_code == 200
        # A stale /next for another question must not advance.
        assert client.post(f'/api/sessions/{sid}/next', json={'question_id': 'q02'}).json()['cursor'] == 0
        assert client.post(f'/api/sessions/{sid}/next', json={'question_id': 'q01'}).json()['cursor'] == 1
        assert client.post(f'/api/sessions/{sid}/next', json={'question_id': 'q01'}).json()['cursor'] == 1
        # Skipping still moves on.
        s = upload(client, sid, 'q02', SKIP)
        assert s['cursor'] == 2
        for n in range(3, 8):
            upload(client, sid, f'q{n:02d}', AUDIO)
            s = client.post(f'/api/sessions/{sid}/next', json={'question_id': f'q{n:02d}'}).json()
        assert s['cursor'] == 7
        s = client.post(f'/api/sessions/{sid}/adjust', json={'choice': 'same'}).json()
        for n in range(8, 16):
            upload(client, sid, f'q{n:02d}', AUDIO)
            assert s['status'] == 'active'
            s = client.post(f'/api/sessions/{sid}/next', json={'question_id': f'q{n:02d}'}).json()
        assert s['status'] == 'completed' and s['cursor'] == 15
        review = client.get(f'/api/sessions/{sid}/review').text
        assert '시도 2' in review and review.count('## ') == 15

        # Exam mode is unchanged: 40-minute deadline, recording advances, no /next.
        e = client.post('/api/sessions', json={**body, 'mode': 'exam'}).json()
        e = client.post(f"/api/sessions/{e['id']}/start").json()
        assert 2395 < e['deadline'] - e['started_at'] <= 2400
        e = upload(client, e['id'], 'q01', AUDIO)
        assert e['cursor'] == 1 and e['answers'][0]['attempt'] == 1
        assert client.post(f"/api/sessions/{e['id']}/next", json={'question_id': 'q02'}).status_code == 409
    print('PASS: practice has no deadline, stays on the question after recording, numbered retries, guarded /next, skip advances, 15-question completion, attempts in review; exam flow unchanged')


if __name__ == '__main__':
    main()
