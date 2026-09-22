// State-machine tests with a fake recognition service, not a live STT accuracy test.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const speechSource=fs.readFileSync('static/browser-speech.js','utf8');
const source=fs.readFileSync('portable/app.js','utf8');
const template=fs.readFileSync('portable/index.html','utf8');
const ids=[...template.matchAll(/id="([^"]+)"/g)].map(m=>m[1]);
function harness(supported=true,storage=new Map(),ttsMode="normal",secure=true,platform="desktop"){
 const elements=new Map(ids.map(id=>[id,{id,hidden:false,disabled:false,textContent:'',innerHTML:'',value:id==='voices'?'':'1',options:[],replaceChildren(...options){this.options=options;},add(option){this.options.push(option);},classList:{toggle(){}},click(){this.onclick?.();}}]));
 const sets=Array.from({length:10},()=>Array.from({length:15},(_,i)=>({prompt:'Question '+(i+1),type:'Test'})));
 elements.get('practice-data').textContent=JSON.stringify({profile:'SH',version:'test-v1',sets});
 let lastRecognition,exported;
 const navigator={userAgent:platform==='android'?'Mozilla/5.0 (Linux; Android 15) Chrome/140.0 Mobile Safari/537.36':'Desktop',userAgentData:{platform:platform==='android'?'Android':'Windows'}};
 class Recognition{
  constructor(){lastRecognition=this;this.providerResults=[];}
  start(){this.onstart?.();}
  stop(){queueMicrotask(()=>this.onend?.());}
  abort(){queueMicrotask(()=>this.onend?.());}
  nativeResult(text,provisional){if(this.providerResults.at(-1)?.[1]===false)this.providerResults.pop();this.providerResults.push([text,!provisional||this.continuous]);this.result(...this.providerResults);}
  result(...parts){this.onresult({results:parts.map(([text,final])=>Object.assign([{transcript:text}],{isFinal:final}))});}
 }
 let lastSpeech,starts=0;
 class Utterance{constructor(text){this.text=text;}}
 const synth={getVoices:()=>[{lang:'en-US',voiceURI:'english',name:'English'}],addEventListener(){},cancel(){},speak(u){lastSpeech=u;starts++;if(ttsMode==='fail'){queueMicrotask(()=>u.onerror?.({error:'not-allowed'}));return;}u.onstart?.();if(ttsMode!=='hold')queueMicrotask(()=>u.onend?.());}};
 const document={getElementById:id=>elements.get(id),querySelectorAll:()=>[],createElement:()=>({click(){}})};
 const sandbox={document,navigator,window:{isSecureContext:secure,speechSynthesis:ttsMode==='unsupported'?undefined:synth,SpeechSynthesisUtterance:Utterance,SpeechRecognition:supported?Recognition:undefined,scrollTo(){},addEventListener(){}},localStorage:{setItem:(k,v)=>storage.set(k,v),getItem:k=>storage.get(k)},Option:function(text,value){this.text=text;this.value=value;},Blob,URL:{createObjectURL:b=>{exported=b;return'blob:test';},revokeObjectURL(){}},Date,console,confirm:()=>true,setTimeout,clearTimeout,setInterval:()=>1,clearInterval(){}};
 const ctx=vm.createContext(sandbox);vm.runInContext(speechSource,ctx);sandbox.BrowserSpeech=sandbox.window.BrowserSpeech;vm.runInContext(source,ctx);
 return {elements,storage,click:async id=>elements.get(id).onclick(),read:code=>vm.runInContext(code,ctx),r:()=>lastRecognition,blob:()=>exported,speech:()=>lastSpeech,starts:()=>starts};
}
(async()=>{
 const h=harness();await h.click('start');assert.equal(h.read('state.answers.length'),15);
 await h.click('play');h.r().result(['Hello',false]);h.r().result(['Hello world.',true]);
 await h.click('next');assert.equal(h.read('state.answers[0].raw'),'Hello world.');assert.equal(h.read('state.cursor'),1);
 // Final recognition event emitted during stop must remain with the old question.
 await h.click('play');const r=h.r();r.stop=function(){this.result(['Late final sentence.',true]);queueMicrotask(()=>this.onend());};
 await h.click('next');assert.equal(h.read('state.answers[1].raw'),'Late final sentence.');assert.equal(h.read('state.answers[2].raw'),'');
 // Permission errors stay explicitly distinguishable from an empty spoken answer.
 await h.click('play');h.r().onerror({error:'not-allowed'});h.r().onend();await h.click('next');assert.equal(h.read('state.answers[2].status'),'stt_error');
 while(h.read('state.cursor')<7)await h.click('skip');assert.equal(h.elements.get('middle').hidden,false);await h.click('continue');
 while(h.read('state.status')==='active')await h.click('skip');assert.equal(h.elements.get('review').hidden,false);
 assert.equal(h.read('state.answers[14].status'),'skipped');assert.match(h.read('exportText()'),/Hello world\./);assert.match(h.read('exportText()'),/STT 오류: not-allowed/);
 await h.click('download-md');assert.match(await h.blob().text(),/원본 STT/);
 const restored=harness(true,h.storage);assert.equal(restored.elements.get('previous').hidden,false);assert.equal(restored.read('state.answers[0].raw'),'Hello world.');
 // Playback is requested synchronously in the click handler (mobile activation).
 const mobile=harness();await mobile.click('start');const playing=mobile.click('play');assert.equal(mobile.starts(),1);await playing;
 assert.equal(mobile.speech().lang,'en-US');assert.equal(mobile.speech().voice.voiceURI,'english');
 assert.equal(mobile.read('current().plays'),1);await mobile.click('play');assert.equal(mobile.read('current().plays'),2);assert.equal(mobile.elements.get('play').disabled,true);
 await mobile.click('play');assert.equal(mobile.starts(),2);
 const failed=harness(true,new Map(),'fail');await failed.click('start');await failed.click('play');assert.equal(failed.read('current().plays'),0);assert.equal(failed.r(),undefined);assert.equal(failed.elements.get('play').disabled,false);
 const held=harness(true,new Map(),'hold');await held.click('start');const pending=held.click('play');assert.equal(held.r(),undefined);held.read('state.deadline=0;tick()');await pending;held.read('tick()');await new Promise(r=>setTimeout(r,10));assert.equal(held.read('state.status'),'completed');assert.equal(held.read('busy'),false);
 const noTts=harness(true,new Map(),'unsupported');assert.equal(noTts.elements.get('start').disabled,false);await noTts.click('start');assert.equal(noTts.read('state'),null);assert.match(noTts.elements.get('start-status').textContent,/질문 음성/);assert.equal(noTts.elements.get('check-audio').disabled,true);
 const insecure=harness(true,new Map(),'normal',false);assert.equal(insecure.elements.get('start').disabled,false);await insecure.click('start');assert.match(insecure.elements.get('start-status').textContent,/HTTPS/);assert.equal(insecure.read('state'),null);
 const unsupported=harness(false);assert.equal(unsupported.elements.get('start').disabled,false);await unsupported.click('start');assert.match(unsupported.elements.get('start-status').textContent,/외부 브라우저/);assert.equal(unsupported.read('state'),null);
 const timeout=harness();await timeout.click('start');timeout.read('state.deadline=0;tick()');await new Promise(r=>setTimeout(r,10));assert.equal(timeout.read('state.reason'),'제한시간 종료');
 // Regression: the Android continuous-mode bridge promotes cumulative partials to finals.
 const android=harness(true,new Map(),'normal',true,'android');await android.click('start');await android.click('play');
 const firstRun=android.r();assert.equal(firstRun.continuous,false);assert.equal(firstRun.interimResults,true);
 for(const text of ['my','my name','my name is','my name is','my name is Countess'])firstRun.nativeResult(text,true);
 assert.equal(android.read('current().raw'),'my name is Countess');
 firstRun.nativeResult('My name is Kyoungtae Ji, hello.',false);firstRun.result(...firstRun.providerResults);
 assert.equal(android.read('current().raw'),'My name is Kyoungtae Ji, hello.');
 firstRun.onend();await new Promise(r=>setTimeout(r,350));assert.notEqual(android.r(),firstRun);
 android.r().nativeResult('I really really like music.',true);android.r().nativeResult('I really really like music.',false);
 assert.equal(android.read('current().raw'),'My name is Kyoungtae Ji, hello. I really really like music.');
 // A late event from an ended run must not append to the new run.
 firstRun.result(['old stale text',true]);
 await android.click('next');assert.equal(android.read('state.answers[0].raw'),'My name is Kyoungtae Ji, hello. I really really like music.');
 assert.equal(android.read('state.answers[1].raw'),'');
 const desktop=harness();await desktop.click('start');await desktop.click('play');assert.equal(desktop.r().continuous,true);
 desktop.r().result(['I agree.',true],['I agree.',true],['very very good',false]);assert.equal(desktop.read('current().raw'),'I agree. I agree. very very good');await desktop.click('next');
 // The optional microphone check is remembered, but never gates starting an exam.
 const checked=harness();await checked.click('check-stt');checked.r().result(['Sample only.',true]);await checked.click('start');assert.equal(checked.read('state.answers[0].raw'),'');assert.equal(checked.read('testing'),false);
 const known=harness(true,checked.storage);assert.match(known.elements.get('check-result').textContent,/이전에/);await known.click('resume');assert.equal(known.read('state.startedAt'),checked.read('state.startedAt'));
 assert(!source.includes('MediaRecorder'));assert(!source.includes('getUserMedia'));assert(!source.includes('fetch('));
 console.log('PASS: 15-question flow, STT final/interim handling, final flush, permission failure, 5-5 midpoint, export, reload recovery, actionable unsupported browser, Android cumulative partials, sentence restart, repeated words preserved, remembered optional check, resume, timeout, no audio recording/upload code');
})().catch(e=>{console.error(e);process.exitCode=1;});
