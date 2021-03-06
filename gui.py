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
from PyQt5.QtWidgets import QApplication, QDialog,QFileDialog
from PyQt5.uic import loadUi
import cv2
import numpy as np
from testplan import *
from preprocessing import Preprocess


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
        self.track_enabled = False
        #self.testplan=Testplan(produto='solo',posto=1)
        #self.preprocess=Preprocess(produto='solo',posto=1)
        #self.imReference=self.testplan.get_imgRef()
              
            
        self.capture=Camera(1280,1080,dispositivo=1,camera_type='WEBCAM')
        self.capture.set_focus(10)
        self.capture.set_exposure(100)
        self.capture.set_exposure_auto(3)
        
        
    
    def load_testplan(self):
        """
        Se o botão salvar for clicado, exibe a caixa de diálogo 
        para salvar o texto, no campo de edição, em um arquivo.
        """

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

    
    def track_webcam(self, status):
        
        self.preprocess.executa_preprocessamento(imgFrame=self.image,imgRef=self.imReference)
        #preprocess.segmentation(self.image)
        self.imageTest, frame2, Result = self.preprocess.custom_processing(self.imReference,self.image)
        
        self.displayImage(self.image,1)
        
        self.stop_webcam()
              
        if(Result==True):
                       
            self.testplan.executa_teste(self.imageTest)     
            self.displayImage(self.imageTest,2)
            
        #self.Test=False
         
    def start_webcam(self):
       
        self.image_label2.setText("Nenhum Teste Realizado")
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)
        
    def update_frame(self):
        ret, self.image = self.capture.camera_read()
        #self.image = cv2.flip(self.image,1)

              
        #if(Result==True):
                       
            #self.Test=True
               
        
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
        

if __name__ == '__main__':

    
    
    app = QApplication(sys.argv)
    window = GuiMain()
    window.setWindowTitle('Inline Inspection')
    
    
    window.show()
    sys.exit(app.exec_())
