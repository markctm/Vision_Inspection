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
from PyQt5.QtWidgets import QApplication, QDialog,QFileDialog,QSlider,QMessageBox,QCheckBox
from PyQt5.uic import loadUi
import cv2
import numpy as np
from testplan import *
from preprocessing import Preprocess
import xml.etree.ElementTree as ET
import os 
from mes import *

class GuiMain(QDialog):
    def __init__(self):
        super(GuiMain, self).__init__()
        loadUi('OpenCV2.ui', self)
        self.image = None
        self.Test=False
        self.imageTest=None
        self.tesplan_load=False
        self.camera_ok=False
        self.sw_version="Inline_Inspection_v0.0.1"
        self.sw_version_label.setText(self.sw_version)

        self.start_button.clicked.connect(self.start_webcam)
        self.stop_button.clicked.connect(self.stop_webcam)
        self.load_button.clicked.connect(self.load_testplan)
        self.test_button.clicked.connect(self.track_webcam)
        self.take_pic.clicked.connect(self.take_picture)
        self.save_button.clicked.connect(self.save_camera_cfg)
        self.focus_slide.valueChanged.connect(self.set_focus)
        self.exposure_slide.valueChanged.connect(self.set_exposure)
        self.zoom_slide.valueChanged.connect(self.set_zoom)
        self.lineEdit_serial.returnPressed.connect(self.track_webcam)
        self.checkBox_calibration_mode.isChecked()
        #Teste
        self.track_enabled = False
        #self.testplan=Testplan(produto='solo',posto=1)
        #self.preprocess=Preprocess(produto='solo',posto=1)
        #self.imReference=self.testplan.get_imgRef()
      
        #MES
        self.customer=""
        self.Serial_Number=""
        self.division=""
        self.assembly_nummber=""
        self.tester_name=""
        self.process_step=""
        self.operator_name=""
        self.TIS_url="http://brbelm0cmp01/MES-TIS/TIS.ASMX?WSDL"
            
        #Corrigindo Bugs da Interface 
        self.timer2 = QTimer(self)
        self.timer3 = QTimer(self)
        self.clear_once_flag

        #self.start_webcam()
        self.capture=Camera(1280,1080,dispositivo=0,camera_type='WEBCAM')
        
        
    def load_testplan(self):
        
        
        options = QFileDialog.Options()
        #notepad_text = self.texto.toPlainText()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Open Testpan File", "./Testplan/","Testplan Files (*.tpl)", options=options)
        

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
            tree = ET.parse("./configs/" +str(produto) +'.xml')
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


    def track_webcam(self):

       print(str(self.timer2.isActive()))

       if self.timer2.isActive()==False:

            # DEBOUNCE MOUSE        
            self.timer2.setInterval(1000)
            self.timer2.setSingleShot(True) 
            self.timer2.start() 

            print("PRESSED\n") 

            self.Serial_Number= self.lineEdit_serial.text()
            self.label_SerialNumber.setText(str(self.Serial_Number))  
            self.lineEdit_serial.clear()   

            img=self.create_blank(1280, 1080, rgb_color=(0, 0, 0))
            self.displayImage(img,2)
            #COMMMENT

            if self.camera_ok==True:

                if self.tesplan_load==True:

                    print("TESTE CALIBRATION MODE")
                    print(str(self.checkBox_calibration_mode.isChecked()))

                    set_data_to_test(self.TIS_url,self.customer,self.customer,self.Serial_Number,self.assembly_nummber,self.tester_name,self.operator_name,self.process_step,self.checkBox_calibration_mode.isChecked())                    
                    res=None
                    if self.checkBox_calibration_mode.isChecked()==False:
                        res=check_ok_test()

                    if(res=="PASS") or (self.checkBox_calibration_mode.isChecked()):
 
                        self.timer3.setInterval(4000)
                        self.timer3.setSingleShot(True) 
                        self.timer3.start()
                        self.clear_once_flag=False 

                        self.testplan.executa_teste(self.image)     
                        self.displayImage(self.image,2)

                    else:
                        cv2.putText(self.image, "ERROR - PROCESS VERIFICATION", (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3, cv2.LINE_AA)
                        self.displayImage(self.image,2)

                else:
                    QMessageBox.about(self, "Message", "No Testplan Loaded. Please select tesplan")
            else:
                QMessageBox.about(self, "Message", "Camera Not Started")

        

    def start_webcam(self):
       
        try:
            #self.capture=Camera(1280,1080,dispositivo=0,camera_type='WEBCAM')
            self.image_label2.setText("Nenhum Teste Realizado")
            self.set_focus()
            self.set_zoom()
            self.set_exposure()
            
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(5)
        except:
             QMessageBox.about(self, "Message", "Camera Not Started")
    
    def take_picture(self):
       
        ret, image_pic = self.capture.camera_read()
        self.displayImage(image_pic,2)    
        name = QFileDialog.getSaveFileName(self, 'Save File',"picture" ," Image File (*.jpg)")
        self.capture.save_frame(str(name[0]) + '.jpg')  
    
    def update_frame(self):
        ret, self.image = self.capture.camera_read()

        if self.timer3.isActive()==False and self.clear_once_flag==False:
            self.clear_once_flag=True
            img=self.create_blank(1280, 1080, rgb_color=(194, 197, 204))
            self.displayImage(img,2)
            
        if self.image is None:
            QMessageBox.about(self, "Camera       ", "Error Camera!")
            self.camera_ok=False
            self.stop_webcam()
        else:
            self.displayImage(self.image,1)
            self.camera_ok=True
     
        
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

        #tree.write(name)

    def create_blank(self,width, height, rgb_color=(0, 0, 0)):
        """Create new image(numpy array) filled with certain color in RGB"""
        # Create black blank image
        image = np.zeros((height, width, 3), np.uint8)

        # Since OpenCV uses BGR, convert the color first
        color = tuple(reversed(rgb_color))
        # Fill image with color
        image[:] = color

        return image

if __name__ == '__main__':
  
    app = QApplication(sys.argv)
    window = GuiMain()
    window.setWindowTitle('Inline Inspection')
    window.show()
    sys.exit(app.exec_())
