from tkinter import *
from PIL import ImageTk,Image
import cv2
import numpy as np
from matplotlib import pyplot as plt
numofdots=0
pts1=[]
pts2=[]
class Application(Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master=master
        master.title("PopiPy")
        self.pack()

    
def motion(event):
  print("Mouse position: (%s %s)" % (event.x, event.y))
  return

def calc(event):
    #pts1=[166,236]
    #pts2=[528,240]
    diskDiameter=9.5
    diameterPx=np.linalg.norm(np.subtract(pts1,pts2))
    diameterPx=np.round(diameterPx,decimals=3)
    distance=diskDiameter/diameterPx
    distance=1000*(np.round(distance,decimals=5))
    print(distance)



def displayGraph(event):
    img=cv2.imread("C:\\Users\\SiddiquW\\Pictures\\sample image.jpg")
    fig,ax=plt.subplots()
    plt.imshow(img)
    
    def onclick(event):
        global numofdots
        numofdots+=1
        xvalue=int(event.xdata)
        yvalue=int(event.ydata)
        if(numofdots==1):
            pts1.append(xvalue)
            pts1.append(yvalue)
        elif(numofdots==2):
            pts2.append(xvalue)
            pts2.append(yvalue)
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
        
      
        cv2.circle(img, (xvalue, yvalue), 1, 255, -10)
        plt.imshow(img),plt.show()

    cid=plt.connect('button_press_event', onclick)
    plt.connect('close_event',calc)
    plt.show()
    print("working")

master = Tk()

img = Image.open('C:\\Users\\SiddiquW\\Pictures\\5099 polished size ref.jpg') 
#img = img.resize((350, 350), Image.ANTIALIAS) 
img = ImageTk.PhotoImage(img) 
msg = Label(master, image = img)
msg.image = img
msg.bind('<Button-1>',displayGraph)
msg.bind('<Button-3>',motion)
msg.pack()
mainloop()