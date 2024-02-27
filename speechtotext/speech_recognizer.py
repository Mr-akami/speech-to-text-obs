'''
change mic priority
ref: https://qiita.com/chiapis2/items/347a9b422706c2d8ebe2
'''
import speech_recognition
import threading
import queue
# import sounddevice


class SpeechRecognizer:

    def __init__(self, energy_threshold=4000, pause_threshold=0.5, dynamic_energy_threshold=False):
        self.recognizer = speech_recognition.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.pause_threshold = pause_threshold
        self.recognizer.dynamic_energy_threshold = dynamic_energy_threshold
        self.mic = speech_recognition.Microphone(sample_rate=16000)
        # self.listen_pool = threading.Thread(target=self.listen)
        self.record_audio_queue = queue.Queue()

    def listen(self):
        print("Listening...")
        print(self.mic)
        with self.mic as source:
            print(source)
            while True:
                audio = self.recognizer.listen(source)
                print(audio)
                self.record_audio_queue.put_nowait(audio)
                
    def make_listen_thread(self):
        return threading.Thread(target=self.listen).start()

    def pop_front_audio(self):
        if self.record_audio_queue.qsize() != 0:
            print("pop_front_audio")
            try:
                a = self.recognizer.recognize_google(self.record_audio_queue.get_nowait(), language='ja-JP')
                print(a)
            except speech_recognition.UnknownValueError:
                print("Could not understand audio")
            # return self.record_audio_queue.get_nowait()
            
    