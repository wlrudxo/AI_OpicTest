"""Validate standalone browser-TTS bundles without models or generated audio."""
from pathlib import Path
import json
import re
import sys
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import practice_bank as kt
import practice_bank_instrument as sh

for profile, bank in [('SH', sh), ('KT', kt)]:
    folder = ROOT / 'data/share' / f'OPIc_{profile}_5-5'
    html = (folder / 'index.html').read_text(encoding='utf-8')
    payload = json.loads(re.search(r'<script id="practice-data" type="application/json">(.*?)</script>', html, re.S)[1])
    assert payload['profile'] == profile
    assert payload['sets'] == [bank.authored_questions(bank.REQUIRED_TOPICS, n) for n in range(1, 11)]
    assert len(payload['sets']) == 10 and all(len(qs) == 15 for qs in payload['sets'])
    assert 'audio' not in payload and 'data:audio' not in html
    assert 'SpeechSynthesisUtterance' in html
    assert not re.search(r'__(?:DATA|APP|STYLE|PROFILE|OPTIONS|SPEECH)__', html)
    assert 'MediaRecorder' not in html
    assert len(html.encode('utf-8')) < 250_000
    with ZipFile(folder.with_suffix('.zip')) as z:
        assert set(z.namelist()) == {f'{folder.name}/{n}' for n in ('index.html', 'START.bat', 'serve.ps1', '사용안내.txt')}
        assert z.testzip() is None
        assert z.read(f'{folder.name}/index.html') == (folder / 'index.html').read_bytes()
print('PASS: 2 x 10 x 15 matching prompts, browser TTS, HTML under 250 KB, 4-file ZIP allowlist, no audio/model payloads')
