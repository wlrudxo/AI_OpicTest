/* Shared browser TTS: call speak directly from a click to retain mobile activation. */
window.BrowserSpeech = (() => {
  const synth = window.speechSynthesis;
  const supported = !!(synth && window.SpeechSynthesisUtterance);
  let active = null;
  const voices = () => supported ? synth.getVoices().filter(v => /^en(?:-|_)/i.test(v.lang)) : [];

  function populate(select) {
    const chosen = select.value;
    select.replaceChildren(new Option('기기 기본 영어 음성', ''));
    for (const voice of voices()) select.add(new Option(voice.name, voice.voiceURI));
    if ([...select.options].some(option => option.value === chosen)) select.value = chosen;
    select.disabled = !supported;
  }

  function cancel() {
    // Resolve ourselves: some mobile engines omit onend/onerror after cancel().
    active?.finish(null, false);
    if (supported) synth.cancel();
  }

  function speak(text, {voiceURI = '', volume = 1, rate = 1, onStart = () => {}} = {}) {
    cancel();
    if (!supported) return Promise.reject(new Error('이 브라우저는 질문 음성을 지원하지 않습니다. 다른 브라우저에서 열어주세요.'));
    return new Promise((resolve, reject) => {
      const utterance = new window.SpeechSynthesisUtterance(text);
      utterance.lang = 'en-US';
      const available = voices();
      const voice = available.find(v => v.voiceURI === voiceURI) || available.find(v => /^en-US$/i.test(v.lang)) || available[0];
      if (voice) utterance.voice = voice;
      utterance.volume = volume;
      utterance.rate = rate;
      let done = false, started = false, timer;
      const finish = (error, completed = true) => {
        if (done) return;
        done = true;
        clearTimeout(timer);
        utterance.onstart = utterance.onend = utterance.onerror = null;
        active = null;
        error ? reject(error) : resolve(completed);
      };
      const timeout = () => {
        finish(new Error('질문 음성이 응답하지 않습니다. 화면을 켜고 PLAY를 다시 눌러주세요.'));
        synth.cancel();
      };
      active = {utterance, finish}; // Retain the utterance until playback completes.
      timer = setTimeout(timeout, 10000);
      utterance.onstart = () => {
        if (started) return;
        started = true;
        clearTimeout(timer);
        timer = setTimeout(timeout, 120000);
        onStart();
      };
      utterance.onend = () => finish();
      utterance.onerror = event => finish(new Error('질문 음성을 재생하지 못했습니다. 다시 눌러주세요. (' + event.error + ')'));
      try { synth.speak(utterance); } catch (error) { finish(error); }
    });
  }

  return {supported, populate, speak, cancel};
})();
