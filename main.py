from textoutput import obsclient
from speechtotext import listener, recognizer
import threading

if __name__ == "__main__":
    print("Hello, World!!!!")
    # obs = obsclient.ObsClient()
    listen = listener.Listener()
    listen.make_listen_thread()

    recognizer = recognizer.Recognizer()
    # recognizer = speech_recognizer.SpeechRecognizer()
    # listen_thread = recognizer.make_listen_thread()
    # listen_thread.start()
    # threading.Thread(target=recognizer.listen).start()
    # while True:
        # audio = recognizer.pop_front_audio()
        # if audio is not None:
        #     print(audio)
        # obs.send_message("Hello World!")
    while True:
        audio = listen.pop_front_audio_wav()
        if audio is None:
            continue

        print('start recognition')
        out_text = recognizer.get_text_from_wav(audio)
        print(out_text)
        # obs.send_message("Hello World!")
    