import xml.etree.ElementTree as ET

tree = ET.parse('config.xml')
root = tree.getroot()

'''
#print(root[0].tag)

for x in root[0]:
    print(x.tag,x.attrib)

for x in root[0]:
    print(x.text)

'''

# findin elements
for x in root.findall('camera'):
    item=x.find('zoom').text
    print(str(item))


#Writing elements

for x in root.iter('zoom'):
    x.text=str(300)

tree.write('config.xml')

