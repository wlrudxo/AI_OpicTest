"""Original practice sets for the instrument/gym survey combination.

No particular instrument, employment, or regular exercise schedule is assumed.
These are practice questions, not official or recalled exam questions.
"""
from practice_bank import block, assemble_questions

BANK_VERSION = 'instrument-v1'
REQUIRED_TOPICS = frozenset({
    'movies', 'shows', 'concerts', 'park', 'instrument', 'jogging',
    'walking', 'gym', 'vacation', 'travel', 'travel_abroad',
})

SETS = [
    [
        block('instrument', '악기 연주', 'survey', """
T02|You indicated that you play a musical instrument. Describe the instrument you play or have played. What does it look and sound like, and what do you like about it?
T03|When you have a chance to play your instrument, how do you spend that time? Describe where you play, what you practice, and how you decide when to finish.
T07|Tell me about a time you felt pleased with something you played. What were you trying to do, what happened during that session, and why did it feel special?
"""),
        block('movies', '영화', 'survey', """
T02|Describe the kinds of movies you enjoy most. What do those movies usually focus on, and which features make you want to watch them?
T05|Tell me about the last movie you watched. How did you choose it, where did you watch it, and what did you think when it ended?
T09|How has your taste in movies changed since you were younger? Compare the stories or characters you liked then with those you enjoy now. What influenced the change?
"""),
        block('home', '집', 'common', """
T02|Describe the home where you live now. Tell me about its layout and the space where you spend the most time. What makes that space comfortable?
T03|What do you usually do after returning home in the evening? Describe the order of your activities and explain which part of that routine you enjoy.
T08|Tell me about a time something in your home did not work properly. What was the problem, what did you do about it, and how was it finally resolved?
"""),
        block('concerts', '콘서트 예매', 'survey', """
T11|You and a friend want to go to a concert, but you have not bought tickets yet. Call the ticket office and ask three or four questions to help you decide which tickets to choose.
T12|You bought two concert tickets, but your friend has just learned that they cannot arrive before the concert starts. Call your friend, explain the situation, and suggest two possible ways to handle the tickets and your plans.
T08|The role-play is over. Tell me about a time you had to change plans for an event with another person. What caused the change, what did you discuss, and what happened afterward?
"""),
        block('park', '공원 이용', 'survey', """
T10|Compare two parks you know. How are their surroundings and facilities alike or different? Explain what you would choose to do at each park.
T13|What changes have you noticed in the way people use parks these days? Describe one change in your area and explain how it affects other visitors.
"""),
    ],
    [
        block('gym', '헬스', 'survey', """
T02|Describe a gym or fitness room you have used or know about. What equipment and spaces are available, and which features do you find useful?
T04|On a day when you decide to work out, how do you prepare and choose what to do? Explain your routine from getting ready to finishing, even if you only exercise occasionally.
T08|Tell me about a time you could not exercise in the way you had planned. What got in the way, how did you respond, and what did you do instead?
"""),
        block('travel', '국내 여행', 'survey', """
T02|Describe a place in your country that you would recommend for a short trip. What is the area like, what can visitors do, and why does it appeal to you?
T04|Explain how you prepare for a short trip within your country. How do you choose transportation and a place to stay, and what do you take with you?
T07|Tell me about a moment on a trip within your country that you still talk about. Where were you, what happened, and what made that moment memorable?
"""),
        block('weather', '날씨', 'common', """
T02|What is the weather usually like in your area at this time of year? Describe the temperature and other conditions, and explain how they affect everyday life.
T09|Compare the way you dealt with rainy days when you were a child with what you do now. What has changed in your clothing, activities, or travel arrangements?
T05|Describe a recent day when the weather surprised you. What had you expected, what was the weather actually like, and how did you spend the day?
"""),
        block('instrument', '악기 대여', 'survey', """
T11|You want to try a different musical instrument before buying one. Call a music shop that offers rentals and ask three or four questions about renting an instrument for a week.
T12|You rented the instrument, but when you get home you discover that an essential accessory is missing. Call the shop, explain why you cannot use the instrument, and propose two possible solutions.
T08|The role-play has ended. Describe a real time an item you received was incomplete or different from what you expected. How did you discover the issue, and what did you do to resolve it?
"""),
        block('movies', '영화 관람 변화', 'survey', """
T09|Compare going to a movie theater today with going to one when you were younger. Discuss the experience before the movie and inside the theater, and explain the most noticeable change.
T14|When watching a movie, some people avoid all reviews while others read many reviews first. Which approach do you prefer, and how does it affect your enjoyment? Give an example.
"""),
    ],
    [
        block('shows', '공연', 'survey', """
T02|Tell me about a live performance you would recommend to a friend. What kind of performance is it, what happens on stage, and what makes it worth seeing?
T03|What do you normally do when you go out to see a performance? Describe how you get ready, what you do at the venue, and how you spend time afterward.
T07|Describe a particularly memorable moment during a live performance you saw. What was happening on stage, how did the audience respond, and how did you feel?
"""),
        block('walking', '걷기', 'survey', """
T02|Describe a route you like to take when you go for a walk. Where does it begin and end, what can you see along the way, and why do you like it?
T05|Tell me about the last time you went for a walk. What made you decide to go, what did you notice along the route, and how did you feel afterward?
T09|Compare your walking habits now with those of a few years ago. Have the places, the people you walk with, or your reasons for walking changed? Explain with details.
"""),
        block('transport', '교통', 'common', """
T03|How do you usually get around when you have several places to visit in one day? Explain how you choose your transportation and organize the journey.
T10|Compare two forms of transportation you have used. Describe how they differ in convenience and comfort, and explain when you would choose each one.
T08|Tell me about a time you got on the wrong bus or train, or took a wrong turn on a journey. How did you realize the mistake, and how did you reach your destination?
"""),
        block('travel', '여행 숙소', 'survey', """
T11|You are planning to stay at a guesthouse for a weekend trip within your country. Call the owner and ask three or four questions before making a reservation.
T12|You reserved a room, but your train has been delayed and you will arrive after the guesthouse's check-in hours. Call the owner, explain the problem, and suggest two ways to arrange your arrival.
T08|That is the end of the role-play. Tell me about a time you arrived somewhere later than planned. What caused the delay, who did you contact, and how did the situation turn out?
"""),
        block('instrument', '악기 연습 방식', 'survey', """
T10|Compare practicing a musical instrument alone with practicing with other people. What is similar, what is different, and what can each experience help a person learn?
T14|Some people learn an instrument mainly from videos, while others prefer lessons with a teacher. What do you see as the advantages and difficulties of each approach?
"""),
    ],
    [
        block('concerts', '콘서트', 'survey', """
T02|Describe a concert venue you have visited or know well. How is the space arranged, what is the atmosphere like, and where would you prefer to sit or stand?
T06|How did you first become interested in going to concerts? Tell me about a person, artist, or early experience that influenced your interest.
T08|Tell me about a difficulty you experienced while attending a concert or another crowded event. What went wrong, how did you deal with it, and were you able to enjoy the event?
"""),
        block('vacation', '집에서 보내는 휴가', 'survey', """
T03|Describe how you spend a vacation day at home when you have no appointments. What do you do in the morning, afternoon, and evening, and how do you decide what to do?
T05|Tell me about the most recent time you spent several days off at home. What did you plan, what did you actually do, and what part was most satisfying?
T09|Compare vacations at home now with those you had when you were younger. How have your activities and the way you spend time with others changed?
"""),
        block('shopping', '생활용품 구매', 'common', """
T02|Describe a place where you buy everyday household items. What does it sell, what is the shopping experience like, and why do you go there?
T04|How do you decide which household product to buy when there are many similar choices? Explain what you check and how you make your final decision.
T08|Describe a time a product you bought failed to meet your expectations. What was wrong with it, how did you contact the seller, and what was the result?
"""),
        block('gym', '헬스장 이용', 'survey', """
T11|You want to visit a nearby gym without committing to a long membership. Call the gym and ask three or four questions about a trial visit or a short-term pass.
T12|You purchased a short-term pass, but the gym announces that it will close for repairs during most of the period you paid for. Call the manager, explain the problem, and suggest two possible solutions.
T08|The role-play is over. Tell me about a time a place you planned to use was unexpectedly closed or unavailable. What did you need to do there, and how did you change your plans?
"""),
        block('travel_abroad', '해외여행 준비', 'survey', """
T09|How has preparing for an overseas trip changed compared with the past? Discuss how travelers obtain information and make arrangements, using examples you know about.
T14|Some travelers prefer returning to a familiar country, while others always choose a new destination. Which would you prefer for your next trip abroad, and why?
"""),
    ],
    [
        block('park', '공원', 'survey', """
T02|Describe your favorite part of a park you visit. What is around it, what can people do there, and what makes you want to spend time in that particular spot?
T05|Tell me about a recent visit to a park. Who went with you, if anyone, what did you do, and was anything different from your usual visits?
T07|Tell me about an interesting encounter you had in a park or another outdoor public space. Describe the people or animals involved, what happened, and why you remember it.
"""),
        block('instrument', '악기와 첫 경험', 'survey', """
T02|Describe the place where you play or used to play an instrument. What is kept there, what is the sound like in that space, and how comfortable is it for practicing?
T06|Tell me about your first experience trying to play an instrument. Why did you try it, who helped you, and what was easy or difficult at the beginning?
T08|Describe a time something interrupted your practice or prevented you from playing an instrument. What happened, what did you do, and when were you able to continue?
"""),
        block('appointments', '약속', 'common', """
T03|How do you usually arrange to meet a friend? Explain how you decide on a time and place, confirm the plans, and keep in touch before the meeting.
T05|Tell me about a recent appointment or meeting in your personal life. Why did you arrange it, how did you prepare, and how did it go?
T08|Tell me about a time you and another person misunderstood the details of an appointment. How did you find out, what did you do to sort it out, and what was the outcome?
"""),
        block('movies', '영화관 좌석', 'survey', """
T11|You are arranging a movie outing for a small group of friends. Call the theater and ask three or four questions about showtimes, available seats, and booking together.
T12|You have booked the outing, but the confirmation shows seats that are far apart instead of together. Call the theater, explain what you expected, and suggest two ways to resolve the booking problem.
T08|The role-play has ended. Tell me about a time a reservation or order contained a mistake. What did you notice, how did you explain the problem, and how was it handled?
"""),
        block('gym', '운동 장소', 'survey', """
T10|Compare doing a simple workout at home with using a gym. How do the space, equipment, and atmosphere differ, and which option suits you better when you want to exercise?
T13|What changes have you noticed in how people around you approach fitness? Describe a particular activity or service that has become more common and explain why people use it.
"""),
    ],
    [
        block('travel_abroad', '해외여행', 'survey', """
T02|Describe a city or area you visited in another country. What were the streets and surroundings like, and which place there left a strong impression on you?
T04|What do you do to prepare for your first day in another country? Explain how you arrange transportation, find your accommodation, and make sure you have what you need.
T08|Tell me about a misunderstanding or unexpected difficulty during an overseas trip. Explain the situation, how you communicated with the people involved, and how you handled it.
"""),
        block('jogging', '조깅', 'survey', """
T02|Describe a place where you have jogged or where people in your area go jogging. What is the route like, and what makes it suitable for a short run?
T03|When you decide to go for a jog, what do you do before, during, and afterward? Describe your own approach, even if jogging is only an occasional activity for you.
T07|Tell me about a jog or other outdoor exercise experience that you remember clearly. Where were you, what happened along the way, and how did you feel when it was over?
"""),
        block('technology', '생활 속 기기', 'common', """
T02|Describe a device that makes your everyday life easier. What does it do, how do you use it, and which feature would you miss most if it were unavailable?
T09|Compare the way you used that kind of device a few years ago with how you use it now. What has changed in the device or in your needs?
T08|Tell me about a time a device ran out of power or stopped working at an inconvenient moment. What were you trying to do, and how did you manage without it?
"""),
        block('shows', '공연 일정 변경', 'survey', """
T11|A local theater is offering several performances next month. Call the box office and ask three or four questions to help you choose a suitable performance to attend with a friend.
T12|You and your friend booked a performance, but it has been canceled. The theater offers a refund or tickets for a different show. Call your friend, explain what happened, and discuss these two alternatives.
T08|That is the end of the role-play. Tell me about a time an activity you looked forward to was canceled. What had you planned, how did you feel, and what did you do instead?
"""),
        block('vacation', '휴가 방식', 'survey', """
T10|Compare taking a vacation at home with taking a short trip away. How do you prepare for each, and what kinds of enjoyment or difficulties does each offer?
T14|Do you prefer to make a schedule for your days off or decide what to do as each day comes? Explain your preference using an example from a vacation or weekend.
"""),
    ],
    [
        block('movies', '영화와 관람 경험', 'survey', """
T02|Describe a movie theater you have been to. What is it like inside and around the building, and what makes the experience there pleasant or unpleasant?
T03|When you watch a movie at home, how do you set things up? Describe how you choose the movie, prepare the room, and deal with interruptions.
T08|Tell me about a time a problem interrupted a movie you were watching. What happened, how did you respond, and did you manage to finish the movie?
"""),
        block('gym', '운동 경험', 'survey', """
T02|Describe a type of exercise you have tried at a gym or fitness room. What do you do, what equipment is involved, and what did you think of the experience?
T06|Tell me about the first time you tried working out at a gym or using fitness equipment. What made you try it, did anyone help you, and how did it go?
T09|How have your feelings about exercise changed over the years? Compare what you used to think or do with your current approach, even if you do not exercise regularly now.
"""),
        block('neighborhood', '동네', 'common', """
T02|Describe the neighborhood around your home. What places do you pass on a short walk, and which features are most useful in your daily life?
T09|Tell me about a change you have noticed in your neighborhood. Describe what the area was like before, what it is like now, and how the change affects you.
T07|Tell me about a memorable interaction with a neighbor or someone in your local area. What brought you together, what happened, and why do you remember it?
"""),
        block('park', '공원에서 만나기', 'survey', """
T11|Your friend has suggested meeting at a park you have never visited. Call your friend and ask three or four questions so that you can find the meeting place and prepare for the outing.
T12|You arrive at the park and discover that the entrance your friend described is closed. Call your friend, explain where you are, and suggest two ways you could still meet.
T08|The role-play is over. Describe a time you had trouble finding someone or reaching a meeting place. What caused the confusion, how did you communicate, and how did you finally meet?
"""),
        block('concerts', '콘서트 관람 방식', 'survey', """
T10|Compare attending a concert in person with watching a live concert online. Describe the sound, atmosphere, and interaction in each case. Which experience do you prefer, and why?
T13|What recent change or issue are concertgoers around you talking about? Describe what you have heard or noticed about tickets, venues, or the concert experience, and explain why it matters to them.
"""),
    ],
    [
        block('shows', '공연 취향', 'survey', """
T02|Describe a performer or performing group you enjoy seeing on stage. What kind of performance do they give, and what do you find distinctive about their style?
T05|Tell me about the last time you watched a live performance, in person or as it was broadcast. What led you to watch it, what did you see, and what was your reaction?
T09|Compare the live performances you were interested in when you were younger with the ones you choose now. What has changed in your preferences, and what influenced you?
"""),
        block('travel', '국내 여행 경험', 'survey', """
T02|Describe somewhere you stayed on a trip within your country. What was the accommodation like, what was nearby, and how did it affect your trip?
T05|Tell me about your most recent trip within your country. Describe your main activities in order and explain which part of the trip you enjoyed most.
T08|Describe a time you had to change your route or schedule during a trip in your country. What caused the change, what options did you consider, and what did you choose?
"""),
        block('recycling', '재활용', 'common', """
T04|Explain how people separate and dispose of recyclable items where you live. What do you do at home, and where do you take the items afterward?
T09|How is recycling today different from what you remember in the past? Discuss the rules or everyday habits that have changed and give a specific example.
T08|Tell me about a time you were unsure how to dispose of an item or encountered a problem with recycling. What made it difficult, how did you find out what to do, and what happened?
"""),
        block('instrument', '연습 공간 예약', 'survey', """
T11|You want to book a room at a music practice studio for one afternoon. Call the studio and ask three or four questions about the room, the equipment, and how to make a reservation.
T12|You arrive for your confirmed reservation, but the studio has assigned your room to another customer. Speak to the receptionist, explain your booking, and suggest two ways to solve the problem.
T08|The role-play has ended. Tell me about a time a facility or service you had arranged was not available when you arrived. How did you explain the issue, and what solution did you reach?
"""),
        block('walking', '걷기와 조깅', 'survey', """
T10|Compare going for a walk with going for a jog. How do your pace, preparation, and attention to your surroundings differ? Explain when you would choose each activity.
T14|What could make your neighborhood more comfortable for people who walk for pleasure? Describe one improvement you would like and explain how it would help different people.
"""),
    ],
    [
        block('concerts', '콘서트 경험', 'survey', """
T02|What kind of concert would you most like to attend? Describe the music and atmosphere you enjoy, and explain what would make it a good concert for you.
T04|Explain how you prepare for a concert outing. Describe what you check beforehand, what you take with you, and how you plan your trip to and from the venue.
T07|Tell me about a concert or musical performance that made a strong impression on you. Describe a particular moment, how it affected you, and what you remember afterward.
"""),
        block('vacation', '집에서 쉬는 경험', 'survey', """
T02|Describe an activity that makes a day off at home enjoyable for you. What do you need for it, where do you do it, and why is it relaxing?
T07|Tell me about a vacation at home that was more enjoyable than you expected. What did you do, who was involved, and what made those days special?
T08|Tell me about a time your plans for a quiet day at home were interrupted. What happened, how did you deal with the interruption, and how did the rest of the day go?
"""),
        block('restaurants', '외식', 'common', """
T02|Describe a restaurant you like or have visited recently. What is the food and atmosphere like, and what would you tell a friend who wanted to go there?
T03|How do you usually choose a restaurant when meeting another person for a meal? Explain what you discuss, how you make a decision, and what you do when you arrive.
T08|Tell me about a time a meal at a restaurant did not go as expected. Describe the problem, how you spoke to the people involved, and what happened in the end.
"""),
        block('travel_abroad', '해외여행 투어', 'survey', """
T11|You are visiting another country and want to join a half-day sightseeing tour. Call the tour organizer and ask three or four questions before deciding whether to reserve a place.
T12|You booked the tour, but the organizer has moved the meeting point to a location you cannot reach by the start time. Call the organizer, explain the difficulty, and suggest two possible arrangements.
T08|That is the end of the role-play. Tell me about a time you needed help changing an arrangement while traveling. What did you need, who helped you, and how did things work out?
"""),
        block('shows', '공연장과 관객', 'survey', """
T10|Compare watching a performance in a small venue with watching one in a large venue. How do the view, atmosphere, and relationship with the performers differ?
T14|People sometimes use their phones to take photos or videos during a performance. What problems or benefits can this create, and what behavior do you think is appropriate? Explain your reasons.
"""),
    ],
    [
        block('instrument', '악기 연주 변화', 'survey', """
T02|Describe a piece of music you enjoy playing or would like to learn on your instrument. What is it like, and which parts do you find appealing or challenging?
T05|Tell me about the most recent time you played an instrument. Where were you, what did you play, and how did the session go from beginning to end?
T09|Compare your approach to playing an instrument now with your approach when you first started. What has changed in your practice, confidence, or choice of music?
"""),
        block('park', '공원의 변화', 'survey', """
T02|What makes a park a pleasant place for you to visit? Describe the paths, facilities, and surroundings you value, using a park you know as an example.
T09|Describe how a park or other outdoor space you know has changed over time. What used to be there, what has been added or removed, and how do you feel about it?
T08|Tell me about a time a park visit was affected by crowds, maintenance, or another unexpected situation. What had you planned to do, and how did you adapt?
"""),
        block('communication', '연락과 소통', 'common', """
T03|How do you keep in touch with friends who live far away? Explain when you contact them, which methods you use, and what you usually talk about.
T10|Compare talking with a friend by phone with talking through messages. What is easier or more difficult about each, and when does one work better than the other?
T07|Tell me about a memorable call or message you received. Who contacted you, what did they tell you, and how did you react to the news?
"""),
        block('walking', '산책 약속', 'survey', """
T11|A friend invites you to walk along an unfamiliar trail this weekend. Call your friend and ask three or four questions about the route and the arrangements so you can decide how to prepare.
T12|The walk is planned, but the forecast now predicts heavy rain during the outing. Call your friend, explain your concern, and suggest two alternatives for spending time together.
T08|The role-play is over. Tell me about a time the weather forced you to change an outdoor plan with someone else. How did you reach a new plan, and did you enjoy what you did instead?
"""),
        block('travel_abroad', '여행지와 관광', 'survey', """
T10|Compare traveling within your country with traveling abroad. What is similar about preparing for the trips, and what differences do you notice once you arrive?
T13|What recent change have you noticed in how people choose or enjoy overseas destinations? Describe an example involving travel information, activities, or visitors' behavior, and explain its effects.
"""),
    ],
]


def authored_questions(topics, set_number):
    if not REQUIRED_TOPICS.issubset(topics):
        return None
    return assemble_questions(SETS, set_number, BANK_VERSION)
