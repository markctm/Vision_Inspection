
import requests
import xml.etree.ElementTree as ET 

def Check_Ok_test(url,CustomerName,Division,SerialNumber,AssemblyNumber,TesterName,ProcessStep):

   url="http://brbelm0cmp01/MES-TIS/TIS.ASMX?WSDL"
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
         return str(name.text)

   except OSError as e:
      print("Erro de conexão com TIS")
      return str("ERROR - Conection Error")

def Send_test_result(Serial_Number,Customer_Name,Operator,Tester_Name,Tester_Process,ResultMes):

   test_data="S"+str(Serial_Number) + "\r" +"C"+str(Customer_Name) + "\r" + "F" + str(Operator) + "\r" + "N" + str(Tester_Name)+"\r" + "P" + str(Tester_Process) + "\r" +"T" + str(ResultMes) + "\r"
   
   url="http://brbelm0cmp01/MES-TIS/TIS.ASMX?WSDL"
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
         return str(name.text)  

   except OSError as e:

      print("Erro de conexão com TIS")
      return str("ERROR - Conection Error")


res = Check_Ok_test("http://brbelm0cmp01/MES-TIS/TIS.ASMX?WSDL","INGENICO","INGENICO", "SS52620702244","296171030CARGA","BRBELTE010","Bateria")
print(res)

res =Send_test_result(Serial_Number="SS52620702244",Customer_Name="INGENICO",Operator="NO_OPERATOR",Tester_Name="BRBELCB001",Tester_Process="BATERIA",ResultMes="P" )
print(res)

