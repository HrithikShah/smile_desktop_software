import cv2
import util 
import numpy as np

def outlinerect(image,rect,color):
    if rect in None:
        return
    x,y,w,h=rect
    cv2.rectangle(image,(x,y),(x+w,y+h),color)
    
    

    
def copyrect(src,dst,srcrect,dstrect,mask=None,
             interpolation=cv2.INTER_LINEAR):
    """COPY part of the source part of the destination."""
    
    x0,y0,w0,h0=srcrect
    x1,y1,w1,h1=dstrect
    
    #resize the contents of the source sub-rectangle.
    #put the results in destination sub-rectangle.
    

    if mask is not None:
        dst[y1:y1+h1,x1:x1+w1]= \
            cv2.resize(src[y0:y0+h0,x0:x0+w0],(w1,h1),interpolation=interpolation)
    
    else:
        if not util.isgray(src):
            #convert the mask to 3 channel likethe image
            mask=mask.repeat(3).reshape(h0,w0,3)

        #perform the copy with the mask applied
        dst[y1:y1+h1, x1:x1+w1] = \
            np.where(cv2.resize(mask, (w1, h1),
                                interpolation = \
                                cv2.INTER_NEAREST),
                    cv2.resize(src[y0:y0+h0, x0:x0+w0], (w1, h1),
                               interpolation = interpolation),
                    dst[y1:y1+h1, x1:x1+w1])

def swaprect(src,dst,rects,mask=None,interpolation=cv2.INTER_LINEAR):
    
    """COPY THE SOURCE WITH TWO OR MORE SUB RECTANGLE SWAPPED"""
    
    if dst is not src:
        dst[:]=src
    
    numrects=len(rects)
    
    if numrects<2:
        return
        #copy the contents of last rectangle into temporay storage
    

    if mask is None:
        mask=[None]*numrects
    
    
    #copy the contents of last rectangle into temporay storage   
    x,y,w,h=rects[numrects-1]
    temp=src[y:y+h,x:x+w].copy()
        
    #copy the content of each rectangle into the next
        
    i=numrects-2
        
    while i>=0:

        copyrect(src,dst,rects[i+1],mask[i],interpolation)
        i-=1
            
    #copy the temporarily stored content into the first rectangle
        
    copyrect(temp,
             dst,
             (0,0,w,h),
             rect[0],
             mask[numrects-1],
             interpolation)
    
    
    
