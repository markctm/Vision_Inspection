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
from PyQt5.QtWidgets import QApplication, QDialog,QFileDialog,QSlider,QMessageBox
from PyQt5.uic import loadUi
import cv2
import numpy as np
from testplan import *
from preprocessing import Preprocess
import xml.etree.ElementTree as ET
import os 

class GuiMain(QDialog):
    def __init__(self):
        super(GuiMain, self).__init__()
        loadUi('OpenCV2.ui', self)
        self.image = None
        self.Test=False
        self.imageTest=None
        self.tesplan_load=False
        self.start_button.clicked.connect(self.start_webcam)
        self.stop_button.clicked.connect(self.stop_webcam)
        self.load_button.clicked.connect(self.load_testplan)
        self.test_button.clicked.connect(self.track_webcam)
        self.take_pic.clicked.connect(self.take_picture)
        self.save_button.clicked.connect(self.save_camera_cfg)
        self.focus_slide.valueChanged.connect(self.set_focus)
        self.exposure_slide.valueChanged.connect(self.set_exposure)
        self.zoom_slide.valueChanged.connect(self.set_zoom)

        #Teste
        self.track_enabled = False
        #self.testplan=Testplan(produto='solo',posto=1)
        #self.preprocess=Preprocess(produto='solo',posto=1)
        #self.imReference=self.testplan.get_imgRef()
      

        #MES
        self.customer=""
        self.division=""
        self.assembly_nummber=""
        self.tester_name=""
        self.process_step=""
            
        self.capture=Camera(1280,1080,dispositivo=1,camera_type='WEBCAM')
        #self.capture.set_focus(120)
        #self.capture.set_exposure(20)
        self.capture.set_exposure_auto(0)
        #self.capture.set_zoom(500)
        
        
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
            #self.preprocess= Preprocess(produto='solo',posto=1)

            
            self.load_config(self.testplan.produto)
            self.tesplan_load=True
            self.label_2.setText(str(self.testplan.produto))

    def load_config(self,produto):
        try:
            tree = ET.parse(str(produto) +'.xml')
            root = tree.getroot()
        
            for x in root.findall('camera'):
                zoom=x.find('zoom').text
                exposure=x.find('exposure').text      
                focus=x.find('focus').text
            
            #Melhorar isso
            self.zoom_slide.setValue(int(zoom))
            self.exposure_slide.setValue(int(exposure))
            self.focus_slide.setValue(int(focus))

            self.set_focus()
            self.set_zoom()
            self.set_exposure()

            for x in root.findall('mes'):
                self.customer=x.find('Customer').text
                self.division=x.find('Division').text      
                self.assembly_nummber=x.find('AssemblyNumber').text
                self.tester_name=x.find('TesterName').text
                self.process_step=x.find('ProcessStep').text
            
            self.label_customer.setText(str( self.customer))
            self.label_division.setText(str( self.division))
            self.label_assembly_number.setText(str(self.assembly_nummber))
            self.label_tester_name.setText(str(self.tester_name))
            self.label_process_step.setText(str(self.process_step))
        
        except:
            QMessageBox.about(self, "Message", "Erro while loading config flle")


    def track_webcam(self, status):
        
        if self.tesplan_load==True:

            #preprocess.segmentation(self.image)
            #self.imageTest, frame2, Result = self.preprocess.custom_processing(self.imReference,self.image)
            
            #self.displayImage(self.image,1)  
            #self.stop_webcam()
            #if(Result==True):
                            
            self.testplan.executa_teste(self.image)     
            self.displayImage(self.image,2)
                
            #self.Test=False
        else:
            QMessageBox.about(self, "Message", "No Testplan Loaded. Please select tesplan")
         
    def start_webcam(self):
       
        self.image_label2.setText("Nenhum Teste Realizado")
        self.set_focus()
        self.set_zoom()
        self.set_exposure()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

        
    
    def take_picture(self):
       
        ret, image_pic = self.capture.camera_read()
        self.displayImage(image_pic,2)
        self.capture.save_frame("photo.jpg")
        
    
    def update_frame(self):
        ret, self.image = self.capture.camera_read()

        if self.image is None:
            QMessageBox.about(self, "Camera       ", "Error Camera !!")
            self.stop_webcam()
        else:
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

    def save_camera_cfg(self):

        name = QFileDialog.getSaveFileName(self, 'Save File',str(self.testplan.produto) ," XML File (*.xml)")
        print(str(name))

        if name:
            xml_str="""<config>
                    <camera>
                        <zoom>""" + str(self.zoom_slide.value()) + """</zoom>
                        <exposure>""" + str(self.exposure_slide.value()) + """</exposure>
                        <focus>"""+  str(self.focus_slide.value()) + """</focus>
                    </camera>
                    <mes>
                        <Customer>"""+  str(self.customer) +"""</Customer>
                        <Division>""" + str(self.customer) + """</Division>
                        <AssemblyNumber>""" + str(self.assembly_nummber) + """</AssemblyNumber>
                        <TesterName>""" + str(self.tester_name)+ """</TesterName>
                        <ProcessStep>"""+ str(self.process_step) + """</ProcessStep>
                        
                    </mes> 
                    </config>
                    """
            
            file = open(str(name[0]) + '.xml', 'w')
            file.write(xml_str)
            file.close()


        """
        save_xml = ET.fromstring(xml_str)
        tree = ET.parse(save_xml)
        root = tree.getroot()
        tree.write(name)

       

        for x in root.iter('zoom'):
            x.text=str(self.zoom_slide.value())
        
        for x in root.iter('exposure'):
            x.text=str(self.exposure_slide.value())
       
        for x in root.iter('focus'):
            x.text=str(self.focus_slide.value())
        
        for x in root.iter('Customer'):
            x.text=str(self.customer)
        
        for x in root.iter('Division'):
            x.text=str(self.customer)
       
        for x in root.iter('AssemblyNumber'):
            x.text=str(self.assembly_nummber)
                
        for x in root.iter('TesterName'):
            x.text=str(self.tester_name)
                       
        for x in root.iter('ProcessStep'):
            x.text=str(self.process_step)
     """
        #tree.write(name)


if __name__ == '__main__':

    
    app = QApplication(sys.argv)
    window = GuiMain()
    window.setWindowTitle('Inline Inspection')
    
    window.show()
    sys.exit(app.exec_())
