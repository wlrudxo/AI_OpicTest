"""Original survey-based practice sets; these are not official exam questions.

Each block stores its actual speaking task, rather than inferring it from order.
The selected activities are prerequisites; negative survey choices are not topics.
"""
from copy import deepcopy

MAX_SETS = 10
BANK_VERSION = 'survey-v3'
REQUIRED_TOPICS = frozenset({
    'movies', 'shows', 'concerts', 'park', 'gaming', 'reading',
    'jogging', 'walking', 'vacation', 'travel', 'travel_abroad',
})
TYPE_LABELS = {
    'T01': '자기소개', 'T02': '대상 묘사·선호', 'T03': '습관·일상',
    'T04': '절차·과정', 'T05': '최근 경험', 'T06': '첫 경험·계기',
    'T07': '기억에 남는 경험', 'T08': '문제 해결 경험',
    'T09': '과거·현재 비교', 'T10': '대상 비교', 'T11': '질문·정보 요청',
    'T12': '문제 해결·대안', 'T13': '최근 동향·이슈', 'T14': '의견·장단점',
}


def block(topic_id, topic, origin, text):
    rows = []
    for line in text.strip().splitlines():
        type_id, prompt = line.strip().split('|', 1)
        rows.append(dict(topic_id=topic_id, topic=topic, origin=origin,
                         type_id=type_id, type=TYPE_LABELS[type_id], prompt=prompt))
    return rows


# The first three blocks each contain three questions, then a three-part
# role-play and a two-question discussion. Titles are never exposed in setup.
SETS = [
    [
        block('gaming', '게임', 'survey', """
T02|Tell me about a game you like to play in your free time. What do you do in the game? What do you enjoy most about it?
T03|How often do you play games? When and where do you usually play? Do you play alone or with other people?
T07|Tell me about a game that turned out differently than you expected. What happened? How did you feel about it?
"""),
        block('reading', '독서', 'survey', """
T02|What kinds of books do you like to read? Pick one kind and tell me what those books are usually about. Why do you like them?
T06|When did you first start reading for fun? Was there a person or a book that got you into reading? Tell me what happened.
T09|How have your reading habits changed since you were younger? What did you read back then, and what do you read now?
"""),
        block('transport', '교통', 'common', """
T02|Tell me about the public transportation near your home. What do you usually take? Why is it convenient for you?
T05|Tell me about the last time you took a bus or a train. Where were you going? What happened on the way?
T08|Have you ever been late because of a traffic jam or a delay? What happened? How did you deal with it?
"""),
        block('shows', '공연 예매', 'survey', """
T11|You want to see a live show with a friend this weekend. Call the theater and ask three or four questions about the shows and the seats.
T12|You booked the tickets, but the theater says the show will start two hours late. Call your friend, explain what happened, and give two ways to change your plans.
T08|That's the end of the role-play. Has the schedule of an event ever changed suddenly on you? What were your plans? What did you do?
"""),
        block('movies', '영화 감상 방식', 'survey', """
T10|Compare watching a movie at home and watching a movie at a theater. What is different about them? Which one do you prefer, and why?
T13|How do people around you choose movies to watch these days? How is it different from before?
"""),
    ],
    [
        block('movies', '영화', 'survey', """
T02|Tell me about an interesting character from a movie you watched. What is the character like? Why do you remember them?
T04|Tell me how you plan a movie night with a friend. How do you pick the movie? What do you prepare before it starts?
T07|Tell me about a movie you talked about a lot with someone after watching it. Who did you talk with? What did you talk about?
"""),
        block('park', '공원', 'survey', """
T02|Tell me about a park you know well. What does it look like? What do people do there?
T03|What do you usually do when you go to a park? How do you get there? How long do you usually stay?
T08|Have you ever had an outing that did not go as planned? What went wrong? What did you do instead?
"""),
        block('weather', '날씨', 'common', """
T02|What is the weather like in your favorite season? What do you like to do when the weather is like that?
T09|How did you spend very hot or very cold days when you were a child? How is it different now?
T05|Tell me about a recent day when the weather changed your plans. What was the weather like? What did you end up doing?
"""),
        block('reading', '독서 모임', 'survey', """
T11|You want to join a reading group at a local library for the first time. Call the person in charge and ask three or four questions about the next meeting.
T12|You signed up for the reading group, but you cannot get the book before the meeting. Call the person in charge, explain the problem, and give two ways you could still take part.
T08|That's the end of the role-play. Have you ever been unable to get something ready for a plan? What was missing? How did you handle it?
"""),
        block('travel_abroad', '해외여행 방식', 'survey', """
T10|Compare traveling abroad on your own and traveling with a group tour. What are the good and bad points of each? Which do you prefer?
T13|What do people worry about when they travel abroad these days? Tell me about one worry. Why is it a problem?
"""),
    ],
    [
        block('shows', '공연', 'survey', """
T02|What kinds of live shows do you like to see? What usually happens during the show? Why do you like watching it in person?
T05|Tell me about the last live show you went to. Where was it? What did you do before and after the show?
T06|When did you first become interested in live shows? Who did you go with? What do you remember about it?
"""),
        block('vacation', '집에서 보내는 휴가', 'survey', """
T03|What do you usually do when you spend your vacation at home? What time do you get up? How is it different from a normal day?
T04|What do you do to get ready for a vacation at home? Do you buy anything or make any plans? Tell me in detail.
T07|Tell me about a day off at home that you really enjoyed. What did you do that day? Why was it so good?
"""),
        block('technology', '생활 속 기기', 'common', """
T02|Tell me about a device you use a lot at home. What do you use it for? Why is it important to you?
T09|Think about something you do with technology today. How did people do it in the past? What is the biggest difference?
T08|Have you ever had a device stop working at a bad time? What were you doing? How did you solve the problem?
"""),
        block('travel', '국내 숙소 예약', 'survey', """
T11|You are planning a short trip to another city in your country. Call a guesthouse and ask three or four questions before you make a reservation.
T12|You booked a room, but you will arrive after the guesthouse's front desk closes. Call the guesthouse, explain the situation, and give two ways to solve the problem.
T08|That's the end of the role-play. Have you ever had to change a plan because you were going to be late? Who did you contact? How did it work out?
"""),
        block('gaming', '게임 방식 비교', 'survey', """
T10|Compare a game you play alone with a game you play with other people. How are they different? Which do you enjoy more?
T14|Some people think playing games together is a good way to spend time with friends, but others do not. What do you think? What are the good and bad sides?
"""),
    ],
    [
        block('concerts', '콘서트', 'survey', """
T02|Tell me about a place where you have seen a concert. What did it look like? Where were you standing or sitting?
T04|What do you usually do to get ready for a concert? What do you check before you go? How do you get to the venue?
T07|Tell me about a moment at a concert that you still remember. What was happening? How did the crowd react?
"""),
        block('walking', '걷기', 'survey', """
T02|Tell me about a place where you like to take a walk. What do you see along the way? Why do you like it?
T03|When do you usually go for a walk? How long do you walk? What do you do while you walk?
T05|Tell me about the last time you went for a walk. Where did you go? How did you feel afterward?
"""),
        block('recycling', '재활용', 'common', """
T04|How do you recycle at home? What do you separate? Where do you take it?
T09|How has the way you throw away trash changed over the years? What did you do in the past, and what do you do now?
T08|Have you ever not known how to throw something away? What was it? How did you find out what to do?
"""),
        block('gaming', '게임 기기 빌리기', 'survey', """
T11|You want to borrow a friend's game console for the weekend. Call your friend and ask three or four questions about borrowing it and setting it up.
T12|You borrowed the console, but one of the controllers will not connect. Call your friend, explain what you have tried, and give two ways to deal with the problem.
T08|That's the end of the role-play. Have you ever borrowed something that did not work properly? What was it? What did you do?
"""),
        block('reading', '독서 취향 변화', 'survey', """
T09|How are the books you liked when you were younger different from the books you like now? Why do you think your taste changed?
T13|Many people say that people read fewer books these days. Do you agree? Why do you think this is happening?
"""),
    ],
    [
        block('gaming', '게임', 'survey', """
T02|What makes a game easy or hard to learn? Use a game you know as an example. What does a new player need to know?
T06|How did you learn to play a game you enjoy now? Who taught you? What was hard at first?
T08|Have you ever had trouble working with your teammates in a game? What happened? How did you handle it?
"""),
        block('travel', '국내 여행', 'survey', """
T02|Tell me about a place in your country you would recommend for a short trip. What is it like? What can people do there?
T04|How do you get ready for a short trip in your country? How do you choose how to get there? What do you pack?
T07|Tell me about a trip in your country when you found something you did not plan to see. How did you find it? Why do you remember it?
"""),
        block('appointments', '약속', 'common', """
T03|How do you usually make plans to meet your friends? How do you decide when and where to meet?
T05|Tell me about the last time you met someone you made plans with. What did you do together? How did the day go?
T08|Have you ever made two plans for the same time by mistake? How did you find out? What did you do?
"""),
        block('park', '공원 프로그램', 'survey', """
T11|You want to join a weekend guided walk at a park. Call the visitor center and ask three or four questions about the walk.
T12|You signed up, but the visitor center says the guided walk has been canceled. Call the friend who was going with you, explain what happened, and suggest two other things you could do.
T08|That's the end of the role-play. Has something you wanted to go to ever been canceled? How did you hear about it? What did you do instead?
"""),
        block('concerts', '콘서트 경험 비교', 'survey', """
T10|Compare a small concert and a big concert. How are the atmosphere and the sound different? Which one would you choose?
T13|How do people share their concert experiences these days? Tell me about something you have noticed. How is it different from the past?
"""),
    ],
    [
        block('reading', '독서', 'survey', """
T02|You indicated in the survey that you enjoy reading. What kinds of books do you usually read? Tell me about a book or an author you like, and explain why in as much detail as possible.
T06|How did you first become interested in reading? Was there a person or a book that made you start? How has your reading changed since then? Tell me about it in detail.
T07|Tell me about a book you read that you still remember well. What was it about? When and why did you read it? Explain what made it so special to you.
"""),
        block('jogging', '조깅', 'survey', """
T02|You indicated in the survey that you go jogging. Where do you usually jog? Describe the place in as much detail as possible. What do you see and hear while you are there?
T03|Tell me about your jogging routine. When and how often do you jog? What do you do before you start and after you finish? Give me as many details as you can.
T07|Tell me about a memorable experience you had while jogging. Maybe something unexpected or interesting happened. When was it, and what exactly happened? Tell me the whole story from beginning to end.
"""),
        block('home', '집', 'common', """
T02|I'd like to know about the place where you live. Is it a house or an apartment? How many rooms does it have? Describe your home in as much detail as possible.
T09|Tell me about the home you lived in when you were a child. How was it different from the home you live in now? Describe the differences in detail.
T08|Tell me about a problem you once had in your home. For example, something was broken or stopped working. What was the problem, and how did you solve it? Tell me everything that happened.
"""),
        block('movies', '영화 보러 가기', 'survey', """
T11|I'd like to give you a situation and ask you to act it out. You want to see a movie with a friend this weekend. Call your friend and ask three or four questions to plan the evening.
T12|I'm sorry, but there is a problem I need you to resolve. On the day of the movie, you find out that the tickets you bought online are for the wrong date. Call the theater, explain the situation, and offer two or three alternatives.
T08|That's the end of the situation. Have you ever had a problem with a ticket or a reservation? What was the problem, and how did you deal with it? Tell me the story from beginning to end.
"""),
        block('free_time', '여가 생활', 'common', """
T09|Let's talk about free time. How do people in your country spend their free time these days? How is it different from the way people spent their free time when you were a child? Explain the changes in detail.
T13|What issues or concerns do people have about free time these days? For example, some people say they do not have enough time to rest. Tell me about one issue and explain why it matters to people.
"""),
    ],
    [
        block('park', '공원', 'survey', """
T02|You indicated in the survey that you go to parks. Tell me about a park you often visit. Where is it, and what does it look like? Describe it in as much detail as possible.
T03|What do you usually do when you go to the park? Who do you go with, and how long do you stay? Tell me about a typical visit from start to finish.
T07|Tell me about a memorable experience you had at a park. When was it, and who were you with? What happened? Tell me the whole story from beginning to end.
"""),
        block('restaurants', '식당과 외식', 'common', """
T02|Tell me about a restaurant you often go to. What kind of food does it serve? What does the place look like? Describe it in as much detail as possible.
T05|Tell me about the last time you ate out. Where did you go, and who were you with? What did you order? Describe that visit from the moment you arrived until you left.
T07|Tell me about a memorable experience you had at a restaurant. Maybe the food or the service was very good or very bad. What happened? Tell me everything in detail.
"""),
        block('travel_abroad', '해외여행', 'survey', """
T02|You indicated in the survey that you travel abroad. Tell me about a country or city you have visited. What does it look like, and what are the people like? Describe it in as much detail as possible.
T06|Tell me about your first trip abroad. Where did you go, and who went with you? What did you see and do there? Give me as many details as you can.
T08|Unexpected things sometimes happen during a trip. Tell me about a time something unexpected happened while you were traveling abroad. What happened, and how did you deal with it? Tell me the whole story.
"""),
        block('travel_abroad', '여행 상품 문의', 'survey', """
T11|I'd like to give you a situation and ask you to act it out. You are planning a trip abroad for your next vacation. Call a travel agency and ask three or four questions about the trip.
T12|I'm sorry, but there is a problem I need you to resolve. You bought a plane ticket that cannot be refunded, but something urgent came up and you cannot travel on that date. Call the travel agency, explain your situation, and suggest two or three alternatives.
T08|That's the end of the situation. Have you ever had to change or cancel a trip? What happened, and what did you do about it? Tell me the story in as much detail as possible.
"""),
        block('housing', '주거 변화', 'common', """
T09|Let's talk about housing in your country. How are homes today different from homes twenty or thirty years ago? Describe the changes in size, style, and the things people have at home.
T13|Tell me about a housing issue that people in your country talk about these days. What is the problem, and what caused it? How does it affect people's lives? Explain in detail.
"""),
    ],
    [
        block('phones', '휴대폰과 인터넷', 'common', """
T02|Tell me about the phone you use. What does it look like, and what do you usually use it for? Which features are most important to you? Describe them in detail.
T09|Think about the first phone you ever had. What was it like, and what could you do with it? Compare it with the phone you use now and explain the biggest differences.
T08|Tell me about a time your phone or the internet caused a problem for you. For example, it stopped working when you needed it. What happened, and how did you solve the problem? Tell me everything.
"""),
        block('movies', '영화', 'survey', """
T02|You indicated in the survey that you like watching movies. What kinds of movies do you enjoy, and why do you like them? Tell me about one of your favorite movies in as much detail as possible.
T03|Tell me what you usually do when you go to see a movie. What do you do before the movie, during it, and after it? Describe a typical day at the movies from beginning to end.
T07|Tell me about the most memorable movie you have seen. What was it about, and who was in it? Why do you still remember it? Explain in as much detail as you can.
"""),
        block('travel', '국내 여행', 'survey', """
T02|You indicated in the survey that you take trips within your country. Tell me about a place you like to visit. Where is it, and what is it like? Explain why you like going there.
T04|What do you do to prepare for a trip? Tell me about the things you check, book, and pack before you leave. Describe the steps in order.
T07|Tell me about a memorable trip you took in your country. Where did you go, and who were you with? What made it special? Tell me the whole story from beginning to end.
"""),
        block('travel', '렌터카', 'survey', """
T11|I'd like to give you a situation and ask you to act it out. You want to rent a car for a weekend trip. Call a car rental company and ask three or four questions about renting a car.
T12|I'm sorry, but there is a problem I need you to resolve. You rented a car, but it broke down in the middle of your trip. Call the rental company, explain what happened, and offer two or three ways to solve the problem.
T08|That's the end of the situation. Have you ever had a problem while you were traveling, such as a problem with a car, a train, or a hotel? What happened, and how did you solve it?
"""),
        block('transport', '교통 변화', 'common', """
T09|Let's talk about transportation. How has the way people travel around your city changed over the years? Compare the transportation people used in the past with what they use today.
T13|What transportation problems do people in your country talk about these days? Choose one problem. Explain what causes it, how it affects people, and what is being done about it.
"""),
    ],
    [
        block('shows', '공연', 'survey', """
T02|You indicated in the survey that you enjoy watching live performances. What kinds of performances do you like to see? Tell me about a theater or hall you have been to and describe what it looks like.
T05|Tell me about the last performance you went to. What was it, and who did you go with? Describe what you did before, during, and after the performance in detail.
T07|Tell me about the most memorable performance you have ever seen. When and where was it? What made it so special? Tell me everything from beginning to end.
"""),
        block('walking', '걷기', 'survey', """
T02|You indicated in the survey that you like to take walks. Where do you usually walk? Describe the place and the things you can see along the way in as much detail as possible.
T06|How did you first start walking regularly? What made you start, and how has your walking routine changed since then? Tell me about it in detail.
T05|Tell me about the last time you went for a walk. When was it, and where did you go? What did you see or do along the way? Describe that walk from beginning to end.
"""),
        block('health', '건강', 'common', """
T02|Tell me about a healthy person you know. What does this person look like, and what kind of person is he or she? Describe what this person does to stay healthy.
T03|What do you do to stay healthy? Tell me about the food you eat, the exercise you do, and any other habits you have. Give me as many details as possible.
T08|Tell me about a time you were sick or had a health problem. What was wrong? What did you do to get better? Tell me what happened from beginning to end.
"""),
        block('health', '병원 예약', 'common', """
T11|I'd like to give you a situation and ask you to act it out. You are not feeling well and want to see a doctor. Call the clinic and ask three or four questions to make an appointment.
T12|I'm sorry, but there is a problem I need you to resolve. You have a doctor's appointment today, but an important meeting at school came up, and you cannot go. Call the clinic, explain your situation, and suggest two or three alternatives.
T08|That's the end of the situation. Have you ever had to cancel or change an appointment at the last minute? What was the reason, and how did you handle it? Tell me the story in detail.
"""),
        block('holidays', '명절과 휴일', 'common', """
T09|Let's talk about holidays in your country. How did your family spend a big holiday when you were a child? How do people spend it these days? Describe what has changed and why.
T13|What do people in your country say about holidays these days? For example, some people travel instead of visiting family. Tell me about one change or concern and explain what you think about it.
"""),
    ],
    [
        block('concerts', '콘서트', 'survey', """
T02|You indicated in the survey that you go to concerts. What kinds of concerts do you like, and which singers or bands do you want to see? Explain what you like about their music in detail.
T03|Tell me what you usually do on the day of a concert. How do you get your tickets, and how do you get there? What do you do before and after the concert?
T07|Tell me about the most memorable concert you have been to. Who performed, and where was it? What happened, and how did the crowd react? Tell me the whole story from beginning to end.
"""),
        block('geography', '지형과 야외 활동', 'common', """
T02|Tell me about the geography of your country. Are there many mountains, rivers, or beaches? Describe what the land looks like in as much detail as possible.
T03|What outdoor activities do people in your country usually do in the mountains or by the sea? Tell me what people do, when they go, and who they go with.
T07|Tell me about a memorable experience you had at a mountain, a river, or a beach. When was it, and who were you with? What happened? Tell me everything from beginning to end.
"""),
        block('vacation', '집에서 보내는 휴가', 'survey', """
T02|You indicated in the survey that you like to stay home during your vacations. What do you usually do at home on those days? Who do you spend time with? Tell me in as much detail as possible.
T05|Tell me about your last vacation at home. What did you do each day, from the first day to the last? Give me as many details as you can.
T07|Tell me about a memorable or unusual experience you had during a vacation at home. What happened, and why do you still remember it? Tell me the story from beginning to end.
"""),
        block('furniture', '가구 구매', 'common', """
T11|I'd like to give you a situation and ask you to act it out. You want to buy a new desk and chair for your room. Call a furniture store and ask three or four questions about the furniture you want.
T12|I'm sorry, but there is a problem I need you to resolve. The furniture you ordered has arrived, but one piece is damaged. Call the store, explain the problem, and suggest two or three ways to solve it.
T08|That's the end of the situation. Have you ever bought something that was damaged or did not work well? What was it, and what did you do about it? Tell me everything in detail.
"""),
        block('gaming', '게임 문화', 'survey', """
T09|Let's talk about games. How are the games people play today different from the games people played when you were a child? Compare how people played then with how they play now.
T14|Some people worry that young people spend too much time playing games. What do people in your country say about this issue? Tell me what you think and give reasons for your opinion.
"""),
    ],
]


def authored_questions(topics, set_number):
    if not REQUIRED_TOPICS.issubset(topics):
        return None
    return assemble_questions(SETS, set_number, BANK_VERSION)


def assemble_questions(sets, set_number, bank_version):
    groups = deepcopy(sets[set_number - 1])
    intro = block('introduction', '자기소개', 'common',
                  'T01|Please introduce yourself. Tell me about your daily life and a few things you enjoy doing in your free time.')
    out = intro
    for block_number, group in enumerate(groups, 1):
        for position, question in enumerate(group, 1):
            question.update(block_id=f'{bank_version}.{set_number:02d}.{block_number}',
                            block_position=position,
                            roleplay_followup=block_number == 4 and position == 3)
        out.extend(group)
    for number, question in enumerate(out, 1):
        question.update(content_id=f'{bank_version}.{set_number:02d}.{number:02d}',
                        bank_version=bank_version, provenance='original')
    return out
