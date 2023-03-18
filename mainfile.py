"""
speechRecognition and translation is done to convert spoken words into French text then into speech.
"""
import os
import tkinter as tk
from tkinter import ttk
import time
import speech_recognition as sr
from translate import Translator
from gtts import gTTS
import pygame


# Initialize recognizer and translator instances
r = sr.Recognizer()

# Initialize Pygame mixer
pygame.mixer.init()

def on_button_click():
    """
    This function is called when the user clicks the 'Commune' button.
    It listens for audio through microphone and translates it into the selected langText and speech.
    """
    # Get the selected language from the dropdown menu
    selected_language = language_selector.get()

    # Set the appropriate language code for Translate and GTTS
    if selected_language == "French":
        to_lang = "fr"
        lang_code = "fr-FR"
    elif selected_language == "Spanish":
        to_lang = "es"
        lang_code = "es-ES"
    elif selected_language == "Arabic":
        to_lang = "ar"
        lang_code = "ar-SA"
    elif selected_language == "English":
        to_lang = "en"
        lang_code = "en-US"
    elif selected_language == "Chinese":
        to_lang = "zh"
        lang_code = "zh-CN"
    elif selected_language == "Hindi":
        to_lang = "hi"
        lang_code = "hi-IN"
    elif selected_language == "Bengali":
        to_lang = "bn"
        lang_code = "bn-BD"
    elif selected_language == "Russian":
        to_lang = "ru"
        lang_code = "ru-RU"
    elif selected_language == "Portuguese":
        to_lang = "pt"
        lang_code = "pt- PT"
    elif selected_language == "Japanese":
        to_lang = "ja"
        lang_code = "ja-JP"
    else:
        # Default to French if no language is selected
        to_lang = "en"
        lang_code = "en-US"

    communulator = Translator(to_lang=to_lang)

    # Listen for audio from the microphone
    with sr.Microphone() as source:
        label.config(text="Speak now!")
        audio = r.listen(source)
        try:
            # Recognize speech using Google's speech recognition service
            speech_text = r.recognize_google(audio, language=lang_code)
            label.config(text=speech_text)

            # Translate the recognized text to the selected language using Translate
            translated_text = communulator.translate(speech_text)
            label.config(text=translated_text)

            # Convert the translated text to speech using the Google Text-to-Speech service
            voice = gTTS(translated_text, lang=to_lang)
            # Generate a unique filename for this audio file
            filename = f"Voice-{int(time.time())}.mp3"
            # Save voice data in memory
            voice.save(filename)

            # Load resulting audio into Pygame mixer
            pygame.mixer.music.load(filename)

            # Play resulting audio directly from memory
            pygame.mixer.music.play()

        except sr.UnknownValueError:
            label.config(text="Commune could not understand")
        except sr.RequestError:
            label.config(text="Commune could not request result from Google")

    # Wait until the audio finishes playing
    while pygame.mixer.music.get_busy():
        pass

    # Remove temporary audio file
    os.remove(filename)


# Create a tkinter window and set its title and size
window = tk.Tk()
window.title("Commune Prototype 0.02")
window.geometry("300x250")
window.configure(background="#333333")

style = ttk.Style()
style.theme_use("clam")

style.configure("TButton", font=("Helvetica", 16), padding=10)
style.configure("TLabel", font=("Helvetica", 16), padding=10)
style.configure(".", background="#333333", foreground="#ffffff")

# Create a label to display messages to the user
label = ttk.Label(window, text="Press the button to speak")
label.pack(fill="x", padx=10, pady=10)

# Create a dropdown menu for selecting the language
language_selector = ttk.Combobox(window, values=["English", "French", "Spanish", "Arabic", "Chinese", "Hindi", "Bengali", "Russian", "Portuguese", "Japanese"])
language_selector.current(0)  # Set the default value to French
language_selector.pack(fill="x", padx=10, pady=5)

# Create a button that calls the on_button_click function when clicked
button = ttk.Button(window, text="Commune", command=on_button_click)
button.pack(fill="x", padx=10, pady=10)

# Start the main loop of the window
window.mainloop()
