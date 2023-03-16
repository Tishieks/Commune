"""
speechRecognition and translation is done to convert spoken words into French text then into speech.
"""
import os
import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
from google_trans_new import google_translator
from gtts import gTTS
from playsound import playsound

# Initialize recognizer and translator instances
r = sr.Recognizer()
communulator = google_translator()


def on_button_click():
    """
    This function is called when the user clicks the 'Commune' button.
    It listens for audio from the microphone and translates it into French text and speech.
    """
    # Listen for audio from the microphone
    with sr.Microphone() as source:
        label.config(text="speak now!")
        audio = r.listen(source)
        try:
            # Recognize speech using Google's speech recognition service
            speech_text = r.recognize_google(audio)
            label.config(text=speech_text)
        except sr.UnknownValueError:
            label.config(text="Commune could not understand")
        except sr.RequestError:
            label.config(text="Commune could not request result from google")

    # Translate the recognized text to French using Google Translate
    translated_text = communulator.translate(speech_text, lang_tgt='fr')
    label.config(text=translated_text)

    # Convert the translated text to speech using the Google Text-to-Speech service
    voice = gTTS(translated_text, lang='fr')
    voice.save("Voice.mp3")
    # Play the resulting audio
    playsound("Voice.mp3")
    # Remove the temporary audio file
    os.remove("Voice.mp3")


# Create a tkinter window and set its title and size
window = tk.Tk()
window.title("Commune Prototype 0.01")
window.geometry("300x200")
window.configure(background="#333333")

style = ttk.Style()
style.theme_use("clam")

style.configure("TButton", font=("Helvetica", 16), padding=10)
style.configure("TLabel", font=("Helvetica", 16), padding=10)
style.configure(".", background="#333333", foreground="#ffffff")

# Create a label to display messages to the user
label = ttk.Label(window, text="         Press the button")
label.pack(fill="x", padx=10, pady=10)

# Create a button that calls the on_button_click function when clicked
button = ttk.Button(window, text="Commune", command=on_button_click)
button.pack(fill="x", padx=10, pady=10)

# Start the main loop of the window
window.mainloop()
