
import requests

url="http://brbelm0cmp01/MES-TIS/TIS.ASMX?WSDL"
#headers = {'content-type': 'application/soap+xml'}
headers = {'content-type': 'text/xml'}
body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mes="http://jabil.com/GMS/MES_TIS">
   <soapenv:Header/>
   <soapenv:Body>
      <mes:OKToTest>
         <!--Optional:-->
         <mes:CustomerName>INGENICO</mes:CustomerName>
         <!--Optional:-->
         <mes:Division>INGENICO</mes:Division>
         <!--Optional:-->
         <mes:SerialNumber>P0750B011321A15430</mes:SerialNumber>
         <!--Optional:-->
         <mes:AssemblyNumber>2962203895ACCARGA</mes:AssemblyNumber>
         <!--Optional:-->
         <mes:TesterName>BRBELTE010</mes:TesterName>
         <!--Optional:-->
         <mes:ProcessStep>Bateria</mes:ProcessStep>
      </mes:OKToTest>
   </soapenv:Body>
</soapenv:Envelope>"""

response = requests.post(url,data=body,headers=headers)
print("TEST")
print(str(response.content))
