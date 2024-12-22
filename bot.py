import tkinter as tk
from tkinter import filedialog, messagebox
import speech_recognition as sr
import pyttsx3
import subprocess
import time
import requests
import threading
import winsound
from PIL import Image, ImageTk
import cv2

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Initialize global variables
pdf_text = ""  # Initialize pdf_text as an empty string
video_playing = True  # Start with video playing
bot_active = False  # Flag to track if the bot is active
current_video = None  # Variable to store the current video path

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
    winsound.PlaySound(r"C:\Users\LEGION\Downloads\voice-assistant-sound-name-unknown.wav", winsound.SND_FILENAME)

# Function to recognize speech
def recognize_speech():
    global bot_active
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening for your question...")
        play_listening_sound()
        audio_data = recognizer.listen(source, timeout=3000)
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
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        if response.status_code == 200:
            bot_responses = response.json()
            if bot_responses:
                return bot_responses[0]['text']
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Rasa: {e}")
        # speak("There was an error communicating with the server.")
    return "Please Wait."

# Function to run the Rasa shell
def run_rasa_shell():
    speak("Starting Rasa shell.")
    process = subprocess.Popen(["rasa", "run"], shell=True)
    time.sleep(5)
    speak("Rasa server is  running.")
    return process

# Function to recognize speech and respond
def recognize_and_respond():
    global bot_active
    while True:
        question = recognize_speech()
        if question:
            if "stop" in question.lower():
                speak("Stopping the program.")
                rasa_process.terminate()
                break
            else:
                bot_active = True
                update_video(r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\Chat Bot Show Loading Data.webm")
                response = communicate_with_rasa(question)
                update_video(r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\Chat Bot Show Process.webm")
                print(f"Bot: {response}")
                update_response_ui(response)
                speak(response)

                bot_active = False
                update_video(r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\merobot.mp4")

# Function to update video based on current state
def update_video(video_file_path):
    global current_video
    current_video = video_file_path
    play_video(video_file_path)

# Function to play video
def play_video(video_file_path):
    cap = cv2.VideoCapture(video_file_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    def update_frame():
        if current_video == video_file_path:
            ret, frame = cap.read()
            if not ret:  # If the video has ended, restart it
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
                # frame = cv2.resize(frame, (700, 500))  # Resize frame to fit in label
                frame = cv2.resize(frame, (1000, 650))  # Resize frame to fit in label

                frame_image = Image.fromarray(frame)
                frame_photo = ImageTk.PhotoImage(frame_image)
                video_label.config(image=frame_photo)
                video_label.image = frame_photo
            root.after(int(100 / fps), update_frame)

        
    update_frame()

def update_response_ui(response):
    response_label.config(text=response)


def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", True)
    return "break"

def end_fullscreen(event=None):
    root.attributes("-fullscreen", False)
    return "break"



# Initialize Tkinter window
root = tk.Tk()
root.title("Tkinter PDF Reader and Video Player")
# root.geometry("700x600")  # Adjusted window size
root.attributes("-fullscreen", True)
root.bind("<Escape>", end_fullscreen)


# Configure grid layout
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)

title_label = tk.Label(root, text="Interactive AI counsellor for Softwarica", font=("Helvetica", 24), bg="white")
title_label.grid(row=0, column=0, columnspan=3, pady=10)

# Create a frame for the video player
video_frame = tk.Frame(root, width=1450, height=1400)
video_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
video_label = tk.Label(video_frame)
video_label.pack()

# Automatically play the initial video
initial_video_path = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\merobot.mp4"
update_video(initial_video_path)

# Create a label to display the bot's response
response_label = tk.Label(root, text="", wraplength=1250,  font=("Helvetica", 20), bg="white")
# response_label.grid(row=2, column=0, padx=10, pady=10, columnspan=1)
response_label.grid(row=2, column=0, padx=20, pady=10)

# Start the Rasa server
rasa_process = run_rasa_shell()

# Start the recognition and response loop in a separate thread
recognize_thread = threading.Thread(target=recognize_and_respond)
recognize_thread.start()
root.configure(bg='white')

# Start the Tkinter main loop
root.mainloop()

print("Program ended.")
