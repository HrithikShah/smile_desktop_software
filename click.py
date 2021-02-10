import cv2
import filters
from manager import PygameWindowManager as WindowManager, CaptureManager
import rects
from tracker import facetracker

class click(object):
    
    def __init__(self):
        self._windowmanager=WindowManager('click',self.onkeypress)
        
        self._capturemanager=CaptureManager(cv2.VideoCapture(0),self._windowmanager,True)
        
        self._facetracker=facetracker()
        self._shoulddrawdebugrects=False
        self._curvefilter=filters.bgrportracurvefilter()
        
    def run(self):
        """run the main loop"""
        
        self._windowmanager.createwindow()
        t=0
        while self._windowmanager.iswindowcreated:
            
            
            self._capturemanager.enterframe()
            frame=self._capturemanager.frame
            
            #todo : to track faces and swap in one camera feed
            
            self._facetracker.update(frame)
            faces=self._facetracker.faces
            rects.swaprect(frame,frame,
                           [face.facerect for face in faces])
            
            #todo to add filters
            if t==0:

                filters.strokeedge(frame,frame)
                self._curvefilter.apply(frame,frame)
                t=1
            
            
            
            self._facetracker.drawdebugrects(frame)
                
            
            
            
            
            self._capturemanager.exitframe()
            self._windowmanager.processevents()
            self._windowmanager.show(frame)
            
            
    def onkeypress(self,keycode):
        
        """handle a keypress
            
            space-> take a screenshot
            
            tab-> start/stop recording a screenshot
            
            x-> start/stop drawing debug rectangles around faces
            
            escape-> quit
            """
        if keycode == 32:# space
            self._capturemanager.writeimage('screenshot.png')
            
        elif keycode == 9: #tab
            if not self._capturemanager.iswritingvideo:
                self._capturemanager.startwritingvideo('screenshot.avi',360)
                
            else:
                self._capturemanager.stopwritingvideo()
        elif keycode==120: #x
            self._shoulddrawdebugrects= \
                not self._shoulddrawdebugrects
        
        elif keycode==27: #esc
            self._windowmanager.destroywindow()
            exit()
            
            
class clickdouble(click):
    
    def __init__(self):
        click.__init__(self)
        self._hiddencapturemanager=capturemanager(cv2.VideoCapture(1))
            
    def run(self):
        """run the main loop"""
        
        self._windowmanager.createwindow()
        while self._windowmanager.enterframe():
            
            self._capturemanager.enterframe()
            self._hiddencapturemanager.enterframe()
            
            frame=self._capturemanager.frame
            hiddenframe=self._hiddencapturemanager.frame
            
            
            self._facetracker.update(hiddenframe)
            
            hiddenfaces=self._facetracker.faces
            
            self._facetracker.update(frame)
            faces=self._facetracker.faces
            
            i=0
            while i<len(faces) and i < len(hiddenfaces):
                
                rects.copyrect(hiddenframe,frame,hiddenfaces[i].facerect,
                              faces[i].facerect)
                i+=1
                
                
            filters.strokeedges(frame,frame)
            
            self._curvefilter.apply(frame,frame)
            
            if self._shoulddrawdebugrects:
                self._facetracker.drawdebugrects(frame)
                
            self._capturemanager.exitframe()
            self.hiddencapturemanager.exitframe()
            self._windowmanager.processEvents()
            



class clickdepth(click):


    def __init__(self):
        self._windowmanager=WindowManager('click',self.onkeypress)
        #device=depth.CV_CAP_OPENNI  #UNCOMMENT THIS with microsoft kinect
        #device=depth.CV_CAP_OPENNI_ASUS  #UNCOMMENT FOR ASUS XTION

        self._capturemanager=CaptureManager(cv2.VideoCapture(device),
                                            self._windowmanager,True)
        self._facetracker=facetracker()
        self._shoulddrawdebugrects=True
        self._curvefilter=filters.bgrportracurvefilter()
    
    def run(self):
        """run the main loop"""

        self._windowmanager.createwindow()
        while self._windowmanager.iswindowcreated():
            self._capturemanager.enterframe()
            self._capturemanager.channel=\
                depth.CV_CAP_OPENNI_DISPARITY_MAP
            disparitymap=self._capturemanager.frame
            self._capturemanager.channel=\
                depth.CV_CAP_OPENNI_VALID_DEPTH_MASK
            validdepthmask=self._capturemanager.frame
            self._capturemanager.channel=\
                depth.CV_CAP_OPENNI_BGR_IMAGE
            frame=self._capturemanager.frame

            self._facetracker.update(frame)
            faces=self._facetracker.faces

            masks=[
                depth.createmedianmask(
                    disparitymap.validdepthmask,face.facerect)\
                for face in faces

            ]

            rects.swaprect(frame,frame,[face.facerect for face in faces],masks)


            filters.strokeedge(frame,frame)
            self._curvefilter.apply(frame,frame)

            if self._shoulddrawdebugrects:
                self._facetracker.drawdebugrects(frame)

            self._capturemanager.exitframe()
            self._windowmanager.processevents()

if __name__=="__main__":
    click().run()#uncomment for single camera
    #clickdouble().run()
    #clickdepth().run()#uncomment with depth camera

    
        
    
