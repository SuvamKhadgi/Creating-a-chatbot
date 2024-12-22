import cv2
import face_recognition
import os
import sqlite3
import time
import threading
import pyttsx3
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from ultralytics import YOLO
from cvzone.HandTrackingModule import HandDetector
from read import label_faces  # Import the labeling function

# Initialize the YOLO model
model = YOLO("yolov8n.pt")

# Function to load labeled faces
def load_labeled_faces(labeled_faces_dir):
    labeled_faces = {}
    for filename in os.listdir(labeled_faces_dir):
        if filename.endswith(".txt"):
            name = filename.split(".")[0]
            encoding = []
            with open(os.path.join(labeled_faces_dir, filename), 'r') as f:
                for line in f:
                    encoding.append(float(line.strip()))
            labeled_faces[name] = encoding
    return labeled_faces

# Function to recognize faces
def recognize_face(image_path, labeled_faces_dir):
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)
    labeled_faces = load_labeled_faces(labeled_faces_dir)

    if not face_encodings:
        print("No faces found in the image.")
        return None

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(list(labeled_faces.values()), face_encoding)
        if True in matches:
            matched_idx = matches.index(True)
            name = list(labeled_faces.keys())[matched_idx]
            print(f"Match found: {name}")
            return name
        else:
            print("No match found.")
            return None

# Function to capture and recognize face
def capture_and_recognize_face(labeled_faces_dir):
    cap = cv2.VideoCapture(0)
    countdown_duration = 10
    countdown_start = time.time()
    captured_frame = None

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            print("Error: Could not read frame.")
            break

        elapsed_time = int(time.time() - countdown_start)
        remaining_time = countdown_duration - elapsed_time

        if remaining_time > 0:
            cv2.putText(frame, str(remaining_time), (250, 250), cv2.FONT_HERSHEY_SIMPLEX, 7, (0, 255, 0), 10, cv2.LINE_AA)
        else:
            captured_frame = frame.copy()
            break

        cv2.imshow("Webcam Person Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if captured_frame is not None:
        image_path = "captured_image.jpg"
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"Deleted existing image: '{image_path}'")

        cv2.imwrite(image_path, captured_frame)
        print(f"Image captured and saved as '{image_path}'.")

        cap.release()
        cv2.destroyAllWindows()

        return recognize_face(image_path, labeled_faces_dir)
    else:
        cap.release()
        cv2.destroyAllWindows()
        return None

# Function to fetch data from the database
def fetch_data_from_db(txtfilename):
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student WHERE id=?", (txtfilename,))
    data = cursor.fetchone()
    conn.close()
    return data

# Function to update the Tkinter window with the fetched data
def update_window_with_data(entries, data):
    if data:
        entries["Citizenship Number"].delete(0, tk.END)
        entries["Citizenship Number"].insert(0, data[1])

        entries["Full Name"].delete(0, tk.END)
        entries["Full Name"].insert(0, data[2])

        entries["Sex"].delete(0, tk.END)
        entries["Sex"].insert(0, data[3])

        entries["Date of Birth"].delete(0, tk.END)
        entries["Date of Birth"].insert(0, data[4])

        entries["Birth Place"].delete(0, tk.END)
        entries["Birth Place"].insert(0, data[5])

        entries["Permanent Address"].delete(0, tk.END)
        entries["Permanent Address"].insert(0, data[6])

        entries["School"].delete(0, tk.END)
        entries["School"].insert(0, data[7])

        entries["Faculty"].delete(0, tk.END)
        entries["Faculty"].insert(0, data[8])

        entries["GPA"].delete(0, tk.END)
        entries["GPA"].insert(0, data[9])

        entries["Passout Year"].delete(0, tk.END)
        entries["Passout Year"].insert(0, data[10])

        entries["Enrollment Course"].delete(0, tk.END)
        entries["Enrollment Course"].insert(0, data[11])
    else:
        messagebox.showinfo("Result", "No data found for the given ID.")

def on_enter(event):
    event.widget['background'] = '#0f5c91'  # Hover color

def on_leave(event):
    event.widget['background'] = '#1283b9'  # Original color

def on_click(event):
    event.widget['background'] = '#0d4a73'  # Click color

def start_process():
    detected_person = capture_and_recognize_face('pic')
    if detected_person:
        print(f"Detected person: {detected_person}")
        data = fetch_data_from_db(detected_person)
        if data:
            print("Data fetched successfully.")
            launch_tkinter_window(data)
        else:
            print("No data found for the detected person.")
    else:
        print("No person recognized.")

def launch_tkinter_window(data):
    def speak(text):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'female' in voice.name.lower() or 'feminine' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.say(text)
        engine.runAndWait()

    def create_full_screen_window():
        global root
        global entries

        root = tk.Tk()
        root.title("Student Details")

        # Maximize the window
        root.state('zoomed')

        # Create the main frame with a blue background
        main_frame = tk.Frame(root, bg='#1283b9')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a frame inside the main frame with a white background
        inner_frame = tk.Frame(main_frame, bg='white', bd=2, relief=tk.RAISED)
        inner_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.95, relheight=0.9)

        # Add a heading label inside the white frame
        heading_label = tk.Label(inner_frame, text="Student Details", font=("Monotype Corsiva", 36, "bold"), bg='white', fg='#1283b9')
        heading_label.pack(pady=20)

        # Create left frame for personal information
        left_frame = tk.Frame(inner_frame, bg='white')
        left_frame.place(relx=0.02, rely=0.2, relwidth=0.45, relheight=0.7)

        # Create right frame for academic information
        right_frame = tk.Frame(inner_frame, bg='white')
        right_frame.place(relx=0.53, rely=0.2, relwidth=0.45, relheight=0.7)

        # Labels and entry boxes for left frame
        personal_info = [
            "Citizenship Number",
            "Full Name","Sex",
            "Date of Birth",
            "Birth Place",
            "Permanent Address"
        ]

        entries = {}
        for i, info in enumerate(personal_info):
            label = tk.Label(left_frame, text=info, font=("Times New Roman", 16), bg='white')
            label.pack(anchor='w', padx=10, pady=5)
            entry = tk.Entry(left_frame, font=("Times New Roman", 14))
            entry.pack(fill='x', padx=10, pady=5)
            entries[info] = entry

        # Labels and entry boxes for right frame
        academic_info = [
            "School",
            "Faculty",
            "GPA",
            "Passout Year",
            "Enrollment Course"
        ]

        for info in academic_info:
            label = tk.Label(right_frame, text=info, font=("Times New Roman", 16), bg='white')
            label.pack(anchor='w', padx=10, pady=5)
            entry = tk.Entry(right_frame, font=("Times New Roman", 14))
            entry.pack(fill='x', padx=10, pady=5)
            entries[info] = entry

        # Submit button at the bottom
        submit_button = tk.Button(inner_frame, text="Update", font=("Times New Roman", 16, "bold"), bg='#1283b9', fg='white', padx=40, pady=8)
        submit_button.pack(pady=40, padx=10, side='bottom')

        # Bind events for hover and click effects
        submit_button.bind("<Enter>", on_enter)
        submit_button.bind("<Leave>", on_leave)
        submit_button.bind("<ButtonPress-1>", on_click)
        submit_button.bind("<ButtonRelease-1>", on_enter)  # Change back to hover color on release

        update_window_with_data(entries, data)

        root.mainloop()

    create_full_screen_window()

def main():
    start_process()

if __name__ == "__main__":
    main()