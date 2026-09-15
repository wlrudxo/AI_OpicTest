"""Practice survey catalog; sources and uncertain labels are documented in docs."""
GROUPS = [
    ('leisure', '귀하는 여가 활동으로 주로 무엇을 하십니까?', 2, [
        ('movies','영화보기','watching movies'),('clubs','클럽/나이트클럽 가기','going to clubs'),
        ('shows','공연보기','watching live performances'),('concerts','콘서트보기','going to concerts'),
        ('museums','박물관가기','visiting museums'),('park','공원가기','visiting parks'),
        ('camping','캠핑하기','camping'),('beach','해변가기','visiting the beach'),
        ('sports_watch','스포츠 관람','watching sports'),('home_improve','주거 개선','improving your home'),
        ('cooking_shows','요리 관련 프로그램 시청','watching cooking shows'),
        ('gaming','게임하기','playing video games'),('social_posts','SNS 글 올리기','posting on social media'),
        ('job_search','구직 활동','looking for a job'),('bars','술집/바에 가기','going to bars'),
        ('texting','친구들과 문자하기','texting friends'),('billiards','당구 치기','playing billiards'),
        ('volunteering','자원봉사','volunteering'),('driving','드라이브하기','going for a drive'),
        ('test_prep','시험 대비 과정 수강','taking test preparation courses'),
        ('news','뉴스 보거나 듣기','watching or listening to the news'),
        ('cafe','카페/커피 전문점 가기','visiting cafes'),('chess','체스하기','playing chess'),
        ('tv','TV 시청','watching television'),('shopping','쇼핑하기','shopping'),
        ('reality_shows','리얼리티 쇼 보기','watching reality shows')]),
    ('hobbies', '귀하의 취미나 관심사는 무엇입니까?', 1, [
        ('reading_child','아이에게 책 읽어주기','reading books to children'),('music','음악 감상하기','listening to music'),
        ('instrument','악기 연주하기','playing a musical instrument'),('singing','혼자 노래부르거나 합창하기','singing'),
        ('dance','춤추기','dancing'),('writing','글쓰기(편지, 단문, 시 등)','writing'),
        ('drawing','그림 그리기','drawing'),('cooking','요리하기','cooking'),('pets','애완동물 기르기','caring for pets'),
        ('travel_reading','여행 잡지/블로그 읽기','reading travel magazines or blogs'),
        ('photography','사진 촬영하기','taking photographs'),('investing','주식 투자','investing in stocks'),
        ('newspapers','신문 읽기','reading newspapers'),('reading','독서','reading books')]),
    ('sports', '귀하는 주로 어떤 운동을 즐기십니까?', 1, [
        ('basketball','농구','playing basketball'),('baseball','야구/소프트볼','playing baseball'),
        ('soccer','축구','playing soccer'),('football','미식축구','playing American football'),
        ('hockey','하키','playing hockey'),('cricket','크리켓','playing cricket'),('golf','골프','playing golf'),
        ('volleyball','배구','playing volleyball'),('tennis','테니스','playing tennis'),('badminton','배드민턴','playing badminton'),
        ('table_tennis','탁구','playing table tennis'),('swimming','수영','swimming'),('cycling','자전거','cycling'),
        ('skiing','스키/스노우보드','skiing or snowboarding'),('skating','아이스 스케이트','ice skating'),
        ('jogging','조깅','jogging'),('walking','걷기','walking'),('yoga','요가','doing yoga'),
        ('hiking','하이킹/트레킹','hiking'),('fishing','낚시','fishing'),('gym','헬스','working out at a gym'),
        ('no_exercise','운동을 전혀 하지 않음','relaxing in your free time'),
        ('taekwondo','태권도','practicing taekwondo'),
        ('exercise_classes','운동 수업 수강하기','taking exercise classes')]),
    ('vacations', '귀하는 어떤 휴가나 출장을 다녀온 경험이 있습니까?', 1, [
        ('business_local','국내출장','taking business trips within your country'),
        ('business_abroad','해외출장','taking business trips abroad'),('vacation','집에서 보내는 휴가','spending vacations at home'),
        ('travel','국내 여행','traveling within your country'),('travel_abroad','해외 여행','traveling abroad')]),
]


def catalog():
    return [{'id': key, 'name': label, 'activity': activity, 'group': group, 'group_label': title, 'minimum': minimum}
            for group, title, minimum, items in GROUPS for key, label, activity in items]
