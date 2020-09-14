import cv2

bg1=cv2.imread("C:\\Users\\SiddiquW\\Pictures\\5099 polished BG1.jpg")
bg2=cv2.imread("C:\\Users\\SiddiquW\\Pictures\\5099 polished BG2.jpg")
fringepic=cv2.imread("C:\\Users\\SiddiquW\\Pictures\\5099 polished fringes.jpg")

#fringepic-bg1-bg2
temp=cv2.subtract(fringepic,bg1)
temp=cv2.subtract(temp,bg2)

print(temp.min())
print(temp.max())

temp=temp-temp.min()
temp=temp/temp.max()

#temp=255*temp


cv2.imshow('image',temp)

cv2.waitKey(0)
cv2.destroyAllWindows()

"""
cv2.imshow('image',temp)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""

