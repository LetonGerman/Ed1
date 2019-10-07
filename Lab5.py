import requests
import urllib.request
import re
import mysql.connector
from bs4 import BeautifulSoup

result = requests.get('https://ru.wikipedia.org/wiki/Университет_ИТМО').text
row = ""
conn = mysql.connector.connect(host='localhost',
                        database='python',
                        user='root',
                        password='shiestwind')

if conn.is_connected():
    db_Info = conn.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
    cursor = conn.cursor()
    cursor.execute("select database();")
    record = cursor.fetchone()
    print("Your connected to database: ", record)

soup = BeautifulSoup(result, 'lxml')
sherlock = soup.find('dt', text="Гранты, бизнес-инкубаторы, коворкинги")
sherlock1 = sherlock.find_parent("dl").find_next_siblings("p")
# sherlock2 = sherlock1.find_next_siblings("p")
for paragraph in sherlock1[:4]:
    year = re.search(r"\b\d{4}\b", paragraph.get_text()).group()
    desc = paragraph.get_text()
    desc = desc.replace("\n", "")
    desc = desc.replace("\xa0", " ")
    mysqlinsert = """ INSERT INTO programming (YEAR, DETAILS) VALUES (%s,%s)"""
    datavalues = (year, desc)
    cursor.execute(mysqlinsert, datavalues)
    conn.commit()

MySQL_select_Query = "select * from programming"
cursor.execute(MySQL_select_Query)
records = cursor.fetchall()
print("Print each row and it's columns values")
for row in records:
    print("year = ", row[0], )
    print("details = ", row[1], "\n")

cursor.close()
conn.close()
