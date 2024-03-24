'''
https://zenn.dev/tsuzukia/articles/1381e6c9a88577
pip install faster_whisper
'''

from datasets import Audio
from faster_whisper import WhisperModel
import io


class Recognizer:
    def __init__(self, language="Japanese", task="transcribe") -> None:
        self.model = WhisperModel("large-v3", device="cpu", compute_type="float32")

    def get_text_from_wav(self, audio: Audio) -> str:
        if audio is None:
            return None
        
        audio_stream = io.BytesIO(audio)
        print("===audio stream===")
        print(audio_stream)
        print("===audio stream===")
        segments, info = self.model.transcribe(audio_stream, beam_size=5, vad_filter=True, without_timestamps=True, initial_prompt="XXXXX", language='ja')
        results = list(segments)
        return ' '.join([result.text for result in results])
