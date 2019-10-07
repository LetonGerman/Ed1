import requests
import urllib.request
import re
import sqlite3
from bs4 import BeautifulSoup

result = requests.get('https://ru.wikipedia.org/wiki/Университет_ИТМО').text
row = ""
conn = sqlite3.connect('years.db')
cursor = conn.cursor()
# cursor.execute("""CREATE TABLE programming (
#                 year integer,
#                 details text
#                 )""")

conn.commit()

soup = BeautifulSoup(result, 'lxml')
sherlock = soup.find('dt', text="Гранты, бизнес-инкубаторы, коворкинги")
sherlock1 = sherlock.find_parent("dl").find_next_siblings("p")
# sherlock2 = sherlock1.find_next_siblings("p")
for paragraph in sherlock1[:4]:
    year = re.search(r"\b\d{4}\b", paragraph.get_text()).group()
    desc = paragraph.get_text()
    desc = desc.replace("\n", "")
    desc = desc.replace("\xa0", " ")
    cursor.execute("INSERT INTO programming VALUES (?, ?)", (year, desc))
    conn.commit()

cursor.execute("SELECT * FROM programming")
print(cursor.fetchall())
conn.close()
