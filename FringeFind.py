import cv2
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
import numpy as np
import math
#from tempfile import TemporaryFile

img=cv2.imread("C:\\Users\\SiddiquW\\hello\\output.jpg") #Change location as per image address
img= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


fringepiccropwidth=img.shape[1]  #Gets rows of img
fringepiccropheight=img.shape[0] #Get coloums of img 
oversample=1
sampledistance=0.25
samplecount=1
xstart=-1
gaussianfilterwidth=12

fringepoints=[]                             #Array which stores the points of all the array 


print("Start.....")

y=0
#Lo
while y in range (fringepiccropheight):                   
    fringesline=[]                          #This array is for one perticular row 
    tmpfringepoints=[]
    for x in range (fringepiccropheight):   #value which moves in a row=640
        tmp=0
        if(y==0 or y==fringepiccropheight-1):
            xpos=x
            ypos=y
            tmp=tmp+img[ypos][xpos]
            fringesline.append(tmp)
        elif(y==1 or y==fringepiccropheight-2):
            for j in range (y-1,y+1):        ## in range y-1 y y+1
                xpos=x
                ypos=j
                tmp=tmp+img[ypos][xpos]
            fringesline.append(tmp/3)    
        else:
            for j in range (y-2,y+3):        ## y-2 y-1 y y+1 y+2
                xpos=x
                ypos=j
                tmp=tmp+img[ypos][xpos]
            fringesline.append(tmp/5)
    #print(fringesline)
    ##---Gausian filter--##
    normalised=[]
    g_array=gaussian_filter1d(fringesline,gaussianfilterwidth)
    normalised=fringesline-g_array
    
    ##--Find Zero Crossings and store in array--#  
    zeroCross=[]
    counter=-1
  
    for x in normalised:
        if(counter!=len(normalised)-2):
            counter+=1
            if (normalised[counter] > 0) != (normalised[counter+1] > 0):
                zeroCross.append(counter) 
        
   
    ##--Itterte through array, pick two points, check if centre value is +/-, --#
    ##--If +, extract all points btwn those two points else if -ve, do notthing and go to next point --#
     
    x_poly=[]
    y_poly=[]
    for i in range(len(zeroCross)-1):
        if(i%2==0):
            x_poly.clear()
            y_poly.clear()
            a=zeroCross[i]
            b=zeroCross[i+1]

            for x in range (a-2,b+2):
                x_poly.append(x)
                y_poly.append(normalised[x])
        
            coefficients = np.polyfit(x_poly, y_poly, 2)
            poly = np.poly1d(coefficients)

            highPoint=(poly[1]/(2*poly[2]))*-1
            tmpfringepoints.append(highPoint)            
    fringepoints.append(tmpfringepoints)
    #Index 0 of fringepoint represent row 1 of image and so on..
    #i.e format of fringepoints is [[all points of row1],[all points of row2],[all points of row3],....] 
    ##--Fit poly onto extracted points and find peak--#
    ##--Store peak location into fringepoints--#
    
    y+=1
    

x_lis=[]
for i in range (len(fringepoints)):
    x_lis.append(i)

fig=plt.figure(figsize=(15,10))
ax = fig.add_subplot(111)
for direction in ["left","bottom"]:
    ax.spines[direction].set_position('zero')
    #ax.spines[direction].set_smart_bounds(True)
for direction in ["right","top"]:
    ax.spines[direction].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.grid(False)

#plt.plot(normalised)
#ax.scatter(fringepoints,x_lis,color='r') ##--> Plots all the fringes found
#plt.show()


image=cv2.imread("C:\\Users\\SiddiquW\\hello\\output.jpg") #Change location as per image address


for coord in fringepoints:
    y=fringepoints.index(coord)
    for i in coord:
        try:   #Try-except to avoid overflow 
            i=int(i)
            cv2.circle(image, (i, y), 1, 255, -100)  #Sometimes trows OverflowError: Python int too large to convert to C long
                                                 #If shows error, Crop Image again with different crop inputs
        except:
            continue

size=0
maxfringe=[]
for points in fringepoints:
    if(len(points)>size):
        maxfringe.clear()
        size=len(points)
        maxfringe=points

maxfringe=fringepoints[fringepoints.index(maxfringe)+5]   ## +5 is not necessary, can be used if maxfringe is a bit off  
for pnt in maxfringe:
    cv2.circle(image, (int(pnt), fringepoints.index(maxfringe)), 1, [0,255,0], -10)


#plt.imshow(image)
#plt.show()

image1=cv2.imread("C:\\Users\\SiddiquW\\hello\\output.jpg")   #Change location as per image address


def calc_index(point):
    for xyz in fringepoints:
        #print(xyz)
        if(point in xyz):
            return fringepoints.index(xyz)


searchdistance=5
calibrationSize=0.02617 
fringes=[]  #Surface Data array
#Main loop which connects fringes
for points in maxfringe:
    print("point found",str(points))
    counter=maxfringe.index(points)
    startpoint=points
    finding_point=True
    close_point=0
    close_point_row=0
    maxfringe_index=fringepoints.index(maxfringe)
    fringes.append([startpoint*calibrationSize,maxfringe_index*calibrationSize,(counter+1)*0.000532])
    tmpPoints=[]
    
    #Search top half of image   
    while(finding_point==True):
        shortestdistance=100
        row=calc_index(startpoint)
        tmpPoints.clear()
        for i in range (row-searchdistance,row):
            for j in fringepoints[i]:
                if(i<0):
                    break
                if( (j>=(startpoint-3.0) and j<=(startpoint+3.0)) and j!=startpoint ):
                    tmpPoints.append(j)
                    distance=math.sqrt((j-startpoint)**2 + (i-row)**2)
                    if(distance<shortestdistance):
                        shortestdistance=distance
                        close_point=j
                        close_point_row=i
                elif( ((i==row-1) and (j==fringepoints[i][-1])) and len(tmpPoints)==0):
                    finding_point=False
      
        
        if(len(tmpPoints)!=0):
            startpoint=close_point
            fringes.append([close_point*calibrationSize,close_point_row*calibrationSize,(counter+1)*0.000532])

            if(maxfringe.index(points)%2==0):
                cv2.circle(image1, (int(startpoint),i), 1, [145,145,0], -1)
            else:
                cv2.circle(image1, (int(startpoint),i), 1, [200,100,0], -1)
        else:
            finding_point=False

    #Search bottom half of image 
    startpoint=points
    finding_point=True
    tmpPoints.clear()
    while(finding_point==True):
        shortestdistance=100   
        row=calc_index(startpoint)
        if(row>=fringepiccropheight-searchdistance):
            finding_point=False
            break
        tmpPoints.clear()
        for i in range (row+1,row+(searchdistance+1)):
            if(i>=len(fringepoints)):
                print("done")
                finding_point=False
                break
            for j in fringepoints[i]:
                if ( (j>=(startpoint-3.0) and j<=(startpoint+3.0)) and j!=startpoint):
                    tmpPoints.append(j)
                    distance=math.sqrt((j-startpoint)**2 + (i-row)**2)
                    if(distance<shortestdistance):
                        shortestdistance=distance
                        close_point=j
                        close_point_row=i
                elif((i==row+searchdistance) and (j==fringepoints[i][-1]) and len(tmpPoints)==0):
                    finding_point=False
                    
               
        if(len(tmpPoints)!=0):
            startpoint=close_point
            fringes.append([close_point*calibrationSize,close_point_row*calibrationSize,(counter+1)*0.000532])
            
            if(maxfringe.index(points)%2==0):
                cv2.circle(image1, (int(startpoint),i), 1, [0,255,0], -10)
            else:
                cv2.circle(image1, (int(startpoint),i), 1, [255,0,0], -10)


#print(fringes)
#plt.imshow(image1)  # Displays the image with connected fringes
#plt.show()

"""
NOTE: SurafceFit will need to be run separately as it is not connected with this module yet.  
"""
def ret_surfaceData():
    surface_data=np.array(fringes)
    surface_data=surface_data.reshape(-1,3)
    return surface_data

#outfile = "C:\\Users\\SiddiquW\\hello\\surface_data"
#np.savez(outfile,fringes)