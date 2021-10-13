#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 01:41:32 2018

@author: trio_pu
"""
from camera import Camera 
import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QDialog,QFileDialog,QSlider
from PyQt5.uic import loadUi
import cv2
import numpy as np
from testplan import *
from preprocessing import Preprocess
import xml.etree.ElementTree as ET


class GuiMain(QDialog):
    def __init__(self):
        super(GuiMain, self).__init__()
        loadUi('OpenCV2.ui', self)
        self.image = None
        self.Test=False
        self.imageTest=None
        self.start_button.clicked.connect(self.start_webcam)
        self.stop_button.clicked.connect(self.stop_webcam)
        self.load_button.clicked.connect(self.load_testplan)
        self.test_button.clicked.connect(self.track_webcam)
        self.take_pic.clicked.connect(self.take_picture)
        
        self.focus_slide.valueChanged.connect(self.set_focus)
        self.exposure_slide.valueChanged.connect(self.set_exposure)
        self.zoom_slide.valueChanged.connect(self.set_zoom)

        #Teste
        self.track_enabled = False
        #self.testplan=Testplan(produto='solo',posto=1)
        #self.preprocess=Preprocess(produto='solo',posto=1)
        #self.imReference=self.testplan.get_imgRef()
      
            
        self.capture=Camera(1280,1080,dispositivo=1,camera_type='WEBCAM')
        self.capture.set_focus(120)
        self.capture.set_exposure(20)
        self.capture.set_exposure_auto(0)
        self.capture.set_zoom(500)
        
        
    
    def load_testplan(self):
        
        options = QFileDialog.Options()
        #notepad_text = self.texto.toPlainText()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        
        if fileName:
        
            #Inicializa Testplan
            self.testplan= Testplan(fileName)
            self.imReference = self.testplan.get_imgRef()
              
            #Inicializa Modelo de Preprocessamento
            self.preprocess= Preprocess(produto='solo',posto=1)

            self.load_config()

    def load_config(self):

        tree = ET.parse('config.xml')
        root = tree.getroot()
    
        for x in root.findall('camera'):
            zoom=x.find('zoom').text
            self.zoom_slide.setValue(int(zoom))
            exposure=x.find('exposure').text
            self.exposure_slide.setValue(int(zoom))
            focus=x.find('focus').text
            self.focus_slide.setValue(int(zoom))
    
    def track_webcam(self, status):
        
        #preprocess.segmentation(self.image)
        #self.imageTest, frame2, Result = self.preprocess.custom_processing(self.imReference,self.image)
        
        #self.displayImage(self.image,1)
        
        #self.stop_webcam()
              
        #if(Result==True):
                       
        self.testplan.executa_teste(self.image)     
        self.displayImage(self.image,2)
            
        #self.Test=False
         
    def start_webcam(self):
       
        self.image_label2.setText("Nenhum Teste Realizado")
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)
        
    
    def take_picture(self):
       
        ret, image_pic = self.capture.camera_read()
        self.displayImage(image_pic,2)
        self.capture.save_frame("photo.jpg")
        
    
    def update_frame(self):
        ret, self.image = self.capture.camera_read()
        #self.image = cv2.flip(self.image,1)

        #if(Result==True):
                       
            #self.Test=True
        #Teste  
       
         
        self.displayImage(self.image,1)
     
        
    def stop_webcam(self):
        #self.capture.release()
        self.timer.stop()
        
    
    def displayImage(self,img,window=1):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3: #[0]=rows, [1]=cols, [2]=channels
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        
        outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0],qformat)
        #BGR to RGB
        outImage = outImage.rgbSwapped()
        
        if window == 1:
            self.image_label1.setPixmap(QPixmap.fromImage(outImage))
            self.image_label1.setScaledContents(True)
        
        if window ==2:
            self.image_label2.setPixmap(QPixmap.fromImage(outImage))
            self.image_label2.setScaledContents(True)

    def set_focus(self):
        
         self.capture.set_focus(self.focus_slide.value())

    def set_zoom(self):
        
         self.capture.set_zoom(self.zoom_slide.value())

    def set_exposure(self):
        
         self.capture.set_exposure(self.exposure_slide.value())




if __name__ == '__main__':

    
    app = QApplication(sys.argv)
    window = GuiMain()
    window.setWindowTitle('Inline Inspection')
    
    window.show()
    sys.exit(app.exec_())
