import requests
import urllib.request
import re
import psycopg2
from bs4 import BeautifulSoup

result = requests.get('https://ru.wikipedia.org/wiki/Университет_ИТМО').text
row = ""
conn = psycopg2.connect(user = "postgres",
                        password = "chicarito",
                        host = "localhost",
                        port = "5432",
                        database = "Lab4post")
cursor = conn.cursor()
print(conn.get_dsn_parameters(), "\n")

cursor.execute("SELECT version();")
record = cursor.fetchone()
print("You are connected to - ", record, "\n")
# createpost = '''CREATE TABLE programming (
#                  YEAR INT PRIMARY KEY,
#                  DETAILS TEXT); '''

# cursor.execute(createpost)
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
    postinsert = """ INSERT INTO programming (YEAR, DETAILS) VALUES (%s,%s)"""
    datavalues = (year, desc)
    cursor.execute(postinsert, datavalues)
    conn.commit()

postgreSQL_select_Query = "select * from programming"

cursor.execute(postgreSQL_select_Query)
mobile_records = cursor.fetchall()

print("Print each row and it's columns values")
for row in mobile_records:
    print("year = ", row[0], )
    print("details = ", row[1], "\n")

cursor.close()
conn.close()
