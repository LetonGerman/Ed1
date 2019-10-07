import requests
import urllib.request
import re
from bs4 import BeautifulSoup

result = requests.get('https://ru.wikipedia.org/wiki/Университет_ИТМО').text
row = ""

soup = BeautifulSoup(result, 'lxml')
sherlock = soup.find('dt', text="Гранты, бизнес-инкубаторы, коворкинги")
sherlock1 = sherlock.find_parent("dl").find_next_siblings("p")
# sherlock2 = sherlock1.find_next_siblings("p")
with open('output1.txt', 'w') as f:
    f.write(sherlock.get_text() + "\n")
for paragraph in sherlock1[:4]:
    year = re.search(r"\b\d{4}\b", paragraph.get_text()).group()
    with open('output1.txt', 'a') as f:
        f.write(year + ": " + paragraph.get_text())