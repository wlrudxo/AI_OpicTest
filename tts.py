"""Cached local English question speech on CPU; GPU stays available for Whisper."""
from hashlib import sha256
from pathlib import Path
from threading import Lock
import asyncio
import logging
import soundfile as sf

ROOT = Path(__file__).resolve().parent / 'data'
lock = Lock()
voice = None
preparation = None
preparation_texts = None


def prepare(texts):
    """Only the latest question set is warmed, in question order."""
    global preparation, preparation_texts
    texts = tuple(texts)
    if texts == preparation_texts and preparation and not preparation.cancelled():
        return
    if preparation:
        preparation.cancel()
    preparation_texts = texts
    preparation = asyncio.create_task(_prepare(texts))


async def _prepare(texts):
    for text in texts:
        try:
            await asyncio.to_thread(synthesize, text)
        except asyncio.CancelledError:
            raise
        except Exception:
            # A failed warm-up must not stop the exam; PLAY retries normally.
            logging.getLogger(__name__).exception('Question audio preparation failed')
        await asyncio.sleep(0)


async def shutdown():
    if preparation:
        preparation.cancel()
        await asyncio.gather(preparation, return_exceptions=True)


def synthesize(text):
    global voice
    # Include model and voice so previous Piper audio is never reused.
    key = 'kokoro-v1.0:af_heart:en-us:1.0:' + text
    output = ROOT / 'question-audio' / (sha256(key.encode('utf-8')).hexdigest()+'.wav')
    # Atomic writes make this safe; ready audio never waits behind synthesis.
    if output.exists():
        return output
    with lock:
        if output.exists():
            return output
        from kokoro_onnx import Kokoro
        if voice is None:
            model_dir = ROOT / 'tts-model/kokoro'
            voice = Kokoro(str(model_dir / 'kokoro-v1.0.onnx'), str(model_dir / 'voices-v1.0.bin'))
        output.parent.mkdir(exist_ok=True)
        temp = output.with_suffix('.tmp')
        samples, rate = voice.create(text, voice='af_heart', speed=1.0, lang='en-us')
        sf.write(str(temp), samples, rate, format='WAV', subtype='PCM_16')
        temp.replace(output)
    return output
