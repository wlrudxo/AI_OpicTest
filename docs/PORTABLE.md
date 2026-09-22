# 설치 없는 PC·모바일 OPIc 연습

질문은 브라우저 기본 TTS로 읽고 답변은 브라우저 STT로 텍스트로 남긴다. Python·CUDA·Whisper·TTS 모델 설치나 MP3 준비가 필요 없다. 기기의 영어 음성을 선택할 수 있으며 음질과 인터넷 필요 여부는 음성에 따라 다르다.

## 모바일 사용

1. 아래 빌드로 만든 `data/share/OPIc_SH_5-5/index.html` 또는 KT 파일을 HTTPS 정적 웹사이트에 올린다. HTML 하나만 제공하면 된다. 호스팅 배포는 자동으로 수행하지 않는다.
2. 휴대폰에서 해당 HTTPS 주소를 Android Chrome 또는 iPhone Safari로 연다. 메신저 첨부 미리보기나 PC의 일반 HTTP 주소 대신 브라우저로 연다.
3. 회차를 고르고 시험 시작을 누른다. 사전 테스트는 필요 없다. 첫 답변 때 마이크 권한을 요청하면 허용한다. 음성 설정·테스트는 선택 메뉴이며 이전 연결 확인 여부를 기억한다.
4. 문항마다 PLAY를 눌러 질문을 듣는다. 인식이 자동 시작되지 않으면 음성인식 다시 시작을 누른다. 시험 중 화면을 켜두고 다른 앱으로 전환하지 않는다.
5. 시험 후 결과 MD/TXT를 내려받아 피드백을 요청한다.

브라우저에 음성인식 기능이 없으면 시작 버튼 옆에서 지원 브라우저로 여는 방법을 안내한다. 같은 브라우저라도 기기·네트워크·권한에 따라 인식 서비스가 실패할 수 있다. 실제 기기의 마이크와 스피커는 시작 전 확인이 필요하다.

## PC 사용

Windows에서는 ZIP을 풀고 `START.bat`을 실행하면 기본 PowerShell로 localhost에서 제공한다. Python이나 모델 설치는 필요 없다. 인터넷에 연결한 Chrome에서 열고 음성·마이크를 확인한다. HTTPS 주소를 사용하는 방법도 가능하다.

## 사용과 데이터

- SH / KT 각각 10회차, 15문항, 난이도 5–5, 40분, 최대 2회 청취.
- 질문 음성 파일을 포함하거나 생성하지 않는다. PLAY를 누른 즉시 브라우저 TTS에 요청한다.
- 브라우저 STT는 음성을 제공업체의 서버로 전송할 수 있다. 앱은 답변 음성 파일을 생성·저장하지 않는다.
- 현재 시험의 텍스트는 프로필별 localStorage에 보관한다. 새로고침이나 창 닫기로 타이머는 멈추지 않는다. 사이트 주소·브라우저를 바꾸면 기존 결과가 이동하지 않는다.
- 결과 TXT·MD에 문항, 원본 STT, 사용자 수정본, 인식 오류와 무응답 상태를 포함한다. 다음 시험 전에 내보낸다.
- 음성 없는 발음·억양 평가나 공식 등급 판정은 제공하지 않는다.
- ZIP은 `index.html`, `START.bat`, `serve.ps1`, `사용안내.txt`만 담는다. 기존 세션·개인 설정·모델은 포함하지 않는다.

## 빌드와 검증

빌드 PC에는 Python 3.10 이상만 필요하다. 표준 라이브러리로 만들며 TTS 패키지나 FFmpeg는 사용하지 않는다.

```powershell
python scripts/build_portable.py
python scripts/verify_portable_package.py
node scripts/verify_portable.cjs
```

결과물: `data/share/OPIc_SH_5-5.zip`, `data/share/OPIc_KT_5-5.zip` 및 각각의 폴더. HTML은 약 90KB, ZIP은 약 20KB다. 기존 `data/portable-audio`와 모델·WAV 캐시는 사용하지 않는다.

자동 검증은 두 은행의 300문항 자리 일치, 음성 파일 없는 패키지 구성, 15문항 이동, STT final/interim 처리, 권한 오류, 내보내기, 복구, TTS 실패·취소, 재생 횟수 제한, 미지원 환경과 제한시간 종료를 확인한다. 가짜 인식·합성 엔진을 사용하는 흐름 검증이며 실제 휴대폰 음질과 인식 정확도를 보장하지 않는다.

동작 근거: [MDN SpeechSynthesis](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis), [SpeechRecognition](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition), [Secure contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Secure_Contexts).

브라우저 화면 검증: 데스크톱 Chromium의 390×844 뷰포트에서 시작·시험 화면과 가로 넘침 없음을 확인했다. 실제 휴대폰의 음성 합성·마이크 인식은 미검증이다.

## Android 전사 처리 (2026-09-22)

Android에서는 `continuous=false`, `interimResults=true`로 문장 단위 인식을 사용한다. Chromium Android의 연속 모드는 중간 가설을 확정 결과로 변환할 수 있어, 짧은 발화가 `my`, `my name`, `my name is`처럼 겹쳐 누적되는 현상을 피하기 위한 설정이다. 문장 인식이 끝나면 앱이 다음 인식을 자동 시작하고 앞 문장은 보존한다. 문장 사이에 재연결 간격이 생길 수 있다.

중간 가설은 같은 결과 자리에서 갱신하고 확정 결과로 교체한다. 실제로 반복해서 말한 단어나 문장을 텍스트 중복 제거로 지우지 않는다. 이름 등 고유명사 오인식은 시험 후 수정할 수 있다. 기존 저장 결과를 임의로 고치지 않는다.

근거: [Chromium Android SpeechRecognitionImpl](https://chromium.googlesource.com/chromium/src/+/e26f3c7e3a932fe4401a979a4bf36e5546b82cb9/content/public/android/java/src/org/chromium/content/browser/SpeechRecognitionImpl.java), [MDN 인식 결과의 갱신 규칙](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognitionEvent/results).
