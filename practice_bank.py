"""Original survey-based practice sets; these are not official exam questions.

Each block stores its actual speaking task, rather than inferring it from order.
The selected activities are prerequisites; negative survey choices are not topics.
"""
from copy import deepcopy

MAX_SETS = 10
BANK_VERSION = 'survey-v2'
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
T14|Some people plan every day of a trip, and others just go with the flow. Which way works better for you when you travel abroad? Why?
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
T14|Do you think talking about a book with other people makes reading more fun? Why or why not? Give me an example.
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
T02|Tell me about a place where you get books to read. What is it like? Why do you go there?
T04|How do you choose a book when you don't have one in mind? What do you look at first? How do you make the final choice?
T05|Tell me about the last book you started reading. How did you find it? What did you think of the first part?
"""),
        block('jogging', '조깅', 'survey', """
T02|Tell me about a place where you have gone jogging, even if you don't jog often. What is the route like? What do you like or dislike about it?
T03|When you go jogging, how do you get ready? How far do you usually go? What do you do after?
T07|Tell me about a time you felt really good after being active outside. It can be jogging or any other outdoor activity. What happened? How did you feel?
"""),
        block('deliveries', '배달·배송', 'common', """
T03|How do you usually get things delivered to your home? How do you order them? How do you receive them?
T05|Tell me about the last package you got. What was it? What did you do after you got it?
T08|Have you ever had a delivery that came late or was not what you ordered? What happened? Who did you contact?
"""),
        block('movies', '영화관 예매', 'survey', """
T11|You want to go to a movie with two friends. Call the movie theater and ask three or four questions about the showtimes and seats.
T12|You booked the seats, but you realize you picked the wrong date. Call the theater, explain your mistake, and give two ways to fix the booking.
T08|That's the end of the role-play. Have you ever made a mistake when booking or ordering something? What happened? How did you fix it?
"""),
        block('vacation', '휴가 방식', 'survey', """
T10|Compare spending a vacation at home and going somewhere on vacation. How are they different? Which do you like better?
T14|Some people think they should do something useful even on their days off. What do you think? What makes a day off worth it for you?
"""),
    ],
    [
        block('park', '공원', 'survey', """
T02|What kinds of people do you see at a park you go to? What do they do there? Tell me in detail.
T09|How has the way you use parks changed over the years? Why did you go to parks in the past? Why do you go now?
T07|Tell me about a memorable time you met someone at a park or another place outdoors. What happened? Why do you remember it?
"""),
        block('travel_abroad', '해외 여행', 'survey', """
T02|Tell me about a place you visited in another country. What did it look like? What do you remember most about it?
T05|Tell me about the first day of your last trip abroad. What did you do after you arrived? How did you find your way around?
T08|Have you ever had trouble communicating while traveling? What were you trying to say? How did it turn out?
"""),
        block('furniture', '가구', 'common', """
T02|Tell me about a piece of furniture you use a lot. Where is it? What does it look like?
T04|How do you decide where to put furniture in a room? What do you think about first?
T08|Have you ever had to move, fix, or replace something at home? What happened? What did you do?
"""),
        block('concerts', '콘서트 좌석', 'survey', """
T11|You want to buy tickets for a concert at a place you've never been to. Call the ticket office and ask three or four questions about the seats and the venue.
T12|You bought two tickets, but the seats are not next to each other. Call the ticket office, explain the problem, and give two ways to fix it.
T08|That's the end of the role-play. Has a booking for you and someone else ever turned out wrong? What was wrong? How did you solve it?
"""),
        block('walking', '걷기 환경', 'survey', """
T10|Compare walking on a busy street and walking in a quiet place. What can you see or do in each place? Which do you prefer?
T14|What would make your neighborhood a better place for walking? What is the most needed change? Why?
"""),
    ],
    [
        block('movies', '영화', 'survey', """
T02|Tell me about a place shown in a movie that you remember. What did it look like? Why was it memorable?
T09|How did you watch movies a few years ago? How do you watch them now? What has changed?
T08|Has anything ever interrupted you while you were watching a movie? What happened? Were you able to finish the movie?
"""),
        block('travel', '국내 여행', 'survey', """
T02|When you travel in your country, is there a place you like to stop on the way? What is it like? What do you do there?
T05|Tell me about the last short trip you took in your country. How did you get there? What did you do?
T09|How are your trips now different from the trips you took when you were younger? How do you choose where to go? Why did it change?
"""),
        block('neighbors', '이웃', 'common', """
T02|Tell me about the area around your home. What places do your neighbors share? Where do you run into them?
T03|How do people in your building or neighborhood share news or information? Give me an example.
T07|Tell me about a time a neighbor helped you or you helped a neighbor. What happened? How did it end?
"""),
        block('travel_abroad', '해외 현지 투어', 'survey', """
T11|You are traveling abroad and want to join a walking tour of the city. Call the tour company and ask three or four questions about the tour.
T12|You booked the tour, but the company moved the meeting place to somewhere you cannot get to in time. Call the company, explain the problem, and give two ways to solve it.
T08|That's the end of the role-play. Have you ever had trouble finding a meeting place? What made it hard? What happened in the end?
"""),
        block('shows', '공연 관람 방식', 'survey', """
T10|Compare seeing a live show in person and watching a video of it. What can you enjoy in each? What do you miss?
T13|How do people find out about shows and performances these days? How is it different from the past?
"""),
    ],
    [
        block('shows', '공연', 'survey', """
T02|Tell me about the audience at a live show. What do people do before and during the show? How does it affect the mood?
T03|What do you usually do on the day you go to a show? When do you get there? What do you do after the show?
T08|Have you ever had a hard time seeing or hearing at an event? What was the problem? What did you do about it?
"""),
        block('walking', '걷기', 'survey', """
T03|When you go for a walk with someone, what do you usually do? Where do you go? What do you talk about?
T10|Compare walking alone and walking with someone else. How are they different? Which do you prefer?
T08|Have you ever had to change your route while walking somewhere? What blocked the way? How did you find another way?
"""),
        block('public_facilities', '공공시설', 'common', """
T02|Tell me about a public place in your area that people can use in their free time. What does it have? Who uses it?
T04|How do people use a service at a public place you know, like a library or community center? What do they need to bring? What do they do when they get there?
T05|Tell me about the last time you went to a public place like a library or community center. Why did you go? What did you do?
"""),
        block('reading', '도서관 대출', 'survey', """
T11|You want to borrow a book from a library you've never used before. Talk to the librarian and ask three or four questions about getting a library card and borrowing books.
T12|You borrowed a book, but you will be away on the due date and cannot return it. Call the library, explain the situation, and give two ways to solve the problem.
T08|That's the end of the role-play. Have you ever had trouble returning something on time? What was it? How did you solve it?
"""),
        block('park', '공원 이용 변화', 'survey', """
T09|How is a park you know used today compared to the past? What has changed? Why do you think it changed?
T14|Some people go to parks to rest quietly, and others go to play sports. How can a park be good for both groups? Give me some ideas.
"""),
    ],
    [
        block('concerts', '콘서트', 'survey', """
T02|What makes you want to go to a certain concert? Is it the singer, the songs, or the place? What matters most to you?
T06|How did you first become interested in concerts? What was your first concert like? Who did you go with?
T05|Tell me about the last concert you went to or watched live online. How did you get the ticket? What happened during the concert?
"""),
        block('vacation', '집에서 보내는 휴가', 'survey', """
T02|Where in your home do you like to spend a day off? What is in that space? Why is it comfortable?
T09|How did you spend your days off at home a few years ago? How do you spend them now? What changed?
T08|Has your rest at home ever been interrupted by something unexpected? What happened? How did you spend the rest of the day?
"""),
        block('communication', '연락 방법', 'common', """
T03|How do you keep in touch with friends you don't see often? Do you call or send messages? How often do you contact them?
T10|Compare calling someone and texting someone to make plans. What is good or bad about each? Which do you use more?
T08|Have you ever had a misunderstanding because of a message? What happened? How did you clear it up?
"""),
        block('travel', '기차 여행', 'survey', """
T11|You are planning a weekend train trip with a friend. Call the train station and ask three or four questions before you buy tickets.
T12|You bought the tickets, but your friend now has to come home one day early. Call the ticket office, explain the situation, and give two ways to change the tickets.
T08|That's the end of the role-play. Have your plans ever changed during a trip or an outing? What happened? How did it turn out?
"""),
        block('reading', '독서와 여가', 'survey', """
T10|Compare spending an evening reading and spending an evening playing games. How are they different? How do you choose which one to do?
T14|Many people feel they don't have enough free time for all their hobbies. How do you decide what to do in your free time? Tell me what you think.
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
