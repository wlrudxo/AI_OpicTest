/* Simple OPIc mock: profile + set selection, each question auto-read twice, count-up answer timer. */
(() => {
const DATA = JSON.parse(document.getElementById('data').textContent);
const $ = id => document.getElementById(id);
const KEY = 'opic-simple-v1';
const saved = (() => { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch { return {}; } })();
const GAP = 2000, WARN = 90, OVER = 120;
const fmt = s => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
const setNo = () => String($('set').value).padStart(2, '0');
let profile = DATA.profiles[saved.profile] ? saved.profile : Object.keys(DATA.profiles)[0];
let qs = [], i = 0, token = 0, answerStart = 0, examStart = 0, ticker = null, times = [];

const save = () => localStorage.setItem(KEY, JSON.stringify({profile, set: $('set').value, voice: $('voice').value, rate: $('rate').value}));
const show = id => ['home', 'exam', 'done'].forEach(s => { $(s).hidden = s !== id; });
const speak = text => BrowserSpeech.speak(text, {voiceURI: $('voice').value, rate: Number($('rate').value)});
const wait = ms => new Promise(r => setTimeout(r, ms));
const setStatus = (status, hint = '') => { $('status').textContent = status; $('hint').textContent = hint; };

function renderProfiles() {
  $('profiles').replaceChildren(...Object.entries(DATA.profiles).map(([key, p]) => {
    const b = document.createElement('button');
    b.textContent = key;
    b.title = p.label;
    b.className = key === profile ? 'on' : '';
    b.onclick = () => { profile = key; renderProfiles(); save(); };
    return b;
  }));
  renderTopics();
}
// Like the full app, do not hint each set's topics before starting.
const renderTopics = () => { $('topics').textContent = `${profile} 설문: ${DATA.profiles[profile].label}`; };

function tick() {
  $('total').textContent = fmt(Math.floor((Date.now() - examStart) / 1000));
  const c = $('clock');
  if (!answerStart) { c.textContent = '0:00'; c.className = ''; return; }
  const s = Math.floor((Date.now() - answerStart) / 1000);
  c.textContent = fmt(s);
  c.className = s >= OVER ? 'over' : s >= WARN ? 'warn' : 'run';
}

async function playQuestion() {
  const my = ++token;
  answerStart = 0; tick();
  try {
    for (let n = 1; n <= 2; n++) {
      setStatus(`🔊 질문 재생 ${n} / 2`, n === 1 ? '잘 들어 두세요.' : '한 번 더 들려줍니다.');
      await speak(qs[i].prompt);
      if (my !== token) return;
      if (n === 1) {
        setStatus('⏸ 잠시 후 다시 재생');
        await wait(GAP);
        if (my !== token) return;
      }
    }
  } catch (e) {
    if (my !== token) return;
    setStatus('⚠ 음성을 재생하지 못했어요', (e && e.message) || '다시 재생을 눌러 주세요.');
    return;
  }
  answerStart = Date.now(); tick();
  setStatus('🎤 답변하세요', '다 말했으면 다음 ❯');
}

function goto(n) {
  if (answerStart) times[i] = Math.max(times[i] || 0, Math.floor((Date.now() - answerStart) / 1000));
  answerStart = 0; token++; BrowserSpeech.cancel();
  document.activeElement?.blur?.(); // so Enter always means "next", not the last clicked button
  if (n >= qs.length) return finish();
  i = Math.max(0, n);
  const q = qs[i];
  $('qno').textContent = i + 1;
  $('qtype').textContent = q.topic === q.type ? q.type : `${q.topic} · ${q.type}`;
  $('text').textContent = q.prompt;
  $('textbox').open = false;
  $('bar').firstElementChild.style.width = `${(i / qs.length) * 100}%`;
  $('prev').disabled = i === 0;
  $('next').textContent = i === qs.length - 1 ? '끝내기 ❯' : '다음 ❯';
  playQuestion();
}
function start() {
  save();
  qs = DATA.profiles[profile].sets[Number($('set').value) - 1];
  times = []; examStart = Date.now();
  $('meta').textContent = `${profile} · ${setNo()}회차`;
  show('exam');
  clearInterval(ticker); ticker = setInterval(tick, 250);
  goto(0);
}
function finish() {
  if (answerStart) times[i] = Math.max(times[i] || 0, Math.floor((Date.now() - answerStart) / 1000));
  answerStart = 0; token++; BrowserSpeech.cancel(); clearInterval(ticker);
  $('summary').textContent = `${profile} · ${setNo()}회차 · 전체 ${fmt(Math.floor((Date.now() - examStart) / 1000))}`;
  $('list').replaceChildren(...qs.map((q, n) => {
    const li = document.createElement('li');
    const meta = document.createElement('span');
    meta.textContent = `${q.topic} · ${q.type}${times[n] != null ? ` · 답변 ${fmt(times[n])}` : ''}`;
    li.append(q.prompt, document.createElement('br'), meta);
    return li;
  }));
  show('done');
}

$('set').replaceChildren(...Array.from({length: 10}, (_, n) => new Option(`${String(n + 1).padStart(2, '0')}회차`, n + 1)));
if (saved.set) $('set').value = saved.set;
if (saved.rate) $('rate').value = saved.rate;
const fillVoices = () => {
  BrowserSpeech.populate($('voice'));
  if (saved.voice && [...$('voice').options].some(o => o.value === saved.voice)) $('voice').value = saved.voice;
};
fillVoices();
window.speechSynthesis?.addEventListener?.('voiceschanged', fillVoices);
renderProfiles();
$('set').onchange = save;
$('voice').onchange = $('rate').onchange = save;
$('test').onclick = () => speak('Please introduce yourself.').catch(e => alert(e.message));
$('start').onclick = start;
$('next').onclick = () => goto(i + 1);
$('prev').onclick = () => goto(i - 1);
$('replay').onclick = () => { $('replay').blur(); token++; BrowserSpeech.cancel(); playQuestion(); };
$('quit').onclick = e => { e.preventDefault(); finish(); };
$('again').onclick = () => show('home');
document.addEventListener('keydown', e => {
  // Enter on a focused exam control keeps its native action (e.g. the text toggle).
  if ($('exam').hidden || e.key !== 'Enter' || e.repeat || (e.target !== document.body && $('exam').contains(e.target))) return;
  e.preventDefault(); goto(i + 1);
});
})();
