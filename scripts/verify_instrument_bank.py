"""Check survey routing, linked role-play, uniqueness and 5-5 session behavior."""
import asyncio
from collections import Counter
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import mock_api
from practice_bank_instrument import SETS, REQUIRED_TOPICS, BANK_VERSION
from practice_bank import TYPE_LABELS
from questions import build_questions

SELECTION = ['movies', 'shows', 'concerts', 'park', 'instrument', 'jogging',
             'walking', 'gym', 'no_exercise', 'vacation', 'travel', 'travel_abroad']


async def check_sessions():
    with TemporaryDirectory() as directory, patch.object(mock_api, 'ROOT', Path(directory)):
        for number in range(1, 11):
            s = await mock_api.create(mock_api.Setup(topics=SELECTION, level=5, set_number=number,
                                                   occupation='일 경험 없음', student='아니오', profile_id='SH'))
            assert s['questions'] == build_questions(SELECTION, number, 5)
            s.update(status='active', cursor=7)
            mock_api.save(s)
            result = await mock_api.adjust(s['id'], mock_api.Adjust(choice='same'))
            assert result['questions'] == s['questions'], '5-5 changed the prompts'
            loaded = await mock_api.get_session(s['id'])
            assert loaded['questions'] == s['questions']
            assert loaded['setup']['profile_id'] == 'SH'


def main():
    assert len(SETS) == 10
    all_questions = []
    observed = set()
    for number in range(1, 11):
        assert [len(group) for group in SETS[number - 1]] == [3, 3, 3, 3, 2]
        qs = build_questions(SELECTION, number, 5)
        assert len(qs) == 15
        assert qs == build_questions(SELECTION[::-1], number, 5)
        assert [q['type_id'] for q in qs[10:13]] == ['T11', 'T12', 'T08']
        assert qs[12]['roleplay_followup']
        for q in qs:
            assert q['bank_version'] == BANK_VERSION
            assert q['topic_id'] not in {'reading', 'gaming', 'no_exercise'}
            if q['origin'] == 'survey':
                assert q['topic_id'] in SELECTION
                observed.add(q['topic_id'])
        for level in range(1, 7):
            result = build_questions(SELECTION, number, level)
            assert len(result) == (12 if level < 3 else 15)
            assert all(q['base_prompt'] in q['prompt'] for q in result[10:12])
        all_questions.extend(qs)
    assert observed == REQUIRED_TOPICS
    assert {q['type_id'] for q in all_questions} == set(TYPE_LABELS)
    assert len({q['content_id'] for q in all_questions}) == 150
    duplicates = [count for count in Counter(q['prompt'] for q in all_questions).values() if count > 1]
    assert duplicates == [10], duplicates  # Shared introduction only.
    assert len({q['prompt'] for q in all_questions}) == 141
    # The new bank must never require an instrument/gym the user did not select.
    for removed in ('instrument', 'gym'):
        qs = build_questions([t for t in SELECTION if t != removed], 1, 5)
        assert not any(q.get('bank_version') == BANK_VERSION for q in qs)
    asyncio.run(check_sessions())
    print('PASS: instrument survey, 10 x 15, 141 unique, all 11 selected activities, 14 types, no reading/gaming, 5-5 persistence, 6 levels')


if __name__ == '__main__':
    main()
