import requests
import urllib.request
import re
import pymongo
from pymongo import MongoClient
from bs4 import BeautifulSoup

result = requests.get('https://ru.wikipedia.org/wiki/Университет_ИТМО').text
cluster = MongoClient("mongodb+srv://project17:Tui3gmQb9xBmL9V3@mdeditor-cs1cq.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["test"]
collection = db["python"]

soup = BeautifulSoup(result, 'lxml')
sherlock = soup.find('dt', text="Гранты, бизнес-инкубаторы, коворкинги")
sherlock1 = sherlock.find_parent("dl").find_next_siblings("p")
# sherlock2 = sherlock1.find_next_siblings("p")
for paragraph in sherlock1[:4]:
    year = re.search(r"\b\d{4}\b", paragraph.get_text()).group()
    desc = paragraph.get_text()
    desc = desc.replace("\n", "")
    desc = desc.replace("\xa0", " ")
    datavalues = {"year": year, "description": desc}
    collection.insert_one(datavalues)

for res in collection.find():
    print(res)

