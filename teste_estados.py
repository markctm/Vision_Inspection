from abc import ABCMeta, abstractmethod
from test_functions import Test


# Métodos obrigatorios para qualquer Teste 

class Estados_de_Teste():
    __metaclass__= ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def inicia(self):
        pass
    
    @abstractmethod
    def aprova(self):
        pass

    @abstractmethod
    def reprova(self):
        pass
    
    @abstractmethod
    def finaliza(self):
        pass
    
    @abstractmethod
    def reinicia(self):
        pass



class Inicializado(Estados_de_Teste):


    def inicia(self):
        pass
    
    def aprova(self):      
        pass
    
    def reprova(self):
        pass

    def finaliza(self,orcamento):
        pass
    
    def reinicia(self):
        pass


class Em_teste(Estados_de_Teste):


    def inicia(self):
        pass
    
    def aprova(self):      
        pass
    
    def reprova(self):
        pass

    def finaliza(self):
        pass
    
    def reinicia(self):
        pass

class Aprovado(Estados_de_Teste):

    def inicia(self):
        pass
    
    def aprova(self):
         pass

    def reprova(self):
        pass

    def finaliza(self):
        pass
    
    def reinicia(self):
        pass


class Reprovado(Estados_de_Teste):

    
    def inicia(self):
        pass
    def aprova(self,orcamento):
        pass

    def reprova(self,orcamento):
        pass

    def finaliza(self,orcamento):
        pass
    
    def reinicia(self):
        pass


class Teste():

    def __init__(self,Lista_Functions=[],Lista_Parameters=[],ImgTest=None,ImgRef=None):
        self.estado_teste = Inicializado()
        self.lista_de_functions=Lista_Functions
        self.lista_de_parametros=Lista_Parameters

    def aprova(self):
        self.estado_atual.aprova()

    def reprova(self):
        self.estado_atual.reprova()

    def finaliza(self):
        self.estado_atual.finaliza()

    def reinicia(self):
        self.estado_atual.reinicia()
    
    
    def start(self,imgTest,ImgRef):
        
      
        for index in range(0,len(self.lista_de_functions)-1,1):
            
            func_name = getattr(Test(), self.lista_de_functions[index])
            parametros= self.lista_de_parametros[index].copy()
            parametros.append(imgTest)
            parametros.append(ImgRef)
            #print(parametros)
            #print("tamanho " + str(len(parametros)))
            result = func_name(*parametros)
            del parametros[:]

