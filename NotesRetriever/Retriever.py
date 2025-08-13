from utils import match_directory
import speech_recognition as sr

r = sr.Recognizer()

class Retriever:
    def __init__(self):
        self.r = sr.Recognizer()

    def run(self):
        self.main()
        return

    def main(self):
        action = None
        with sr.Microphone() as source:
            print("What notes do you want?")
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)
            try:
                action = r.recognize_google(audio)
                print(f"You said: {action}")
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

        if action:
            path = match_directory(action)
            print(f"The most relevant subdirectory is: {path}")
