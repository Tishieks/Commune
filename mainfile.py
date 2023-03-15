import os
import speech_recognition as sr
from google_trans_new import google_translator
from gtts import gTTS
from playsound import playsound
from PyQt6 import QtWidgets, QtCore, QtGui

# Initialize recognizer and translator instances
r = sr.Recognizer()
communulator = google_translator()

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle("Commune Prototype 0.01")
        self.resize(300, 200)

        # Set the window flags to remove the default window frame and enable transparency
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        # Create a layout to organize the widgets
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Create a label to display messages to the user
        self.label = QtWidgets.QLabel("          COMMUNE: created by Team MADLABS")
        self.label.setStyleSheet("color: white;")
        layout.addWidget(self.label)

        # Create a button that calls the on_button_click method when clicked
        button = QtWidgets.QPushButton("Click to commune")
        button.clicked.connect(self.on_button_click)
        button.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: white;
                border-radius: 15px;
                padding: 5px 20px;
            }
            QPushButton:hover {
                background-color: #444;
            }
            QPushButton:pressed {
                background-color: #555;
            }
        """)
        layout.addWidget(button)

    def on_button_click(self):
        # Listen for audio from the microphone
        with sr.Microphone() as source:
            self.label.setText("speak now!")
            audio = r.listen(source)
            try:
                # Recognize speech using Google's speech recognition service
                speech_text = r.recognize_google(audio)
                
                if speech_text.lower() == "exit":
                    QtWidgets.QApplication.quit()
                    return
                
                self.label.setText(speech_text)
            except sr.UnknownValueError:
                self.label.setText("could not understand")
            except sr.RequestError:
                self.label.setText("Could not request result from google")

        # Translate the recognized text to French using Google Translate
        translated_text = communulator.translate(speech_text, lang_tgt='fr')
        self.label.setText(translated_text)

        # Convert the translated text to speech using the Google Text-to-Speech service
        voice = gTTS(translated_text, lang='fr')
        voice.save("Voice.mp3")
        
        # Play the resulting audio
        playsound("Voice.mp3")
        
        # Remove the temporary audio file
        os.remove("voice.mp3")

    def paintEvent(self, event):
         # Override the paintEvent method to draw a custom window frame with rounded corners

         # Create a QPainter instance and set its pen and brush
         painter = QtGui.QPainter(self)
         painter.setPen(QtCore.Qt.PenStyle.NoPen)
         painter.setBrush(QtGui.QColor(80, 80, 80))

         # Draw a rounded rectangle that fills the entire widget area
         painter.drawRoundedRect(self.rect(), 20, 20)

# Create a QApplication instance (required by PyQt6)
app = QtWidgets.QApplication([])

# Create and show the main window
window = MainWindow()
window.show()

# Start the main loop of the application
app.exec()
