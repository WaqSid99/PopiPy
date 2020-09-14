
import numpy as np
import cv2
from PIL import Image

# Create a black image
#img = np.zeros((512,512,3), np.uint8)
img =cv2.imread("C:\\Users\\SiddiquW\\Pictures\\5099 polished size ref.jpg")
dimension = img.shape
print(dimension)

# Draw a diagonal blue line with thickness of 5 px
def mouse_click(event,x,y,flags,param):
    global img
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x)
        print(y)
        img = cv2.circle(img,(x,y),1,(255,0,0),5)
        cv2.imshow('image',img)
    if event == cv2.EVENT_RBUTTONDOWN:
        print("Show calibration here")
        func(x,y)
       

def func(a,b):
    print(a+b)
    cv2.destroyAllWindows() 


cv2.imshow('image',img)

cv2.setMouseCallback('image', mouse_click)
print("hurray")
cv2.waitKey(0)
cv2.destroyAllWindows()
