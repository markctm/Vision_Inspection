import requests
import xml.etree.ElementTree as ET 
import os

url= ""
CustomerName = ""
Division = ""
SerialNumber = ""
AssemblyNumber= ""
TesterName= ""
ProcessStep= ""
Operator=""
calibration_mode=False
FailDescription=""



def set_data_to_test(set_url,set_CustomerName,set_Division,set_serial_number,set_AssemblyNumber,set_TesterName,set_Operator,set_ProcessStep,set_calibration_mode):

   global url
   global CustomerName
   global Division
   global SerialNumber
   global AssemblyNumber
   global TesterName
   global ProcessStep
   global Operator
   global calibration_mode

   url=set_url
   CustomerName=set_CustomerName
   SerialNumber=set_serial_number
   Division=set_Division
   AssemblyNumber=set_AssemblyNumber
   TesterName=set_TesterName
   ProcessStep=set_ProcessStep
   Operator=set_Operator
   calibration_mode=set_calibration_mode

def get_data_to_test():

   global url
   global CustomerName
   global Division
   global SerialNumber
   global AssemblyNumber
   global TesterName
   global ProcessStep
   global Operator
   

   return str(url),str(CustomerName),str(Division),str(SerialNumber),str(AssemblyNumber),str(TesterName),str(ProcessStep),str(Operator)


def check_ok_test():

   global url
   global CustomerName
   global Division
   global SerialNumber
   global AssemblyNumber
   global TesterName
   global ProcessStep
   global Operator
 
   url="http://172.24.72.186/MES-TIS/TIS.ASMX?WSDL"
   #headers = {'content-type': 'application/soap+xml'}
   headers = {'content-type': 'text/xml'}
   body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mes="http://jabil.com/GMS/MES_TIS">
      <soapenv:Header/>
      <soapenv:Body>
         <mes:OKToTest>
            <!--Optional:-->
            <mes:CustomerName>""" + str(CustomerName) + """</mes:CustomerName>
            <!--Optional:-->
            <mes:Division>""" + str(Division) + """</mes:Division>
            <!--Optional:-->
            <mes:SerialNumber>""" + str(SerialNumber) + """</mes:SerialNumber>
            <!--Optional:-->
            <mes:AssemblyNumber>"""+ str(AssemblyNumber) + """</mes:AssemblyNumber>
            <!--Optional:-->
            <mes:TesterName>""" + str(TesterName) + """</mes:TesterName>
            <!--Optional:-->
            <mes:ProcessStep>""" + str(ProcessStep) + """</mes:ProcessStep>
         </mes:OKToTest>
      </soapenv:Body>
   </soapenv:Envelope>"""

   print(body)
   try:
      response = requests.post(url,data=body,headers=headers) 
      #print(str(response.content))

            # define namespace mappings to use as shorthand below
      namespaces = {
         'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
         'a': 'http://jabil.com/GMS/MES_TIS',
      }

      dom = ET.fromstring(response.content)     
      
      names = dom.findall(
         './soap:Body'
         '/a:OKToTestResponse'
         '/a:OKToTestResult',
         namespaces,
      )
      for name in names:
         return str(name.text).upper().strip()

   except OSError as e:
      print("Erro de conexão com TIS")
      return str("ERROR - Conection Error")

def send_test_result(ResultMes):

   global url
   global CustomerName
   global Division
   global SerialNumber
   global AssemblyNumber
   global TesterName
   global ProcessStep
   global Operator
   global calibration_mode
   
   if calibration_mode==False:
      
      test_data="S"+str(SerialNumber) + "\r" +"C"+str(CustomerName) + "\r" + "F" + str(Operator) + "\r" + "N" + str(TesterName)+"\r" + "P" + str(ProcessStep) + "\r" +"T" + str(ResultMes) + "\r"
      
      url="http://172.24.72.186/MES-TIS/TIS.ASMX?WSDL"
      headers = {'content-type': 'text/xml'}
      body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mes="http://jabil.com/GMS/MES_TIS">
         <soapenv:Header/>
         <soapenv:Body>
            <mes:ProcessTestData>
               <!--Optional:-->
               <mes:TestData>""" + str(test_data) + """</mes:TestData>
               <!--Optional:-->
               <mes:DataFormat>Generic</mes:DataFormat>
            </mes:ProcessTestData>
         </soapenv:Body>
      </soapenv:Envelope>"""

      try:
         response = requests.post(url,data=body,headers=headers)

         namespaces = {
            'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
            'a': 'http://jabil.com/GMS/MES_TIS',
         }

         dom = ET.fromstring(response.content)     
         
         names = dom.findall(
            './soap:Body'
            '/a:ProcessTestDataResponse'
            '/a:ProcessTestDataResult',
            namespaces,
         )

         for name in names:
            return str(name.text).upper().strip()

      except OSError as e:

         print("Erro de conexão com TIS")
         return str("ERROR - Conection Error")

   else:
      print("Calibration Mode Activated")
      return str("Calibration Mode Activated")


def send_test_result_parser(ResultMes="",Fail_Description="",Fixture=""):

   global url
   global CustomerName
   global Division
   global SerialNumber
   global AssemblyNumber
   global TesterName
   global ProcessStep
   global Operator
   global calibration_mode

   print("Calibration Mode:" + str(calibration_mode))

   if calibration_mode==False:
   
      
      if ResultMes=="P":
         body= """S""" + str(SerialNumber) + """\r\n""" +  """C""" + str(CustomerName) + """\r\n""" +  """F""" + str(Operator)  + """\r\n"""+  """N""" + str(TesterName)   + """\r\n""" +  """P""" + str(ProcessStep) + """\r\n""" +  """T""" + str(ResultMes) +  """\r\n""" +  """f""" + str(Fixture) +  """\r\n"""
      else:
         body= """S""" + str(SerialNumber) + """\r\n""" +  """C""" + str(CustomerName) + """\r\n""" +  """F""" + str(Operator)  + """\r\n"""+  """N""" + str(TesterName)   + """\r\n""" +  """P""" + str(ProcessStep) + """\r\n""" +  """T""" + str(ResultMes) +  """\r\n"""  +  """F""" + str(Fail_Description) +  """\r\n"""

      print(str(body))

      file = open("./parser/" +str(SerialNumber) + '.txt', 'w')
      file.write(body)
      file.close()



'''
res = set_data_to_test("http://172.24.72.186/MES-TIS/TIS.ASMX?WSDL","INGENICO","INGENICO", "SS52620702244","296171030CARGA","BRBELTE010","","Bateria")
print(res)

res=check_ok_test()
print(res)

res = Send_test_result(Serial_Number="SS52620702244",Customer_Name="INGENICO",Operator="NO_OPERATOR",Tester_Name="BRBELCB001",Tester_Process="BATERIA",ResultMes="P" )
print(res)

'''