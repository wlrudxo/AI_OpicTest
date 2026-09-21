"""Check authored-set coverage, role instructions, snapshots and API boundaries."""
import asyncio
from collections import Counter
from pathlib import Path
import re
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pydantic import ValidationError
import mock_api
from practice_bank import SETS, REQUIRED_TOPICS, TYPE_LABELS, MAX_SETS
from questions import build_questions, adjusted_prompt

SELECTION = ['movies', 'shows', 'concerts', 'park', 'gaming', 'reading',
             'jogging', 'walking', 'no_exercise', 'vacation', 'travel', 'travel_abroad']


async def check_api():
    for invalid in (0, 11):
        try:
            mock_api.Setup(topics=SELECTION, set_number=invalid)
        except ValidationError:
            pass
        else:
            raise AssertionError('out-of-range set accepted')
    with TemporaryDirectory() as directory, patch.object(mock_api, 'ROOT', Path(directory)):
        saved = []
        for number in range(1, 11):
            session = await mock_api.create(mock_api.Setup(topics=SELECTION, set_number=number))
            assert session['status'] == 'ready' and session['started_at'] is None
            assert session['questions'] == build_questions(SELECTION, number, 5)
            saved.append(session)
        # Reading an existing session must never regenerate its questions.
        old = saved[0]
        old['questions'][1]['prompt'] = 'Stored legacy prompt that must remain unchanged.'
        mock_api.save(old)
        with patch.object(mock_api, 'build_questions', side_effect=AssertionError('must not regenerate')):
            loaded = await mock_api.get_session(old['id'])
        assert loaded['questions'][1]['prompt'] == old['questions'][1]['prompt']
        for choice, number in (('easier', 2), ('same', 3), ('harder', 4)):
            s = saved[number - 1]
            s.update(status='active', cursor=7)
            mock_api.save(s)
            result = await mock_api.adjust(s['id'], mock_api.Adjust(choice=choice))
            assert result['questions'][:7] == s['questions'][:7]
            for q in result['questions'][10:12]:
                assert q['base_prompt'] in q['prompt'], 'role instructions were lost'


def main():
    assert len(SETS) == MAX_SETS == 10
    questions = []
    observed_topics = set()
    for number in range(1, 11):
        assert [len(b) for b in SETS[number-1]] == [3, 3, 3, 3, 2]
        standard = build_questions(SELECTION, number, 5)
        assert len(standard) == 15
        assert [q['type_id'] for q in standard[10:13]] == ['T11', 'T12', 'T08']
        assert standard[12]['roleplay_followup']
        assert standard == build_questions(list(reversed(SELECTION)), number, 5)
        for q in standard:
            assert q['type_id'] in TYPE_LABELS
            assert q['provenance'] == 'original'
            if q['origin'] == 'survey':
                assert q['topic_id'] in SELECTION
                observed_topics.add(q['topic_id'])
            assert q['topic_id'] != 'no_exercise'
        for level in range(1, 7):
            result = build_questions(SELECTION, number, level)
            assert len(result) == (12 if level <= 2 else 15)
            assert [q['id'] for q in result] == [f'q{i:02d}' for i in range(1,len(result)+1)]
            for q in result[10:12]:
                assert q['base_prompt'] in q['prompt']
                assert adjusted_prompt(q, 'easier') == q['base_prompt']
        questions.extend(standard)
    assert observed_topics == REQUIRED_TOPICS
    assert len({q['content_id'] for q in questions}) == 150
    repeats = {text:count for text,count in Counter(q['prompt'] for q in questions).items() if count > 1}
    assert len(repeats) == 1 and next(iter(repeats.values())) == 10, repeats
    assert set(q['type_id'] for q in questions) == set(TYPE_LABELS)
    # No topic or difficulty hints in the set chooser; exactly ten numbered options.
    html = (Path(__file__).resolve().parents[1] / 'static/index.html').read_text(encoding='utf-8')
    select = re.search(r'<select id="set-number">(.*?)</select>', html, re.S).group(1)
    assert re.findall(r'<option value="(\d+)">(.*?)</option>', select) == [(str(n),f'{n:02d}') for n in range(1,11)]
    asyncio.run(check_api())
    print('PASS: 10 x 15 positions, 141 unique prompts, 14 types, 11 selected activity topics, 6 levels, intact role instructions, saved sessions, API range, hint-free chooser')


if __name__ == '__main__':
    main()
