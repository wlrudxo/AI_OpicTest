// Browser flow check for data/share/simple/index.html with a fake TTS engine (not a real audio test).
// Run: python scripts/build_simple.py; node scripts/verify_simple.cjs [screenshot-dir]
const path = require('node:path'), assert = require('node:assert/strict');
const {chromium} = require('playwright');
const file = 'file:///' + path.resolve('data/share/simple/index.html').replace(/\\/g, '/');
const shots = process.argv[2];

const fakeTTS = () => {
  window.__spoken = [];
  const synth = {
    getVoices: () => [{lang: 'en-US', voiceURI: 'fake-us', name: 'Fake US'}],
    addEventListener() {}, cancel() {},
    speak(u) {
      window.__spoken.push({text: u.text, rate: u.rate, t: Date.now()});
      setTimeout(() => u.onstart?.(), 10);
      setTimeout(() => u.onend?.(), 300);
    },
  };
  Object.defineProperty(window, 'speechSynthesis', {value: synth});
  window.SpeechSynthesisUtterance = function (text) { this.text = text; };
};

(async () => {
  const browser = await chromium.launch({channel: 'chrome', headless: true});
  const page = await browser.newPage({viewport: {width: 390, height: 844}});
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.addInitScript(fakeTTS);
  await page.goto(file);
  if (shots) await page.screenshot({path: path.join(shots, '1_home.png'), fullPage: true});

  await page.click('#profiles button:has-text("SH")');
  await page.selectOption('#set', '3');
  await page.click('#start');
  assert.equal(await page.textContent('#meta'), 'SH · 03회차');
  assert.equal(await page.textContent('#clock'), '0:00');
  await page.waitForFunction(() => document.getElementById('status').textContent.includes('답변하세요'), null, {timeout: 6000});
  const spoken = await page.evaluate(() => window.__spoken);
  assert.equal(spoken.length, 2, 'question read twice');
  assert.equal(spoken[0].text, spoken[1].text);
  assert.ok(spoken[1].t - spoken[0].t >= 2000, 'gap between plays');
  assert.equal(spoken[0].rate, 0.7);
  await page.waitForTimeout(1300);
  assert.match(await page.textContent('#clock'), /^0:0[1-9]$/);
  assert.ok(await page.evaluate(() => document.getElementById('clock').className === 'run'));
  if (shots) await page.screenshot({path: path.join(shots, '2_answer.png'), fullPage: true});

  // Next during playback cancels it and starts a fresh two-play cycle on Q2.
  await page.click('#next');
  assert.equal(await page.textContent('#qno'), '2');
  assert.equal(await page.textContent('#clock'), '0:00');
  await page.click('#next');
  await page.click('#prev');
  assert.equal(await page.textContent('#qno'), '2');
  await page.waitForFunction(() => document.getElementById('status').textContent.includes('답변하세요'), null, {timeout: 6000});

  // Persisted selection survives reload.
  await page.click('#quit');
  assert.equal(await page.locator('#list li').count(), 15);
  assert.match(await page.textContent('#list li:first-child span'), /답변 0:0\d/);
  if (shots) await page.screenshot({path: path.join(shots, '3_done.png'), fullPage: true});
  await page.reload();
  assert.equal(await page.inputValue('#set'), '3');
  assert.ok(await page.evaluate(() => document.querySelector('#profiles .on').textContent === 'SH'));

  // KT set 05 Q2 matches the GD question list.
  await page.click('#profiles button:has-text("KT")');
  await page.selectOption('#set', '5');
  await page.click('#start');
  await page.keyboard.press('Enter');
  assert.equal(await page.textContent('#qno'), '2');
  const q = await page.evaluate(() => document.getElementById('text').textContent);
  console.log('KT 05 Q2:', q);

  assert.deepEqual(errors, []);
  await browser.close();
  console.log('verify_simple: OK');
})().catch(e => { console.error(e); process.exit(1); });
