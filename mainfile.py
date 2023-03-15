import os
import speech_recognition as sr
from google_trans_new import google_translator
from gtts import gTTS
from playsound import playsound

r = sr.Recognizer()
communulator = google_translator()

while True:
    with sr.Microphone() as source:
        print("speak now!")
        audio = r.listen(source)
        try:
            speech_text = r.recognize_google(audio)
            print(speech_text)
            if(speech_text == "exit"):
                break
        except sr.UnknownValueError:
            print("could not understand")
        except sr.RequestError:
            print("Could not request result from google")

    translated_text = communulator.translate(speech_text, lang_tgt= 'fr')
    print(translated_text)

    voice = gTTS(translated_text, lang='fr')
    voice.save("Voice.mp3")
    playsound("Voice.mp3")
    os.remove("voice.mp3")
