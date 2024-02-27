from textoutput import obsclient
from speechtotext import speech_recognizer
import threading

if __name__ == "__main__":
    print("Hello, World!!!!")
    # obs = obsclient.ObsClient()
    recognizer = speech_recognizer.SpeechRecognizer()
    # listen_thread = recognizer.make_listen_thread()
    # listen_thread.start()
    threading.Thread(target=recognizer.listen).start()
    while True:
        audio = recognizer.pop_front_audio()
        if audio is not None:
            print(audio)
        # obs.send_message("Hello World!")
