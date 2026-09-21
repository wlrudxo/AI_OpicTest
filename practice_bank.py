"""Original survey-based practice sets; these are not official exam questions.

Each block stores its actual speaking task, rather than inferring it from order.
The selected activities are prerequisites; negative survey choices are not topics.
"""
from copy import deepcopy

MAX_SETS = 10
BANK_VERSION = 'survey-v1'
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
T02|Describe a game you like to play in your free time. What does a player do in this game, and which part of it do you find most enjoyable?
T03|Tell me about a typical gaming session for you. How do you decide when to play, whether to play alone or with others, and when it is time to stop?
T07|Tell me about a time a game turned out differently from what you expected. Describe what you were trying to do, what actually happened, and how you reacted afterward.
"""),
        block('reading', '독서', 'survey', """
T02|Describe the kinds of books you enjoy reading. Choose one kind and explain what you usually find inside those books and what keeps you interested in them.
T06|How did you first become interested in reading for pleasure? Tell me about a person, a book, or an experience that encouraged you to read, and describe what happened.
T09|How have your reading habits changed since you were younger? Compare where you read and how you choose books now with what you used to do, and explain the changes.
"""),
        block('transport', '교통', 'common', """
T02|Describe the public transportation available near your home. Which service is convenient for you, and what should a visitor know about using it?
T05|Tell me about the last time you used public transportation. Where were you going, what was the journey like, and what did you do when you arrived?
T08|Tell me about a time a delay made it difficult to reach a destination. What caused the delay, how did you respond, and how did the situation end?
"""),
        block('shows', '공연 예매', 'survey', """
T11|You want to see a live performance with a friend this weekend. Call the theater's ticket office and ask three or four questions that will help you choose a performance and book seats.
T12|You and your friend have now booked tickets, but the theater announces that the performance will start two hours later. Call your friend, explain the change, and suggest two ways to handle your plans.
T08|The role-play is over. Tell me about a real time the schedule for an event changed unexpectedly. What plans did you have, what changed, and what did you decide to do?
"""),
        block('movies', '영화 감상 방식', 'survey', """
T10|Compare watching a movie at home with watching one at a theater. Describe the atmosphere and the choices you can make in each place. When would you prefer one experience over the other?
T13|What changes have you noticed in the way people choose movies to watch? Describe one trend you have seen among people around you and explain how it affects their choices.
"""),
    ],
    [
        block('movies', '영화', 'survey', """
T02|Describe a movie character you found interesting. What is the character like, what role does the character have in the story, and why did that person catch your attention?
T04|Explain how you arrange a movie night with another person. Describe how you choose a movie, decide where to watch it, and prepare before it begins.
T07|Tell me about a movie that led to an interesting conversation afterward. Who did you talk with, what did you discuss, and did the conversation change how you felt about the movie?
"""),
        block('park', '공원', 'survey', """
T02|Describe a park you know well. What are its main features, what do visitors do there, and which part of the park would you show to someone visiting for the first time?
T03|What do you usually do during a short visit to a park? Tell me how you get there, how you spend your time, and what affects how long you stay.
T08|Tell me about a time an outdoor outing did not go as planned. What were you expecting to do, what got in the way, and how did you change your plans?
"""),
        block('weather', '날씨', 'common', """
T02|Describe the weather in your area during the season you enjoy most. What is a typical day like, and which activities are comfortable to do at that time of year?
T09|Compare the way you spent very hot or cold days as a child with what you do now. What has changed in your activities, and what has stayed the same?
T05|Tell me about a recent day when the weather affected your routine. Describe the weather, the plans you had, and what you actually did that day.
"""),
        block('reading', '독서 모임', 'survey', """
T11|You are interested in attending a reading group at a local library for the first time. Call the organizer and ask three or four questions about joining the next meeting.
T12|You have signed up for the reading group, but you cannot get a copy of the book before the meeting. Call the organizer, explain the difficulty, and suggest two possible ways you could still participate.
T08|The role-play has ended. Describe a time you could not prepare something you needed for a planned activity. What was missing, how did you deal with it, and what happened in the end?
"""),
        block('travel_abroad', '해외여행 방식', 'survey', """
T10|Compare traveling abroad independently with joining an organized group tour. What choices do travelers have in each case, and what kinds of people might prefer each option?
T14|Some travelers plan every day in advance, while others leave most of the trip open. Which approach works better for you when visiting another country? Explain your view with specific reasons.
"""),
    ],
    [
        block('shows', '공연', 'survey', """
T02|Describe the kinds of live performances you like. What happens on stage in a performance you enjoy, and what makes seeing it in person appealing to you?
T05|Tell me about the most recent live performance you attended. Describe where it took place, what you saw, and how you spent your time before and after the performance.
T06|Tell me about an early experience that sparked your interest in live performances. How did you decide to go, who was involved, and what do you remember about that experience?
"""),
        block('vacation', '집에서 보내는 휴가', 'survey', """
T03|When you spend a vacation at home, how is your daily routine different from an ordinary day? Tell me about when you get up, the activities you choose, and how you relax.
T04|Explain how you prepare to enjoy several days off at home. What do you take care of beforehand, what do you arrange, and how do you decide what to do?
T07|Tell me about a day off at home that was especially satisfying. Describe what happened during the day and explain why it felt different from your usual time at home.
"""),
        block('technology', '생활 속 기기', 'common', """
T02|Describe a device you use often at home. What do you use it for, which features matter to you, and where does it fit into your daily life?
T09|Think about a task you do with technology today. How did you or people around you do the same task in the past? Compare the two ways and explain the biggest difference.
T08|Tell me about a time a device stopped working at an inconvenient moment. What were you doing, what did you try to fix, and how did you finish what you needed to do?
"""),
        block('travel', '국내 숙소 예약', 'survey', """
T11|You are planning a short trip to another city in your country and need a place to stay. Call a guesthouse and ask three or four questions before making a reservation.
T12|You have reserved a room, but your transportation will arrive after the guesthouse's check-in desk closes. Call the guesthouse, explain your situation, and suggest two possible arrangements.
T08|That is the end of the role-play. Tell me about a time you had to change an arrangement because you were going to arrive late. Who did you contact, and how was the problem resolved?
"""),
        block('gaming', '게임 방식 비교', 'survey', """
T10|Compare a game you enjoy playing alone with a game you enjoy playing with other people. How do the goals, pace, and experience of playing differ?
T14|People sometimes disagree about whether playing games together is a good way to spend time with friends. What do you think? Explain what can make the experience enjoyable or frustrating.
"""),
    ],
    [
        block('concerts', '콘서트', 'survey', """
T02|Describe a place where you have attended a concert. What was the space like, how was the audience arranged, and what could you see and hear from your spot?
T04|Explain what you normally do to prepare for a concert. Describe the steps from deciding to attend to arriving at the venue, including anything you check in advance.
T07|Tell me about a moment at a concert that you still remember clearly. What was happening, how did the people around you react, and why did that moment stay with you?
"""),
        block('walking', '걷기', 'survey', """
T02|Describe a route you like to walk, even if you only go occasionally. Where does it lead, what do you pass along the way, and what do you like about it?
T03|When you decide to go for a walk, how do you choose the time, route, and length of the walk? Tell me what you usually do along the way.
T05|Tell me about a recent walk you took. Where did you go, what caught your attention, and how did you feel by the time you returned?
"""),
        block('recycling', '재활용', 'common', """
T04|Explain how you sort and dispose of recyclable items where you live. What do you separate, where do you take it, and what steps do you follow?
T09|How has the way you handle household waste changed over time? Compare what you do now with what you remember doing before, and explain one reason for the change.
T08|Tell me about a time you were unsure how to get rid of something you no longer needed. What was the item, how did you find out what to do, and what did you eventually do?
"""),
        block('gaming', '게임 기기 빌리기', 'survey', """
T11|You would like to borrow a friend's game console for a weekend gathering. Call your friend and ask three or four questions about borrowing it and setting it up.
T12|Your friend has lent you the console, but you discover that one controller will not connect. Call your friend, explain what you have tried, and suggest two ways to deal with the problem.
T08|The role-play is finished. Tell me about a time something you borrowed did not work as expected. What was it, what did you do, and how did you handle the situation with its owner?
"""),
        block('reading', '독서 취향 변화', 'survey', """
T09|Compare the books that appealed to you earlier in life with the books you prefer now. What features do you look for today, and what experiences helped change your preferences?
T14|Do you think discussing a book with other people adds to the experience of reading it? Explain your opinion and describe a situation in which a discussion might help or get in the way.
"""),
    ],
    [
        block('gaming', '게임', 'survey', """
T02|Describe what makes a game easy or difficult for you to learn. Use a game you know as an example and explain the parts a new player needs to understand.
T06|Tell me about how you learned to play a game you now enjoy. Who or what helped you, what was difficult at first, and how did you improve?
T08|Tell me about a time you had difficulty coordinating with other people during a game. What were you trying to do, what went wrong, and how did you respond?
"""),
        block('travel', '국내 여행', 'survey', """
T02|Describe a destination in your country that you would recommend for a short trip. What is the place like, what can visitors do there, and why does it appeal to you?
T04|How do you prepare for a short trip within your country? Explain how you choose transportation, decide what to pack, and organize the things you want to do.
T07|Tell me about a local trip when you discovered something you had not planned to see. How did you find it, what did you do there, and why do you remember it?
"""),
        block('appointments', '약속', 'common', """
T03|How do you usually arrange to meet a friend? Tell me how you choose a time and place and how you keep track of the plans you make.
T05|Tell me about the last time you met someone after making plans in advance. How did you arrange the meeting, what did you do together, and how did the day go?
T08|Describe a time two plans conflicted with each other. How did you notice the problem, what choices did you have, and how did you decide what to do?
"""),
        block('park', '공원 프로그램', 'survey', """
T11|You want to join a weekend guided walk at a park. Call the visitor center and ask three or four questions about the walk so you can decide whether it suits you.
T12|You have signed up, but the visitor center tells you that the guided walk has been canceled. Call the friend who planned to join you, explain the cancellation, and suggest two alternative activities.
T08|The role-play is over. Tell me about a time an activity you wanted to attend was canceled. How did you hear about it, how did you react, and what did you do instead?
"""),
        block('concerts', '콘서트 경험 비교', 'survey', """
T10|Compare attending a small concert with attending a large one. How might the atmosphere, sound, and interaction with performers differ? Explain which experience you would choose and why.
T13|What changes have you noticed in how people share their concert experiences? Describe a habit or trend you have observed and explain how it affects the audience or their friends.
"""),
    ],
    [
        block('reading', '독서', 'survey', """
T02|Describe a place where you find books to read. What is available there, how do you look through the choices, and what makes the place useful to you?
T04|Explain how you choose a book when you do not already have a title in mind. What do you look at first, what information do you use, and how do you make your final decision?
T05|Tell me about the last time you started reading a new book. How did you find it, what were your first impressions, and what did you decide to do after reading the opening part?
"""),
        block('jogging', '조깅', 'survey', """
T02|Describe a place you have used for a light jog, even if you do not jog regularly. What is the route like, and what makes it comfortable or inconvenient to use?
T03|On a day when you choose to go for a short jog, how do you get ready? Tell me how you choose a pace and distance and what you do afterward.
T07|Tell me about an outdoor activity that left you feeling different afterward. You can discuss a short jog or another casual outing. What happened, and how did your mood or energy change?
"""),
        block('deliveries', '배달·배송', 'common', """
T03|When you have something delivered to your home, how do you usually arrange it? Tell me how you provide instructions, check its arrival, and receive the delivery.
T05|Tell me about a recent delivery you received. What were you expecting, how did it arrive, and what did you do after receiving it?
T08|Describe a time an item arrived late or was different from what you expected. How did you notice the problem, who did you contact, and what was the result?
"""),
        block('movies', '영화관 예매', 'survey', """
T11|You want to arrange a movie outing for yourself and two friends. Call the cinema and ask three or four questions that will help you choose a screening and seats.
T12|You have booked the seats, but you notice that you selected the wrong date. Call the cinema, explain the mistake, and suggest two possible ways to correct the booking.
T08|The role-play is complete. Tell me about a real time you made a mistake while booking or ordering something. What happened, how did you try to correct it, and what was the outcome?
"""),
        block('vacation', '휴가 방식', 'survey', """
T10|Compare spending a vacation mostly at home with spending it away from home. How do the costs, daily choices, and opportunities to rest differ for you?
T14|Some people feel they must be productive even during their days off. What do you think makes time off worthwhile? Explain your view using examples of activities you find meaningful.
"""),
    ],
    [
        block('park', '공원', 'survey', """
T02|Describe the kinds of people you see using a park you know. What do different visitors do there, and how does the park provide space for those activities?
T09|How has your use of parks changed over the years? Compare your reasons for visiting parks in the past with your reasons today, and explain what led to the change.
T07|Tell me about a memorable encounter with someone during an outing to a park or another public outdoor place. What happened, what did you say or do, and why do you remember it?
"""),
        block('travel_abroad', '해외 여행', 'survey', """
T02|Describe a place you have visited in another country. What did the surroundings look like, what did people do there, and which details stood out to you?
T05|Tell me about the first day of your most recent trip abroad. Describe what you did after arriving, how you found your way around, and what you remember most about that day.
T08|Tell me about a time it was difficult to communicate while traveling. What were you trying to understand or explain, what did you try, and how did the situation turn out?
"""),
        block('furniture', '가구', 'common', """
T02|Describe a piece of furniture you use often. Where is it, what does it look like, and how does it help you carry out an activity at home?
T04|Explain how you decide where to put furniture in a room. What do you consider first, what do you measure or check, and how do you know the arrangement works?
T08|Tell me about a time you had to move, repair, or replace something at home. What led to the change, what steps did you take, and how did the space work afterward?
"""),
        block('concerts', '콘서트 좌석', 'survey', """
T11|You are considering tickets for a concert at a venue you have never visited. Call the ticket office and ask three or four questions about the seating and the experience at the venue.
T12|You have bought tickets, but the confirmation shows two separate seats instead of seats together. Call the ticket office, explain the problem, and propose two acceptable solutions.
T08|That is the end of the role-play. Tell me about a time an arrangement for you and another person was not what you expected. What was different, and how did you work out a solution?
"""),
        block('walking', '걷기 환경', 'survey', """
T10|Compare walking along busy streets with walking in a quieter outdoor area. What can you do or notice in each setting, and how do you decide which route suits your day?
T14|What changes would make your neighborhood more pleasant for people taking short walks? Describe the most useful improvement and explain why it would matter to people who live there.
"""),
    ],
    [
        block('movies', '영화', 'survey', """
T02|Describe a movie setting that you found memorable. What kind of place was shown, what details created its atmosphere, and how did the setting contribute to your experience of the movie?
T09|Compare how you watched movies several years ago with how you watch them now. What has changed in the devices, places, or people involved, and why did those changes happen?
T08|Tell me about a time something interrupted a movie you were watching. What caused the interruption, how did you deal with it, and were you able to continue watching?
"""),
        block('travel', '국내 여행', 'survey', """
T02|Describe a place you like to stop at during a trip within your country. What can travelers do there, and what makes the stop different from simply passing through?
T05|Tell me about the most recent short trip you took within your country. How did you get there, what did you do during the trip, and what was the journey home like?
T09|How are your short trips today different from the trips you took when you were younger? Compare how you choose destinations and spend your time, and explain why your preferences changed.
"""),
        block('neighbors', '이웃', 'common', """
T02|Describe the area immediately around your home. What places or features do neighbors share, and where do people tend to run into one another?
T03|How do people in your neighborhood usually communicate about shared matters? Describe the ways information is passed around and give an example of when those ways are useful.
T07|Tell me about a time someone nearby helped you, or you helped someone else. What was the situation, what did each person do, and how did the interaction end?
"""),
        block('travel_abroad', '해외 현지 투어', 'survey', """
T11|During a trip abroad, you want to join a guided walking tour of the city. Call the tour company and ask three or four questions to check whether the tour fits your plans.
T12|You have booked the tour, but the company moves the meeting point to a place you cannot reach in time. Call the company, explain the difficulty, and suggest two ways to resolve it.
T08|The role-play has ended. Tell me about a time you had trouble finding or reaching a meeting place. What made it difficult, how did you contact the other people, and what happened next?
"""),
        block('shows', '공연 관람 방식', 'survey', """
T10|Compare seeing a live performance in person with watching a recording of it. What can you notice or enjoy in each format, and what might you miss?
T13|What changes have you noticed in the way people learn about live performances? Describe how a recommendation or a new way of sharing information can affect what people decide to attend.
"""),
    ],
    [
        block('shows', '공연', 'survey', """
T02|Describe what you notice about the audience at a live performance. How do people behave before, during, and after the show, and how does that affect the atmosphere?
T03|What do you usually do on the day of a live performance? Tell me how you organize your other plans, when you arrive, and what you do after the show ends.
T08|Tell me about a time it was difficult to see, hear, or enjoy an event. What caused the difficulty, what did you do about it, and how did the experience end?
"""),
        block('walking', '걷기', 'survey', """
T03|When you take a walk with someone else, how do you spend that time? Tell me how you choose a route, what you talk about or notice, and how you decide when to return.
T10|Compare taking a walk alone with taking one with another person. What is different about the pace, the choices you make, and the way you feel afterward?
T08|Tell me about a time you had to change your route while going somewhere on foot. What blocked your original route, how did you find another way, and what happened in the end?
"""),
        block('public_facilities', '공공시설', 'common', """
T02|Describe a public facility in your area that people can use in their free time. What does it offer, who uses it, and what makes it useful to the community?
T04|Explain how someone can use a service at a public facility you know. Describe what they need to check or prepare and the steps they follow when they arrive.
T05|Tell me about a recent visit to a shared public place, such as a library or community center. Why did you go, what did you do there, and how was the visit?
"""),
        block('reading', '도서관 대출', 'survey', """
T11|You want to borrow a book from a library you have not used before. Speak to a librarian and ask three or four questions about becoming a member and borrowing books.
T12|You have borrowed a book, but you will be away when it is due and cannot return it in person. Call the library, explain your situation, and suggest two possible arrangements.
T08|The role-play is finished. Tell me about a time you had difficulty returning something on time. What had you borrowed, what prevented the return, and how did you settle the matter?
"""),
        block('park', '공원 이용 변화', 'survey', """
T09|Compare how a park or outdoor public space you know is used today with how it was used in the past. What activities or facilities have changed, and what might explain those changes?
T14|Parks serve people who want quiet rest and people who want active recreation. How do you think a park can meet both needs? Explain your ideas with practical examples.
"""),
    ],
    [
        block('concerts', '콘서트', 'survey', """
T02|Describe what makes you interested in attending a particular concert. What do you look for in the performers, the program, or the venue, and which factor matters most to you?
T06|Tell me about how you first became interested in going to concerts. What introduced you to the experience, and what did you learn from an early concert you attended?
T05|Tell me about the last concert you went to or watched live online. Describe how you arranged to watch it, what happened during the performance, and what you did afterward.
"""),
        block('vacation', '집에서 보내는 휴가', 'survey', """
T02|Describe the space at home where you most enjoy spending a day off. What do you keep there, what can you do there, and what makes it comfortable for you?
T09|Compare the way you spent days off at home a few years ago with the way you spend them now. Which activities have changed, and what caused your routine to change?
T08|Tell me about a day off when a task or an unexpected event interrupted your rest. What happened, how did you handle it, and how did you spend the rest of the day?
"""),
        block('communication', '연락 방법', 'common', """
T03|How do you usually keep in touch with friends you do not see often? Tell me which ways of communicating you use and how you decide when to contact them.
T10|Compare making a phone call with exchanging text messages when arranging plans. What is easier or harder about each method, and when do you prefer one over the other?
T08|Tell me about a time a message led to a misunderstanding. What did each person think, how did you discover the confusion, and how did you clear it up?
"""),
        block('travel', '기차 여행', 'survey', """
T11|You are planning a weekend train trip with a friend. Call the train company's information desk and ask three or four questions before deciding which tickets to buy.
T12|You have purchased the tickets, but your friend now needs to return home a day earlier. Call the ticket office, explain the change, and suggest two ways to adjust the travel arrangements.
T08|That is the end of the role-play. Tell me about a time someone's plans changed during a trip or outing. What needed to change, how did you arrange it, and how did things turn out?
"""),
        block('reading', '독서와 여가', 'survey', """
T10|Compare spending an evening reading with spending an evening playing a game. How do the two activities hold your attention, and what makes you choose one on a particular day?
T14|Many people have several leisure activities competing for their free time. How do you think someone can decide what to spend time on without feeling rushed? Explain your view using your own interests.
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
