from DBE import DBExecutor
import xml.etree.ElementTree as ET
import os


ex = DBExecutor("db.db")

root_node = ET.parse(os.path.join(os.getcwd(),"db\\test_data\\db.xml")).getroot()

requests = [i[1] for i in ex.getRequests()]
synonyms = [i[1] for i in ex.getSynonyms()]

r = root_node.find("Requests")

for tag in r.findall("Item"):

    if(tag.get("r") not in requests):
        ex.insertRequest(tag.get("r"), tag.get("a"))

s = root_node.find("Synonyms")

for tag in s.findall("Item"):
    if(tag.get("w") not in synonyms):
        ex.insertSynonym(tag.get("w"), tag.get("s"))


print(ex.getSynonyms())