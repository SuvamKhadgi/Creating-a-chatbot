from fuzzywuzzy import fuzz, process
import cv2
import numpy as np
import os
from PIL import Image
import pytesseract

    
    


def text_to_2d_array(lines):
    # Initialize an empty 2D array
    word_array = []
    
    # Process each line
    for line in lines:
        # Split the line into words
        words = line.split()
        # Append the list of words as a new row in the 2D array
        word_array.append(words)

    print("2d array", word_array)



    return word_array


from fuzzywuzzy import fuzz

def find_citizenship(text):
    # Define the target keywords
    target_keywords = ["citizenship", "full name", "date of birth", "birthplace", "permanent address"]

    # Split the text into words
    words = text.split()

    # Check for fuzzy matches
    for word in words:
        for target_word in target_keywords:
            if fuzz.ratio(word.lower(), target_word.lower()) > 80:  # Using a threshold of 80 for fuzzy matching
                return True
    return False


def find_phrase_end_coordinates(word_array, target_phrase, threshold=80):
    coordinates = []
    words = target_phrase.split()
    num_words = len(words)
    
    # Iterate over each row (line)
    for i, row in enumerate(word_array):
        row_length = len(row)
        # Check each possible starting point in the row
        for j in range(row_length):
            if j + num_words <= row_length:
                match = True
                # Check if the subsequent words match using fuzzy matching
                for k in range(num_words):
                    similarity = fuzz.ratio(row[j + k], words[k])
                    if similarity < threshold:
                        match = False
                        break
                if match:
                    # Append the end coordinates
                    coordinates.append((i, j + num_words - 1))
                    break

    return coordinates


def find_phrase_start_coordinates(word_array, target_phrase, threshold=80):
    coordinates = []
    words = target_phrase.split()
    num_words = len(words)
    
    # Iterate over each row (line)
    for i, row in enumerate(word_array):
        row_length = len(row)
        # Check each possible starting point in the row
        for j in range(row_length):
            if j + num_words <= row_length:
                match = True
                # Check if the subsequent words match using fuzzy matching
                for k in range(num_words):
                    similarity = fuzz.ratio(row[j + k], words[k])
                    if similarity < threshold:
                        match = False
                        break
                if match:
                    # Append the start coordinates
                    coordinates.append((i, j))
                    break

    return coordinates


def get_data_between_phrases(word_array, phrase1, phrase2):
    # Find end coordinates of phrase1
    end_coords_phrase1 = find_phrase_end_coordinates(word_array, phrase1)
    # Find start coordinates of phrase2
    print("start")
    print(end_coords_phrase1)
    start_coords_phrase2 = find_phrase_start_coordinates(word_array, phrase2)
    print("end")
    print(start_coords_phrase2)
    
    if not end_coords_phrase1 or not start_coords_phrase2:
        return None

    end_row1, end_col1 = end_coords_phrase1[0]
    start_row2, start_col2 = start_coords_phrase2[0]
    
    if end_row1 > start_row2 or (end_row1 == start_row2 and end_col1 >= start_col2):
        return None  # Phrase2 starts before phrase1 ends or they overlap
    
    data_between = []
    
    # If phrases are in the same row
    if end_row1 == start_row2:
        data_between.append(word_array[end_row1][end_col1 + 1:start_col2])
    else:
        # Extract data from the end of phrase1's row to the end of the row
        data_between.append(word_array[end_row1][end_col1 + 1:])
        
        # Extract data from the rows in between
        for row in range(end_row1 + 1, start_row2):
            data_between.append(word_array[row])
        
        # Extract data from the start of phrase2's row to the start of phrase2
        data_between.append(word_array[start_row2][:start_col2])
    
    # Flatten the list of lists into a single list
    flattened_data = [item for sublist in data_between for item in sublist]
    
    return ' '.join(flattened_data)


def get_data_after_phrase(word_array, phrase):
    # Find end coordinates of the phrase
    end_coords_phrase = find_phrase_end_coordinates(word_array, phrase)
    
    if not end_coords_phrase:
        return None

    end_row, end_col = end_coords_phrase[0]
    
    # Collect all data after the phrase
    data_after = []
    
    # Extract data from the end of the phrase's row to the end of the row
    data_after.append(word_array[end_row][end_col + 1:])
    
    # Extract data from the rows after the phrase's row
    for row in range(end_row + 1, len(word_array)):
        data_after.append(word_array[row])
    
    # Flatten the list of lists into a single list
    flattened_data = [item for sublist in data_after for item in sublist]
    
    return ' '.join(flattened_data)

def get_birdeye_view(image_path):
    # Read the input image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image at path '{image_path}' not found.")
    
    # Define the source points (the points on the original image)
    # These should be the points of the area you want to transform
    # Here we assume a simple case where the image is a rectangle
    h, w = image.shape[:2]
    src_points = np.float32([
        [0, h],       # Bottom-left corner
        [w, h],       # Bottom-right corner
        [0, 0],       # Top-left corner
        [w, 0]        # Top-right corner
    ])

    # Define the destination points (the points on the output image)
    dst_points = np.float32([
        [0, h],       # Bottom-left corner
        [w, h],       # Bottom-right corner
        [0, 0],       # Top-left corner
        [w, 0]        # Top-right corner
    ])

    # Compute the perspective transformation matrix
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)

    # Apply the perspective transformation to get the bird's-eye view
    birdseye_view = cv2.warpPerspective(image, matrix, (w, h))

    # Generate the output path
    base, ext = os.path.splitext(image_path)
    output_path = f"{base}_birdseye{ext}"

    # Save the resulting image
    cv2.imwrite(output_path, birdseye_view)

    return output_path
