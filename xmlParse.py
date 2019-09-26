from bs4 import BeautifulSoup
f = open("MIB.xml", "r")
soup = BeautifulSoup(f.read(), 'html.parser')
for serType in soup.find_all("servicetype"):
    typeVal = serType.get("value")
    for subtype in serType.find_all("servicesubtype"):
        print(typeVal, subtype.get("value"))
	print(subtype.get("name"))
