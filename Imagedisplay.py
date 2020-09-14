import sys
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk,Image
from tkinter import filedialog
import cv2
import numpy as np
from tkinter import messagebox

class Application(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master=master
        master.title("PopiPy")
        self.pack()
x=""
img=""

distance=0

def open_img():
    global panel
    global x
    global img
    x = filedialog.askopenfilename(title ='Select an Image') 
    try:
        #--Show error message as a 
        img = Image.open(x) 
        #img = img.resize((350, 350), Image.ANTIALIAS) 
        img = ImageTk.PhotoImage(img) 
        panel = tk.Label(root, image = img)
        panel.image = img
        #panel.grid(row=2) 
        panel.pack()
        loadButton['state']="disabled"
        closeButton['state']="normal"
        calib['state']="normal"
    except:
        messagebox.showerror("Error","Image not correct")
        print(sys.exc_info()[0]," occurred")

def close_img():
    panel.destroy()
    loadButton['state']="normal"
    closeButton['state']="disabled"


def calibCalc():
    global x    #String address of image
    global img
    global text
    img =cv2.imread(x)
    pts1=[]
    pts2=[]
    

    def mouse_click(event,x,y,flags,param):        
        global img
        #global counter
        
        if event == cv2.EVENT_LBUTTONDOWN:
            #print(x)
            #print(y)
            if(len(pts1)==0 and len(pts2)==0):
                pts1.append(x)
                pts1.append(y)
            elif(len(pts2)==0):
                pts2.append(x)
                pts2.append(y)
            #counter+=1
            cv2.circle(img,(x,y),1,(255,0,0),3)
            cv2.imshow('image',img)
        if event == cv2.EVENT_RBUTTONDOWN:
            print("Show calibration here")
            func()
            cv2.destroyAllWindows()

       

    def func():
        global distance
        
        diskDiameter=9.5
        diameterPx=np.linalg.norm(np.subtract(pts1,pts2))
        diameterPx=np.round(diameterPx,decimals=3)
        distance=diskDiameter/diameterPx
        distance=1000*(np.round(distance,decimals=4))
        #print(distance) 
        #String="Resolution is : "+str(distance)+' \u03BCm/px'
        #text.destroy()      
        #text=tk.Label(root,text=String)
        #text.pack()

    cv2.imshow('image',img)
    cv2.setMouseCallback('image', mouse_click)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    text.destroy()
    String="Resolution is : "+str(distance)+' \u03BCm/px'
    text.destroy()      
    text=tk.Label(root,text=String)
    text.pack()

def doCrop():
    from imgCropCircle import cropClass
    obj=cropClass(img)
    print("Import done")

"""
def createTab():
    my_notebook=ttk.Notebook(root)
    my_notebook.pack(pady=67)

    my_frame=tk.Frame(my_notebook)
    my_frame.pack(fill="both",expand=1)

    my_button=tk.Button(my_frame,text="button",command).pack()

    my_notebook.add(my_frame,text="Tab 1")
"""

root=tk.Tk()
root.iconbitmap('C:\\Users\\SiddiquW\\hello\\0_vW3_icon.ico')
root.geometry("750x750")
app=Application(root)

text=tk.Label(root)

loadButton=tk.Button(root,text="Load Image",width=10,command=open_img)
loadButton.place(relx = 0.20, rely = 0.95,anchor="s")
#loadButton.pack()

closeButton=tk.Button(master=root,text="Close Image",width=10, command=close_img)
closeButton.place(relx = 0.49, rely = 0.95,anchor="s")
closeButton['state']="disabled"

calib=tk.Button(master=root,text="Find Calibration", width=15,command=calibCalc)
calib.place(relx=0.65, rely=0.95,anchor="s")#
calib['state']="disabled"
#calib.pack()


tab=tk.Button(master=root,text="Crop",width=10, command=doCrop)
tab.place(relx = 0.88, rely = 0.95,anchor="s")

root.mainloop()

