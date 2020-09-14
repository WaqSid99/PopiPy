import cv2

img=cv2.imread("C:\\Users\\SiddiquW\\Pictures\\5099 polished size ref.jpg")
dst = cv2.fastNlMeansDenoising(img,None,10,7,21)

cv2.imshow('image',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()