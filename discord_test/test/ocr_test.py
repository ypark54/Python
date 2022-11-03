import easyocr
import cv2


reader = easyocr.Reader(['ko'])
img = cv2.imread('C:/Python/poe_img/name.png')
result = reader.readtext(img)
print(result)
