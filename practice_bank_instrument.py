"""Original practice sets for the instrument/gym/yoga survey combination.

No particular instrument, employment, or regular exercise schedule is assumed.
These are practice questions, not official or recalled exam questions.
"""
from practice_bank import block, assemble_questions

BANK_VERSION = 'instrument-v3'
REQUIRED_TOPICS = frozenset({
    'yoga', 'shows', 'concerts', 'park', 'instrument', 'jogging',
    'walking', 'gym', 'vacation', 'travel', 'travel_abroad',
})

SETS = [
    [
        block('instrument', '악기 연주', 'survey', """
T02|Tell me about the musical instrument you play or used to play. What does it look like? What do you like about it?
T03|When do you usually play your instrument? Where do you play? What do you practice?
T07|Tell me about a time you felt proud of something you played. What were you playing? Why was it special?
"""),
        block('yoga', '요가', 'survey', """
T02|Tell me about the place where you do yoga. What does it look like? Why do you like doing yoga there?
T05|Tell me about the last time you did yoga. Where were you? What poses did you do?
T09|How has your yoga practice changed since you first started? What was hard at the beginning? What is different now?
"""),
        block('home', '집', 'common', """
T02|Tell me about the home you live in now. What does it look like? Where do you spend the most time?
T03|What do you usually do when you get home in the evening? Tell me about your routine.
T08|Have you ever had something in your home break or stop working? What was the problem? How did you fix it?
"""),
        block('concerts', '콘서트 예매', 'survey', """
T11|You and a friend want to go to a concert. Call the ticket office and ask three or four questions before you buy tickets.
T12|You bought two concert tickets, but your friend just found out they can't get there before the concert starts. Call your friend, explain the situation, and give two ways to handle it.
T08|That's the end of the role-play. Have you ever had to change plans with someone for an event? Why did the plans change? What happened after that?
"""),
        block('park', '공원 이용', 'survey', """
T10|Compare two parks you know. How are they alike, and how are they different? What do you do at each park?
T13|How do people use parks these days? Tell me about a change you have noticed in your area.
"""),
    ],
    [
        block('gym', '헬스', 'survey', """
T02|Tell me about a gym you have been to or know about. What equipment does it have? What do you find useful there?
T04|When you decide to work out, how do you get ready? What do you do from start to finish? It's fine if you only work out once in a while.
T08|Has anything ever stopped you from working out as planned? What happened? What did you do instead?
"""),
        block('travel', '국내 여행', 'survey', """
T02|Tell me about a place in your country that is good for a short trip. What is the area like? Why do you like it?
T04|How do you get ready for a trip in your country? How do you choose where to stay? What do you bring?
T07|Tell me about a memorable moment from a trip in your country. Where were you? What happened?
"""),
        block('weather', '날씨', 'common', """
T02|What is the weather like in your area at this time of year? How does it affect people's daily lives?
T09|What did you do on rainy days when you were a child? What do you do now? What has changed?
T05|Tell me about a recent day when the weather surprised you. What did you expect? What was it actually like?
"""),
        block('instrument', '악기 대여', 'survey', """
T11|You want to try a new instrument before buying one. Call a music store that rents instruments and ask three or four questions about renting one for a week.
T12|You rented the instrument, but when you get home, you find that an important part is missing. Call the store, explain the problem, and give two ways to solve it.
T08|That's the end of the role-play. Have you ever received something that was missing a part or was not what you expected? How did you find out? What did you do?
"""),
        block('yoga', '요가 배우는 방식', 'survey', """
T09|How are yoga classes today different from the past? How did people learn yoga before? How do they learn it now?
T14|Some people say yoga is more about the mind than the body. What do you think? Why?
"""),
    ],
    [
        block('shows', '공연', 'survey', """
T02|Tell me about a live show you would recommend to a friend. What kind of show is it? What happens on stage?
T03|What do you usually do when you go to see a show? How do you get ready? What do you do after the show?
T07|Tell me about a memorable moment at a live show you saw. What was happening on stage? How did the audience react?
"""),
        block('walking', '걷기', 'survey', """
T02|Tell me about a place where you like to go for a walk. What can you see there? Why do you like it?
T05|Tell me about the last time you went for a walk. Why did you go? What did you see along the way?
T09|How are your walks now different from a few years ago? Where did you walk back then? Who did you walk with?
"""),
        block('transport', '교통', 'common', """
T03|How do you usually get around when you have several places to go in one day? How do you choose what to take?
T10|Compare two kinds of transportation you have used. How are they different? When do you use each one?
T08|Have you ever taken the wrong bus or train? How did you notice? How did you get to where you were going?
"""),
        block('travel', '여행 숙소', 'survey', """
T11|You are planning to stay at a guesthouse for a weekend trip in your country. Call the owner and ask three or four questions before you make a reservation.
T12|You booked a room, but your train is delayed and you will arrive after check-in time. Call the owner, explain the problem, and give two ways to handle your arrival.
T08|That's the end of the role-play. Have you ever arrived somewhere much later than planned? Why were you late? How did it turn out?
"""),
        block('instrument', '악기 연습 방식', 'survey', """
T10|Compare practicing an instrument alone and practicing with other people. How are they different? What can you learn from each?
T14|Some people learn an instrument from online videos, and others take lessons from a teacher. What are the good and bad points of each way?
"""),
    ],
    [
        block('concerts', '콘서트', 'survey', """
T02|Tell me about a concert hall or venue you have been to. What does it look like inside? Where do you like to sit or stand?
T06|How did you first become interested in concerts? Was there a person or a singer who got you into it?
T08|Have you ever had a problem at a concert or a crowded event? What went wrong? How did you deal with it?
"""),
        block('vacation', '집에서 보내는 휴가', 'survey', """
T03|How do you spend a vacation day at home when you have no plans? What do you do in the morning, afternoon, and evening?
T05|Tell me about the last time you had a few days off at home. What did you plan to do? What did you actually do?
T09|How are your vacations at home now different from when you were younger? What did you do back then?
"""),
        block('shopping', '생활용품 구매', 'common', """
T02|Tell me about a store where you buy things for your home. What does it sell? Why do you go there?
T04|How do you choose what to buy when there are many similar products? What do you check first?
T08|Have you ever bought something that was not as good as you expected? What was wrong with it? What did you do?
"""),
        block('gym', '헬스장 이용', 'survey', """
T11|You want to try a nearby gym before signing up for a long membership. Call the gym and ask three or four questions about a one-day pass or a short-term pass.
T12|You bought a one-month pass, but the gym says it will close for repairs for most of that month. Call the manager, explain the problem, and give two ways to solve it.
T08|That's the end of the role-play. Have you ever gone somewhere and found it unexpectedly closed? What did you need to do there? What did you do instead?
"""),
        block('travel_abroad', '해외여행 준비', 'survey', """
T09|How is getting ready for a trip abroad different from the past? How did people find information back then? How about now?
T14|Some people like to go back to a country they know, and others always choose a new place. Which do you prefer for your next trip abroad? Why?
"""),
    ],
    [
        block('park', '공원', 'survey', """
T02|Tell me about your favorite spot in a park you go to. What is around it? Why do you like to spend time there?
T05|Tell me about the last time you went to a park. Who did you go with? What did you do there?
T07|Tell me about an interesting person or animal you met at a park. What happened? Why do you remember it?
"""),
        block('instrument', '악기와 첫 경험', 'survey', """
T02|Tell me about the place where you play or used to play your instrument. What is in that room? Is it a good place to practice?
T06|Tell me about the first time you tried to play an instrument. Why did you try it? Who helped you?
T08|Has anything ever stopped you from practicing your instrument? What happened? When were you able to play again?
"""),
        block('appointments', '약속', 'common', """
T03|How do you usually make plans to meet a friend? How do you decide on a time and place?
T05|Tell me about a recent time you met up with someone. Why did you meet? How did it go?
T08|Have you and a friend ever mixed up the time or place of a meeting? How did you find out? What did you do?
"""),
        block('yoga', '요가 수업 예약', 'survey', """
T11|You want to try a yoga class at a new studio near your home. Call the studio and ask three or four questions about the classes.
T12|You booked a trial class, but you just found out you have an important appointment at the same time. Call the studio, explain the situation, and give two ways to solve the problem.
T08|That's the end of the role-play. Have you ever had to cancel or change a class or lesson you signed up for? Why? What did you do?
"""),
        block('gym', '운동 장소', 'survey', """
T10|Compare working out at home and working out at a gym. How are they different? Which is better for you?
T13|What kinds of exercise have become popular among people around you these days? Why do you think people like them?
"""),
    ],
    [
        block('travel_abroad', '해외여행', 'survey', """
T02|Tell me about a city you visited in another country. What were the streets like? What place do you remember most?
T04|What do you do on your first day in another country? How do you get to your hotel? What do you check?
T08|Have you ever had a problem or a misunderstanding during a trip abroad? What happened? How did you handle it?
"""),
        block('jogging', '조깅', 'survey', """
T02|Tell me about a place where you have jogged or where people in your area go jogging. What is the path like?
T03|When you go jogging, what do you do before, during, and after? It's okay if you only jog once in a while.
T07|Tell me about a time jogging or exercising outside that you remember well. Where were you? What happened?
"""),
        block('technology', '생활 속 기기', 'common', """
T02|Tell me about a device that makes your life easier. What does it do? How do you use it?
T09|How did you use that kind of device a few years ago? How do you use it now? What has changed?
T08|Has your phone or another device ever died or stopped working at a bad time? What were you doing? What did you do without it?
"""),
        block('shows', '공연 일정 변경', 'survey', """
T11|A theater near you has several shows next month. Call the box office and ask three or four questions to choose a show to see with a friend.
T12|You and your friend booked a show, but it has been canceled. The theater offers a refund or tickets for another show. Call your friend, explain what happened, and talk about the two choices.
T08|That's the end of the role-play. Has something you were looking forward to ever been canceled? What had you planned? What did you do instead?
"""),
        block('vacation', '휴가 방식', 'survey', """
T10|Compare spending a vacation at home and taking a short trip. How do you get ready for each? What is good or bad about each one?
T14|Do you like to make a plan for your days off, or do you decide as you go? Why? Give me an example.
"""),
    ],
    [
        block('yoga', '요가 루틴', 'survey', """
T02|Tell me about a yoga pose you like. How do you do it? How does it make you feel?
T03|What is your usual yoga routine like? When do you do it? How long does it take? It's okay if you only do yoga once in a while.
T08|Have you ever had a problem while doing yoga, like hurting yourself or not being able to do a pose? What happened? What did you do?
"""),
        block('gym', '운동 경험', 'survey', """
T02|Tell me about a kind of exercise you have tried at a gym. What do you do? What equipment do you use?
T06|Tell me about the first time you worked out at a gym. Why did you go? Did anyone help you?
T09|How have your thoughts about exercise changed over the years? What did you think before? What do you think now?
"""),
        block('neighborhood', '동네', 'common', """
T02|Tell me about your neighborhood. What places are near your home? Which places do you use the most?
T09|Tell me about a change in your neighborhood. What was it like before? What is it like now?
T07|Tell me about a memorable time with a neighbor or someone in your area. What happened? Why do you remember it?
"""),
        block('park', '공원에서 만나기', 'survey', """
T11|Your friend wants to meet at a park you have never been to. Call your friend and ask three or four questions about how to find the place and what to bring.
T12|You arrive at the park, but the entrance your friend told you about is closed. Call your friend, explain where you are, and give two ways you could still meet.
T08|That's the end of the role-play. Have you ever had trouble finding someone you were supposed to meet? What happened? How did you finally meet?
"""),
        block('concerts', '콘서트 관람 방식', 'survey', """
T10|Compare going to a concert in person and watching a concert online. How are they different? Which do you prefer, and why?
T13|What are people around you saying about concerts these days, like ticket prices or getting tickets? Why is it an issue for them?
"""),
    ],
    [
        block('shows', '공연 취향', 'survey', """
T02|Tell me about a performer or group you like to see on stage. What kind of show do they do? What is special about them?
T05|Tell me about the last live show you watched, in person or on TV. Why did you watch it? What did you think?
T09|How are the shows you like now different from the ones you liked when you were younger? What changed?
"""),
        block('travel', '국내 여행 경험', 'survey', """
T02|Tell me about a place you stayed on a trip in your country. What was it like? What was nearby?
T05|Tell me about your last trip in your country. What did you do first? What was the best part?
T08|Have you ever had to change your plans during a trip in your country? What happened? What did you decide to do?
"""),
        block('recycling', '재활용', 'common', """
T04|How do people recycle where you live? What do you do at home? Where do you take the recycling?
T09|How is recycling today different from the past? What rules or habits have changed?
T08|Have you ever had a problem with recycling or throwing something away? What was it? How did you find out what to do?
"""),
        block('instrument', '연습 공간 예약', 'survey', """
T11|You want to book a room at a music practice studio for an afternoon. Call the studio and ask three or four questions about the room and how to book it.
T12|You arrive at the studio, but your room was given to someone else. Talk to the person at the front desk, explain your booking, and give two ways to solve the problem.
T08|That's the end of the role-play. Have you ever arrived somewhere and found that your booking was not there? What did you say? How was it solved?
"""),
        block('walking', '걷기와 조깅', 'survey', """
T10|Compare going for a walk and going for a jog. How are they different? When do you choose each one?
T14|What would make your neighborhood more comfortable for people who like to walk? What change would you like to see? Why?
"""),
    ],
    [
        block('concerts', '콘서트 경험', 'survey', """
T02|What kind of concert would you most like to go to? What kind of music would it have? Why would you like it?
T04|How do you get ready to go to a concert? What do you check before you leave? What do you bring?
T07|Tell me about a concert that left a strong impression on you. What happened? How did you feel?
"""),
        block('vacation', '집에서 쉬는 경험', 'survey', """
T02|What do you like to do on a day off at home? What do you need for it? Why is it relaxing?
T07|Tell me about a vacation at home that was better than you expected. What did you do? Who were you with?
T08|Has a quiet day at home ever been interrupted? What happened? How did the rest of the day go?
"""),
        block('restaurants', '외식', 'common', """
T02|Tell me about a restaurant you like. What is the food like? What is the atmosphere like?
T03|How do you choose a restaurant when you meet someone for a meal? Who decides? What do you usually order?
T08|Have you ever had a problem at a restaurant? What was the problem? What happened in the end?
"""),
        block('travel_abroad', '해외여행 투어', 'survey', """
T11|You are visiting another country and want to join a half-day tour. Call the tour company and ask three or four questions before you book.
T12|You booked the tour, but the company changed the meeting place to somewhere you cannot reach in time. Call the company, explain the problem, and give two ways to solve it.
T08|That's the end of the role-play. Have you ever needed help changing your plans while traveling? Who helped you? How did it work out?
"""),
        block('shows', '공연장과 관객', 'survey', """
T10|Compare watching a show at a small theater and at a big theater. How are they different? Which do you prefer?
T14|Some people take photos or videos with their phones during a show. What do you think about this? Is it okay or not? Why?
"""),
    ],
    [
        block('instrument', '악기 연주 변화', 'survey', """
T02|Tell me about a song or piece of music you like to play or want to learn. What is it like? What part is hard for you?
T05|Tell me about the last time you played your instrument. Where were you? What did you play?
T09|How is the way you play your instrument now different from when you first started? What has changed?
"""),
        block('park', '공원의 변화', 'survey', """
T02|What makes a park a nice place for you? Use a park you know as an example. What does it have?
T09|How has a park you know changed over time? What was there before? What is there now?
T08|Has a visit to a park ever been ruined by crowds, construction, or something else? What happened? What did you do?
"""),
        block('communication', '연락과 소통', 'common', """
T03|How do you keep in touch with friends who live far away? How often do you talk? What do you talk about?
T10|Compare talking on the phone and sending messages to a friend. What is good or bad about each?
T07|Tell me about a memorable phone call or message you got. Who was it from? What did they tell you?
"""),
        block('walking', '산책 약속', 'survey', """
T11|A friend asks you to go for a walk this weekend on a trail you don't know. Call your friend and ask three or four questions about the walk.
T12|You planned the walk, but now heavy rain is expected that day. Call your friend, explain your concern, and suggest two other things you could do together.
T08|That's the end of the role-play. Has bad weather ever made you change an outdoor plan? What did you do instead? Did you enjoy it?
"""),
        block('travel_abroad', '여행지와 관광', 'survey', """
T10|Compare traveling in your country and traveling abroad. What is the same when you get ready? What is different when you get there?
T13|How do people choose where to travel abroad these days? What has changed? Give me an example.
"""),
    ],
]


def authored_questions(topics, set_number):
    if not REQUIRED_TOPICS.issubset(topics):
        return None
    return assemble_questions(SETS, set_number, BANK_VERSION)
