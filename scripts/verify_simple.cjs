// Fake-TTS browser flow checks; these do not verify real device audio.
// Run after build_simple.py: node scripts/verify_simple.cjs [screenshot-dir]
const path = require('node:path'), fs = require('node:fs'), assert = require('node:assert/strict');
const {chromium} = require('playwright');
const file = 'file:///' + path.resolve('data/share/simple/index.html').replace(/\\/g, '/');
const shots = process.argv[2] || 'output/playwright/simple';
const fakeTTS = () => {
  window.__spoken = []; let active;
  window.__end = () => { const u = active; active = null; u?.onend?.(); };
  Object.defineProperty(window, 'speechSynthesis', {value: {
    getVoices: () => [{lang: 'en-US', voiceURI: 'fake-us', name: 'Fake US'}],
    addEventListener() {}, cancel() { active = null; },
    speak(u) { active = u; window.__spoken.push({text: u.text, rate: u.rate, t: Date.now()}); u.onstart?.(); },
  }});
  window.SpeechSynthesisUtterance = function(text) { this.text = text; };
};
(async () => {
  fs.mkdirSync(shots, {recursive: true});
  const browser = await chromium.launch({channel: 'chrome', headless: true});
  try {
    const page = await browser.newPage({viewport: {width: 390, height: 844}}), errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.addInitScript(fakeTTS); await page.clock.install(); await page.goto(file);
    const text = id => page.textContent('#' + id);
    const count = () => page.evaluate(() => window.__spoken.length);
    const advance = ms => page.clock.runFor(ms);
    const end = () => page.evaluate(() => window.__end());
    const status = s => page.waitForFunction(s => document.getElementById('status').textContent.includes(s), s);
    const shot = name => page.screenshot({path: path.join(shots, name + '.png'), fullPage: true});
    const clocks = async () => [await text('clock'), await text('total')];
    const layout = async () => assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), '390px has no horizontal overflow');
    await page.click('#profiles button:has-text("SH")'); await page.selectOption('#set', '3');
    assert.equal(await page.isChecked('#autoplay'), false);
    await page.click('#start'); assert.equal(await text('meta'), 'SH · 03회차');
    assert.equal(await count(), 1, 'first question starts immediately');
    await end(); await status('잠시 후'); await advance(2000); assert.equal(await count(), 2);
    await end(); await status('답변하세요');
    const spoken = await page.evaluate(() => window.__spoken);
    assert.equal(spoken[0].text, spoken[1].text); assert.equal(spoken[0].rate, 0.7);
    assert.ok(spoken[1].t - spoken[0].t >= 2000);
    await advance(2500); assert.equal(await text('clock'), '0:02'); await shot('answer'); await layout();
    await page.click('#pause'); await status('일시정지 중');
    const frozen = await clocks(); await advance(5500); assert.deepEqual(await clocks(), frozen);
    await shot('paused'); await layout();
    await page.keyboard.press('Space'); await advance(1000); assert.equal(await text('clock'), '0:03');
    await page.click('#next'); assert.equal(await text('qno'), '2');
    const beforeWait = await count(), waitClocks = await clocks();
    await advance(4500); assert.equal(await count(), beforeWait); assert.deepEqual(await clocks(), waitClocks);
    assert.equal(await text('clock'), '0:00'); await shot('waiting'); await layout();
    assert.equal(await page.locator('#textbox').getAttribute('open'), null);
    await page.keyboard.press('Enter'); assert.equal(await count(), beforeWait + 1);
    // Pausing the first play restarts that same play; stale completions cannot advance it.
    await page.keyboard.press('Space'); const playFrozen = await clocks();
    await advance(3000); assert.deepEqual(await clocks(), playFrozen);
    await page.click('#pause'); assert.equal(await count(), beforeWait + 2); await status('1 / 2');
    await end(); await status('잠시 후');
    await page.click('#pause'); await advance(3000); await page.click('#pause'); await status('2 / 2');
    assert.equal(await count(), beforeWait + 3);
    // Pause during the second play also resumes the second play, not the first.
    await page.click('#pause'); await page.click('#pause'); await status('2 / 2');
    assert.equal(await count(), beforeWait + 4);
    await page.click('#skip'); await status('답변하세요'); await advance(1250); assert.equal(await text('clock'), '0:01');
    assert.equal(await page.locator('#skip').isVisible(), false);
    // Replay resets the answer clock and starts two plays; skip also works during the gap.
    await page.click('#replay'); assert.equal(await text('clock'), '0:00'); await status('1 / 2');
    await end(); await status('잠시 후'); const gapCount = await count();
    await page.click('#skip'); await advance(2500); assert.equal(await count(), gapCount); await status('답변하세요');
    // Threshold colors and no automatic navigation, using virtual time.
    await advance(88000); assert.equal(await page.locator('#clock').getAttribute('class'), 'warn');
    await advance(30000); assert.equal(await page.locator('#clock').getAttribute('class'), 'over');
    assert.equal(await text('qno'), '2');
    await page.click('#pause'); await page.keyboard.press('Enter'); assert.equal(await text('qno'), '3');
    assert.equal(await page.locator('#exam').getAttribute('class'), '');
    await page.click('#prev'); assert.equal(await text('qno'), '2'); await status('대기');
    // Finish from paused answer preserves exactly the displayed active times.
    const listenCount = await count();
    await page.click('#listen'); await end(); await advance(2000); await end(); await status('답변하세요');
    assert.equal(await count(), listenCount + 2, 'listen from waiting completes exactly two plays');
    await advance(2500); await page.click('#pause');
    const finalTotal = await text('total'); await advance(5000); await page.click('#quit');
    assert.ok((await text('summary')).endsWith('전체 ' + finalTotal));
    assert.equal(await page.locator('#list li').count(), 15);
    assert.match(await page.textContent('#list li:first-child span'), /답변 0:03/);
    assert.match(await page.textContent('#list li:nth-child(2) span'), /답변 2:0/);
    await page.click('#again'); await page.locator('#home details summary').click();
    await page.check('#autoplay'); await page.selectOption('#voice', 'fake-us'); await page.selectOption('#rate', '0.85');
    await page.reload(); assert.equal(await page.isChecked('#autoplay'), true);
    assert.equal(await page.inputValue('#set'), '3'); assert.equal(await page.inputValue('#rate'), '0.85');
    assert.equal(await page.inputValue('#voice'), 'fake-us'); assert.equal(await page.textContent('#profiles .on'), 'SH');
    await page.click('#start'); const autoCount = await count(); await page.keyboard.press('Enter');
    assert.equal(await text('qno'), '2'); assert.equal(await count(), autoCount + 1, 'autoplay setting restores immediate speech');
    await end(); await advance(2000); await end(); await status('답변하세요');
    await page.click('#quit'); await page.click('#again');
    await page.click('#profiles button:has-text("KT")'); await page.selectOption('#set', '5'); await page.click('#start');
    await page.keyboard.press('Enter'); assert.equal(await text('qno'), '2');
    assert.deepEqual(errors, []); console.log('verify_simple: OK (waiting, pause/resume, both plays/gap, skip, clocks, persistence, mobile layout)');
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exit(1); });
