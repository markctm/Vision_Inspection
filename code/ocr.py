import pytesseract 
from PIL import Image
import cv2 


image = cv2.imread('picture.jpg')
cv2.imshow("Image", image)
cv2.waitKey(0)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (7, 7), 0)
cv2.imshow("Image", blurred)
cv2.waitKey(0)

(T, threshInv) = cv2.threshold(blurred, 230, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
cv2.imshow("Simple Thresholding", threshInv)
cv2.waitKey(0)

text = pytesseract.image_to_string(threshInv)
print(text)





