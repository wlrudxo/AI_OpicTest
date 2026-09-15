# 로컬 음성 전사

faster-whisper large-v3를 CUDA float16으로 사용한다. 외부 STT API에 녹음을 전송하지 않는다.

## 환경 준비

- Python 의존성은 루트의 `requirements.txt`로 설치한다. `requirements-stt-lock.txt`는 개발 당시 전체 패키지 스냅샷이다.
- large-v3 모델을 로컬 캐시에 미리 준비해야 한다. `load_model()`은 자동 다운로드하지 않는다.
- Windows에서 호환 cuDNN 9·cuBLAS 12 DLL을 찾을 수 있어야 한다. 필요하면 `OPIC_CUDA_DLL_DIR`를 해당 디렉터리로 지정한다.
- `stt.py`는 가상환경과 기본 Python의 `Lib/site-packages/torch/lib`도 검사한다. CUDA DLL은 저장소에 포함되지 않는다.
- GPU가 없는 환경을 위한 CPU 전사 fallback은 구현되어 있지 않다.

근거: [faster-whisper 공식 설치 안내](https://github.com/SYSTRAN/faster-whisper#gpu).

## 사용

```powershell
.\transcribe.bat "C:\path\answer.webm" --output "data\answer.json"
```

원문, 구간·단어별 시간, 처리 상태, 로컬 음성 경로가 JSON에 저장된다. 결과에는 개인정보가 포함될 수 있으므로 공개 저장소에 올리지 않는다.

웹앱은 서버 시작 시 모델을 한 번 로드하고 단일 GPU worker로 문항별 전사를 처리한다. `/mic`에서 마이크만 점검할 수도 있다. 자세한 흐름은 README를 참고한다.

## 검증

`scripts/verify_stt.py`는 별도로 준비된 영어 테스트 음성과 무음을 검사한다. 이는 사용자 발화 정확도·발음 평가를 보장하는 검사가 아니다. 테스트 결과와 오디오는 `data/verification/`에 저장하며 Git에서 제외한다.
