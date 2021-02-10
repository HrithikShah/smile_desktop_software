import numpy as np

# Devices. 
CV_CAP_OPENNI = 900 # OpenNI (for Microsoft Kinect) 
CV_CAP_OPENNI_ASUS = 910 # OpenNI (for Asus Xtion) 
# Channels of an OpenNI-compatible depth generator. 
CV_CAP_OPENNI_DEPTH_MAP = 0 # Depth values in mm (CV_16UC1) 
CV_CAP_OPENNI_POINT_CLOUD_MAP = 3 # XYZ in meters (CV_32FC3) 
CV_CAP_OPENNI_DISPARITY_MAP = 2 # Disparity in pixels (CV_8UC1) 
CV_CAP_OPENNI_DISPARITY_MAP_32F = 3 # Disparity in pixels (CV_32FC1) 
CV_CAP_OPENNI_VALID_DEPTH_MASK = 4 # CV_8UC1 
# Channels of an OpenNI-compatible RGB image generator. 
CV_CAP_OPENNI_BGR_IMAGE = 5 
CV_CAP_OPENNI_GRAY_IMAGE = 6 

"""
import cv2
    
cap=cv2.VideoCapture(0)

while (True):
    
    reg,frame=cap.read()
    
    gray=cv2.cvtColor(frame,cv2.CV_32FC1)
    
    cv2.imshow('point cloud map',gray)
    
    if cv2.waitKey(20) & 0xff==ord('q'):
        break
        
cap.release()
cv2.destroyWindow('point cloud map')

"""

import numpy as np


def createmedianmask(disparitymap,validdepthmask,rect=None):
    """return a mask selecting the median layer,plus shadows."""
    
    if rect is not None:
        x,y,w,h=rect
        disparitymap=disparitymap[y:y+h,x:x+w]
        
        validdepthmask=validdepthmask[y:y+h,x:x+w]
        
    median=np.median(disparitymap)
    return np.where((validdepthmask==0)|\
        (abs(disparitymap-median)<12),1.0,0.0)


