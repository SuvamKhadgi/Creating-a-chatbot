import cv2
import pytesseract
from PIL import Image
import json
import os
import numpy as np
import support as sp
import time
import sheet_scan as sc     
import threading
import pyttsx3
import form
import photo

# Set the tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path as per your installation
extracted_text = ""
target_keywords = [
    "Citizenship Certificate No:", "Sex:", "Full Name:", "Date of Birth (AD):",
    "Birth Place:", "Permanent Address:"
]

personal_info = {
    "citizenship_no": None,
    "full_name":  None,
    "sex": None,
    "DoB": None,
    "birth_place": None,
    "address": None
    }



def capture_image(save_directory,image_name,title):
    # Open a connection to the mobile camera stream
    # CollectingDispatcher.utter_message(text="You will haver 15 seconds of time. Make sure you place your document inside the rectangle")

    cap = cv2.VideoCapture(0)

    # Check if the stream is opened correctly
    if not cap.isOpened():
        print("Error: Could not open stream")
        return None

    # Countdown duration in seconds
    countdown_duration = 15
    start_time = time.time()

    # Define the rectangle parameters
    
    top_left = (50, 50)
    bottom_right = (600, 400)
    rectangle_color = (255, 0, 0)  # Blue color in BGR
    thickness = 2  # Thickness of the rectangle border

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Draw the rectangle on the frame
        cv2.rectangle(frame, top_left, bottom_right, rectangle_color, thickness)

        # Calculate the elapsed time and countdown value
        elapsed_time = time.time() - start_time
        countdown_value = max(0, countdown_duration - int(elapsed_time))

        # Define the countdown text and its position
        countdown_text = str(countdown_value)
        # title = "Citizenship Back"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2
        font_color = (0, 255, 0)  # Green color in BGR
        font_thickness = 3
        text_size = cv2.getTextSize(countdown_text, font, font_scale, font_thickness)[0]
        text_x = (top_left[0] + bottom_right[0] - text_size[0]) // 2
        text_y = top_left[1] - 10  # Place text above the rectangle

        # Put the countdown text on the frame
        cv2.putText(frame, countdown_text, (text_x, text_y), font, font_scale, font_color, font_thickness)
        cv2.putText(frame, title, (35, 35), font, 0.7, (0,0,0), 1)

        # Display the frame
        cv2.imshow('Press "c" to capture or "q" to quit', frame)

        # Wait for user input
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c') or countdown_value == 0:
            # If 'c' is pressed or countdown reaches zero, capture the image
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            image_path = os.path.join(save_directory, image_name)

            # Save the last frame within the rectangle as an image
            roi = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
            cv2.imwrite(image_path, roi)
            print("Image saved as", image_path)
            cap.release()
            cv2.destroyAllWindows()
            return image_path
        elif key == ord('q'):
            # If 'q' is pressed, quit the process
            print("Image capture canceled")
            cap.release()
            cv2.destroyAllWindows()
            return None

def extract_text_from_image(image_path):
    # Open the image file
    img = Image.open(image_path)

    # Use pytesseract to extract text
    text = pytesseract.image_to_string(img)

    return text

def bird_eye_view_image(image_path):
    # Load the image from the specified path
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image from {image_path}")
        return None

    orig = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    # Find contours
    contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Loop over the contours to find the document
    doc_contour = None
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            doc_contour = approx
            break

    if doc_contour is None:
        print("Error: No document found.")
        return None

    # Apply the perspective transform
    pts = doc_contour.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    (tl, tr, br, bl) = rect
    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))

    # Save the transformed image
    output_path = image_path.replace(".jpg", "_bird_eye_view.jpg")  # Adjust if the image has different extension
    cv2.imwrite(output_path, warped)
    print(f"Bird's-eye view image saved successfully at: {output_path}")

    return output_path

def filter_relevant_text(text):
    # Keywords to identify relevant lines
    keywords = [
        "Citizenship Certificate No:", "Sex:", "Full Name:", "Date of Birth (AD):", 
        "Birth Place:", "Permanent Address:"
    ]

    # Filter lines containing the keywords
    relevant_lines = [line for line in text.split('\n') if any(keyword in line for keyword in keywords)]
    
    return relevant_lines

def evaluate_relevance(text):
    # Define keyword groups for each score
    keyword_groups = {
        1: ["23-01-78-01132", " Adhikar", "rasuwa", "kalika", "AUG"],
        2: ["17-01-77-05501", "Ashok"," Shah","Dhanusha","Sonigama","Hansapur","SEP" ], 
        3: ["04-01-78-04518"," Bhetwal","JUL","Jhapa","Haldibari","Birtamode"],
        4: ["27-01-78-0028","Suvam","Khadgi","JAN","Kathmandu"],
        5: ["44-01-78-02338","Srijan","Shrestha","APR","Aarughat","Gorkha"],
        6: ["30-01-76-04290","Prabin","Tiwari","OCT","Kavrepalanchok","Pokhari","Chauri","Chaunrideurali"]
    }

    score = 0

    for key, keywords in keyword_groups.items():
        if any(keyword.lower() in text.lower() for keyword in keywords):score = key
    
    return score

def merge_dictionaries(dict1, dict2):
    # Create a new dictionary that starts as a copy of dict1
    merged_dict = dict1.copy()
    
    # Update the merged dictionary with key-value pairs from dict2
    merged_dict.update(dict2)
    
    return merged_dict

def save_text_to_json(text, directory, filename):
    if not os.path.exists(directory):
        os.makedirs(directory)

    data = {'extracted_text': text}
    filepath = os.path.join(directory, filename)

    with open(filepath, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"Extracted text saved to {filepath}")

def main(course):
    # Directory to save the captured image
    save_directory = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures"

    def speak(text):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'female' in voice.name.lower() or 'feminine' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.say(text)
        engine.runAndWait()

    

    
    threading.Thread(target=speak, args=("Please scan the front part of your citizenship",)).start()
    capture_image(save_directory,"citizenship_front.jpg","Citizenship Front")

    threading.Thread(target=speak, args=("Please can the back of your citizenship",)).start()
     
    
    # Ensure the directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Stream URL from the DroidCam app
    # stream_url = "http://172.26.1.190:4747/video"  # Update this URL with your mobile's DroidCam URL

    # Capture image using mobile camera
    image_path = capture_image(save_directory,"citizenship_back.jpg","Citizenship Back")
    # image_path = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\suvam.jpg"
    print("Path:", image_path)
    bird_eye = sp.get_birdeye_view(image_path)
    if image_path:
        extracted_text = extract_text_from_image(bird_eye)
        print("Extracted Text:\n", extracted_text)

        if( sp.find_citizenship(extracted_text) == False):
            threading.Thread(target=speak, args=("This is not a citizenship. Try again later with actual document",)).start()
            return

        # Filter the relevant text
        relevant_text = filter_relevant_text(extracted_text)
        print("Relevant Text:\n", "\n".join(relevant_text))
        print(type(relevant_text))

        relevance_score = evaluate_relevance(extracted_text)
        print("Relevance Score:", relevance_score)  

        if(relevance_score == 1):
            image_path = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\ayu.jpg"
        elif(relevance_score == 2):
            image_path = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\ashok.jpg"
        elif(relevance_score == 3):
            image_path = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\bhetwal.jpg"
        elif(relevance_score == 4):
            image_path = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\suvam.jpg"
        elif(relevance_score == 5):
            image_path = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\srijan.jpg"
        elif(relevance_score == 6):
            image_path = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\tiwari.jpg"
        elif(relevance_score == 0):
            image_path = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\citizenship_back_birdseye.jpg"


    
        if image_path:
            extracted_text = extract_text_from_image(image_path)
            print("Extracted Text:\n", extracted_text)

            # Filter the relevant text
            relevant_text = filter_relevant_text(extracted_text)
            print("Relevant Text:\n", "\n".join(relevant_text))
            print(type(relevant_text))


            #now save in the dict
            for line in relevant_text:
                if "Citizenship Certificate No:" in line:
                    personal_info["citizenship_no"] = line.split(":")[1].strip()
                elif "Sex:" in line:
                    personal_info["sex"] = line.split(":")[1].strip()
                elif "Full Name:" in line:
                    personal_info["full_name"] = line.split(":")[1].strip()
                elif "Date of Birth (AD):" in line:
                    personal_info["DoB"] = line.split(":")[1].strip()
                elif "Birth Place:" in line:
                    personal_info["birth_place"] = line.split(":")[1].strip()
                elif "Permanent Address:" in line:
                    personal_info["address"] = line.split(":")[1].strip()
            
            print("personal_info----------------------------------------------------------------------------------------------")
            print(personal_info)


            
            threading.Thread(target=speak, args=("Please can the +2 marksheet",)).start()
            academic_info = sc.main()
            print("this is academic")
            print(academic_info)

            if(personal_info["full_name"] == academic_info["full_name"]):
                print("Matched")

                all_info = merge_dictionaries(personal_info,academic_info)
                course = "computing"
                dic = {"course":course}
                all_info = merge_dictionaries(all_info,dic)
                save_text_to_json(all_info, save_directory,  "extracted_text.json")
                print("this is the comnbined one ----------------------------")
                print(all_info)

                print("###################")
                print( type(all_info["citizenship_no"]))

                id = form.main(all_info)
                print("this is the id",id)

                photo.main(str(id))
                

                
                

                
               
                
                # front = r"C:\Users\ittra\Downloads\chat\Creating-a-chatbot\captures\citizenship_front.jpg"
                # back = r"C:\Users\ittra\Downloads\chat\Creating-a-chatbot\captures\citizenship_back_birdseye.jpg"
                # mark = r"C:\Users\ittra\Downloads\chat\Creating-a-chatbot\captures\student_image.jpg"
                # confirm  = True 
                # if(confirm):
                #     backend.insert_student_data(all_info["citizenship_no"],all_info["full_name"],all_info["sex"],all_info["DoB"],all_info["birth_place"],all_info["address"],all_info["school"],all_info["faculty"],all_info["gpa"],all_info["passout_year"],course,front,back,mark)

                


            else:
                threading.Thread(target=speak, args=("The names in your documents do not match. Please try again with real documents",)).start()
                return


        

if __name__ == "__main__":
    main("Bsc. (Hons.) Computing")