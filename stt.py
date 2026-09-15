"""Local CUDA transcription. Run with .venv/Scripts/python.exe."""
import argparse
import json
import os
from pathlib import Path
import sys
import time

_DLL_HANDLES = []


def configure_cuda():
    """Reuse installed CUDA DLLs without importing or modifying global torch."""
    if sys.platform != 'win32':
        return []
    candidates = []
    override = os.environ.get('OPIC_CUDA_DLL_DIR')
    if override:
        candidates.append(Path(override))
    candidates.extend([
        Path(sys.prefix) / 'Lib/site-packages/torch/lib',
        Path(sys.base_prefix) / 'Lib/site-packages/torch/lib',
    ])
    selected = []
    for directory in candidates:
        if directory.is_dir() and directory not in selected:
            _DLL_HANDLES.append(os.add_dll_directory(str(directory)))
            selected.append(directory)
    if selected:
        os.environ['PATH'] = os.pathsep.join(map(str, selected)) + os.pathsep + os.environ.get('PATH', '')
    return [str(p) for p in selected]


def load_model(model_name='large-v3'):
    configure_cuda()
    from faster_whisper import WhisperModel
    return WhisperModel(model_name, device='cuda', compute_type='float16', local_files_only=True)


def transcribe(model, audio):
    start = time.perf_counter()
    segments, info = model.transcribe(
        str(audio), language='en', task='transcribe', beam_size=5,
        condition_on_previous_text=False, vad_filter=True, word_timestamps=True,
    )
    result = []
    for segment in segments:
        result.append({
            'start': segment.start, 'end': segment.end, 'text': segment.text,
            'words': [{'start': w.start, 'end': w.end, 'word': w.word, 'probability': w.probability}
                      for w in (segment.words or [])],
        })
    return {
        'audio_path': str(Path(audio).resolve()),
        'device': 'cuda', 'compute_type': 'float16', 'language': info.language,
        'duration_seconds': info.duration,
        'transcription_seconds': round(time.perf_counter() - start, 3),
        'text': ''.join(s['text'] for s in result).strip(), 'segments': result,
        'status': 'completed' if result else 'no_speech',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('audio', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--model', default='large-v3')
    args = parser.parse_args()
    if not args.audio.is_file():
        parser.error(f'Audio file does not exist: {args.audio}')
    start = time.perf_counter()
    model = load_model(args.model)
    load_seconds = time.perf_counter() - start
    result = transcribe(model, args.audio)
    result.update(model=args.model, model_load_seconds=round(load_seconds, 3))
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + '\n', encoding='utf-8')
    print(payload)


if __name__ == '__main__':
    main()
