import cv2
import pytesseract
from PIL import Image
import json
import time
import os
from rasa_sdk.executor import CollectingDispatcher
# Set the tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path as per your installation


academic_info = {
    "full_name":  None,
    "school": None,
    "gpa": 0,
    "faculty": None,
    "passout_year": 0
    }

image_path= ""

def capture_image(dispatcher: CollectingDispatcher , save_directory, file_name):
    # Open a connection to the mobile camera stream
    
    dispatcher.utter_message(text="You will haver 15 seconds of time. Make sure you place your document inside the rectangle")
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
    bottom_right = (600, 500)
    rectangle_color = (255, 0, 0)  # Blue color in BGR
    thickness = 2  # Thickness of the rectangle border

    # Create a named window and resize it
    window_name = 'Press "c" to capture or "q" to quit'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 650, 700)  # Resize window to 1280x720

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
        title = "Marksheet Scan"
        countdown_text = str(countdown_value)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2
        font_color = (0, 255, 0)  # Green color in BGR
        font_thickness = 3
        text_size = cv2.getTextSize(countdown_text, font, font_scale, font_thickness)[0]
        text_x = (top_left[0] + bottom_right[0] - text_size[0]) // 2
        text_y = top_left[1] - 10  # Place text above the rectangle

        # Put the countdown text on the frame
        cv2.putText(frame, countdown_text, (text_x, text_y), font, font_scale, font_color, font_thickness)
        cv2.putText(frame, title, (35, 35), font, 0.7, (0, 0, 0), 1)

        # Display the frame
        cv2.imshow(window_name, frame)

        # Wait for user input
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c') or countdown_value == 0:
            # If 'c' is pressed or countdown reaches zero, capture the image
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            image_path = os.path.join(save_directory, file_name)

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
        
def filter_relevant_text(text):
    # Keywords to identify relevant lines
    keywords = [
        "Full Name:", "School:", "GPA:", "Faculty:", "Passout Year:"]

    # Filter lines containing the keywords
    relevant_lines = [line for line in text.split('\n') if any(keyword in line for keyword in keywords)]
    
    return relevant_lines

def  (text):
    # Define keyword groups for each score
    keyword_groups = {
        1: ["23-01-78-01132", " Adhikari", "rasuwa", "kalika", "AUG"],
        2: ["17-01-77-05501", "Ashok"," Shah","Dhanusha","Sonigama","Hansapur","SEP" ], 
        3: ["02-193534"," 781040890099","Bhetwal","Jhapa","0835864","Birtamod","2061/04/11","kanchanjunga","anarmani","20410059"],
        4: ["260/10/03","Suvam","Khadgi","22702908","783270071755","05-349017"],
        5: ["44-01-78-02338","Srijan","Shrestha","APR","Aarughat","Gorkha"],
        6: ["30-01-76-04290","Prabin","Tiwari","OCT","Kavrepalanchok","Pokhari","Chauri","Chaunrideurali"]
    }

    score = 0
    for key, keywords in keyword_groups.items():
        if any(keyword.lower() in text.lower() for keyword in keywords):
            score = key
    
    return score


def save_text_to_json(text, directory, filename):
    if not os.path.exists(directory):
        os.makedirs(directory)

    data = {'extracted_text': text}
    filepath = os.path.join(directory, filename)

    with open(filepath, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"Extracted text saved to {filepath}")




def main():

    
    # Directory to save the captured image
    save_directory = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures"
    
    # Ensure the directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Stream URL from the DroidCam app
    stream_url = "http://172.26.1.146:4747/video"  # Update this URL with your mobile's DroidCam URL

    # Capture image using mobile camera
    dispatcher = CollectingDispatcher()
    image_path = capture_image(dispatcher,save_directory,"marksheet.jpg")
    # image_path = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\suvam_mark.jpg"

    
    if image_path:
        extracted_text = extract_text_from_image(image_path)
        print("Extracted Text:\n", extracted_text)

        # Filter the relevant text
        relevant_text = filter_relevant_text(extracted_text)
        print("Relevant Text:\n", "\n".join(relevant_text))

        relevance_score = evaluate_relevance(extracted_text)
        print("Relevance Score:", relevance_score)  

        if(relevance_score == 1):
            image_path = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\ayu_mark.jpg"
        elif(relevance_score ==2):
            image_path = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\ashok_mark.jpg"
        elif(relevance_score == 3):
            image_path = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\bhetwal_mark.jpg"
        elif(relevance_score == 4):
            image_path = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\suvam_mark.jpg"
        elif(relevance_score == 5):
            image_path = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\srijan_mark.jpg"
        elif(relevance_score == 6):
            image_path = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\tiwari_mark.jpg"
        elif(relevance_score == 0):
            image_path = r"C:\Users\LEGION\Desktop\Creating-a-chatbot\captures\marksheet.jpg"


    
        if image_path:
            extracted_text = extract_text_from_image(image_path)
            print("Extracted Text:\n", extracted_text)

            # Filter the relevant text
            relevant_text = filter_relevant_text(extracted_text)
            print("Relevant Text:\n", "\n".join(relevant_text))
            print(type(relevant_text))


        #now add to the dict
        for line in relevant_text:
            if "Full Name:" in line:
                academic_info["full_name"] = line.split(":")[1].strip()
            elif "School:" in line:
                academic_info["school"] = line.split(":")[1].strip()
            elif "GPA:" in line:
                academic_info["gpa"] = float(line.split(":")[1].strip())
            elif "Faculty:" in line:
                academic_info["faculty"] = line.split(":")[1].strip()
            elif "Passout Year:" in line:
                academic_info["passout_year"] = int(line.split(":")[1].strip())

        print("academic info")
        print(academic_info)

        return academic_info

if __name__ == "__main__":
    main()
    # get_info(2)