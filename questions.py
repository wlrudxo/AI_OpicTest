"""Original practice prompts. The grouping imitates OPIc practice conventions."""
TOPICS = {
    'gaming': ('게임', [
        'Tell me about a video game you enjoy. What do you do in the game, and what makes it fun for you?',
        'When and where do you usually play video games? Describe how you choose a game and who you play with.',
        'Tell me about a memorable time playing a video game. What happened, how did you react, and how did it end?']),
    'reading': ('독서', [
        'Describe a book you enjoy. What is it about, and why do you like it?',
        'Tell me about your reading habits. When and where do you read, and how do you choose your next book?',
        'Tell me about a time a book surprised you or changed your perspective. What did you read, and how did you react?']),
    'home': ('집', [
        'Tell me about your home. What is your favorite space there, and what makes it comfortable for you?',
        'Walk me through a typical evening at home. What do you usually do after you get back?',
        'Think of a time something unexpected happened at home. What happened, and how did you handle it?']),
    'cafe': ('카페', [
        'Describe a cafe you enjoy visiting. What does it look like, and why do you choose that place?',
        'What do you normally do when you visit a cafe? Tell me about your usual order and how you spend your time.',
        'Tell me about a memorable visit to a cafe. Who were you with, and what made that visit different?']),
    'movies': ('영화', [
        'What kinds of movies do you enjoy? Describe a movie you like and explain what appeals to you about it.',
        'Tell me how you usually watch movies. How do you choose a film, and who do you watch it with?',
        'Tell me about a time a movie surprised you. What did you expect, and how did you feel afterward?']),
    'music': ('음악', [
        'Tell me about the music you like. Describe an artist you enjoy and explain what you like about their music.',
        'When and where do you usually listen to music? Explain how music fits into your daily routine.',
        'Tell me about a memorable experience involving music. What happened, and why do you still remember it?']),
    'park': ('공원·걷기', [
        'Describe a park or walking route you enjoy. What can you see there, and what do you like about it?',
        'What do you usually do when you go for a walk? Tell me about your routine from beginning to end.',
        'Tell me about a walk that did not go as planned. What happened, and what did you decide to do?']),
    'travel': ('여행', [
        'Describe a place you like to visit on vacation. What is it like, and what makes it special to you?',
        'How do you prepare for a trip? Walk me through the things you do before you leave.',
        'Tell me about a memorable moment on a trip. Describe where you were, what happened, and how you felt.']),
    'shopping': ('쇼핑', [
        'Describe a store or shopping area you like. What does it sell, and why do you shop there?',
        'How do you decide what to buy? Tell me about your usual shopping routine.',
        'Tell me about a problem with something you bought. How did you discover the problem, and what did you do?']),
    'vacation': ('집에서 보내는 휴가', [
        'What makes staying home for a vacation enjoyable for you? Describe the setting and activities you prefer.',
        'How do you spend a day off at home? Describe the day from morning to evening.',
        'Tell me about a memorable vacation you spent at home. What did you do that made it special?']),
}
SURPRISE = [
    ('교통', ['Describe the transportation options in your area. Which one do you use most often, and why?', 'Tell me about a recent journey using public transportation. Where did you go, and how was the trip?', 'Tell me about a time you were delayed while traveling somewhere. What caused the delay, and how did you respond?']),
    ('날씨', ['What is the weather like where you live? Describe your favorite season and explain why you like it.', 'How do your daily activities change depending on the weather? Give me some examples.', 'Tell me about a time unusual weather changed your plans. What happened, and what did you do instead?']),
    ('기술', ['Tell me about a device you use regularly. Describe it and explain why it is useful to you.', 'How do you use technology during a typical day? Give me examples from your own routine.', 'Tell me about a time a device stopped working when you needed it. What did you do to solve the problem?']),
]
from survey import catalog
for item in catalog():
    if item['id'] not in TOPICS:
        activity = item['activity']
        TOPICS[item['id']] = (item['name'], [
            f'You selected {activity} in the survey. Tell me what you enjoy about it. Describe the place or setting where you usually do this.',
            f'Tell me about your usual routine for {activity}. What do you do before, during, and afterward?',
            f'Think of a memorable experience related to {activity}. What happened, who was involved, and why do you remember it?',
        ])

ROLES = [
    ('숙소 예약', [
        'You want to book a room for a weekend trip. Call the hotel and ask three or four questions about the room and the services you need.',
        'The hotel tells you that the room you reserved is no longer available. Explain your situation and suggest two or three ways to resolve the problem.',
        'Tell me about a time a reservation or plan went wrong in your own life. What happened, and how was it resolved?']),
    ('공연 예매', [
        'You want to attend a concert with a friend. Call the ticket office and ask three or four questions before buying tickets.',
        'You bought concert tickets, but your friend cannot go on that date. Call the ticket office, explain the problem, and suggest two or three possible solutions.',
        'Tell me about a time you had to change plans with a friend. What happened, and how did you work things out?']),
    ('물건 빌리기', [
        'You would like to borrow a camera from your friend for a trip. Call your friend and ask three or four questions about borrowing and using the camera.',
        'While using your friend\'s camera, you discover that it will not turn on. Call your friend, explain what happened, and offer two or three ways to deal with the situation.',
        'Tell me about a time something you borrowed or owned was damaged. What happened, and what did you do about it?']),
]


def build_questions(topics, set_number, level):
    selected = list(dict.fromkeys(topics))
    group_by_id = {item['id']: item['group'] for item in catalog()}
    leisure = [t for t in selected if group_by_id.get(t) == 'leisure'] or selected
    other = [t for t in selected if group_by_id.get(t) != 'leisure'] or selected[1:]
    first = leisure[(set_number-1) % len(leisure)]
    second = other[(set_number-1) % len(other)]
    out = [{'topic': '자기소개', 'type': '자기소개', 'prompt': 'Please introduce yourself. Tell me a little about your daily life and the things you enjoy doing.'}]
    for topic, prompts in [TOPICS[first], TOPICS[second], SURPRISE[set_number - 1]]:
        for kind, prompt in zip(['묘사', '습관·일상', '과거 경험'], prompts):
            out.append({'topic': topic, 'type': kind, 'prompt': prompt})
    topic, prompts = ROLES[set_number - 1]
    for kind, prompt in zip(['질문하기', '문제 해결', '관련 경험'], prompts):
        out.append({'topic': topic, 'type': kind, 'prompt': prompt})
    out.extend([
        {'topic': '생활 변화', 'type': '비교', 'prompt': 'Compare the way you spend your free time now with the way you spent it several years ago. What has changed, and what caused those changes?'},
        {'topic': '기술과 일상', 'type': '의견', 'prompt': 'People often use their phones while spending time with friends. What problems can this cause, and what do you think people should do about it? Give specific examples.'},
    ])
    if level <= 2:
        out = out[:12]
    for i, q in enumerate(out):
        q.update(id=f'q{i+1:02d}', order=i+1, base_prompt=q['prompt'])
        if level <= 2:
            q['prompt'] = q['prompt'].split('. ')[0] + ('' if q['prompt'].split('. ')[0].endswith('?') else '.')
        if level == 6:
            q['prompt'] += ' Explain your reasons with specific details.'
    return out
