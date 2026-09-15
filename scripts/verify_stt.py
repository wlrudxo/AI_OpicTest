"""Verify cached CUDA model against downloaded English, WebM and silent fixtures."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from stt import load_model, transcribe


def main():
    model = load_model()
    expected = 'and so my fellow americans ask not what your country can do for you ask what you can do for your country'
    reports = []
    for name in ['jfk.flac', 'jfk.webm', 'silence.wav']:
        result = transcribe(model, ROOT / 'data/verification' / name)
        if name == 'silence.wav':
            assert result['status'] == 'no_speech' and not result['text'], result
        else:
            normalized = ' '.join(re.findall(r'[a-z]+', result['text'].lower()))
            assert normalized == expected, result['text']
            assert any(s['words'] for s in result['segments']), 'Missing word timestamps'
        reports.append({k: v for k, v in result.items() if k != 'segments'})
    target = ROOT / 'data/verification/report.json'
    target.write_text(json.dumps(reports, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(reports, indent=2))


if __name__ == '__main__':
    main()
