import pytesseract 
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\100064613\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

# Simple image to string
print(pytesseract.image_to_string(Image.open('test_image3.jpg')))


'''
# Timeout/terminate the tesseract job after a period of time
try:
    print(pytesseract.image_to_string('test_image.jpg', timeout=2)) # Timeout after 2 seconds
    print(pytesseract.image_to_string('_image.jpg', timeout=0.5)) # Timeout after half a second
except RuntimeError as timeout_error:
    # Tesseract processing is terminated
    pass

# Get bounding box estimates
print(pytesseract.image_to_boxes(Image.open('test_image_out.png')))

'''