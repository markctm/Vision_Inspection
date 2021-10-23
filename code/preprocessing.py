import numpy as np
import cv2

class Preprocess():
 
    def __init__(self,produto,posto): 

        self.model_name= str(produto)+ "_" + str(posto) + "_preprocess" + ".mdl"
        self.functions_list=[]
        self.parameters_list=[]
        self.imgRef=[]
        self.imgFrame=[]
        #self.__carrega_modelo_preprocessamento()
    
    def __carrega_modelo_preprocessamento(self):
        
        ''' Carrega o Modelo de Pre-Processamento ''' 
        
        model=open('Preprocessing_Models/'+ str(self.model_name),'r')
        lines = model.readlines()
        print(lines)

        for line in lines:
            
            #TRATA LINHAS 
            line=line.replace('\n', '')
            functions=line.split(':')[0]
            parameters=line.split(':')[1].split(',')
            
            #CRIA LISTA DE FUNCOES E PARAMETROS
            self.functions_list.append(functions)
            self.parameters_list.append(parameters)

        return None

    def executa_preprocessamento(self,imgFrame,imgRef):
        
        self.imgRef=imgRef
        self.imgFrame=imgFrame
        
        return 


    def feature_match(self,img1, img2):
              
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


    def alignImages(self,im1, im2):
        
        #---------- ALIGNMENT FEATURES------------

        MAX_MATCHES = 1000
        GOOD_MATCH_PERCENT = 0.8
      
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
    
    
    def custom_processing(self,imReference,frame1):
            
        print("Chegou aqui ")  
    
        try:
            x_detect,y_detect,score=self.feature_match(imReference, frame1)
        except:
            score=0
            pass
        
        fonte = cv2.FONT_HERSHEY_SIMPLEX
        print(str(score))
        
        #Gambiarra
        imReg= frame1
        result=False
        if(score>160):

            cv2.putText(frame1, "BOARD DETECTED", (10, 35), fonte, 0.5, (180,255,255), 1, cv2.LINE_AA)
            #imagem_recorte=np.empty((550,550))
            #imagem=frame1[y_detect-250:y_detect+300,x_detect-350:x_detect+200]
            #cv2.rectangle(frame1,(x_detect-250,y_detect-300),(x_detect+350,y_detect+200),(255,255,0),2)
            #imagem=self.segmentation_solo(frame1)
            
            
            try:
                imReg, h = self.alignImages(imagem, imReference)
                result=True
                print("Imagem Alinhada")
            except:
                print("Erro ao alinhar")
                imReg= frame1
                result=False
            
            
        return imReg, frame1, result
    
    def segmentation_solo(self,img):
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray,240,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        # noise removal
               
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
        # sure background area
        sure_bg = cv2.dilate(opening,kernel,iterations=10)
  
        contornos, hierarquia=cv2.findContours(sure_bg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        area_maior=0
        contorno_area_maior=0
        #print(contornos.type)
        for index in range(0,len(contornos)-1,1):
            area=cv2.contourArea(contornos[index])
            
            if area > area_maior:
                contorno_area_maior=index
                area_maior=area   
     
     
        image = cv2.drawContours(img, contornos,contorno_area_maior, (0, 255, 0), 1)      
        
        #
        mask = np.zeros_like(gray) # Create mask where white is what we want, black otherwise
        cv2.drawContours(mask, contornos,contorno_area_maior, (255,255,255), -1)    
        out = np.zeros_like(img) # Extract out the object and place into output image       
       
        out[mask == 255] = img[mask == 255]
        
        
        
        
        # Now crop
        (y, x) = np.where(mask == 255)
        (topy, topx) = (np.min(y), np.min(x))
        print(str((topy, topx)))
        (bottomy, bottomx) = (np.max(y), np.max(x))
        print(str((bottomy, bottomx)))
        out = out[topy:bottomy+1, topx:bottomx+1]
        
        #cv2.rectangle(mask,(topx,topy),(bottomx,bottomy),(243,255,150),1)
        #cv2.rectangle(out,(140,200),(190,280),(0,255,0),1)
        
        
        #cv2.imshow('frame3', mask)
        #cv2.imshow('frame', out)
        
        
       # cv2.rectangle(img,(250+topx,200 +topy),(300+topx,280 +topy),(0,255,0),1)
        return out
    
    
