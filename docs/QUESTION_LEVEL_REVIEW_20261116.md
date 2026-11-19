# KT·SH 모의고사 문항의 5–5 수준 검토

검토일: 2026-11-16 · 대상: `data/share/KT_모의고사_질문목록.md`(survey-v2), `SH_모의고사_질문목록.md`(instrument-v3) 각 10회차×15문항, 300자리 전수 · 문제은행은 고치지 않았다.

## 1. 결론

길이와 어휘는 5–5에 맞고, 오히려 실전보다 쉬운 쪽이다. 2026-09-28 개정은 "어려운 단어·요구 항목 과다" 문제를 해결했다. 300자리 중 35단어를 넘는 문항은 없고, 요구 항목 4개는 3문항뿐이며, B2를 넘는 단어는 찾지 못했다. 남은 문제는 난도가 높아서가 아니라 다음 세 가지다.

1. **14–15번이 실전 5–5보다 가볍다.** 15번 20개 중 주변·사회의 동향·이슈를 묻는 것은 7개다. 6개는 "나는 어느 쪽이 좋은가" 수준의 개인 선호이고 3개는 개선안을 내라는 제안형이다. 실전에서 가장 어려운 자리의 연습이 비어 있다.
2. **21문항은 영어가 아니라 "할 말 떠올리기"가 어렵다.** 묘사 자리에 추상 분석형(`What makes a game easy or hard to learn?`)이 들어가 있거나, 전제가 좁은 경험, 대상이 모호한 돌발 문항이다. 05회차 연습기록에서 KT 05-02 답이 묘사가 아닌 원인 분석으로 흘러간 것이 이 유형이다.
3. **질문이 실전보다 짧다.** 평균 22–23단어이고 참고한 공개 5–5 세트는 문항당 약 28–58단어다. 답하기는 편하지만 실전의 긴 질문을 듣고 기억하는 연습은 되지 않는다. 이것은 고칠 결함이라기보다 알고 쓸 한계다.

## 2. 판정 기준

### 실전 5–5 구성

| 자리 | 실전에서 흔한 구성 | 근거 |
|---|---|---|
| 1 | 자기소개 | P2·P3 본문 확인 |
| 2–4, 5–7, 8–10 | 같은 주제 3문항 묶음. 첫 문항은 묘사, 둘째는 습관·과거현재 비교·첫 경험 중 하나, 셋째는 기억에 남는 경험이나 문제 경험. 세 묶음 중 한두 개가 설문 밖(돌발) 주제 | P2·P3 본문 확인, 커뮤니티 검색 발췌 |
| 11–13 | 질문 3–4개 역할극 → 문제 설명과 대안 역할극 → 역할극 종료 후 관련 경험 | P2·P3 본문 확인 |
| 14–15 | 14는 변화·집단 비교(개인이 아니라 사람들·사회 수준), 15는 최근 이슈·뉴스·우려. 5–6 선택에서만 나오는 가장 어려운 묶음 | P2·P3 본문 확인, 커뮤니티 검색 발췌 |

P2는 오픽만수르 5·6 난이도 1회, P3는 오픽만수르 5-5 세트 2다(링크는 [SOURCES](SOURCES.md)). 둘 다 사설 제작 모의고사이며 공식 기출이 아니다. 이번에 두 페이지를 다시 열어 문항별 유형·길이를 받았는데, 요약 모델을 거친 값이라 단어 수는 근사치다. 커뮤니티 검색 발췌(링커리어 후기 등)는 검색 결과 요약만 보았고 본문은 열지 않았다. 공식 자료(O4)는 12–15문항이라는 것만 말하고 번호별 배치는 정하지 않는다. 그래서 위 표는 "흔한 구성"이지 규칙이 아니다.

### 질문 문장 기준

| 항목 | 이번 검토의 기준 | 참고 세트(P2·P3, 근사) |
|---|---|---|
| 단어 수 | 35 이하 정상, 36 이상 초과 | 일반 문항 28–41, 역할극 43–58 |
| 문장 수 | 2–4 | 3–5 |
| 요구 항목 | 3 이하 정상, 4 이상 초과 | 2–4 |
| 가장 긴 문장 | 20단어 이하 정상, 25 이상 초과 | 확인 안 함 |
| 어휘 | CEFR B1–B2 안. 그 밖 단어는 문제로 표시 | `indicated`, `resolve`, `unavailable`, `stained`, `responsibilities` 등이 쓰인다 |

기준은 사용자가 지적한 문제(어려운 단어, 요구 과다)를 잡도록 참고 세트보다 엄격하게 잡았다. 어휘는 CEFR 사전과 기계 대조하지 않고, 7자 이상 단어 전체 목록과 300문항 본문을 읽어 판단했다.

## 3. 정량 점검

집계 스크립트는 `output/question_level_count.py`(커밋 안 함). 요구 항목은 의문문 수 + 명령문(`Tell me`, `Compare`, `Call` 등) 수 + 한 문장 안에 `, and what/how…`로 이어 붙인 물음 수로 셌다. 역할극의 "질문 서너 개"는 1개로 셌다.

| 항목 | KT (150) | SH (150) |
|---|---|---|
| 단어 수 평균 / 중앙 / 범위 | 22.8 / 22 / 15–33 | 22.1 / 21 / 14–34 |
| 단어 15 이하 · 16–25 · 26–35 · 36 이상 | 1 · 116 · 33 · 0 | 2 · 121 · 27 · 0 |
| 문장 수 2 · 3 · 4 | 40 · 109 · 1 | 47 · 101 · 2 |
| 요구 항목 1 · 2 · 3 · 4 | 20 · 24 · 105 · 1 | 22 · 29 · 97 · 2 |
| 가장 긴 문장 평균 / 최대 | 12.6 / 19 | 12.8 / 20 |
| **기준 초과: 단어 36+** | 0 | 0 |
| **기준 초과: 요구 4+** | 1 (01-14) | 2 (01-14, 07-14) |
| **기준 초과: 긴 문장 25+** | 0 | 0 |
| B2 밖 단어 | 0 | 0 |

요구 4개인 세 문항도 `Which one do you prefer, and why?`처럼 짧게 붙은 형태라 고칠 필요는 없다. 어휘에서 가장 어려운 축은 `venue`, `atmosphere`, `misunderstanding`, `interrupted`, `equipment`, `console`, `trail` 정도이고 모두 B1–B2다.

## 4. 문제 문항

심한 순이다. 수정 제안은 이번에 새로 쓴 문장이며 그대로 넣기 전에 리드가 고른다.

### A. 묘사 자리에 추상 분석형 (4개)

묶음 첫 문항인데 대상을 묘사하지 않고 원인·기준을 분석하게 한다. 실전 첫 문항은 눈에 보이는 대상을 묻는다.

| 회차-번호 | 원문 | 수정 제안 |
|---|---|---|
| KT 05-02 | What makes a game easy or hard to learn? Use a game you know as an example. What does a new player need to know? | Tell me about a game you play often. What kind of game is it? How do you play it? |
| KT 10-02 | What makes you want to go to a certain concert? Is it the singer, the songs, or the place? What matters most to you? | Tell me about a singer or band you want to see in concert. What kind of music do they play? Why do you like them? |
| SH 10-05 | What makes a park a nice place for you? Use a park you know as an example. What does it have? | Tell me about a park you often go to. Where is it? What does it have? |
| KT 09-02 | Tell me about the audience at a live show. What do people do before and during the show? How does it affect the mood? | Tell me about a theater or hall where you watch live shows. What does it look like? Where do you usually sit? |

### B. 15번이 이슈가 아닌 개인 선호·제안형 (9개)

15번 20개의 내용을 나누면 동향·이슈 7개(KT 01·05·08, SH 01·05·07·10), 사람들의 찬반을 묻는 의견 4개(KT 03, SH 02·03·09), 개인 선호 6개, 제안형 3개다. 개인 선호형은 14번의 `Which do you prefer?`와 답이 겹친다. 제안형은 가정·해결책 논의에 가까워 설계 문서가 기본 세트에서 뺀 T16 쪽이다.

| 회차-번호 | 원문 | 문제 | 수정 제안 |
|---|---|---|---|
| KT 09-15 | Some people go to parks to rest quietly, and others go to play sports. How can a park be good for both groups? Give me some ideas. | 제안형 | What problems do people have at parks these days? Tell me about one problem. What do people say about it? |
| KT 07-15 | What would make your neighborhood a better place for walking? What is the most needed change? Why? | 제안형, SH 08-15와 거의 같은 질문 | What problems do people have when they walk in your city? Why is it a problem? What is being done about it? |
| SH 08-15 | What would make your neighborhood more comfortable for people who like to walk? What change would you like to see? Why? | 제안형 | More people walk or jog for their health these days. Why do you think that is? What have you noticed? |
| KT 10-15 | Many people feel they don't have enough free time for all their hobbies. How do you decide what to do in your free time? Tell me what you think. | 개인 선호 | How do people around you spend their free time these days? How is it different from the past? Why did it change? |
| KT 02-15 | Some people plan every day of a trip, and others just go with the flow. Which way works better for you when you travel abroad? Why? | 개인 선호, 숙어 | What do people worry about when they travel abroad these days? Tell me about one concern. Why is it a problem? |
| KT 06-15 | Some people think they should do something useful even on their days off. What do you think? What makes a day off worth it for you? | 개인 선호, 숙어 | How do people in your country spend their vacations these days? What has changed? Why? |
| SH 06-15 | Do you like to make a plan for your days off, or do you decide as you go? Why? Give me an example. | 개인 선호 | KT 06-15 제안과 같은 방향 |
| SH 04-15 | Some people like to go back to a country they know, and others always choose a new place. Which do you prefer for your next trip abroad? Why? | 개인 선호 | Which countries are popular with travelers from your country these days? Why do people go there? |
| KT 04-15 | Do you think talking about a book with other people makes reading more fun? Why or why not? Give me an example. | 개인 선호(가벼움) | Do people read less than before? What do people around you say about it? Why do you think so? |

### C. 대상이 모호하거나 답할 내용이 잘 안 떠오르는 문항 (10개)

| 회차-번호 | 원문 | 문제 | 수정 제안 |
|---|---|---|---|
| KT 03-09 | Think about something you do with technology today. How did people do it in the past? What is the biggest difference? | 대상을 스스로 정해야 함 | How has the phone you use changed since you were younger? What was your first phone like? What can you do now? |
| KT 07-09 | How do you decide where to put furniture in a room? What do you think about first? | 일상에서 거의 하지 않는 판단 | How has the furniture in your home changed since you were a child? What did you have back then? |
| KT 08-09 | How do people in your building or neighborhood share news or information? Give me an example. | 내용이 없을 수 있음 | How often do you see your neighbors? What do you usually do or talk about when you meet them? |
| KT 08-08 | Tell me about the area around your home. What places do your neighbors share? Where do you run into them? | 묻는 것이 어색함, 숙어 | Tell me about your neighbors. Who lives near you? What are they like? |
| KT 09-09 | How do people use a service at a public place you know, like a library or community center? What do they need to bring? What do they do when they get there? | 33단어, 대상 모호 | How do you borrow a book from a library? What do you need? What do you do first? |
| SH 06-09 | How did you use that kind of device a few years ago? How do you use it now? What has changed? | `that kind of device`가 앞 답변에 의존 | How has the device you use the most changed over the years? What was it like before? |
| SH 02-14 | How are yoga classes today different from the past? How did people learn yoga before? How do they learn it now? | 요가 수업의 과거를 알아야 함 | Compare doing yoga at home and doing it in a class. How are they different? Which is better for you? |
| SH 03-08 | How do you usually get around when you have several places to go in one day? How do you choose what to take? | 조건이 좁음 | How do you usually get around? What do you take? Why do you use it? |
| KT 08-02 | Tell me about a place shown in a movie that you remember. What did it look like? Why was it memorable? | 특이한 대상 | Tell me about the movie theater you often go to. Where is it? What does it look like? |
| KT 08-05 | When you travel in your country, is there a place you like to stop on the way? What is it like? What do you do there? | 특이한 대상 | Tell me about a place in your country you like to visit. Where is it? What is it like? |

### D. 전제가 좁은 경험 (7개)

실전의 경험 문항은 `a memorable experience at/while …`처럼 넓게 묻는다. 아래는 해당 경험이 없으면 지어내야 한다. 조건을 떼고 넓히면 된다.

| 회차-번호 | 좁은 전제 | 수정 방향 |
|---|---|---|
| KT 01-04 | 예상과 다르게 흘러간 게임 | Tell me about a memorable time you played a game. … |
| KT 02-04 | 본 뒤 누군가와 많이 이야기한 영화 | 기억에 남는 영화 한 편 |
| KT 05-07 | 계획에 없던 것을 발견한 국내 여행 | 기억에 남는 국내 여행 |
| KT 07-04 | 공원·야외에서 누군가를 만난 기억 | 공원에서 있었던 기억에 남는 일 |
| KT 05-10 | 같은 시간에 약속을 두 개 잡은 실수 | 약속을 바꾸거나 취소해야 했던 일 |
| SH 05-04 | 공원에서 만난 흥미로운 사람·동물 | 공원에서 있었던 기억에 남는 일 |
| SH 09-06 | 기대보다 좋았던 집 휴가 | 기억에 남는 집 휴가 |

### E. 구어 숙어 (9곳, 가벼움)

단어 자체는 쉽지만 TTS로 들으면 놓치기 쉬운 구동사·숙어다. 실전 질문은 이런 표현을 잘 쓰지 않는다. 고치면 좋고 안 고쳐도 5–5 범위 안이다.

`go with the flow`(KT 02-15), `got you into`(KT 01-06, SH 04-03), `run into`(KT 08-08), `clear it up`(KT 10-10), `ended up`(KT 02-10), `worth it`(KT 06-15), `died`(SH 06-10, 기기 방전), `decide as you go`(SH 06-15). 각각 `follow no plan`, `made you interested in`, `meet`, `solve it`, `do instead`, `a good day off`, `ran out of battery`, `decide on the day` 정도로 바꾸면 된다.

## 5. 유형·배치 점검

전체 배치는 실전의 흔한 구성과 맞는다. 고난도 6단계용 추상 논증(T16)은 섞여 있지 않다.

- **1번, 11–13번**: 20회차 모두 자기소개, 질문 3–4개 → 문제 설명과 대안 2개 → 종료 선언 뒤 관련 경험. 참고 세트와 같다. 길이만 짧다(우리 약 21–34단어, 참고 43–58).
- **2–10번 묶음**: 60개 묶음 중 49개가 묘사로 시작하고 11개가 습관·절차로 시작한다. 둘째·셋째 문항의 조합이 다양한 것도 참고 세트와 같다. 다만 9개 묶음은 셋째가 경험이 아니라 과거·현재 비교나 첫 경험으로 끝난다(예: KT 01회차 5–7, SH 01회차 5–7). 어긋난다고 볼 정도는 아니다.
- **돌발 비중**: 모든 회차에서 8–10번이 설문 밖 주제이고 2–7번은 설문 주제다. 흔한 구성 그대로지만 위치가 고정이라 "8번부터 돌발"을 예측하게 된다. 실전은 돌발 묶음이 2–4나 5–7에도 온다.
- **문제 해결 경험**: 회차당 2–3개(13번 포함, KT 24개·SH 25개). 참고 세트는 세트당 2개다. 10번 자리의 70%가 문제 경험이라 조금 치우쳐 있다.
- **14–15번**: 가장 어긋나는 곳이다. 14번은 비교 16개·과거현재 4개로 유형은 맞지만 대부분 "내 취향의 A와 B"이고, 참고 세트의 14번은 세대·사회 수준의 변화나 집단 비교다. 15번은 4절 B와 같다. 또 14–15번 주제가 20회차 모두 설문 주제인데, 참고 세트는 둘 다 돌발 주제(인터넷, 재활용)였다.

## 6. 권장 조치

1. **(2026-11-17 15번 9개 적용: 4절 B를 T13 동향·이슈형으로 교체. 14번은 미적용)** **15번을 "주변·사회의 동향·이슈"로 통일하고 14번 일부를 사람들 수준의 비교로 올린다.** 15번은 `What issues/problems/changes do people talk about … these days? Why?` 틀로 4절 B의 9개를 바꾼다. 14번은 20개 중 절반쯤을 `How is … different between younger and older people / from the past in your country?` 형태로 바꾼다. 어휘는 지금 수준을 유지한다.
2. **묶음 첫 문항과 경험 문항의 규칙을 정해 4절 A·C·D의 21개를 고친다.** 첫 문항은 `Tell me about + 눈에 보이는 대상`으로 시작하고 `What makes …`, `How does it affect …`를 쓰지 않는다. 경험 문항의 전제는 "기억에 남는", "최근", "문제가 있었던" 세 가지까지만 붙인다. 돌발은 사용자가 대상을 고르게 하지 말고 질문이 대상을 정해 준다.
3. **길이는 더 줄이지 않는다.** 여유가 있으면 회차의 몇 문항에 실전식 도입 문장(`You indicated in the survey that you like …`)을 붙이고, 돌발 묶음 위치를 회차마다 2–4·5–7·8–10으로 돌린다. 시험이 12/3이라 1·2번을 먼저 하고 이것은 뒤로 미뤄도 된다.

## 7. 공식 예시 대조와 KT 06–10회차 개편 (2026-11-19)

사설 세트만 참고한 한계를 줄이려고 공식 공개 예시 두 가지의 원문을 받아 대조했다.

| 자료 | 문항 길이 | 눈에 띄는 점 |
|---|---|---|
| [LTI OPIc Examinee Handbook](https://www.languagetesting.com/pub/media/wysiwyg/PDF/opic-examinee-handbook.pdf)(2018) Advanced 예시 4개 | 약 40–50단어(시사 보도 1개는 21단어) | `Tell me the whole story … from beginning to end in as much detail as you can`처럼 길고 자세한 답을 요구한다. Intermediate 예시는 10–25단어다 |
| [멀티캠퍼스 주관사 가이드](https://www.opic.co.kr/senior/mail/2016/0729/images/a/opic_guide.pdf)(2016) 모의고사 15문항 | 12–38단어 | `You indicated in the survey that …`, `Tell me in detail`, 역할극의 `I'd like to give you a situation …`, `I'm sorry, but there is a problem you need to resolve.` |

판정은 1절과 같다. 유형과 배치는 맞고 난도는 실전보다 쉬운 쪽이다. 새로 확인한 것은 우리 문항에 "자세히, 처음부터 끝까지" 요구가 없어 짧은 답으로 끝나기 쉽다는 점이다. 2026-09-28 KT 모의고사의 답변 중앙값이 54초였다.

설문 개편 이후의 실제 기출 복기는 공개 자료에서 찾지 못했다. 위 두 자료도 2016, 2018년 것이다.

조치: KT 06–10회차를 실전형으로 다시 썼다(survey-v3, [구현 범위](PRACTICE_SETS.md)). 4절의 KT 문항 중 06–10회차에 있던 9개(A의 09-02, 10-02, C의 07-09, 08-02, 08-05, 08-08, 08-09, 09-09, D의 07-04)는 이 개편으로 없어졌다. KT 01–05회차의 6개와 SH의 문항은 그대로다.

## 한계

- 실전 구성과 길이의 근거는 사설 모의고사 두 세트와 커뮤니티 요약이다. 공식 번호별 배치나 실제 기출 원문과 대조한 것이 아니다.
- 참고 세트의 단어 수는 페이지를 요약 모델로 받아 근사치다.
- 어휘는 사람이 읽어 판단했고 CEFR 목록과 기계 대조하지 않았다.
- TTS로 들었을 때의 난도는 확인하지 않았다.
- 4절의 개수(A 4, B 9, C 10, D 7, E 9곳)는 검토자의 판단이며 경계에 있는 문항이 더 있을 수 있다.
