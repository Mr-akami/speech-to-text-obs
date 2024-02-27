import speech_recognition
import threading
# import sounddevice


class SpeechRecognizer:

    def __init__(self, energy_threshold=4000, pause_threshold=0.5, dynamic_energy_threshold=False):
        self.recognizer = speech_recognition.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.pause_threshold = pause_threshold
        self.recognizer.dynamic_energy_threshold = dynamic_energy_threshold
        self.mic = speech_recognition.Microphone(sample_rate=16000)
        # self.listen_pool = threading.Thread(target=self.listen)
        self.record_audio_queue = []

    def listen(self):
        with self.mic as source:
            while True:
                audio = self.recognizer.listen(source)
                # print(audio)
                self.record_audio_queue.put_nowait(audio)
                
    def make_listen_thread(self):
        return threading.Thread(target=self.listen)

    def pop_front_audio(self):
        return self.record_audio_queue.get_nowait()
    