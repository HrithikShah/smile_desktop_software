import cv2
import rects
import util


class face(object):
    """
    data on facial features"""
    def __init__(self):
        self.facerect=None
        self.rigtheyerect=None
        self.lefteyerect=None
        self.noserect=None
        self.mouthrect=None
        
class facetracker(object):
    """a tracker for facial features:face,eyes,nose,mouth"""
    
    def __init__(self,
                 scaleFactor=1.2,
                 minNeighbors=2,
                flags=cv2.CASCADE_SCALE_IMAGE):
        
        
        self.scalefactor=scaleFactor
        self.minneighbors=minNeighbors
        self.flags=flags
        
        self._faces=[]
        
        self._faceclassifier=cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
        #self._eyeclassifier=cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
        #self._noseclassifier=cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
        #self._mouthclassifier=cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
        
        
        
    
    @property
    def faces(self):
        """the tracked facial features"""
        return self._faces
    
    
    def update(self,image):
        """update the tracked facial features"""
        
        self._faces=[]
        
        if util.isgray(image):
            image=cv2.equalizeHist(image)
            
        else:
            
            image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            cv2.equalizeHist(image,image)
            
        minsize=util.widthheightdividedby(image,8)

        

        
        facerect=self._faceclassifier.detectMultiScale(image,
                                                        self.scalefactor,
                                                        self.minneighbors,
                                                        self.flags,
                                                        minsize)
        
        """if facerects is not None:
            
            for facerect in facerects:
                face=face()
                
                face.facerect=facerect
                
                
                x,y,w,h=facerect
                
                # Seek an eye in the upper-left part of the face.                
                searchRect = (x+w/7, y, w*2/7, h/2)                
                face.leftEyeRect = self._detectOneObject(                    
                    self._eyeClassifier, image, searchRect, 64)                                
                
                
                
                # Seek an eye in the upper-right part of the face.                
                searchRect = (x+w*4/7, y, w*2/7, h/2)                
                face.rightEyeRect = self._detectOneObject(                    
                    self._eyeClassifier, image, searchRect, 64)                                
                
                
                
                # Seek a nose in the middle part of the face.                
                searchRect = (x+w/4, y+h/4, w/2, h/2)                
                face.noseRect = self._detectOneObject(                    
                    self._noseClassifier, image, searchRect, 32)                                
               
                # Seek a mouth in the lower-middle part of the face.                
                searchRect = (x+w/6, y+h*2/3, w*2/3, h/3)                
                face.mouthRect = self._detectOneObject(                    
                    self._mouthClassifier, image, searchRect, 16)                                
                
                
                
                self._faces.append(face)

        
        
        def _detectoneobject(self,
                             classifier,
                             image,
                             rect,
                             imagesizetominsizeratio):
            
            x ,y ,w ,h=rect
            
            minsize=util.widthheightdividedby(image,
                                               imagesizetominsizeratio)
            
            subimage=image[y:y+h,x:x+w]
            
            subrect=classifier.dectectMultiScale(subimage,
                                                self.scalefactor,
                                                self.minneighbors,
                                                self.flags,
                                                minsize)
            
            if len(subrect)==0:
                return None
            
            subx,suby,subw,subh=subrects[0]
            
            return (x+subx,y+suby,w+subw,h+subh)
        
        """
    def drawdebugrects(self,image):
            
            """draw rectangle around the tracked facial features."""
            
            if util.isgray(image):
                faceColor = 255            
                """leftEyeColor = 255            
                rightEyeColor = 255            
                noseColor = 255           
                mouthColor = 25"""
                
            else:
                faceColor = (255,0,0) # white            
                """leftEyeColor = (0, 0, 255) # red           
                rightEyeColor = (0, 255, 255) # yellow            
                noseColor = (0, 255, 0) # green            
                mouthColor = (255, 0, 0) # blue """    
                
                
            for face in self.faces:
                
                rects.outlinerect(image,face.facerect,facecolor)
                #rects.outlineRect(image, face.leftEyeRect, leftEyeColor)            
                #rects.outlineRect(image, face.rightEyeRect,rightEyeColor)            
                #rects.outlineRect(image, face.noseRect, noseColor)            
                #rects.outlineRect(image, face.mouthRect, mouthColor)
