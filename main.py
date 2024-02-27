from textoutput import obsclient
from speechtotext import speech_recognizer

if __name__ == "__main__":
    print("Hello, World!!!!")
    # obs = obsclient.ObsClient()
    recognizer = speech_recognizer.SpeechRecognizer()
    # listen_thread = recognizer.make_listen_thread()
    # listen_thread.start()
    # while True:
    #     audio = recognizer.pop_front_audio()
    #     print(audio)
    #     obs.send_message("Hello World!")
