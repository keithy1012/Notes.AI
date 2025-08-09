import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say Retrieve or Generate")
    # Adjust for ambient noise to improve recognition accuracy
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
    try:
        action = r.recognize_google(audio)
        print(f"You said: {action}")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
