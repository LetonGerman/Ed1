#!C:/Users/USER/AppData/Local/Programs/Python/Python37-32/python.exe
print("Content-type:text/html\r\n\r\n")
import requests
import urllib.request
import re
from bs4 import BeautifulSoup
result = requests.get('https://ru.wikipedia.org/wiki/Университет_ИТМО').text
result.encode("utf-8")
row = ""
soup = BeautifulSoup(result, 'lxml')
sherlock = soup.find('dt', text="Гранты, бизнес-инкубаторы, коворкинги")
sherlock1 = sherlock.find_parent("dl").find_next_siblings("p")
print("<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=windows-1251\"></head><body>")
print("<p>" + sherlock.get_text() + "</p>")
print("<table border=\"1\">")
for paragraph in sherlock1[:4]:
    print("<tr>")
    year = re.search(r"\b\d{4}\b", paragraph.get_text()).group()
    print("<td>" + year + "</td><td>" + paragraph.get_text() + "</td></tr>")
print("</body></html>")