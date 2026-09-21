"""Build a small standalone HTML using browser TTS; no models or audio assets."""
import json
from pathlib import Path
import sys
from zipfile import ZipFile, ZIP_DEFLATED

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import practice_bank as kt
import practice_bank_instrument as sh


def build(profile, bank):
    sets=[bank.authored_questions(bank.REQUIRED_TOPICS,n) for n in range(1,11)]
    payload={'profile':profile,'version':bank.BANK_VERSION,'sets':sets}
    source=ROOT/'portable'
    html=(source/'index.html').read_text(encoding='utf-8')
    replacements={'__PROFILE__':profile,'__STYLE__':(source/'style.css').read_text(encoding='utf-8'),
                  '__APP__':(source/'app.js').read_text(encoding='utf-8'),
                  '__SPEECH__':(ROOT/'static/browser-speech.js').read_text(encoding='utf-8'),
                  '__OPTIONS__':''.join(f'<option value="{n}">{n:02}</option>' for n in range(1,11)),
                  '__DATA__':json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')}
    for key,value in replacements.items():
        html=html.replace(key,value)
    target=ROOT/'data/share'/f'OPIc_{profile}_5-5'
    target.mkdir(parents=True,exist_ok=True)
    (target/'index.html').write_text(html,encoding='utf-8')
    for name in ('START.bat','serve.ps1'):
        (target/name).write_bytes((source/name).read_bytes())
    readme=f'''{profile} OPIc 5–5 연습 · 10회차

PC 실행 (Windows)
1. ZIP을 폴더에 모두 압축 해제합니다.
2. START.bat을 더블클릭합니다. Python, CUDA, AI 모델 설치는 필요 없습니다.
3. Chrome이 열리면 인터넷 연결 상태에서 마이크 · STT 확인을 누릅니다.
4. 마이크를 허용하고 영어 인식 결과를 확인합니다. 회차를 고르고 시작합니다.
5. 질문이 끝나면 답변하세요. Next로 이동합니다. 7번 뒤 같은 난이도로 계속합니다.
6. 종료 후 결과 MD 또는 TXT를 받아 로컬 에이전트에 피드백을 요청합니다.
7. 시험이 끝나면 실행 창을 닫습니다.

index.html에 10회분 질문 텍스트가 들어 있습니다. 질문은 브라우저 기본 TTS로 읽습니다.

모바일 실행
index.html을 HTTPS 정적 웹사이트에 올린 뒤 그 주소를 Android Chrome 또는 iPhone Safari에서 엽니다.
앱 설치는 필요 없습니다. 휴대폰에서 ZIP/HTML 첨부 미리보기나 PC의 HTTP 주소로 열지 마세요.
질문 음성과 마이크 · STT 확인을 먼저 누르고, 시험 중 화면을 켜두세요.
음성인식이 자동 시작되지 않으면 음성인식 다시 시작을 누르세요.
HTML을 직접 열었을 때 마이크/STT가 동작하지 않으면 위 START.bat 방식으로 여세요.
음성 종류와 인식 서비스는 기기와 브라우저에 따라 다릅니다. 실제 휴대폰 마이크·스피커는 시작 전 확인하세요.
브라우저의 STT 기능이 없는 경우 이 페이지에서 시험을 시작할 수 없습니다.
Chrome에서도 네트워크/브라우저 정책으로 STT가 실패할 수 있으므로 사전 확인이 필요합니다.

데이터 처리
- 질문은 기기/브라우저의 영어 TTS로 읽습니다. MP3 사전 생성이나 TTS 모델 설치가 필요 없습니다.
- 음성에 따라 인터넷 연결이 필요할 수 있습니다.
- STT는 인터넷을 이용하며 음성이 브라우저 제공업체의 인식 서버로 전송될 수 있습니다.
- 앱은 답변 음성 파일을 녹음하거나 저장하지 않습니다. 브라우저의 서비스 정책은 별개입니다.
- 현재 시험의 질문별 인식 텍스트는 이 브라우저에 자동 저장됩니다. 파일은 직접 내려받습니다.
- 새 시험 시작 전 최근 결과를 파일로 보관하세요. 브라우저 사이트 데이터를 지우면 임시 결과는 사라집니다.
- 제한시간은 새로고침/창 닫기 중에도 계속 흐릅니다. 돌아오면 이어하기를 누르세요.
- 결과에는 원본 STT와 사용자가 고친 텍스트, 인식 오류 메모가 함께 들어갑니다.

피드백 요청 예시
“첨부한 OPIc 연습 결과를 읽고 문항 충족도, 구성, 문법, 어휘를 문항별로 피드백해줘.
STT 오류 가능성을 감안하고, 내 답변을 바탕으로 자연스러운 개선 답변도 써줘.
음성이 없으므로 발음·억양이나 공식 등급을 확정하지 마.”

공식 기출문항이 아닌 자체 제작 연습문항입니다. 채점 API나 자동 피드백 서비스는 포함하지 않습니다.
'''
    (target/'사용안내.txt').write_text(readme,encoding='utf-8-sig')
    archive=target.with_suffix('.zip')
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        # Explicit allowlist: never recursively collect data/ or session files.
        for name in ('index.html','START.bat','serve.ps1','사용안내.txt'):
            z.write(target/name,arcname=f'{target.name}/{name}')
    print(json.dumps({'profile':profile,'tts':'browser','html_MB':round((target/'index.html').stat().st_size/1e6,2),'zip_MB':round(archive.stat().st_size/1e6,2),'zip':str(archive)},ensure_ascii=False))


if __name__=='__main__':
    for profile,bank in [('SH',sh),('KT',kt)]:
        build(profile,bank)
