from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
import os
import numpy as np
from matplotlib import pyplot as plt
#from yellowbrick.features.pca import PCADecomposition
from matplotlib import pyplot as plt
import cv2
#from PacotesPalavras import PacoteDePalavras
#from Descritoresfunc import get_descritores,carregar_descritores,salvar_descritor
from sklearn.metrics import confusion_matrix
import numpy as np
import time 

import Functions


#--- TESTE THREAD

import datetime
from threading import Thread



class Camera:
    
    def __init__(self,DISPOSITIVO,WIDTH,HIGH):
        
        self.dispositivo=DISPOSITIVO
        self.cap = cv2.VideoCapture(DISPOSITIVO)
        
        self.cap.set(3,WIDTH)
        self.cap.set(4,HIGH)
        
       
    def Configura_Camera(self):
        
        os.system('sudo v4l2-ctl -d /dev/video'+ str(self.dispositivo)+' --set-ctrl=focus_auto=0')
        os.system('sudo v4l2-ctl -d /dev/video'+ str(self.dispositivo)+' --set-ctrl=focus_absolute=30')
        os.system('sudo v4l2-ctl -d /dev/video'+ str(self.dispositivo)+' --set-ctrl=exposure_auto=0')
        os.system('sudo v4l2-ctl -d /dev/video'+ str(self.dispositivo)+' --set-ctrl=exposure_absolute=30')
    
    def camera_read(self):
        ret,frame = self.cap.read()
        
        
        return ret,frame
    
    def set_focus(self,focus):
        os.system('sudo v4l2-ctl -d /dev/video'+ str(self.dispositivo)+' --set-ctrl=focus_absolute='+ str(focus))    
    
    def save_frame(self,name):
        ret,frame = self.cap.read()
        
        frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(str(name),frame)
        
        

def get_descritores(img_caminho):

    LARGURA = 360
    ALTURA = 360
    try:
      # Ler a imagem
      img_teste = cv2.imread(img_caminho, 0)

      # Redimensionar
      img_redimensionada = cv2.resize(img_teste, (LARGURA, ALTURA), interpolation=cv2.INTER_CUBIC)

    # Remover ruídos
      img_equalizada = cv2.equalizeHist(img_redimensionada)
      img_suavizada = cv2.GaussianBlur(img_equalizada, (9,9), 1)

      # Determinar pontos chaves
      orb = cv2.ORB_create(nfeatures=512)
      pontos_chave = orb.detect(img_suavizada, None)

      pontos_chave, descritores = orb.compute(img_suavizada, pontos_chave)
      return descritores, True

    except:
      return 0, False

def carregar_descritores(caminho,nome_arquivo='orb_descritor.csv'):
  descritores=np.loadtxt(os.path.join(caminho,nome_arquivo),delimiter=',')
  print('formato do array de descritores: ', descritores.shape)
  return descritores



def salvar_descritor(descritor, caminho, nome_arquivo):
    descritor =descritor.reshape((1,descritor.size))
    arquivo=open(os.path.join(caminho,nome_arquivo),'a')
    np.savetxt(arquivo,descritor,delimiter=',',fmt='%i')
    arquivo.close()



class PacoteDePalavras:

    def gerar_dicionario(self, lista_descritores):
        kmeans = KMeans(n_clusters=QUANTIDADE_PALAVRAS_VIRTUAIS)
        kmeans = kmeans.fit(lista_descritores)
        self.dicionario = kmeans.cluster_centers_

    def histograma_de_frequencia(self, descritor):

        try:
            algoritmo_knn = NearestNeighbors(n_neighbors=1)
            algoritmo_knn.fit(self.dicionario)
            mais_proximos = algoritmo_knn.kneighbors(descritor, return_distance=False)
            histograma_caracteristica = np.histogram(mais_proximos, bins=np.arange(self.dicionario.shape[0] + 1))[0]

            return histograma_caracteristica
        except AttributeError:
            print("O atributo dicionario nao foi definido")
            return False

    def salvar_dicionario(self, caminho='', nome_dicionario='dicionario.csv'):
        try:
            np.savetxt(os.path.join(caminho, nome_dicionario), self.dicionario, delimiter=',', fmt='%f')
            print("Dicionario salvo")

        except AttributeError:
            print("Dicionario Vazio")

    def carregar_dicionario(self, caminho='', nome_dicionario='dicionario.csv'):
        self.dicionario = np.loadtxt(os.path.join(caminho, nome_dicionario), delimiter=',')
        





class Homography:
    
    def __init__ (self):
        
        self.max_matches=1000
        self.good_match_percent=0.8
        self.window=30
        self.media_movel_homography= np.zeros([1,self.window])
        
    

    def alignImages(self,im1, im2):
        # Convert images to grayscale
        im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

        # Detect ORB features and compute descriptors.
        orb = cv2.ORB_create(self.max_matches)
        keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
        keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

        # Match features.
        matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        matches = matcher.match(descriptors1, descriptors2, None)

        # Sort matches by score
        matches.sort(key=lambda x: x.distance, reverse=False)

        # Remove not so good matches
        numGoodMatches = int(len(matches) * self.good_match_percent)
        matches = matches[:numGoodMatches]
        #print(str(numGoodMatches))

        # Draw top matches
        #imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
        #cv2.imwrite("matches.jpg", imMatches)

        # Extract location of good matches
        points1 = np.zeros((len(matches), 2), dtype=np.float32)
        points2 = np.zeros((len(matches), 2), dtype=np.float32)

        for i, match in enumerate(matches):
            points1[i, :] = keypoints1[match.queryIdx].pt
            points2[i, :] = keypoints2[match.trainIdx].pt

        # Find homography
        try:
            h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)
        except:
            h=0
            pass


        # Use homography
        height, width, channels = im2.shape
        try:
            im1Reg = cv2.warpPerspective(im1, h, (width, height))
            #cv2.imshow('frame3', im1Reg)
        except:
            im1Reg=im1
            pass

        return im1Reg, h



    def media_homography(self,new_value):
        
        
        for n in range(self.window-1,1,-1):
            
            self.media_movel_homography[0,n]= self.media_movel_homography[0,n-1]

        self.media_movel_homography[0, 0] = new_value
        media_mov= np.sum(self.media_movel_homography)/self.window
        media_mov=np.std(self.media_movel_homography)


        return media_mov


    def best_align_score(self,ref_img):
               
        img_align, h =self.alignImages(ref_img, ref_img)
        score=np.linalg.det(h)

        return score





















        
'''

class FPS:
    
    def __init__(self):
        
        self._start= None
        sef._end= None
        self._numFrames= 0
        
    def start(self):
        #inicia o timer
        self._start = datetime.datetime.now()
        return self
    
    def stop(self):
        # para o timer
        self._end = datetime.datetime.now()
        
    def update(self):
   
       self._numFrames +=1
    
    def elapsed(self):
        # return the total number of seconds between the start and end interval
        
        return(self._end - self._start).total_seconds()
    
    def fps(self):
        
        # computa o FPS aproximado 
        return self._numFrames / self.elapsed()
        

class WebcamVideoStream:
    
    def __init__(self, src=0):
        
        #initialize the video camera stream and read tje first  frame
        # from rhe stream
        
        self.stream= cv2.VideoCapture(src)
        (self.grabbed, self.frame)= self.stream.read()
        
        # Initialize the variable used to indicate if the thread should be stopped
        
        self.stopped= False
        
    def start(self):
        
        Thread(target=self.update, args=()).start()
        
        return self
    
    def update(self):
        
        #keep looping infinitely until the thread is stopped
        
        while True:
            
            if self.stopped:
                return
            
            #otherwise, read the next frame from the stream
            
            (self.grabbed,self.frame)=self.stream.read()
            
            
    def read(self):
        #return the frame most recently read
        return self.frame
    
    def stop(self):
        
        self.stopped=True
        
        
 '''       
    
        
        
        
        


