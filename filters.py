import cv2
import numpy as np
import util as ut




class vfuncfilter(object):
    
    """a filter  that applies a function to V(or all of bgr)"""
    
    def __init__(self,vfunc=None,dtype=np.uint8):
        length=np.iinfo(dtype).max+1
        self._vlookuparray=ut.createlookuparray(vfunc,length)
        
    
    def apply(self,src,dst):
        """apply the filter with a bgr or gray source/destination"""
        
        srcflatview=ut.flatview(src)
        dstflatview=ut.flatview(dst)
        ut.applylookuparray(self._vlookuparray,srcflatview,dstflatview)
        
        


        
class vcurvefilter(vfuncfilter):
    
    
    
    """a filter which apply a curve to v(all bgr)"""
    
    def __init__(self,vpoints,dtype=np.uint8):
        
        vfuncfilter.__init__(self,ut.createcurvefunc(vpoints),dtype)
        
        
    
    

    
class bgrfuncfilter(object):
    """a filter that applies different function to each of bgr."""
    
    def __init__(self,vfunc=None,bfunc=None,gfunc=None,rfunc=None,dtype=np.uint8):
        
        length=np.iinfo(dtype).max+1
        
        self._blookuparray=ut.createlookuparray(
            ut.createcompositefunc(bfunc,vfunc),length)
        self._glookuparray=ut.createlookuparray(
            ut.createcompositefunc(gfunc,vfunc),length)
        self._rlookuparray=ut.createlookuparray(
            ut.createcompositefunc(rfunc,vfunc),length)
        
    
    
    def apply(self,src,dst):
        """apply the filters with a bgr source/destination"""
        
        b,g,r=cv2.split(src)
        
        ut.applylookuparray(self._blookuparray,b,b)
        
        ut.applylookuparray(self._blookuparray,b,b)
        
        ut.applylookuparray(self._blookuparray,b,b)
        
        cv2.merge([b,g,r],dst)
        
        
        
        
class bgrcurvefilter(bgrfuncfilter):
    """a filter that applies different curves to each of bgr"""
    
    def __init__(self,
                 vpoints=None,
                 bpoints=None,
                 gpoints=None,
                 rpoints=None,
                 dtype=np.uint8
                ):
        
        bgrfuncfilter.__init__(self,
                              ut.createcurvefunc(vpoints),
                              ut.createcurvefunc(bpoints),
                              ut.createcurvefunc(gpoints),
                              ut.createcurvefunc(rpoints),
                               dtype
                              )
            
            
            
class bgrportracurvefilter(bgrcurvefilter):   
    """A filter that applies Portra-like curves to bgr."""        
    
    def __init__(self, dtype = np.uint8):        
        
        bgrcurvefilter.__init__(self,           
                                vpoints = [(0,0),(23,20),(157,173),(255,255)],
                                bpoints = [(0,0),(41,46),(231,228),(255,255)],
                                gpoints = [(0,0),(52,47),(189,196),(255,255)],
                                rpoints = [(0,0),(69,69),(213,218),(255,255)],
                                dtype = dtype) 
        
        
        
class bgrproviacurvefilter(bgrcurvefilter):    
    """A filter that applies Provia-like curves to bgr."""
    def __init__(self, dtype = np.uint8):        
        
        bgrcurvefilter.__init__(self,            
                                bpoints = [(0,0),(35,25),(205,227),(255,255)],
                                gpoints = [(0,0),(27,21),(196,207),(255,255)],
                                rpoints = [(0,0),(59,54),(202,210),(255,255)],
                                dtype = dtype)
        
        
        
class bgrVelviaCurveFilter(bgrcurvefilter):
    """A filter that applies Velvia-like curves to bgr."""
    
    def __init__(self, dtype = np.uint8):        
        
        bgrcurvefilter.__init__(            self,
                                vpoints = [(0,0),(128,118),(221,215),(255,255)],
                                bpoints = [(0,0),(25,21),(122,153),(165,206),(255,255)],
                                gpoints = [(0,0),(25,21),(95,102),(181,208),(255,255)],
                                rpoints = [(0,0),(41,28),(183,209),(255,255)],
                                dtype = dtype)        
        
        
class bgrCrossProcessCurveFilter(bgrcurvefilter):
    """A filter that applies cross-process-like curves to bgr."""
    
    def __init__(self, dtype = np.uint8):        
        
        bgrcurvefilter.__init__(            self,
                                bpoints = [(0,20),(255,235)],
                                gpoints = [(0,0),(56,39),(208,226),(255,255)],
                                rpoints = [(0,0),(56,22),(211,255),(255,255)],
                                dtype = dtype)
        


        
        
def strokeedge(src,dst,blurksize=7,edgeksize=5):
    
    if blurksize>=3:
        
        blursrc=cv2.medianBlur(src,blurksize)
        graysrc=cv2.cvtColor(blursrc,cv2.COLOR_BGR2GRAY)
    
    else:
        
        graysrc=cv2.cvtColor(src,cv2.COLOR_bgr2GRAY)
        
    cv2.Laplacian(graysrc,cv2.CV_8U,graysrc,ksize=edgeksize)
    
    normalizedinversealpha=(1.0/255)*(255-graysrc)
    channels=cv2.split(src)
    for channel in channels:
        
        channel[:]=channel*normalizedinversealpha
        
    cv2.merge(channels,dst)

    
    
class vconvolutionfilter(object):
    """a filter that applies a convolution to v(or all of bgr)
    
    """
    
    def __init__(self,kernel):
        
        self._kernel=kernel
        
    def apply(self,src,dst):
        
        """apply the filter with a bgr or gray source/destination"""
        
        cv2.filter2D(src,-1,self.kernel,dst)
        
        
class sharpenfilter(vconvolutionfilter):
    """a sharpen filter with a 1-pixel radius"""
    
    def __init__(self):
        
        kernel=np.array([[-1, -1, -1],
                         [-1,  9, -1],
                         [-1, -1, -1]])
        vconvolutionfilter.__init__(self,kernel)
        
        
        

        
class findedgefilter(vconvolutionfilter):
    
    """
    an edge finding filter with a pixel radius"""
    
    def __init__(self):
        
        kernel=np.array([[-1 , -1,  -1],
                          [-1  ,8   -1],
                          [-1 ,-1,  -1]])
        
        vconvolutionfilter.__init__(self.kernel)
        
        
        
class blurfilter(vconvolutionfilter):
    
    """a blur filter with a 2 pixel radius"""
        
    def __init__(self):
            kernel= np.array([[0.04, 0.04, 0.04, 0.04, 0.04],
                                 [0.04, 0.04, 0.04, 0.04, 0.04],
                                 [0.04, 0.04, 0.04, 0.04, 0.04],
                                 [0.04, 0.04, 0.04, 0.04, 0.04],
                                 [0.04, 0.04, 0.04, 0.04, 0.04]])
            
            vconvolutionfilter.__init__(self,kernel)
            

            
            
class embossfilter(vconvolutionfilter):
    
    """an emboss filter with a 1 pixel radius"""
    
    def __init__(self):
        kernel=np.array([[-2, -1, 0],
                         [-1,  1, 1],
                         [ 0,  1, 2]]) 
        
        
        vconvolutionfilter.__init__(self,kernel)
