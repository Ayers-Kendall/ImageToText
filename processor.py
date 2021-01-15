import cv2
from PIL import Image
import pytesseract

img = cv2.imread('./pre-data/000000003.jpg')
img = Image.open('./pre-data/000000006.jpg')
print(pytesseract.image_to_string(img, lang='eng'))