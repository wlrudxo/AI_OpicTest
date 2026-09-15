"""Offline checks for expanded survey selection and generated exam snapshots."""
import asyncio
from collections import Counter
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import mock_api
from questions import TOPICS, build_questions
from survey import catalog


def main():
    items = catalog()
    ids = [item['id'] for item in items]
    assert len(ids) == len(set(ids)) == 69
    assert Counter(item['group'] for item in items) == {
        'leisure': 26, 'hobbies': 14, 'sports': 24, 'vacations': 5}
    # Old choices remain valid; stored exam snapshots must not be rewritten.
    legacy = ['movies', 'shows', 'concerts', 'park', 'music', 'jogging',
              'walking', 'no_exercise', 'business_local', 'vacation', 'travel', 'travel_abroad']
    mock_api.validate_setup(mock_api.Setup(topics=legacy))
    for item in items:
        # Put each choice first in its group to exercise it in an actual set.
        selection = list(dict.fromkeys([item['id'], *legacy]))
        mock_api.validate_setup(mock_api.Setup(topics=selection))
        for number in (1, 2, 3):
            for level in range(1, 7):
                questions = build_questions(selection, number, level)
                assert len(questions) == (12 if level <= 2 else 15)
                assert [q['id'] for q in questions] == [f'q{i:02d}' for i in range(1, len(questions)+1)]
                assert all(q['prompt'].strip() for q in questions)
        if item['group'] in ('leisure', 'hobbies', 'sports', 'vacations'):
            questions = build_questions(selection, 1, 5)
            assert any(q['base_prompt'] == TOPICS[item['id']][1][0] for q in questions)
    new_choices = ['gaming', 'cafe', 'shopping', 'tv', 'news', 'bars',
                   'reading', 'photography', 'taekwondo', 'exercise_classes', 'travel', 'vacation']
    async def roundtrip():
        with TemporaryDirectory() as directory, patch.object(mock_api, 'ROOT', Path(directory)), patch.object(mock_api.tts, 'prepare'):
            session = await mock_api.create(mock_api.Setup(topics=new_choices))
            loaded = await mock_api.get_session(session['id'])
            assert loaded['setup']['topics'] == new_choices
            assert loaded['questions'] == session['questions']
            assert loaded['questions'][1]['topic'] == '게임'
            assert loaded['questions'][4]['topic'] == '독서'
    asyncio.run(roundtrip())
    print('PASS: 69 topics, all 3 sets and 6 levels, legacy choices, new session roundtrip')


if __name__ == '__main__':
    main()
