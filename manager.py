import cv2
import numpy as np
import time
import pygame
import util


class CaptureManager(object):
    
    
    
    def __init__(self,capture,previewWindowManager=None,
                 shouldMirrorPreview=False):
       
        self.previewWindowManager=previewWindowManager
        self.shouldMirrorPreview=shouldMirrorPreview
        
        self._capture=capture
        self._channel=0;
        self._enteredframe=False
        self._frame=None
        
        self._imagefilename=None
        self._videofilename=None
        self._videoencoding=0
        self._videowriter=None
        
        self._starttime=None
        self._frameselapsed=0
        self._fpsestimate=None
        
    @property   
    def channel(self):
        return self._channel
    
    
    
    @channel.setter
    def channel(self,value):
        if self._channel != value:
            self._channel=value
            self._frame=None
            
    @property
    def frame(self):
        if self._enteredframe and self._frame is None:
            _,self._frame=self._capture.retrieve()
        
        return self._frame
    
    @property
    def isWritingImage(self):
        return self._imagefilename is not None
    
    @property
    def isWritingVideo(self):
        return self._videofilename is not None
    
    
    def enterframe(self):
        #capture the next frame if any
        
        #but check if there if any other frame
        
        
        if self._capture is not None:
            self._enteredframe=self._capture.grab()
    
    
    
    def exitframe(self):
        
        #to check whether any grabbed frame is retrievable.
        if self.frame is not None:
            self._enteredframe=False
            return
        
        #update the fps estimate and related variables
        
        if self._frameselasped == 0:
            self._starttime=time.time()
        
        else:
            timeelasped=time.time()-self._starttime
            self._fpsestimate=self._frameselapsed/timeelasped
            
        self._frameselapsed+=1
        
        
        
        
        #draw a window ,if any.
        
        
        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                
                mirroredframe=np.fliplr(self._frame).copy()
                self.previewWindowManager.show(self.frame)
                
                
        #write image file if any is present
        
        if self.iswritingimage:
            cv2.imwriter(self.imagefilename,self.frame)
            self._imagefilename=None
            
        #write  to the video file
        
        self.writevideoframe()
        
        
        
        #release the frame
        
        self._frame=None
        self._enteredframe=False
        
                
    def writeimage(self,filename):
        """writing next exited frame to an image file"""
        
        self.imagefilename=filename
        
        cv2.imwrite(self.imagefilename,self._frame)
        
    
    def startwritingvideo(self,filename,encoding=360):
        
        """start writing exited filename to video filename"""
        
        self._videofilename=filename
        self._videoencoding=encoding
        
        
    def stopwritingvideo(self):
        """stop writing exited frame to a video file."""
        
        self._videofilename=None
        self._videoencoding=None
        self._videowriter=None
        
        
    def writevideoframe(self):
          
        if not self.iswritingvideo:
            return
        
        if self._videowriter is None:
            
            fps=self._capture.get(cv2.cv.CV_CAP_PROP_FPS)
            
            if fps==0.0:
                #the capture's fps is unknown so use an estimate.
                if self._frameselapsed < 20:
                    """wait until more frame elapsed so that the estimate is more stable"""
                    return
                else:
                    fps=self._fpsestimate
            
            size=(int(self._capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
                 int(self._capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
            
            self._videowriter=cv2.VideoWriter(self._videofilename,self._videoencoding ,fps,size)
        
                  
                  
        self._videowriter.write(self._frame)      
    
                  
                  
                  

                
                
                  
class WindowManager(object):
    
                  
    
                  
    def __init__(self,windowname,keypresscallback=None):
        self.keypresscallback=keypresscallback
        self._windowname=windowname
        self._iswindowcreated=False
                  
            
                  
            
    def iswindowcreated(self):
                  
        return self._iswindowcreated
                  
    def createwindow(self):
        cv2.namedWindow(self._windowname)
        self._iswindowcreated=True
                  
            
    def show(self,frame):
        cv2.imshow(self._windowname,frame)
                  
    def destroywindow(self):
        cv2.destroyWindow(self._windowname)
        self._iswindowcreated=False
                  
    def processevents(self):
        keycode=cv2.waitKey(1)
                 
        if self.keypresscallback is not None and keycode != -1:
                  
                  keycode&= 0xFF
                  self.keypresscallback(keycode)




class PygameWindowManager(WindowManager):


    def createwindow(self):
        pygame.display.init()
        pygame.display.set_caption(self._windowname)

        self._iswindowcreated=True

    def show(self,frame):

        #find the frame dimensions
        framesize=frame.shape[1::-1]
        #convert the frame to RGB Which pygame requries
        if  util.isgray(frame):
            conversiontype=cv2.COLOR_GRAY2RGB
        else:
            conversiontype=cv2.COLOR_BGR2RGB

        rgbframe=cv2.cvtColor(frame,conversiontype)

        #convert the frame to pygame surface type
        pygameframe=pygame.image.frombuffer(rgbframe.tostring(),framesize,'RGB')
        #RESIZE THE WINDOW TO MATCH THE FRAME

        displaysurface=pygame.display.set_mode(framesize)

        #bllit and display the frame

        displaysurface.blit(pygameframe,(0,0))
        pygame.display.flip()

    def destroywindow(self):
        pygame.display.quit()
        self._iswindowcreated=False

    def processevents(self):
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN and self.keypresscallback is not None:
                self.keypresscallback(event.key)

            elif event.type==pygame.QUIT:
                self.destroywindow()
                return

            
                  
                  

    
    
    
    
    
    
    
    
