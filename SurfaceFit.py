import numpy as np
from scipy.interpolate import griddata
import plotly.graph_objects as go
from scipy.optimize import minimize
from FringeFind import ret_surfaceData
"""
f = "C:\\Users\\SiddiquW\\Desktop\\surface data in mm.txt"  #Replaced by surafce data obtained in FringeFind
def readline(filename,skiplines=0):
    with open(filename) as ff:
        for _ in range(skiplines):
            ff.readline()
        return ff.readline()

#d = np.fromstring(readline(f,12).replace('[','').replace(']',''),sep=',')
#d = d.reshape(-1,3)
"""
d=ret_surfaceData() #Using this function to directly read surface data value from FringeFind.py instead of reading from file

#Center X and Y coordinates
d[:,0] -= (d[:,0].max()-d[:,0].min())/2
d[:,1] -= (d[:,1].max()-d[:,1].min())/2

#Remove Plane
def removeplane(d):
    """ Remove plane from data"""
    X1 = d[:,0]
    X2 = d[:,1]
    XX = np.hstack([np.ones((len(X1)))[:,np.newaxis],X1[:,np.newaxis],X2[:,np.newaxis]])
    Y = d[:,2]
    theta = np.dot(np.dot(np.linalg.pinv(np.dot(XX.transpose(), XX)), XX.transpose()), Y)
    plane = np.dot(XX, theta)
    out = d.copy()
    out[:,2] -= plane
    return out

#Surface Visualization
def diskmesh(d,N=2**7):
    """Take point cloud and return meshgrids for plotting"""
    X = np.linspace(d[:,0].min(),d[:,0].max(),N)
    Y = np.linspace(d[:,1].min(),d[:,1].max(),N)
    XI,YI = np.meshgrid(X,Y)
    ZI = griddata(d[:,:2],d[:,2],(XI,YI),method='cubic')
    return XI,YI,ZI

dflat = removeplane(d)
XI, YI, ZI = diskmesh(dflat)
#fig = go.Figure(data=[go.Surface(x=XI,y=YI,z=ZI)])
#fig.update_layout(title='Disk Surface - plane removed', height=800)
#fig.show()

#Remove Ellipsoid
def model(x,data,remove=False):
    """ 
    Fits ellipsoid to point cloud
    
    o: offset
    t: ellipsoid angle w.r.t. x
    a,b: Axes of ellipsoid
    x0, y0: ellipsoid center point
    """
    d = np.array(data)
    o, t, a, b, x0, y0 = x
    ellipsoid = o+a*(1-np.sqrt(1-((d[:,0]-x0)*np.cos(t)-(d[:,1]-y0)*np.sin(t))**2/a**2)) + b*(1-np.sqrt(1-((d[:,0]-x0)*np.cos(t)+(d[:,1]-y0)*np.sin(t))**2/b**2))
    if not remove:
        #L2 residuals for fitting
        return sum((ellipsoid-d[:,2])**2)
    else:
        #remove ellipsoid from surface data
        return d[:,2]-ellipsoid

#Set boundaries for fit parameters
bounds = [
    [-2,2],
    [0,np.pi/4],
    [1000,None],
    [1000,None],
    [-4,4],
    [-4,4]
]

#Estimate center point for ellipsoid
X0, Y0 = d[np.argmin(dflat[:,2]),:2]

#estimate ROC
y = dflat[:,2].max()-dflat[:,2].min()
xmax = d[:,0].max()
a,b = [(xmax**2+y**2)/2/y]*2

#estimate ROC
o = dflat[:,2].min()
res = minimize(model,[o,0,a,b,X0,Y0],bounds=bounds,method='Powell',args=(dflat,))

dwave = dflat.copy()
dwave[:,2] = model(res.x,dflat,remove=True)
#Analysis
_, angle, a, b, _, _ = res.x
angle = angle*360/2/np.pi
rms = np.sqrt(np.sum(dwave[:,2]**2)/dwave.shape[0])*1e6
print(f'Angle = {angle:.1f} deg, ROC_A = {a*1e-3:.2f} m, ROC_B = {b*1e-3:.2f} m, RMS={rms:.2f} nm')

#plot
XI, YI, ZI = diskmesh(dwave)
fig = go.Figure(data=[go.Surface(x=XI,y=YI,z=ZI)])
fig.update_layout(title=f'Disk Surface - Plane and Ellipsoid removed', height=800)
fig.show()

