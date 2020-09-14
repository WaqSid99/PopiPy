"""
This python module is the main driver of the program.
The home screen would include all the buttons necessary for the opertaion
This module is connected with FringeFind which then uses the SurfaceFit. The relation is as follows:
        imgCropCircle --> FringeFind --> SurfaceFit
"""
import sys
import cv2
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import numpy as np
from tkinter import filedialog
from matplotlib import pyplot as plt
import math
from tkinter import messagebox

imglocation=""  #Stores the image location



def select_image():
    """
        select_image()
        Usage: Used as a command function for "Select an image" button (This func executes when button is pressed)
        Gets the user to select the input image and enables all the buttons after dislaying the image

        [In]: None

        [Out]: Displays the selected image on the tkinter canvas and enables all the button for other operations
    """ 
    global Panel
    global imglocation
    try:
        imglocation = filedialog.askopenfilename(title ='Select an Image')
        image = cv2.imread(imglocation)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


        imageDisplay = Image.fromarray(image)   #CV2 IMAGE TO PIL Format image
        imageDisplay = ImageTk.PhotoImage(imageDisplay)
        Panel=tk.Label(image=imageDisplay)
        Panel.image=imageDisplay
        #panel.pack(side="right", padx=2, pady=2)
        #panel.place(anchor="n",height=100,width=100)
        Panel.pack()
        selectImage['state']="disabled"
        show['state']="normal"
        crop['state']="normal"
        backSub['state']="normal"
        closeButton['state']="normal"
        calib['state']="normal"
        findFringe['state']="normal"
    except:
        messagebox.showerror("Error","Image not correct")
        print(sys.exc_info()[0]," occurred")

def close_img():
    """
    close_img()
    Usage: Used as a command function for "Close Image" button
    Removes the current image and disables all buttons

    [In]: None

    [Out]: Close the selected image 

    TODO: 
    This function could further be used to close/remove display item or data variables (Optional)

    """
    text.destroy()
    Panel.destroy()
    selectImage['state']="normal"
    closeButton['state']="disabled"
    calib['state']="disabled"
    crop['state']="disabled"
    show['state']="disabled"
    backSub['state']="disabled"

def calibCalc():
    """
    calibCalc()
    Usage: Used as a command function for "Find Calibration" button
    Finds the calibration size (Microns/pixel) between two selected points on the image. 
    To select a point left click on image. When selected two points, click right mouse button to 
    exit the image frame and calculate the calibration size. 
    By default, it finds the distance between the first two selected points

    [In]: None

    [Out]: Displays the calibration size on the tkinter frame

    TODO: 
    1- Include an input field/messege box asking for Disk Diameter. Here by default it is set at 9.5
    but could change so better to get the value from the user
    2- Maybe a more intuitive way to close the image frame where points are selected can be 
    implemented (Optional)

    """
    #global x    #String address of image
    global image
    global text
    diskDiameter=9.5
    image =cv2.imread(imglocation)
    pts1=[]
    pts2=[]
    #distance=0
    """
    def diskDia():
        top=tk.Toplevel(root)
        label=tk.Label(top,text="Disk Diameter")
        label.pack()
        entry=tk.Entry(top)
        entry.pack()
        def ret_dd():
            global diskDiameter 
            diskDiameter=entry.get()
        btn=tk.Button(top,text="OK",command=ret_dd)
        btn.pack()
    """

    def mouse_click(event,x,y,flags,param):        
        global image
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
            cv2.circle(image,(x,y),1,(255,0,0),3)
            cv2.imshow('image',image)
        if event == cv2.EVENT_RBUTTONDOWN:
            print("Show calibration here")
            #func()
            cv2.destroyAllWindows()

       

    def func():
        distance=0
        
         
        diameterPx=np.linalg.norm(np.subtract(pts1,pts2))
        diameterPx=np.round(diameterPx,decimals=3)
        distance=diskDiameter/diameterPx
        distance=1000*(np.round(distance,decimals=4))
        return distance
        #print(distance) 
        #String="Resolution is : "+str(distance)+' \u03BCm/px'
        #text.destroy()      
        #text=tk.Label(root,text=String)
        #text.pack()

    #diskDia()
    cv2.imshow('image',image)
    cv2.setMouseCallback('image', mouse_click)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    dist=func()

    text.destroy()
    String="Resolution is : "+str(dist)+' \u03BCm/px'
    text.destroy()      
    text=tk.Label(root,text=String)
    text.pack()

def show():
    """ 
    show()
    Usage: Displays the region to be cropped on the display Image

    [In]: None
    [Out]: Display image with area to be cropped

    """ 
    global Panel

    x=int(xcord.get())
    y=int(ycord.get())
    dia=int(diameter.get())

    image = cv2.imread(imglocation)
    cv2.circle(image,(x,y),dia,255,2)
    
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)

    Panel.pack_forget()
    Panel.configure(image=image)
    Panel.image=image
    Panel.pack()

def cropImg(image):
    """
    cropImg()
    Usage: Function to return the cropped image.
    Does so by taking a square surrounding the circle and croping along its boundry

    [In]: image -> Image to be cropped
    [Out]: croppedImage -> Cropped image
    """
    croppedImage=image
    x=int(xcord.get())
    y=int(ycord.get())
    dia=int(diameter.get())
    topleft=(int(x-(dia)),int(y-(dia)))
    bottomright=(int(x+(dia)),int(y+(dia)))

    croppedImage=croppedImage[topleft[1]:bottomright[1],topleft[0]:bottomright[0]]
    return croppedImage

def imageCrop():
    """
        imageCrop()
    Usage: Displays the cropped image

    [In]: None
    [Out]: Shows the cropped image

    """
    image = cv2.imread(imglocation)
    croppedImage=cropImg(image)
    
    cv2.imshow('image',croppedImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def fourierFilter(img):
    """
    fourierFilter()
    Usage: Applies fourier filter to the image for noise reduction.
    Image needs to be filtered since origanl image is very noisey which causes issue with fringe finding
    Source: https://github.com/bnsreenu/python_for_image_processing_APEER/blob/master/tutorial41_image_filters_using_fourier_transform_DFT.py

    [In]: img -> Input Image for noise reduction
    [Out]: img_back -> Image with fourier filter applied 

    TODO: 
    1- Fourier filter is not working as expected and work needs to be done on this. 
    Could look for some other ways to reduce noise if fft doesnt work
    2- It applys a circular mask on the origanl image but could also do with a cross (as done
    in mathematica). The code commented out does apply a cross mask but that doesn't work either

    """

    dft=cv2.dft(np.float32(img),flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift=np.fft.fftshift(dft)
    magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))
   
   
    dia=int(diameter.get())    
    rows, cols = img.shape
    mask = np.zeros((rows, cols, 2), np.uint8)
    r = 100
    x, y = np.ogrid[:rows, :cols]
    mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= r*r
    mask[mask_area] = 1
    """
    np_mask_horizontal=np.array([])
    mask=[]
    
    for i in range(rows):
        for j in range(cols):
            a=np.array([1-math.exp(-(i-cols/2)**2/9)])
            b=np.array([1-math.exp(-(i-cols/2)**2/9)])
            np_mask_horizontal=np.concatenate((a,b))
            mask.append(np_mask_horizontal)
    horizontal_line=np.array([mask])
    horizontal_line=np.reshape(horizontal_line,(dia*2,dia*2,2))

    np_mask_vertical=np.array([])
    mask.clear()
    for i in range (rows):
        for j in range (cols):
            a=np.array([1-math.exp(-(j-cols/2)**2/9)])
            b=np.array([1-math.exp(-(j-cols/2)**2/9)])
            np_mask_vertical=np.concatenate((a,b))
            mask.append(np_mask_vertical)
    vertical_line=np.array([mask])
    vertical_line=np.reshape(vertical_line,(dia*2,dia*2,2))

    fourierfactor3=0.005
    fourierfactor4=0.05
    np_mask=np.array([])
    mask.clear()
    for i in range(rows):
        for j in range(cols):
            a=np.array([1-(1-fourierfactor4)*math.exp(-(math.sqrt(min(j,cols-j)**2 + min(i,rows-i)**2)/(0.5*rows))**2/fourierfactor3**2)])
            b=np.array([1-(1-fourierfactor4)*math.exp(-(math.sqrt(min(j,cols-j)**2 + min(i,rows-i)**2)/(0.5*rows))**2/fourierfactor3**2)])
            np_mask=np.concatenate((a,b))
            mask.append(np_mask)
    additional_filter=np.array([mask])
    additional_filter=np.reshape(additional_filter,(dia*2,dia*2,2))
    #print(additional_filter)
    """
    # apply mask and inverse DFT: Multiply fourier transformed image (values)
    #with the mask values. 
    fshift =  dft_shift* mask
    print(fshift)
    #Get the magnitude spectrum (only for plotting purposes)
    fshift_mask_mag = 20 * np.log(cv2.magnitude(fshift[:, :, 0], fshift[:, :, 1]))

    #Inverse shift to shift origin back to top left.
    f_ishift = np.fft.ifftshift(fshift)

    #Inverse DFT to convert back to image domain from the frequency domain. 
    #Will be complex numbers
    img_back = cv2.idft(f_ishift)

    #Magnitude spectrum of the image domain
    img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

    fig = plt.figure(figsize=(12, 12))
    ax1 = fig.add_subplot(2,2,1)
    ax1.imshow(img, cmap='gray')
    ax1.title.set_text('Input Image')
    ax2 = fig.add_subplot(2,2,2)
    ax2.imshow(magnitude_spectrum, cmap='gray')
    ax2.title.set_text('FFT of image')
    ax3 = fig.add_subplot(2,2,3)
    ax3.imshow(fshift_mask_mag, cmap='gray')
    ax3.title.set_text('FFT + Mask')
    ax4 = fig.add_subplot(2,2,4)
    ax4.imshow(img_back, cmap='gray')
    ax4.title.set_text('After inverse FFT')
    plt.show()

    return img_back

def backgroundSub():
    """
    backgroundSub()
    Usage: Subtracts fringepic,bg1 and bg2. The result of the subtracted image is the passed on
    to fourier filter for noise reduction

    [In]: None
    [Out]: Saves the filtered image as "output.jpg" in the project directory.

    NOTE: Since fourier filter was not working during the time of development,
    I simply cropped the temp image (background sub image) using snipping tool. Could do the same
    to get the work going

    """
    
    bg1=cv2.imread("C:\\Users\\SiddiquW\\Pictures\\5099 polished BG1.jpg",0)
    bg2=cv2.imread("C:\\Users\\SiddiquW\\Pictures\\5099 polished BG2.jpg",0)
    fringepic=cv2.imread("C:\\Users\\SiddiquW\\Pictures\\5099 polished fringes.jpg",0)
    
    bg1=cropImg(bg1)
    bg2=cropImg(bg2)
    fringepic=cropImg(fringepic)

    temp=cv2.subtract(fringepic,bg1)
    temp=cv2.subtract(temp,bg2)

    #plt.imsave("5099 Fourier image.jpg",temp,cmap='gray')  #Saves the background subtracted image (Optional) 
    
    output=fourierFilter(temp)
    output=output-temp.min()
    output=output/temp.max()  ##Resulting temp has range 0-1
    plt.imsave('output.jpg', output, cmap='gray')
    #temp=temp*255   #Scale temp to full range of 255 to get a grayscale image

def Fringe():
    """
    Fringe()
    Usage: Connects this module with Fringe Find module. It takes the output.jpg (or as specified in the path)
    and find fringe on that image

    TODO: Again, this is not working completly and needs further work. To check fringe finding, 
    run the FringeFind.py script separately and it should work fine
    """
    import FringeFind

root=tk.Tk()
Panel=None
root.iconbitmap('0_vW3_icon.ico')
root.geometry("750x750")
root.title("PopiPy")


text=tk.Label(root)

xcord=tk.Entry(root)
xcord.insert(0,350)
ycord=tk.Entry(root)
ycord.insert(0,245)
diameter=tk.Entry(root)
diameter.insert(0,130)

L1=tk.Label(root,text="X Coordinate: ")
L2=tk.Label(root,text="Y Coordinate: ")
L3=tk.Label(root,text="Diameter: ")

L1.pack()
xcord.pack(anchor="s")
L2.pack()
ycord.pack(anchor="s")
L3.pack()
diameter.pack(anchor="s")

selectImage = tk.Button(root, text="Select an image", command=select_image)
#btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
selectImage.place(relx = 0.10, rely = 0.95,anchor="s")

closeButton=tk.Button(master=root,text="Close Image",width=10, command=close_img)
closeButton.place(relx = 0.19, rely = 0.95,anchor="s")
closeButton['state']="disabled"

calib=tk.Button(master=root,text="Find Calibration", width=15,command=calibCalc)
calib.place(relx=0.29, rely=0.95,anchor="s")#
calib['state']="disabled"

show=tk.Button(root, text="Show Crop Region", command=show)
show.place(relx = 0.40, rely = 0.95,anchor="s")
show['state']="disabled"

crop=tk.Button(root, text="Crop", command=imageCrop)
crop.place(relx = 0.55, rely = 0.95,anchor="s")
crop['state']="disabled"

backSub=tk.Button(root, text="Background Subtract", command=backgroundSub)
backSub.place(relx = 0.70, rely = 0.95,anchor="s")
backSub['state']="disabled"

findFringe=tk.Button(root, text="Fringe", command=Fringe)
findFringe.place(relx = 0.90, rely = 0.95,anchor="s")
findFringe['state']="disabled"

root.mainloop()




