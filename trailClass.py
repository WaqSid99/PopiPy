import cv2
from matplotlib import pyplot as plt 
import numpy as np
import sys

imageaddress=""
img=""
clickCounter=0
pts1=[]
pts2=[]
distance=0

"""
def onclick(event):

    global clickCounter
    global pts1
    global pts2

    if(clickCounter<2):
        xvalue=int(event.xdata)
        yvalue=int(event.ydata)

        clickCounter+=1
        if(clickCounter==1):
            pts1.append(xvalue)
            pts1.append(yvalue)
        elif(clickCounter==2):
            pts2.append(xvalue)
            pts2.append(yvalue)

        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
            ('double' if event.dblclick else 'single', event.button,
            event.x, event.y, event.xdata, event.ydata))

        cv2.circle(img, (xvalue, yvalue), 3, 255, -5)
#        plt.imshow(img),plt.show()
        
    else:
        print("Disconnecting....")
        print(someClass.displayData(self=someClass))
        plt.close()
    
"""
class someClass:
 
    def __init__(self,address):
        global imageaddress
        
        global img
        imageaddress=address
        img=cv2.imread(address)
    
    def returnAddress(self):
        print(imageaddress)
        print(type(imageaddress))
    
    def loadImage(self):
        img=cv2.imread(imageaddress)
        plt.imshow(img),plt.show()
    
    def displayData(self):
        global distance
        diskDiameter=9.5
        diameterPx=np.linalg.norm(np.subtract(pts1,pts2))
        diameterPx=np.round(diameterPx,decimals=3)
        distance=diskDiameter/diameterPx
        distance=1000*(np.round(distance,decimals=5))
        return(distance)
        

    
    def eventHandle(self):
        plt.imshow(img)
        def onclick(event):

            global clickCounter
            global pts1
            global pts2

            if(clickCounter<2):
                xvalue=int(event.xdata)
                yvalue=int(event.ydata)

                clickCounter+=1
                if(clickCounter==1):
                    pts1.append(xvalue)
                    pts1.append(yvalue)
                elif(clickCounter==2):
                    pts2.append(xvalue)
                    pts2.append(yvalue)

                print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                    ('double' if event.dblclick else 'single', event.button,
                    event.x, event.y, event.xdata, event.ydata))

                cv2.circle(img, (xvalue, yvalue), 3, 255, -5)
        #        plt.imshow(img),plt.show()
                
            else:
                print("Disconnecting....")
                print(someClass.displayData(self=someClass))
                plt.close()
                print("gone down")

        
        cid=plt.connect('button_press_event', onclick)
        #plt.connect('close_event',closePlot)
        if(clickCounter<2):
            plt.show()
        else:
            return distance
        #plt.disconnect(cid)
      
        


#obj=someClass("C:\\Users\\SiddiquW\\Pictures\\5099 polished size ref.jpg")
#obj.eventHandle()
#obj.displayData()
