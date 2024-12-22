import cv2
import face_recognition
import os
import subprocess

def label_faces(image_path, output_path,citi_no):
    # Load the image
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    # Convert the image to RGB (from BGR used by OpenCV)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Draw bounding box and label
        cv2.rectangle(image_rgb, (left, top), (right, bottom), (0, 0, 255), 2)
        name = citi_no
        # Draw label with name below the face
        cv2.rectangle(image_rgb, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(image_rgb, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Save face encoding with label
        with open(f"{output_path}/{name}.txt", 'w') as f:
            for value in face_encoding:
                f.write(f"{value}\n")

    # Save labeled image
    cv2.imwrite(f"{output_path}/labeled_image.jpg", image_rgb)
    print(f"Labeled image saved to {output_path}/labeled_image.jpg")

    # Open the labeled image using default image viewer (Windows)
    subprocess.Popen(['start', f"{output_path}/labeled_image.jpg"], shell=True)

# Example usage (comment this out when importing as a module)
# label_faces('captured_image.jpg', 'output_directory')