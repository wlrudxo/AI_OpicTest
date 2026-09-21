# 공개 모의고사와 설계 근거

## 2026-09-17 문제 유형 추가 조사

[문제 유형 조사](QUESTION_TYPE_RESEARCH_2026-09-17.md)에 공식·주관사 5개와 사설·교육 10개 자료의 확인 범위, 출처별 차이, 핵심 14유형과 확장 2유형을 정리했다. [문제은행 제작 기준](QUESTION_BANK_BLUEPRINT.md)에는 자체 예시 16개와 생성·저장·검수 기준이 있다. 이후 지정 관심 주제 조합의 자체 제작 10세트를 앱에 반영했다. [구현 범위](PRACTICE_SETS.md)는 조사 근거와 구별한다.

## 기존 조사

확인일: 2026-09-08. 아래 목록은 원문에 접근해 확인한 자료의 링크·주제 요약이다. 앱에 문제 전문이나 영상 파일을 가져온 상태는 아니다.

## 바로 사용할 공개 모의고사 3개

| 자료 | 확인한 내용 | 활용 |
|---|---|---|
| [오픽만수르 5·6 난이도 1회](https://opicmansur.com/오픽만수르-모의고사-난이도-5-6-1회/) | 15문항 구성, 집·카페·가구·여행·재활용, 영한 질문과 영상·PDF 안내 | 첫 실전 연습 참고 |
| [오픽만수르 5-5 세트 2](https://mansour.tistory.com/entry/오픽-5-5-기출문제-PDF-다운로드-2회) | 15문항 구성, 술집·교통·음악·렌터카·인터넷, 질문과 PDF 링크 | 두 번째 실전 연습 참고 |
| [멀티캠퍼스 공식 주관사 가이드](https://www.opic.or.kr/senior/mail/2016/0729/images/a/opic_guide.pdf?opicnativepopup=true) | 2016 자료, 인쇄 쪽수 68부터 실전 모의고사 부록, 유형 설명 | 공식 주관사의 질문 스타일 참고 |

오픽만수르 세트 2는 작성자가 실제 시험과 동일한 기출 원문이 아니라 경험을 바탕으로 만든 예상문제라고 명시한다. 모의고사의 90초 답변 제한도 해당 자료의 연습 설정이다.

공개 모의고사는 원문 링크에서 사용한다. 앱에는 출처 정보를 남기며, 전문 재배포·번안 대신 일반적인 주제와 질문 기능을 참고해 독립적인 문항을 생성한다. 특히 세트 2는 링크 공유만 허용하고 자료 재배포·2차 편집 금지를 표시한다.

## 보조 자료

- [오픽만수르 3·4 난이도 2회](https://opicmansur.com/오픽만수르-모의고사-난이도-3-4-2회/): 은행·술집·카페·음악 기기·걷기. 쉬운 워밍업 참고.
- [공유 Sample Questions PDF](https://jkmentorslibrary.weebly.com/uploads/3/7/8/0/37805557/opic_sample_questions.pdf): 7페이지 유형별 질문 모음. 완성형 국내 모의고사나 공식 자료로 분류하지 않는다.
- 여우오픽은 검색에서 확인했으나 YouTube 직접 열기에 실패했다. 이번 확인 완료 목록에는 포함하지 않는다.

## 시험 구성·평가

- [국내 OPIc 공식 시험소개](https://www.opic.or.kr/opics/servlet/controller.opic.site.about.AboutServlet?p_process=move-introduce-opic): 12~15문항, 40분, 설문·자기평가, 전체 답변 종합 평가.
- [ACTFL OPIc 설명과 평가 기준](https://www.actfl.org/assessments/postsecondary-assessments/oral-proficiency-interview-computer-opic): Function, Accuracy, Content/Context, Text Type. 개별 기준을 독립적인 점수 합산으로 다루지 않는다.
- [ACTFL 수험자 안내](https://www.actfl.org/assessments/postsecondary-assessments/opi/tips-for-opi-and-opic-test-takers): 자발적인 발화 평가에 관한 참고.
- 앞의 공식 주관사 PDF: 시험 진행·다시 듣기·난이도 재조정 참고. 2016 발행이므로 세부 UI 규칙의 현재 동일성은 추가 확인 대상.

## 구현 근거

- [faster-whisper 공식 저장소](https://github.com/SYSTRAN/faster-whisper): CUDA 설치 조건, CTranslate2/cuDNN 호환성, GPU 추론·타임스탬프·VAD 옵션.
- [Google Chirp 3](https://docs.cloud.google.com/speech-to-text/docs/models/chirp-3): V2 모델과 동기/배치 인식 길이, 지역별 기능 확인.
- [Google STT 가격](https://cloud.google.com/speech-to-text/pricing): API 도입 시 호출 방식과 저장소 비용을 함께 확인. 이번 계획은 유료 API를 실행하지 않았다.
- [OpenRouter 오디오 문서](https://openrouter.ai/docs/guides/overview/multimodal/audio): 오디오 입력 지원. 이번 MVP에서는 전용 STT 대안으로 Google 선택.
- [MDN MediaRecorder](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder): 브라우저 녹음.
- [MDN dataavailable](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder/dataavailable_event): stop 뒤 마지막 Blob 수신을 기다린 후 업로드.
- [MDN getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia): 마이크 권한과 localhost 보안 컨텍스트.

- [MDN SpeechSynthesis](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis): 기기의 음성 목록, 브라우저 TTS, voiceschanged 처리.
- [MDN SpeechRecognition](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition): 브라우저별 인식 지원과 서버 기반 인식.
- [MDN Secure contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Secure_Contexts): HTTPS와 localhost 보안 컨텍스트.
