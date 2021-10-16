
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

   response = requests.post(url,data=body,headers=headers) 
   #print(str(response.content))

  
   responseXml = ET.fromstring(response.text)
   print(str(responseXml))

   TESTE = responseXml.find('.//{http://jabil.com/GMS/MES_TIS}OKToTestResult')
   #TESTE = responseXml.find('.//{http://schemas.xmlsoap.org/soap/envelope/}OKToTestResult')
   
   print(str(TESTE))
   print(str(TESTE.attrib['text']))
   #testId = responseXml.find('OKToTestResponse').find('OKToTestResult')
   #('.//{http://tempuri.org/wsSalesQuotation/Service1}LoginResult')
   #print(str(testId))
   
   #print(str(testId.text))

   
   #tree = ET.parse(response.content)
   #root = tree.getroot()

   
   #print("TEST")
   #print(str(response.content))








def send_test_result(test_data):

   url="http://brbelm0cmp01/MES-TIS/TIS.ASMX?WSDL"
   headers = {'content-type': 'text/xml'}
   body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mes="http://jabil.com/GMS/MES_TIS">
      <soapenv:Header/>
      <soapenv:Body>
         <mes:ProcessTestData>
            <!--Optional:-->
            <mes:TestData>?</mes:TestData>
            <!--Optional:-->
            <mes:DataFormat>?</mes:DataFormat>
         </mes:ProcessTestData>
      </soapenv:Body>
   </soapenv:Envelope>"""

   response = requests.post(url,data=body,headers=headers)
   print("TEST")
   print(str(response.content))




Check_Ok_test("http://brbelm0cmp01/MES-TIS/TIS.ASMX?WSDL","INGENICO","INGENICO", "81361278","2962203895ACCARGA","BRBELTE010","Bateria")