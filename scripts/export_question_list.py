"""Write <PROFILE>_모의고사_질문목록.md (10 sets x 15 questions) to data/share/ for sharing."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import practice_bank as kt
import practice_bank_instrument as sh

# Survey order follows survey.py; no_exercise is a survey answer, not a topic.
SURVEYS = {
    'KT': (kt, 'movies, shows, concerts, park, gaming, reading, jogging, walking, no_exercise, vacation, travel, travel_abroad'),
    'SH': (sh, 'shows, concerts, park, instrument, jogging, walking, yoga, gym, vacation, travel, travel_abroad'),
}


def render(profile):
    bank, survey = SURVEYS[profile]
    lines = [f'# {profile} OPIc 모의고사 질문 목록 (01–10회차)', '',
             f'설문: {survey}  ',
             f'난이도 5–5 · 회차당 15문항 · 문제은행 `{bank.BANK_VERSION}` · 자체 제작 연습문항(공식 기출 아님)', '']
    for n in range(1, 11):
        lines += [f'## {n:02}회차', '', '| # | 주제 | 유형 | 질문 |', '|---|---|---|---|']
        for i, q in enumerate(bank.authored_questions(bank.REQUIRED_TOPICS, n), 1):
            lines.append(f"| {i} | {q['topic']} | {q['type']} | {q['prompt'].replace('|', '/')} |")
        lines.append('')
    return '\n'.join(lines)


if __name__ == '__main__':
    out = ROOT / 'data/share'
    out.mkdir(parents=True, exist_ok=True)
    for profile in sys.argv[1:] or SURVEYS:
        path = out / f'{profile}_모의고사_질문목록.md'
        path.write_text(render(profile), encoding='utf-8')
        print(path)
