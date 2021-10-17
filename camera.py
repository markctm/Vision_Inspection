
import os
import cv2
import numpy as np
import datetime
import time 
from threading import Thread

from picamera.array import PiRGBArray
from picamera import PiCamera



class Camera():
    
    '''
        Classe Camera -> Configuracao de recursos da camera          
    '''
       
    def __init__(self,WIDTH,HEIGHT,dispositivo=1,camera_type='WEBCAM'):
        
        self.__dispositivo=dispositivo
        self.__camera_type=camera_type
        
        if(self.__camera_type=='WEBCAM'):

            self.cap = cv2.VideoCapture(dispositivo)     
            self.cap.set(3,WIDTH)
            self.cap.set(4,HEIGHT)
            self.init_config_camera_usb()
            
        
        elif(self.__camera_type=='PICAMERA'):
            
            self.cap=PiCamera()
            self.cap.resolution=(WIDTH,HEIGHT)       
            self.cap.framerate=30           
            self.rawcapture=PiRGBArray(self.cap, size=(WIDTH,HEIGHT))
                       
            #self.init_config_camera_picamera()
                 
       
    def init_config_camera_usb(self):
        
        os.system('sudo v4l2-ctl -d /dev/video'+ str(self.__dispositivo)+' --set-ctrl=focus_auto=0')
        os.system('sudo v4l2-ctl -d /dev/video'+ str(self.__dispositivo)+' --set-ctrl=focus_absolute=30')
        os.system('sudo v4l2-ctl -d /dev/video'+ str(self.__dispositivo)+' --set-ctrl=exposure_auto=1')
        os.system('sudo v4l2-ctl -d /dev/video'+ str(self.__dispositivo)+' --set-ctrl=exposure_absolute=30')

    def init_config_camera_picamera(self):
        pass
    
    def camera_read(self):
        
        #PICAMERA
        if self.__camera_type=='PICAMERA':
        
           for frame in self.cap.capture_continuous(self.rawcapture, format="bgr", use_video_port=True):
                
                image = frame.array
                self.rawcapture.truncate(0)
                
                return None,image
        #WEBCAM    
        else:    
            
            ret,frame = self.cap.read()       
            return ret,frame
    
    
    
    def set_focus(self,focus):
        
        if self.__camera_type=='WEBCAM': 
        
            os.system('sudo v4l2-ctl -d /dev/video'+ str(self.__dispositivo)+' --set-ctrl=focus_absolute='+ str(focus))
        
        elif self.__camera_type=='PICAMERA':
            
            os.system('raspivid -br' + str(focus))
            pass
    
    def set_zoom(self,zoom):
        
        if self.__camera_type=='WEBCAM': 
        
            os.system('sudo v4l2-ctl -d /dev/video'+ str(self.__dispositivo)+' --set-ctrl=zoom_absolute='+ str(zoom))
        
        elif self.__camera_type=='PICAMERA':
            
   
            pass
              
    def set_focus_auto(self,focus_auto):
        os.system('sudo v4l2-ctl -d /dev/video'+ str(self.__dispositivo)+' --set-ctrl=focus_auto=' + str(focus_auto))

    def set_exposure_auto(self,exposure_auto):
        os.system('sudo v4l2-ctl -d /dev/video'+ str(self.__dispositivo)+' --set-ctrl=exposure_auto=' + str(exposure_auto))
    
    def set_exposure(self,exposure):
        os.system('sudo v4l2-ctl -d /dev/video'+ str(self.__dispositivo)+' --set-ctrl=exposure_absolute='+ str(exposure)) 
    
    def save_frame(self,name):
        ret,frame = self.cap.read()
        
        frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(str(name),frame)
        

