import pytesseract 
from PIL import Image
import cv2 
import numpy as np


image = cv2.imread('picture.jpg')
image = cv2.resize(image, (640, 480), interpolation=cv2.INTER_CUBIC)
#cv2.imshow("Image", image)
#cv2.waitKey(0)

imagem_recorte1=np.empty((50,6400))
imagem_recorte1=image[0:49,0:639]

cv2.imshow("Image", imagem_recorte1)
cv2.waitKey(0)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
#cv2.imshow("Image", blurred)
#cv2.waitKey(0)

thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 10)
#cv2.imshow("Image", thresh)

#v2.imshow("Simple Thresholding", thresh)
#cv2.waitKey(0)

text = pytesseract.image_to_string(thresh)





print(text)