import pytesseract
from PIL import Image
import os

# Set the path to the Tesseract executable
tesseract_path = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
print(f"Tesseract path: {tesseract_path}")
pytesseract.pytesseract.tesseract_cmd = tesseract_path

def extract_text(image_path):
    print(f"Image path: {image_path}")
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    # Correct the image orientation
    
    image = Image.open(image_path)
    print("Image opened successfully")
    
    # Ensure the image has a valid resolution
    image = image.convert('RGB')
    image.save(image_path, dpi=(300, 300))
    
    # Perform OCR on the image for both English and Nepali
    try:
        text = pytesseract.image_to_string(image, lang='eng+nep')
        print("OCR completed")
    except pytesseract.TesseractError as e:
        print(f"Tesseract OCR Error: {e}")
        text = ""

    return text

