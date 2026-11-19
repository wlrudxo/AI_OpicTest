/* Simple OPIc mock: two question plays, optional waiting, pausable active-time clocks. */
(() => {
const DATA = JSON.parse(document.getElementById('data').textContent);
const $ = id => document.getElementById(id);
const KEY = 'opic-simple-v1';
const saved = (() => { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch { return {}; } })();
const GAP = 2000, WARN = 90, OVER = 120;
const fmt = s => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
const setNo = () => String($('set').value).padStart(2, '0');
let profile = DATA.profiles[saved.profile] ? saved.profile : Object.keys(DATA.profiles)[0];
let qs = [], i = 0, token = 0, ticker = null, times = [];
let phase = 'waiting', paused = false, round = 1, answerMs = 0, totalMs = 0, lastTime = performance.now();
const save = () => localStorage.setItem(KEY, JSON.stringify({profile, set: $('set').value, voice: $('voice').value, rate: $('rate').value, autoplay: $('autoplay').checked}));
const show = id => ['home', 'exam', 'done'].forEach(s => { $(s).hidden = s !== id; });
const speak = text => BrowserSpeech.speak(text, {voiceURI: $('voice').value, rate: Number($('rate').value)});
const wait = ms => new Promise(r => setTimeout(r, ms));
const setStatus = (status, hint = '') => { $('status').textContent = status; $('hint').textContent = hint; };
const playing = () => phase === 'playing' || phase === 'gap';
const blur = () => document.activeElement?.blur?.();
function renderProfiles() {
  $('profiles').replaceChildren(...Object.entries(DATA.profiles).map(([key, p]) => {
    const b = document.createElement('button');
    b.textContent = key; b.title = p.label; b.className = key === profile ? 'on' : '';
    b.onclick = () => { profile = key; renderProfiles(); save(); };
    return b;
  }));
  $('topics').textContent = `${profile} 설문: ${DATA.profiles[profile].label}`;
}
function tick() {
  const now = performance.now(), delta = now - lastTime;
  lastTime = now;
  if (!paused && (playing() || phase === 'answering')) totalMs += delta;
  if (!paused && phase === 'answering') answerMs += delta;
  const s = Math.floor(answerMs / 1000);
  $('total').textContent = fmt(Math.floor(totalMs / 1000));
  $('clock').textContent = fmt(s);
  $('clock').className = phase !== 'answering' ? '' : s >= OVER ? 'over' : s >= WARN ? 'warn' : 'run';
}
function controls() {
  $('listen').hidden = phase !== 'waiting';
  $('skip').hidden = !playing() || paused;
  $('pause').disabled = phase === 'waiting' || phase === 'error';
  $('pause').textContent = paused ? '▶ 계속' : '⏸ 일시정지';
  $('pause').setAttribute('aria-pressed', String(paused));
  $('exam').classList.toggle('paused', paused);
}
function cancel() { ++token; BrowserSpeech.cancel(); }
function answer() {
  tick(); cancel(); paused = false; phase = 'answering';
  setStatus('🎤 답변하세요', '다 말했으면 다음 ❯'); controls(); tick();
}
async function playQuestion(from = 1) {
  tick(); cancel();
  const my = token;
  paused = false; phase = 'playing'; round = from; controls();
  try {
    for (let n = from; n <= 2; n++) {
      round = n; phase = 'playing';
      setStatus(`🔊 질문 재생 ${n} / 2`, n === 1 ? '잘 들어 두세요.' : '한 번 더 들려줍니다.');
      await speak(qs[i].prompt);
      if (my !== token) return;
      if (n === 1) {
        tick(); phase = 'gap'; round = 2;
        setStatus('잠시 후 다시 재생', '바로 답변을 눌러 건너뛸 수 있어요.');
        await wait(GAP);
        if (my !== token) return;
      }
    }
  } catch (e) {
    if (my !== token) return;
    tick(); phase = 'error'; controls();
    setStatus('⚠ 음성을 재생하지 못했어요', (e && e.message) || '다시를 눌러 주세요.');
    return;
  }
  answer();
}
function pause() {
  blur();
  if (phase === 'waiting' || phase === 'error') return;
  tick();
  if (paused) {
    paused = false;
    if (playing()) { playQuestion(round); return; }
    setStatus('🎤 답변하세요', '다 말했으면 다음 ❯');
  } else {
    paused = true; cancel();
    setStatus('⏸ 일시정지 중', playing() ? `계속하면 질문 ${round}회차를 다시 읽어요.` : '계속을 누르면 답변 시계가 이어져요.');
  }
  controls(); tick();
}
function remember() {
  if (phase === 'answering') times[i] = Math.max(times[i] || 0, Math.floor(answerMs / 1000));
}
function goto(n, autoplay = $('autoplay').checked) {
  tick(); remember(); cancel(); blur(); paused = false; phase = 'waiting'; answerMs = 0;
  if (n >= qs.length) return finish();
  i = Math.max(0, n);
  const q = qs[i];
  $('qno').textContent = i + 1;
  $('qtype').textContent = q.topic === q.type ? q.type : `${q.topic} · ${q.type}`;
  $('text').textContent = q.prompt; $('textbox').open = false;
  $('bar').firstElementChild.style.width = `${(i / qs.length) * 100}%`;
  $('prev').disabled = i === 0;
  $('next').textContent = i === qs.length - 1 ? '끝내기 ❯' : '다음 ❯';
  setStatus('질문 듣기 대기', '준비되면 눌러 주세요. 시계는 멈춰 있어요.'); controls(); tick();
  if (autoplay) playQuestion();
}
function start() {
  save(); qs = DATA.profiles[profile].sets[Number($('set').value) - 1];
  times = []; totalMs = answerMs = 0; phase = 'waiting'; lastTime = performance.now();
  $('meta').textContent = `${profile} · ${setNo()}회차`; show('exam');
  clearInterval(ticker); ticker = setInterval(tick, 250); goto(0, true);
}
function finish() {
  tick(); remember(); cancel(); paused = false; phase = 'waiting'; clearInterval(ticker);
  $('summary').textContent = `${profile} · ${setNo()}회차 · 전체 ${fmt(Math.floor(totalMs / 1000))}`;
  $('list').replaceChildren(...qs.map((q, n) => {
    const li = document.createElement('li'), meta = document.createElement('span');
    meta.textContent = `${q.topic} · ${q.type}${times[n] != null ? ` · 답변 ${fmt(times[n])}` : ''}`;
    li.append(q.prompt, document.createElement('br'), meta); return li;
  })); show('done');
}
$('set').replaceChildren(...Array.from({length: 10}, (_, n) => new Option(`${String(n + 1).padStart(2, '0')}회차`, n + 1)));
if (saved.set) $('set').value = saved.set;
if (saved.rate) $('rate').value = saved.rate;
$('autoplay').checked = saved.autoplay === true;
const fillVoices = () => {
  BrowserSpeech.populate($('voice'));
  if (saved.voice && [...$('voice').options].some(o => o.value === saved.voice)) $('voice').value = saved.voice;
};
fillVoices(); window.speechSynthesis?.addEventListener?.('voiceschanged', fillVoices); renderProfiles();
$('set').onchange = $('voice').onchange = $('rate').onchange = $('autoplay').onchange = save;
$('test').onclick = () => speak('Please introduce yourself.').catch(e => alert(e.message));
$('start').onclick = start;
$('next').onclick = () => goto(i + 1);
$('prev').onclick = () => goto(i - 1);
$('listen').onclick = () => { blur(); playQuestion(); };
$('pause').onclick = pause;
$('skip').onclick = () => { blur(); answer(); };
$('replay').onclick = () => { blur(); tick(); answerMs = 0; playQuestion(); tick(); };
$('quit').onclick = e => { e.preventDefault(); blur(); finish(); };
$('again').onclick = () => show('home');
document.addEventListener('keydown', e => {
  if ($('exam').hidden || e.repeat || !['Enter', ' '].includes(e.key)) return;
  // A deliberately focused text disclosure keeps its native keyboard action.
  if (e.target.closest?.('summary')) return;
  e.preventDefault(); blur();
  if (e.key === ' ') pause();
  else if (phase === 'waiting') playQuestion();
  else goto(i + 1);
});
})();
