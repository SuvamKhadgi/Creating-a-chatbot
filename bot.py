import tkinter as tk
from tkinter import filedialog, messagebox
import speech_recognition as sr
import pyttsx3
import subprocess
import time
import requests
import threading
import winsound
from PyPDF2 import PdfReader
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Initialize global variables
pdf_text = ""  # Initialize pdf_text as an empty string

# Set speech rate
def set_speech_rate(rate):
    engine.setProperty('rate', rate)

# Set speech rate to a slower speed (e.g., 150 words per minute)
set_speech_rate(150)

# Function to make the bot speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to play a sound indicating that the program is listening
def play_listening_sound():
    winsound.PlaySound(r"C:\Users\rujan\Downloads\voice-assistant-sound-name-unknown.wav", winsound.SND_FILENAME)

# Function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening for your question...")
        play_listening_sound()
        audio_data = recognizer.listen(source, timeout=300)
        try:
            question = recognizer.recognize_google(audio_data)
            print(f"You said: {question}")
            return question
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            speak("There was an error with the speech recognition service.")
            return None

# Function to communicate with the Rasa server
def communicate_with_rasa(question):
    url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {
        "sender": "user",
        "message": question
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        bot_responses = response.json()
        if bot_responses:
            return bot_responses[0]['text']
    return "Sorry, I couldn't get a response from the server."

# Function to run the Rasa shell
def run_rasa_shell():
    speak("Starting Rasa shell.")
    process = subprocess.Popen(["rasa", "run"], shell=True)
    time.sleep(5)
    speak("Rasa server is up and running.")
    return process

# Function to recognize speech and respond
def recognize_and_respond():
    while True:
        question = recognize_speech()
        if question:
            if "stop" in question.lower():
                speak("Stopping the program.")
                rasa_process.terminate()
                break
            else:
                pdf_response = answer_from_pdf(question)
                if pdf_response:
                    response = pdf_response
                else:
                    response = communicate_with_rasa(question)
                print(f"Bot: {response}")
                speak(response)

# Function to upload and read PDF
def upload_pdf():
    global pdf_text
    pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if pdf_file_path:
        pdf_text = read_pdf(pdf_file_path)
        messagebox.showinfo("PDF Upload", "PDF uploaded successfully!")

# Function to read PDF content
def read_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

# Function to answer questions based on PDF content
def answer_from_pdf(question):
    if not pdf_text:  # Check if pdf_text is empty
        return None
    sentences = sent_tokenize(pdf_text)
    for sentence in sentences:
        if question.lower() in sentence.lower():
            return sentence
    return None

# Initialize Tkinter window
root = tk.Tk()
root.title("Tkinter PDF Reader")
root.geometry("400x300")

# Create a button to upload PDF
upload_button = tk.Button(root, text="Upload PDF", command=upload_pdf)
upload_button.pack(pady=20)

# Start the Rasa server
rasa_process = run_rasa_shell()

# Start the recognition and response loop in a separate thread
recognize_thread = threading.Thread(target=recognize_and_respond)
recognize_thread.start()

# Start the Tkinter main loop
root.mainloop()

print("Program ended.")
