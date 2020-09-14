import tkinter as tk

# loading Python Imaging Library 
from PIL import ImageTk, Image 

# To get the dialog box to open when required 
from tkinter import filedialog 

def open_img(): 
	# Select the Imagename from a folder 
	x = filedialog.askopenfilename(title ='open') 

	# opens the image 
	img = Image.open(x) 
	
	# resize the image and apply a high-quality down sampling filter 
	img = img.resize((350, 350), Image.ANTIALIAS) 

	# PhotoImage class is used to add image to widgets, icons etc 
	img = ImageTk.PhotoImage(img) 

	# create a label 
	panel = tk.Label(root, image = img) 
	
	# set the image as img 
	panel.image = img 
	panel.grid(row = 2) 

def openfilename(): 

	# open file dialog box to select image 
	# The dialogue box has a title "Open" 
	filename = filedialog.askopenfilename(title ='"open') 
	return filename 


# Create a windoe 
root = tk.Tk() 

# Set Title as Image Loader 
root.title("Image Loader") 

# Set the resolution of window 
root.geometry("550x550") 

# Allow Window to be resizable 
root.resizable(width = True, height = True) 

# Create a button and place it into the window using grid layout 
btn = tk.Button(root, text ='open image', command = open_img) 
btn.grid(row = 1, columnspan = 4)
root.mainloop() 


