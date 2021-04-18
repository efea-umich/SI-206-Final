import bs4
import requests
import sqlite3
import re
import time

conn = sqlite3.Connection('static/onion_barn.db')
cur = conn.cursor()

def cleanupWhiteSpace(text):
    return re.sub("\s+", ' ', text)

def dropClickhole():
    cur.execute("DROP TABLE Clickhole")

def scrapeClickhole(numArticles=2, page=1):
    counter = 0
    cur.execute("CREATE TABLE IF NOT EXISTS Clickhole (id INTEGER PRIMARY KEY, body TEXT UNIQUE)")
    while counter < numArticles:
        soup = bs4.BeautifulSoup(requests.get(f"https://clickhole.com/category/news/page/{page}/").text, 'html.parser')
        for el in soup.find_all("h2", class_="post-title"):
            try:
                print(f"Getting article #{counter+1}")
                articleSoup = bs4.BeautifulSoup(requests.get(el.find("a")['href']).text, 'html.parser')
                cur.execute("INSERT OR IGNORE INTO Clickhole (body) VALUES (?)", (cleanupWhiteSpace(articleSoup.find('div', class_="post-content").text),))
                print("Article gotten and stored. Waiting for a second before moving on to the next article")
            except Exception as e:
                print("Error getting article. Moving on to the next article.")
                print(f"Exception: {e}")
            finally:
                time.sleep(1)
            counter += 1
            if counter == numArticles:
                conn.commit()
                break
        print("Waiting for 5 seconds before moving on to the next page")
        time.sleep(5)
        page += 1

scrapeClickhole(10)

cur.execute("SELECT * FROM Clickhole")

for art in cur:
    print(art)