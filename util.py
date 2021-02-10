import cv2
import numpy as np
import scipy.interpolate




def createcurvefunc(points):
    """return a function dervied from control points"""
    
    if points is None:
        return None
    numpoints=len(points)
    
    if numpoints <2:
        return None
    
    xs,ys=zip(*points)
    if numpoints<3:
        kind="linear"
        
    else:
        kind="cubic"
        
    return scipy.interpolate.interp1d(xs,ys,kind,bounds_error=False)


def createlookuparray(func,length=256):
    
    """return a lookup for whole-number input to a function
    the look up array value are clamped to [0,length-1]
    
    """
    if func is None:
        return None
    
    lookuparray=np.empty(length)
    
    i=0
    while i<length:
        func_i=func(i)
        lookuparray[i]=min(max(0,func_i),length-1)
        i+=1
    return lookuparray


def applylookuparray(lookuparray,src,dst):
    """map a source to a destination using a lookup"""
    
    if lookuparray is None:
        return 
    dst[:]=lookuparray[src]
    
    
def createcompositefunc(func0,func1):
    """return a composition of two function"""
    
    if func0 is None:
        return func1
    if func1 is None:
        return func0
    return lambda x:func0(func1(x))


def createflatview(array):
    """return a 1d view of any array of any dimensionality"""
    
    flatview=array.view()
    flatview.shape=array.size
    return flatview

def isgray(image):
    """return true if image is color """
    h,w,c=image.shape

    return c < 3

def widthheightdividedby(image,divisor):
    """return an image dimension,divided by a value."""
    
    h,w=image.shape[:2]
    return (int(w/divisor),int(h/divisor))

