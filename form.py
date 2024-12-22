# import tkinter as tk
# from tkinter import ttk
# from tkinter import messagebox
# from PIL import Image, ImageTk
# import json
# import backend

# def main(all_info):
#     new_id = [None]  # Mutable object to store the new ID

#     def get_from_json():
#         filepath = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\extracted_text.json"
#         with open(filepath, 'r', encoding='utf-8') as file:
#             all_info = json.load(file)
#             return all_info

#     def populate_entries():
#         # Get the data from the JSON
#         data = get_from_json().get("extracted_text", {})

#         # Map JSON keys to Entry widgets
#         entry_map = {
#             "citizenship_no": citizenship_no_entry,
#             "full_name": full_name_entry,
#             "sex": sex_label_entry,
#             "DoB": dob_year_entry,
#             "birth_place": birth_place_entry,
#             "address": permanent_address_entry,
#             "school": school_entry,
#             "gpa": gpa_entry,
#             "faculty": faculty_entry,
#             "passout_year": passout_year_entry,
#             "course": enrollment_course_entry
#         }

#         # Insert the data into the Entry widgets
#         for key, entry_widget in entry_map.items():
#             # Convert non-string data types to string
#             value = data.get(key, "")
#             if isinstance(value, (int, float)):
#                 value = str(value)
#             entry_widget.delete(0, tk.END)  # Clear the current content
#             entry_widget.insert(0, value)  # Insert the new content

#     def submit_data():
#         updated_info = {
#             "citizenship_no": citizenship_no_entry.get(),
#             "full_name": full_name_entry.get(),
#             "sex": sex_label_entry.get(),
#             "DoB": dob_year_entry.get(),
#             "birth_place": birth_place_entry.get(),
#             "address": permanent_address_entry.get(),
#             "school": school_entry.get(),
#             "faculty": faculty_entry.get(),
#             "gpa": gpa_entry.get(),
#             "passout_year": passout_year_entry.get(),
#             "course": enrollment_course_entry.get()
#         }

#         course = "computing"
#         front = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\citizenship_front.jpg"
#         back = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\citizenship_back.jpg"
#         mark = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\marksheet.jpg"
#         pic = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\student_image.jpg"
        
#         new_id[0] = backend.insert_student_data(
#             updated_info["citizenship_no"],
#             updated_info["full_name"],
#             updated_info["sex"],
#             updated_info["DoB"],
#             updated_info["birth_place"],
#             updated_info["address"],
#             updated_info["school"],
#             updated_info["faculty"],
#             updated_info["gpa"],
#             updated_info["passout_year"],
#             course,
#             front,
#             back,
#             mark
#         )

#         if new_id[0] is not None:
#             messagebox.showinfo("Success", f"Student data inserted successfully. New ID: {new_id[0]}")
#         else:
#             messagebox.showerror("Error", "Failed to insert student data.")

#         window.destroy()

#     # Initialize the main window
#     window = tk.Tk()

#     # Get the screen width and height
#     screen_width = window.winfo_screenwidth()
#     screen_height = window.winfo_screenheight()

#     # Calculate the position to center the window horizontally
#     window_width = 580
#     window_height = 800
#     x = (screen_width // 2) - (window_width // 2)
#     y = 0  # Set the y position to 0 for top of the screen

#     window.geometry(f'{window_width}x{window_height}+{x}+{y}')
#     window.title("Data Entry Form")
#     window.configure(background='white')

#     # Load the background image
#     background_image_path = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\logo.jpg"
#     background_image = Image.open(background_image_path)
#     background_image = background_image.resize((window_width, window_height))  # Resize to fit the window
#     background_photo = ImageTk.PhotoImage(background_image)

#     # Create a canvas and place it in the main window
#     canvas = tk.Canvas(window, width=window_width, height=window_height)
#     canvas.pack(fill="both", expand=True)

#     # Add the background image to the canvas
#     canvas.create_image(0, 0, image=background_photo, anchor="nw")

#     # Create a frame on top of the canvas for other widgets
#     frame = ttk.Frame(canvas, padding="10", style="TFrame")
#     frame.place(relwidth=1, relheight=1)

#     # Top Frame for Company Name and Logo
#     top_frame = ttk.Frame(frame, padding="10")
#     top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

#     # Company Logo
#     logo_image_path = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\logo.jpg"
#     logo_image = Image.open(logo_image_path)
#     resized_logo_image = logo_image.resize((500, 45))  # Example size (500x65)
#     logo_photo = ImageTk.PhotoImage(resized_logo_image)
#     logo_label = ttk.Label(top_frame, image=logo_photo, background='white')
#     logo_label.grid(row=0, column=0, padx=5, pady=0)

#     # Keep a reference to the image to prevent garbage collection
#     logo_label.image = logo_photo

#     # Styling
#     style = ttk.Style()
#     style.configure("TLabel", font=("Helvetica", 10), background='white')
#     style.configure("TEntry", font=("Helvetica", 12))  # Larger font
#     style.configure("TButton", font=("Helvetica", 12))
#     style.configure("TFrame", background='white')

#     # Create a style for the submit button with skyblue background
#     style.configure("TSubmit.TButton", background="skyblue")

#     # Main Frame Content
#     main_content_frame = ttk.Frame(frame)
#     main_content_frame.grid(row=1, column=0, padx=10, pady=0)

#     # User Info
#     user_info_frame = ttk.LabelFrame(main_content_frame, text="User Information", padding="10")
#     user_info_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

#     # Citizenship Certificate No
#     citizenship_no_label = ttk.Label(user_info_frame, text="Citizenship Certificate No")
#     citizenship_no_label.grid(row=0, column=0, sticky="w")
#     citizenship_no_entry = ttk.Entry(user_info_frame, width=50)  # Increased width
#     citizenship_no_entry.grid(row=1, column=0, columnspan=3, sticky="ew")

#     # Names
#     full_name_label = ttk.Label(user_info_frame, text="Full Name")
#     full_name_label.grid(row=2, column=0, sticky="w")
#     full_name_entry = ttk.Entry(user_info_frame, width=70)  # Increased width
#     full_name_entry.grid(row=3, column=0, sticky="ew")

#     # Sex
#     sex_label = ttk.Label(user_info_frame, text="Sex")
#     sex_label.grid(row=4, column=0, sticky="w")
#     sex_label_entry = ttk.Entry(user_info_frame, width=70)  # Increased width
#     sex_label_entry.grid(row=5, column=0, sticky="ew")

#     # Date of Birth
#     dob_label = ttk.Label(user_info_frame, text="Date of Birth (AD)")
#     dob_label.grid(row=6, column=0, sticky="w")
#     dob_year_entry = ttk.Entry(user_info_frame,  width=68)  # Increased width
#     dob_year_entry.grid(row=7, column=0, sticky="ew")

#     # Birth Place
#     birth_place_label = ttk.Label(user_info_frame, text="Birth Place - District")
#     birth_place_label.grid(row=8, column=0, sticky="w")
#     birth_place_entry = ttk.Entry(user_info_frame, width=70)  # Increased width
#     birth_place_entry.grid(row=9, column=0, sticky="ew")

#     # Permanent Address
#     permanent_address_label = ttk.Label(user_info_frame, text="Permanent Address - District")
#     permanent_address_label.grid(row=10, column=0, sticky="w")
#     permanent_address_entry = ttk.Entry(user_info_frame, width=70)  # Increased width
#     permanent_address_entry.grid(row=11, column=0, sticky="ew")

#     # Education Info
#     education_info_frame = ttk.LabelFrame(main_content_frame, text="Education Information", padding="10")
#     education_info_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

#     # School
#     school_label = ttk.Label(education_info_frame, text="School")
#     school_label.grid(row=0, column=0, sticky="w")
#     school_entry = ttk.Entry(education_info_frame, width=50)  # Increased width
#     school_entry.grid(row=1, column=0, columnspan=3, sticky="ew")

#     # Faculty
#     faculty_label = ttk.Label(education_info_frame, text="Faculty")
#     faculty_label.grid(row=2, column=0, sticky="w")
#     faculty_entry = ttk.Entry(education_info_frame, width=70)  # Increased width
#     faculty_entry.grid(row=3, column=0, sticky="ew")

#     # GPA
#     gpa_label = ttk.Label(education_info_frame, text="GPA")
#     gpa_label.grid(row=4, column=0, sticky="w")
#     gpa_entry = ttk.Entry(education_info_frame, width=70)  # Increased width
#     gpa_entry.grid(row=5, column=0, sticky="ew")

#     # Passout Year
#     passout_year_label = ttk.Label(education_info_frame, text="Passout Year")
#     passout_year_label.grid(row=6, column=0, sticky="w")
#     passout_year_entry = ttk.Entry(education_info_frame, width=70)  # Increased width
#     passout_year_entry.grid(row=7, column=0, sticky="ew")

#     # Enrollment Course
#     enrollment_course_label = ttk.Label(education_info_frame, text="Enrollment Course")
#     enrollment_course_label.grid(row=8, column=0, sticky="w")
#     enrollment_course_entry = ttk.Entry(education_info_frame, width=70)  # Increased width
#     enrollment_course_entry.grid(row=9, column=0, sticky="ew")

#     # Submit Button Frame
#     submit_button_frame = ttk.Frame(main_content_frame)
#     submit_button_frame.grid(row=3, column=0, padx=10, pady=10)

#     # Submit Button
#     submit_button = ttk.Button(submit_button_frame, text="Submit", style="TSubmit.TButton", command=submit_data)
#     submit_button.pack(pady=10)

#     # Call populate_entries when the window initializes
#     populate_entries()

#     # Start the main event loop
#     window.mainloop()

#     return new_id[0]  # Return the new ID after the main loop ends

# if __name__ == "__main__":
#     new_id = main(None)
#     print(f"The new ID is: {new_id}")


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import backend

def main(all_info):
    new_id = [None]  # Mutable object to store the new ID

    def get_from_json():
        filepath = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\extracted_text.json"
        with open(filepath, 'r', encoding='utf-8') as file:
            all_info = json.load(file)
            return all_info

    def on_enter(event):
        event.widget['background'] = '#0f5c91'  # Hover color

    def on_leave(event):
        event.widget['background'] = '#1283b9'  # Original color

    def on_click(event):
        event.widget['background'] = '#0d4a73'  # Click color

    def populate_entries(data):
        entry_map = {
            "citizenship_no": citizenship_no_entry,
            "full_name": full_name_entry,
            "sex": sex_label_entry,
            "DoB": dob_year_entry,
            "birth_place": birth_place_entry,
            "address": permanent_address_entry,
            "school": school_entry,
            "gpa": gpa_entry,
            "faculty": faculty_entry,
            "passout_year": passout_year_entry,
            "course": enrollment_course_entry
        }

        # Insert the data into the Entry widgets
        for key, entry_widget in entry_map.items():
            # Convert non-string data types to string
            value = data.get(key, "")
            if isinstance(value, (int, float)):
                value = str(value)
            entry_widget.delete(0, tk.END)  # Clear the current content
            entry_widget.insert(0, value)  # Insert the new content

    def submit_data():
        updated_info = {
            "citizenship_no": citizenship_no_entry.get(),
            "full_name": full_name_entry.get(),
            "sex": sex_label_entry.get(),
            "DoB": dob_year_entry.get(),
            "birth_place": birth_place_entry.get(),
            "address": permanent_address_entry.get(),
            "school": school_entry.get(),
            "faculty": faculty_entry.get(),
            "gpa": gpa_entry.get(),
            "passout_year": passout_year_entry.get(),
            "course": enrollment_course_entry.get()
        }

        course = "Bsc. (Hons.) Computing"
        front = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\citizenship_front.jpg"
        back = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\citizenship_back.jpg"
        mark = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\marksheet.jpg"
        pic = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\student_image.jpg"
        
        new_id[0] = backend.insert_student_data(
            updated_info["citizenship_no"],
            updated_info["full_name"],
            updated_info["sex"],
            updated_info["DoB"],
            updated_info["birth_place"],
            updated_info["address"],
            updated_info["school"],
            updated_info["faculty"],
            updated_info["gpa"],
            updated_info["passout_year"],
            course,
            front,
            back,
            mark
        )

        if new_id[0] is not None:
            messagebox.showinfo("Success", f"Student data inserted successfully. New ID: {new_id[0]}")
        else:
            messagebox.showerror("Error", "Failed to insert student data.")
            
        root.destroy()

    root = tk.Tk()
    root.title("Student Registration Form")

    # Maximize the window
    root.state('zoomed')

    # Create the main frame with a blue background
    main_frame = tk.Frame(root, bg='#1283b9')
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Create a frame inside the main frame with a white background
    inner_frame = tk.Frame(main_frame, bg='white', bd=2, relief=tk.RAISED)
    inner_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.95, relheight=0.9)

    # Add a heading label inside the white frame
    heading_label = tk.Label(inner_frame, text="Student Registration Form", font=("Monotype Corsiva", 36, "bold"), bg='white', fg='#1283b9')
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
        "Full Name",
        "Sex",
        "Date of Birth",
        "Birth Place",
        "Permanent Address"
    ]

    entry_vars = {}
    for i, info in enumerate(personal_info):
        label = tk.Label(left_frame, text=info, font=("Times New Roman", 16), bg='white')
        label.pack(anchor='w', padx=10, pady=5)
        entry = tk.Entry(left_frame, font=("Times New Roman", 14))
        entry.pack(fill='x', padx=10, pady=5)
        entry_vars[info.lower().replace(' ', '_')] = entry

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
        entry_vars[info.lower().replace(' ', '_')] = entry

    # Assign entries to global variables for submission and population
    global citizenship_no_entry, full_name_entry, sex_label_entry, dob_year_entry, birth_place_entry, permanent_address_entry
    global school_entry, faculty_entry, gpa_entry, passout_year_entry, enrollment_course_entry

    citizenship_no_entry = entry_vars["citizenship_number"]
    full_name_entry = entry_vars["full_name"]
    sex_label_entry = entry_vars["sex"]
    dob_year_entry = entry_vars["date_of_birth"]
    birth_place_entry = entry_vars["birth_place"]
    permanent_address_entry = entry_vars["permanent_address"]
    school_entry = entry_vars["school"]
    faculty_entry = entry_vars["faculty"]
    gpa_entry = entry_vars["gpa"]
    passout_year_entry = entry_vars["passout_year"]
    enrollment_course_entry = entry_vars["enrollment_course"]

    # Submit button at the bottom
    submit_button = tk.Button(inner_frame, text="Submit", font=("Times New Roman", 16, "bold"), bg='#1283b9', fg='white', padx=40, pady=8, command=submit_data)
    submit_button.pack(pady=40, padx=10, side='bottom')

    # Bind events for hover and click effects
    submit_button.bind("<Enter>", on_enter)
    submit_button.bind("<Leave>", on_leave)
    submit_button.bind("<ButtonPress-1>", on_click)
    submit_button.bind("<ButtonRelease-1>", on_enter)  # Change back to hover color on release

    # Populate the entries with JSON data
    all_info = get_from_json()
    populate_entries(all_info)

    root.mainloop()

    return new_id[0]

if __name__ == "__main__":
    new_id = main(None)
    print(f"The new ID is: {new_id}")