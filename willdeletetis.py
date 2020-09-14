from matplotlib import pyplot as plt 
import matplotlib.image as mpimg
import cv2
import numpy as np


img=cv2.imread("C:\\Users\\SiddiquW\\Pictures\\sample image.jpg")

fig,ax=plt.subplots()
plt.imshow(img)
xvalue=0

pts1=[]
pts2=[]

clickCounter=0

def onclick(event):
    global clickCounter
    clickCounter+=1
    diskDiameter=9.5

    xvalue=int(event.xdata)
    yvalue=int(event.ydata)

    if(clickCounter==1):
        pts1.append(xvalue)
        pts1.append(yvalue)
    else:
        pts2.append(xvalue)
        pts2.append(yvalue)

    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    
    cv2.circle(img, (xvalue, yvalue), 3, 255, -5)
    plt.imshow(img),plt.show()
    #print(xvalue)

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()


print(pts1)
print(pts2)
norm=np.subtract(pts1,pts2)
print(np.subtract(pts1,pts2))
print(np.linalg.norm(norm))
xy=0.01*(9.5/np.linalg.norm(norm))

print("XY resolution is :",xy)