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


QUANTIDADE_PALAVRAS_VIRTUAIS = 512
DICIONARIO_NOME = 'dicionario.csv'
QUANTIDADE_DE_DADOS_TREINAMENTO =36
QUANTIDADE_DE_DADOS_TESTE=32
NOME_DESCRITOR='orb_descritor.csv'
dados_treinamento = ['Treinamento/positivos/', 'Treinamento/negativos/']
dados_teste = ['Teste/positivos/', 'Teste/negativos/']




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


#--------------------------Carregar Dicionário-------------------------------------------------


img_representacao = PacoteDePalavras()
img_representacao.carregar_dicionario('Treinamento/', DICIONARIO_NOME)

#----------------------------------------------------------------------------------------------
descritores = np.empty((0, QUANTIDADE_PALAVRAS_VIRTUAIS))

for caminho in dados_treinamento:
    print(caminho)
    descritores = np.append(descritores, carregar_descritores(caminho, NOME_DESCRITOR), axis=0)

print("Descritores Carregados")


#--------------------------------Acuracia do Modelo Criado -------------------------------------------
rotulos_treinamento = np.ones(QUANTIDADE_DE_DADOS_TREINAMENTO, dtype=np.uint8)
rotulos_treinamento= np.append(rotulos_treinamento, np.zeros(QUANTIDADE_DE_DADOS_TREINAMENTO, dtype=np.uint8))

knn=KNeighborsClassifier(n_neighbors=7)
knn.fit(descritores,rotulos_treinamento)


#dados_teste = ['Teste/positivos/', 'Teste/negativos/']
dados_teste = ['Teste/foto/']
img_teste_descritores= np.empty((0,QUANTIDADE_PALAVRAS_VIRTUAIS),dtype=np.uint8)

for caminho in dados_teste:
  for raiz, diretorios, arquivos in os.walk(caminho):
    for arquivo in arquivos:
      if arquivo.endswith('.jpg'):
        img_descritor,res =get_descritores(os.path.join(caminho,arquivo))
        #print(str(res))
        #print(img_descritor.shape)
        if(res==True):
          img_descritor= img_representacao.histograma_de_frequencia(img_descritor)
          #print(img_descritor)
          img_dim_expandida=np.expand_dims(img_descritor,axis=0)
          img_teste_descritores=np.append(img_teste_descritores,img_dim_expandida,axis=0)


#--------------------------------------- Matriz de Confusão -----------------------------------------------

rotulos_previstos = knn.predict(img_teste_descritores)
print(rotulos_previstos)










