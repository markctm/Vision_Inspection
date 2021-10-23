from camera import Camera 
import os
import cv2
import numpy as np
from testplan import *
from preprocessing import Preprocess


if __name__ == '__main__':

    #os.system('sudo raspivid -br 80')
    cam=Camera(1280,1080,dispositivo=1,camera_type='WEBCAM')
    cam.set_focus(25)
    cam.set_exposure(100)
    cam.set_exposure_auto(3)
    
    #Inicializa Testplan
    testplan= Testplan(produto='solo',posto=1)
    imReference = testplan.get_imgRef()
    
    
    #Inicializa Modelo de Preprocessamento
    preprocess= Preprocess(produto='solo',posto=1)

    
    while True:
            
        ret,frame1 = cam.camera_read()
        frame1 = cv2.resize(frame1, (640, 480), interpolation=cv2.INTER_CUBIC)
                    
        preprocess.executa_preprocessamento(imgFrame=frame1,imgRef=imReference)
        #preprocess.segmentation(frame1)
        imReg, frame2, Result = preprocess.custom_processing(imReference,frame1)
        
        
        if(Result==True):
                       
            testplan.executa_teste(imReg)
  
        cv2.imshow('frame', frame2)
        cv2.imshow('frame2', imReg)

        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

