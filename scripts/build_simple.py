"""Build simple/index.html into data/share/simple/index.html (KT·SH 10 sets each, browser TTS only)."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import practice_bank as kt
import practice_bank_instrument as sh

LABELS = {'KT': '영화·공연·콘서트·공원·게임·독서', 'SH': '공연·콘서트·공원·악기·헬스·요가'}
FIELDS = ('topic', 'type', 'prompt')


def main():
    profiles = {}
    for key, bank in (('KT', kt), ('SH', sh)):
        sets = [[{f: q[f] for f in FIELDS} for q in bank.authored_questions(bank.REQUIRED_TOPICS, n)]
                for n in range(1, 11)]
        assert all(len(s) == 15 for s in sets)
        profiles[key] = {'label': LABELS[key], 'version': bank.BANK_VERSION, 'sets': sets}
    data = json.dumps({'profiles': profiles}, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    src = ROOT / 'simple'
    html = (src / 'index.html').read_text(encoding='utf-8')
    parts = {'__SPEECH__': (ROOT / 'static/browser-speech.js').read_text(encoding='utf-8'),
             '__APP__': (src / 'app.js').read_text(encoding='utf-8'),
             '__DATA__': data}
    for key, value in parts.items():
        assert html.count(key) == 1, key
        html = html.replace(key, value)
    target = ROOT / 'data/share/simple/index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding='utf-8')
    print(json.dumps({'html': str(target), 'KB': round(target.stat().st_size / 1e3, 1)}))


if __name__ == '__main__':
    main()
