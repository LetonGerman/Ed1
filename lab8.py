from collections import namedtuple

from flask import Flask, render_template, redirect, url_for, request
import requests
import urllib.request
import re
import sqlite3
import os
from bs4 import BeautifulSoup
app = Flask(__name__)
result = requests.get('https://ru.wikipedia.org/wiki/Университет_ИТМО').text
result.encode("utf-8")
row = ""
grantYear = namedtuple('grantYear', 'year desc')
grantYears = []
conn = sqlite3.connect('flask.db')
cursor = conn.cursor()
soup = BeautifulSoup(result, 'lxml')
cursor.execute("""CREATE TABLE IF NOT EXISTS programming (
                year integer,
                details text
                )""")

conn.commit()
sherlock = soup.find('dt', text="Гранты, бизнес-инкубаторы, коворкинги")
sherlock1 = sherlock.find_parent("dl").find_next_siblings("p")
cursor.execute("SELECT * FROM programming")
if not cursor.fetchall():
    for paragraph in sherlock1[:4]:
        year = re.search(r"\b\d{4}\b", paragraph.get_text()).group()
        desc = paragraph.get_text()
        desc = desc.replace("\n", "")
        desc = desc.replace("\xa0", " ")
        cursor.execute("INSERT INTO programming VALUES (?, ?)", (year, desc))
        conn.commit()

cursor.execute("SELECT * FROM programming")
records = cursor.fetchall()
for row in records:
    grantYears.append(grantYear(row[0], row[1]))
conn.close()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', years=grantYears)

@app.route('/addyear', methods=['GET'])
def addyear():
    return render_template('insert.html')


@app.route('/insert', methods=['POST'])
def add_message():
    with sqlite3.connect("flask.db") as con:
        query_year = request.form['year']
        query_desc = request.form['desc']
        grantYears.append(grantYear(query_year, query_desc))
        cursor = con.cursor()
        cursor.execute("INSERT INTO programming VALUES (?, ?)", (query_year, query_desc))
        con.commit()

    return redirect(url_for('addyear'))