from __future__ import print_function
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

from Functions import *
#------------------------------------------------

# import the necessary packages


from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,help="Whether or not frames should be displayed")
args = vars(ap.parse_args())

#----------- INICIALIZA CAMERA ----------


QUANTIDADE_PALAVRAS_VIRTUAIS = 512
DICIONARIO_NOME = 'dicionario.csv'
QUANTIDADE_DE_DADOS_TREINAMENTO =183
QUANTIDADE_DE_DADOS_TESTE=32
NOME_DESCRITOR='orb_descritor.csv'
dados_treinamento = ['Treinamento/positivos/', 'Treinamento/negativos/']
dados_teste = ['Teste/positivos/', 'Teste/negativos/']
DISPOSITIVO=0


#---------- ALIGNMENT FEATURES------------

NDIM=100
media= np.ones([NDIM,480,640],dtype=np.uint8)
print(media.shape)

MAX_MATCHES = 1000
GOOD_MATCH_PERCENT = 0.8

WINDOW=30
media_movel_homography = np.zeros([1,WINDOW])




def check_espuma(x1,y1,x2,y2,img1,imgref):
    
    imagem_recorte1=np.empty((x2-x1,y2-y1))
    imagem_recorte2=np.empty((x2-x1,y2-y1))
    
    imagem_recorte1=img1[y1:y2,x1:x2]
    imagem_recorte2=imgref[y1:y2,x1:x2]
    
    cv2.imshow("teste1",imagem_recorte1)
    cv2.imshow("teste2",imagem_recorte2)
    
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
    
       
    cv2.imshow("teste",change)
    
    return score
    

def check_CoinCell(x1,y1,x2,y2,img1,imgref):
    
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


    








def feature_match(img1, img2):
    

    img1_eq = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_eq = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    

    # Initiate ORB detector
    orb = cv2.ORB_create()
    # find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(img1_eq,None)
    kp2, des2 = orb.detectAndCompute(img2_eq,None)
    
    
    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # Match descriptors.
    matches = bf.match(des1,des2)
    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)
    
    
    
    good=[]
    for i, m in enumerate(matches):
        #Considera somente Descritores com distâncias diferentes
        if i < len(matches) - 1 and m.distance < 0.98* matches[i+1].distance:
            good.append(m)
    
    print(len(good))
    
    # Draw first 10 matches.
    img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    #plt.imshow(img3),plt.show()
    print(len(matches)) 
    
    
    # Initialize lists
    list_kp1 = []
    list_kp2 = []
    x1_aux=0
    y1_aux=0
    
    # For each match...
    for mat in matches:

        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # Get the coordinates
        (x1, y1) = kp2[img2_idx].pt
        
        x1_aux+=x1
        y1_aux+=y1
        


    return int(x1_aux/len(matches)),int(y1_aux/len(matches)),len(matches)


def alignImages(im1, im2):
    # Convert images to grayscale
    im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
    
    # Convert Eqalize
    im1Gray = cv2.equalizeHist(im1Gray)
    im2Gray = cv2.equalizeHist(im2Gray)

    # Detect ORB features and compute descriptors.
    orb = cv2.ORB_create(MAX_MATCHES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)
    print("Tamanho matches",len(matches))
    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)

    # Remove not so good matches
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]
    #print(str(numGoodMatches))

    # Draw top matches
    imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches[:10], None)
    #cv2.imwrite("matches.jpg", imMatches)
    #cv2.imshow('frame3', imMatches)
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




def media_homography(new_value):
    global  media_movel_homography
    global WINDOW

    for n in range(WINDOW-1,1,-1):
        media_movel_homography[0,n]= media_movel_homography[0,n-1]

    media_movel_homography[0, 0] = new_value
    media_mov= np.sum(media_movel_homography)/WINDOW
    media_mov=np.std(media_movel_homography)


    return media_mov


#-------------------------- Inicializa Camera ---------------------------------------------------

Cam=Camera(DISPOSITIVO,1280,1080)
Cam.Configura_Camera()
Cam.set_focus(30)
#Cam.save_frame('Ref.jpg')

Hm=Homography()
imReference = cv2.imread('Ref.jpg', cv2.IMREAD_COLOR)
score=Hm.best_align_score(imReference)
print("resultador=", score)
#--------------------------Carregar Dicionário-------------------------------------------------
'''

img_representacao = PacoteDePalavras()
img_representacao.carregar_dicionario('Treinamento/', DICIONARIO_NOME)

#----------------------------------------------------------------------------------------------
descritores = np.empty((0, QUANTIDADE_PALAVRAS_VIRTUAIS))

for caminho in dados_treinamento:
    print(caminho)
    descritores = np.append(descritores, carregar_descritores(caminho, NOME_DESCRITOR), axis=0)

print("Descritores Carregados")

#34441824
#--------------------------------Acuracia do Modelo Criado -------------------------------------------
rotulos_treinamento = np.ones(QUANTIDADE_DE_DADOS_TREINAMENTO, dtype=np.uint8)
rotulos_treinamento= np.append(rotulos_treinamento, np.zeros(QUANTIDADE_DE_DADOS_TREINAMENTO, dtype=np.uint8))

knn=KNeighborsClassifier(n_neighbors=7)
knn.fit(descritores,rotulos_treinamento)

count=0
count2=0
count3=0
ok2predict=False

'''
#vs = WebcamVideoStream(src=0).start()
#fps = FPS().start()


#LARGURA = 1280
#ALTURA = 1080

LARGURA = 640
ALTURA = 480

#Inicializa Frame de Referência

refFilename = "Ref.jpg"
imReference = cv2.imread(refFilename, cv2.IMREAD_COLOR)
count=0
# loop over some frames...this time using the threaded stream
while True:

    #frame = vs.read()

#while True:

    ret,frame1 = Cam.camera_read()
   
    frame = cv2.resize(frame1, (640, 480), interpolation=cv2.INTER_CUBIC)
    
    
    
    refFilename = "Ref.jpg"
    #print("Reading reference image : ", refFilename)
    imReference = cv2.imread(refFilename, cv2.IMREAD_COLOR)

    # The estimated homography will be stored in h.
    # imReg, h = alignImages(frame, imReference)
    
    x_detect,y_detect,score=feature_match(imReference, frame1)
    fonte = cv2.FONT_HERSHEY_SIMPLEX
    print(str(score))
    if(score>150):
        
        
        cv2.putText(frame1, "BOARD DETECTED", (15, 65), fonte, 1, (255,0,255), 2, cv2.LINE_AA)
        imagem_recorte=np.empty((550,550))
        imagem=frame1[y_detect-250:y_detect+300,x_detect-350:x_detect+200]    
        
        try:
            imReg, h = alignImages(imagem, imReference)   
            
            #ESPUMA ESQUERDA           
            
            score=check_espuma(140,200,190,280,imReg,imReference)
            
            if(score>0.2):
                cv2.rectangle(imReg,(140,200),(190,280),(0,0,255),2)
            else:
                cv2.rectangle(imReg,(140,200),(190,280),(0,255,0),2)
                
                
            #ESPUMA DIREITA
            
            score=check_espuma(250,200,300,280,imReg,imReference)
    
            
            if(score>0.2):
                cv2.rectangle(imReg,(250,200),(300,280),(0,0,255),2)
            else:
                cv2.rectangle(imReg,(250,200),(300,280),(0,255,0),2)
            
            
            #COIN CELL
            
            
            score=check_CoinCell(450,70,465,85,imReg,imReference)
            
            
            if(score>0.5):
                cv2.rectangle(imReg,(350,30),(500,180),(0,255,0),2)
            else:
                cv2.rectangle(imReg,(350,30),(500,180),(0,0,255),2)
            
            
            
            #cv2.rectangle(imReg,(350,70),(465,185),(255,255,0),1)
            
            #ZEBRA Superior / Esquerda 
            cv2.rectangle(imReg,(80,240),(120,300),(255,255,0),1)
            
            #ZEBRA Superior / Direita 
            cv2.rectangle(imReg,(400,240),(440,300),(255,255,0),1)
            
            
            
            
            cv2.imshow('frame2', imReg)
            #cv2.rectangle(frame1,(x_detect-350,y_detect-250),(x_detect+200,y_detect+300),(255,255,0),2)
        
        except Exception as inst:
            print(str(inst))
            pass
    
        finally:
            cv2.rectangle(frame1,(x_detect-350,y_detect-250),(x_detect+200,y_detect+300),(255,255,0),2)
            
    else:
        cv2.putText(frame1, "NO BOARD DETECTED", (15, 65), fonte, 1, (255,0,255), 2, cv2.LINE_AA)
        
        try:
            cv2.destroyWindow('frame2')
        except:
            pass
    '''
    fonte = cv2.FONT_HERSHEY_SIMPLEX
    ok2predict=False
    
    
    ROI_WIDTH=520
    ROI_HIGH=520
    X=100
    Y=320
    
    try:
        
        res=Hm.media_homography(np.linalg.det(h))
        print(res)
        
        
        nome = str(res) + ".jpg"
        if (res > 0.07)  and (res < 0.13):
            change=cv2.putText(imReg, "ALIGN: OK", (45, 115), fonte, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "ALIGN: OK", (45, 115), fonte, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            ok2predict=True
            #cv2.imwrite(nome, change)
            
            
            imagem=np.empty((ROI_HIGH,ROI_WIDTH))
            imagem=imReg[X:ROI_HIGH+X,Y:ROI_HIGH+Y]
            #cv2.imshow('frame4', imagem)  
            
            count= count + 1
            nome = str(count) + "no.jpg"
            cv2.imwrite(os.path.join('Teste/foto/', nome),imReg[X:ROI_HIGH+X,Y:ROI_HIGH+Y] )
            
        else:
            change=cv2.putText(imReg, "ALIGN: NOK", (45, 115), fonte, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "ALIGN: NOK", (45, 115), fonte, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            ok2predict=False


        #cv2.rectangle(change,(Y,X),(Y+ROI_HIGH,X+ROI_HIGH),(255,255,0),2)
        #cv2.rectangle(change,(270,30),(270+200,30+200),(255,255,0),2)   
        #cv2.imshow('frame2', imReg)
        #cv2.imshow('frame2', change)
        
        
        
        #height=1080
        #width=1280
        #frame1 = cv2.warpPerspective(frame1, h, (width, height))
        
        
        
            
    except:
        
        cv2.putText(frame, "NO BOARD", (15, 65), fonte, 1, (0, 0, 255), 2, cv2.LINE_AA)     
        print("NULL homography")
        pass
    
    #---------------------------------------------------------------
    
    #imagem=np.empty((ROI_HIGH,ROI_WIDTH))
    #imagem=frame1[X:ROI_HIGH+X,Y:ROI_HIGH+Y]
    
    
    #count= count + 1
    #nome = str(count) + ".jpg"
    #cv2.imwrite(os.path.join('Teste/foto/', nome), frame1[X:ROI_HIGH+X,Y:ROI_HIGH+Y])
    #cv2.rectangle(frame1,(Y,X),(Y+ROI_HIGH,X+ROI_HIGH),(255,255,0),2)
    #---------------------------------------------------------------
    
    #imagem=np.empty((200,200))
    #imagem=imReg[270:470,30:230]
    #cv2.imshow('frame4', imagem) 
    
    
    
    
   
    
    #----------------------------------------------------------------
  
    #count= count + 1
    #nome = str(count) + ".jpg"
    #cv2.imwrite(os.path.join('Teste/foto/', nome), frame)

    #dados_teste = ['Teste/positivos/', 'Teste/negativos/']
    dados_teste = ['Teste/foto/']
    img_teste_descritores = np.empty((0, QUANTIDADE_PALAVRAS_VIRTUAIS), dtype=np.uint8)
    
    for caminho in dados_teste:
        for raiz, diretorios, arquivos in os.walk(caminho):
            for arquivo in arquivos:
                if arquivo.endswith('.jpg'):
                    img_descritor, res = get_descritores(os.path.join(caminho, arquivo))
                    # print(str(res))
                    # print(img_descritor.shape)
                    if (res == True):
                        img_descritor = img_representacao.histograma_de_frequencia(img_descritor)
                        # print(img_descritor)
                        img_dim_expandida = np.expand_dims(img_descritor, axis=0)
                        img_teste_descritores = np.append(img_teste_descritores, img_dim_expandida, axis=0)

    
    # --------------------------------------- Matriz de Confusão -----------------------------------------------
    if(ok2predict):
        
        rotulos_previstos = knn.predict(img_teste_descritores)
        print(rotulos_previstos)

        fonte = cv2.FONT_HERSHEY_SIMPLEX

        if (rotulos_previstos[0] == 1):
            cv2.putText(frame, "COM LED", (15, 65), fonte, 1, (0, 255, 0), 2, cv2.LINE_AA)
            count3= count3 + 1
            nome = str(count3) + "_com_led2.jpg"
            #cv2.imwrite(os.path.join('Teste/amostras/', nome), imReg[370:470,30:130])

        else:
            cv2.putText(frame, "SEM LED", (15, 65), fonte, 1, (0, 0, 255), 2, cv2.LINE_AA)
            
            count2= count2 + 1
            nome = str(count2) + "_sem_led2.jpg"
            #cv2.imwrite(os.path.join('Teste/amostras/', nome), imReg[370:470,30:130])
        
    else:
        print('')
        
        
    '''
    
    #height=1080
    #width=1280
    #frame1 = cv2.warpPerspective(frame1, h, (width, height))
    cv2.imshow('frame', frame1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break















