import requests
import urllib.request
import re

result = requests.get('https://ru.wikipedia.org/wiki/Университет_ИТМО').text
row = ""

matchObj = re.findall(r'<table class="standard">(.*?)</table>', result, re.M | re.I | re.S)
matchObj1 = re.findall(r'<th>(.*?)</th>', matchObj[1], re.M | re.I | re.S)
matchObj2 = re.findall(r'<td>(.*?)</td>', matchObj[1], re.M | re.I | re.S)
for num, res in enumerate(matchObj2):
#    print(res)
    sherlock1 = re.findall(r'<a (.*?)</a>', res, re.M | re.I | re.S)
    for link in sherlock1:
#        print(link)
        if link:
            res1 = re.findall(r'<span class="wrap">(.*?)</span>', link, re.M | re.I | re.S)
            for span in res1:
                if span:
                    #print(span)
                    matchObj2[num] = span

for num, res in enumerate(matchObj2):
#    print(res)
    sherlock1 = re.findall(r'<a (.*?)>(.*?)</a>', res, re.M | re.I | re.S)
    for link in sherlock1:
        print(link)
        if link:
            matchObj2[num] = link[1]

for i, td in enumerate(matchObj1):
    matchObj1[i] = td.rstrip()

for i, td in enumerate(matchObj2):
    matchObj2[i] = td.rstrip()

for i in range(0, 5):
    row += matchObj1[i] + " "

with open('output.txt', 'w') as f:
    f.write(row + "\n")

j = 0
for n, d in enumerate(matchObj1[5::]):
    row = ""
    row += matchObj1[n+5]
    row += " "
    for i in range(0, 4):
        row += matchObj2[j]
        row += " "
        j = j + 1
    with open('output.txt', 'a') as f:
        f.write(row + "\n")