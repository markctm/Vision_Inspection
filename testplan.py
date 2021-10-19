from teste_estados import Teste
import numpy as np
import cv2

class Testplan():

  def __init__(self,nome_tesplan=''): 

    self.posto=nome_tesplan.split('/')[-1].split('_')[1]
    self.produto=nome_tesplan.split('/')[-1].split('_')[0]
    self.functions_list=[]
    self.parameters_list=[]  
    self.__testplan_nome=str(self.produto) + "_" + str(self.posto) + "_testplan" + ".tpl"
    self.__imgRef_nome= str(self.produto) + "_" + str(self.posto) + "_imgRef" + ".jpg"
    self.imgRef=0
    self.__carrega_testplan()
    
    
  def verifica_testplan(self):
    ''' Verifica a existência do testplan'''
    

  def __carrega_testplan(self):
    # self.verifica_testplan()
    ''' Carrega o Testplan ''' 
    
    #CARREGA IMAGEM REFERÊNCIA
    
    self.__carrega_imgRef()
    
    #CARREGA TESTPLAN
    
    model=open('Testplan/'+ str(self.__testplan_nome),'r')
    lines = model.readlines()
    print(lines)
    
    for line in lines:
        line=line.replace('\n', '')
        functions=line.split(':')[0]
        parameters=line.split(':')[1].split(',')
        
        #print(functions)
        #print(parameters)
        
        #self.testlist.update({functions:parameters})
        self.functions_list.append(functions)
        self.parameters_list.append(parameters)

    return None

  def __carrega_imgRef(self):
    
    ''' Carrega a Imagem Referência '''
      
    
    self.imgRef = cv2.imread('Imagens_Golden/'+ str(self.__imgRef_nome), cv2.IMREAD_COLOR)
    print(str("Imagem Golden Carregado: ") + str(self.__imgRef_nome))
    
    return

  def executa_teste(self,Img):
    
    ''' Inicia um objeto Teste '''
    
    teste=Teste(Lista_Functions=self.functions_list,Lista_Parameters=self.parameters_list,ImgTest=Img,ImgRef=self.imgRef)
    teste.start(Img,self.imgRef)
   
    pass

  def get_imgRef(self):
    return self.imgRef


