import tkinter as tk
from PIL import ImageTk,Image
from tkinter import filedialog
import cv2
import numpy as np
from matplotlib import pyplot as plt 
import matplotlib.image as mpimg
import trailClass 




class Application(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master=master
        master.title("PopiPy")
        self.pack()


x=""  #Image Address
inta=76
def open_img():
    global panel
    global img
    global x
    global inta
    x = filedialog.askopenfilename(title ='Select an Image') 
    img = Image.open(x) 
    img = img.resize((350, 350), Image.ANTIALIAS) 
    img = ImageTk.PhotoImage(img) 
    panel = tk.Label(root, image = img)
    panel.image = img
    #panel.grid(row=2) 
    panel.pack()
    loadButton['state']="disabled"
    closeButton['state']="normal"
    calib['state']="normal"
    obj=trailClass.someClass(x)
    inta=obj.eventHandle()
    print(inta)

   # imgcv=cv2.imread("C:\\Users\\SiddiquW\\Pictures\\5099 polished size ref.jpg")
   # px=imgcv[300]
    

def close_img():
    panel.destroy()
    loadButton['state']="normal"
    closeButton['state']="disabled"

counter=0
def calibrationCalc():
    print(inta)
    text=tk.Label(master=root,text=inta)
    text.pack()   
         
        
root=tk.Tk()

root.geometry("500x500")
app=Application(root)

loadButton=tk.Button(root,text="Load Image",width=10,command=open_img)
loadButton.place(relx = 0.20, rely = 0.95,anchor="s")
#loadButton.pack()

closeButton=tk.Button(master=root,text="Close Image",width=10, command=close_img)
closeButton.place(relx = 0.49, rely = 0.95,anchor="s")
closeButton['state']="disabled"

calib=tk.Button(master=root,text="Find Calibration", width=15,command=calibrationCalc)
calib.place(relx=0.80, rely=0.95,anchor="s")#
calib['state']="disabled"
#calib.pack()

root.mainloop()

