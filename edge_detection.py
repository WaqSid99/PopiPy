# import the required library 
import numpy as np 
import cv2 
from matplotlib import pyplot as plt 
import matplotlib.image as mpimg
from PIL import Image

# read the image 
img = cv2.imread("C:\\Users\\SiddiquW\\Pictures\\5099 polished size ref.jpg") 
#"C:\\Users\\SiddiquW\Downloads\\corner1.png"

# convert image to gray scale image 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

# detect corners with the goodFeaturesToTrack function. 
corners = cv2.goodFeaturesToTrack(gray, 27, 0.01, 10) 
corners = np.int0(corners) 

# we iterate through each corner, 
# making a circle at each point that we think is a corner. 
print(corners)
for i in corners: 
	x, y = i.ravel() 
	cv2.circle(img, (x, y), 3, 255, -1) 

plt.imshow(img),plt.show() 

"""

# read the image 
#img = cv2.imread("C:\\Users\\SiddiquW\\Pictures\\5099 polished size ref.jpg") 
#"C:\\Users\\SiddiquW\Downloads\\corner1.png"
#plt.imshow(img)

img = cv2.imread("C:\\Users\\SiddiquW\\Pictures\\5099 polished size ref.png")
#img=Image.open("C:\\Users\\SiddiquW\\Pictures\\5099 polished size ref.jpg")

fig, ax = plt.subplots()
#ax.plot(np.random.rand(20))
imgplot = plt.imshow(img)

def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()  
"""