from NotesGenerator import Generator
from NotesRetriever import Retriever
import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say Retrieve or Generate")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
    try:
        action = r.recognize_google(audio)
        print(f"You said: {action}")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

retriever = Retriever()

if "GENERATE" in action.upper():
    file_path = input("Enter file path to notes")
    output_path = input("Enter output path")
    instructions = input("Enter instructions")
    generator = Generator(file_path, output_path, instructions)

if "RETRIEVE" in action.upper():
    retriever = Retriever()