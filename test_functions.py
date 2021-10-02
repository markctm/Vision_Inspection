import numpy as np
import cv2 
from preprocessing import Preprocess



class Test():
    
    def Test_Version(self,a=None,b=None):
        version='0.0.1'
        print(str(version))
        return version
    
      
    def check_espuma(self,x1,y1,x2,y2,img1,imgref):
        
        x1=int(x1)
        x2=int(x2)
        y1=int(y1)
        y2=int(y2)
        
        imagem_recorte1=np.empty((x2-x1,y2-y1))
        imagem_recorte2=np.empty((x2-x1,y2-y1))
        
        imagem_recorte1=img1[y1:y2,x1:x2]
        imagem_recorte2=imgref[y1:y2,x1:x2]
        
        #cv2.imshow("teste1",imagem_recorte1)
        #cv2.imshow("teste2",imagem_recorte2)
        
        imagem_recorte1 = cv2.cvtColor(imagem_recorte1, cv2.COLOR_BGR2GRAY)
        imagem_recorte2 = cv2.cvtColor(imagem_recorte2, cv2.COLOR_BGR2GRAY)
            
        change = cv2.absdiff(imagem_recorte1, imagem_recorte2)
        ret, change = cv2.threshold(change, 80, 255, cv2.THRESH_BINARY)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
        change = cv2.morphologyEx(change, cv2.MORPH_OPEN, kernel)
        
        #Detecta os contornos
        
        contornos, hierarquia=cv2.findContours(change,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        area_list=[]
        for contorno in contornos:
            
            area=cv2.contourArea(contorno)       
            print("area:"+ str(area))
            
            # Elimina area relativamente pequena redução de ruído  
            if(area<250):
                contornos.remove(contorno)
            else:
                area_list.append(int(area))
        
        
        #Se caso nenhum area detectada 
        if(len(area_list)==0):
            score=0
        else:   
            area_list.sort()
            score=area_list[len(area_list)-1]/(len(change)*len(change[0]))    
        
        
        '''
        
        image = cv2.drawContours(imagem_recorte1, contornos, -1, (0, 255, 0), 2)
        
        cv2.imshow("componentes conexas",image)
        
        print("Contornos:" + str(contornos))
        
        count_pixel=0
        for i in range(0, len(change)):
            for j in range(0,len(change[0])):
                #print(str(change[i][j]))
                if(change[i][j]!=0):
                    count_pixel= count_pixel + 1
        
        score=count_pixel/(len(change)*len(change[0]))
        '''
        print("score:" + str(score))
        
           
        #cv2.imshow("teste",change)
        
        
        if(score>0.2):
            cv2.rectangle(img1,(x1,y1),(x2,y2),(0,0,255),2)
        else:
            cv2.rectangle(img1,(x1,y1),(x2,y2),(0,255,0),2)
        
        #cv2.imshow("result",img1)
        
        return score
        


    def check_CoinCell(self,x1,y1,x2,y2,img1,imgref):
        
        imagem_recorte1=np.empty((x2-x1,y2-y1))
        imagem_recorte2=np.empty((x2-x1,y2-y1))
        
        imagem_recorte1=img1[y1:y2,x1:x2]
        imagem_recorte2=imgref[y1:y2,x1:x2]
        
        #cv2.imshow("teste1",imagem_recorte1)
        #cv2.imshow("teste2",imagem_recorte2)
        
        imagem_recorte1 = cv2.cvtColor(imagem_recorte1, cv2.COLOR_BGR2GRAY)
        imagem_recorte2 = cv2.cvtColor(imagem_recorte2, cv2.COLOR_BGR2GRAY)
            
        #change = cv2.absdiff(imagem_recorte1, imagem_recorte2)
        ret, change = cv2.threshold(imagem_recorte1, 127, 255, cv2.THRESH_BINARY)
        
        #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        #change = cv2.morphologyEx(change, cv2.MORPH_OPEN, kernel)
        
        count_pixel=0
        for i in range(0, len(change)):
            for j in range(0,len(change[0])):
                #print(str(change[i][j]))
                if(change[i][j]!=0):
                    count_pixel= count_pixel + 1
        
        score=count_pixel/(len(change)*len(change[0]))
        print("score:" + str(score))
        

        #cv2.imshow("teste",change)
        
        return score
        
        
    def check_Label(self,x1,y1,x2,y2,img1,imgref):

        imagem_recorte1=np.empty((x2-x1,y2-y1))
        imagem_recorte2=np.empty((x2-x1,y2-y1))

        imagem_recorte1=img1[y1:y2,x1:x2]
        imagem_recorte2=imgref[y1:y2,x1:x2]

        cv2.imshow("teste1",imagem_recorte1)
        cv2.imshow("teste2",imagem_recorte2)

        return 0


    def test_feature_match(self,tresh,retest,img1,imgref):
            
        print("Test_feature_match")  
        
        process = Preprocess("NA","NA") 
        
        try:
            x_detect,y_detect,score=process.feature_match(img1, imgref)
       
        except:
            score=0
            pass
        
        print(str("Score of Feature Match") + str(score))
        
        fonte = cv2.FONT_HERSHEY_SIMPLEX
        
        if(score>int(tresh)):
            cv2.putText(img1, "PASS - LABEL DETECTED", (50, 400), fonte, 3, (0,255,0), 3, cv2.LINE_AA)
        else:
            cv2.putText(img1, "FAIL- NO LABEL", (50, 400), fonte, 3, (0,0,255), 3, cv2.LINE_AA)
        
        return score

        
        
    def blank(self,x,y):
       # print("Hello Mundo!")
       # print(x)
       # print(y)
        pass




