import bs4
import requests
import sqlite3
import re
import time

conn = sqlite3.Connection('static/onion_barn.db')
cur = conn.cursor()

def cleanupWhiteSpace(text):
    return re.sub("\s+", ' ', text)

def dropArticles():
    cur.execute("DROP TABLE Clickhole")
    cur.execute("DROP TABLE AP_News")


def scrapeClickhole(numArticles=2, page=1):
    counter = 0
    cur.execute("CREATE TABLE IF NOT EXISTS Clickhole (id INTEGER PRIMARY KEY, body TEXT UNIQUE, news_source TEXT)")
    while counter < numArticles:
        soup = bs4.BeautifulSoup(requests.get(f"https://clickhole.com/category/news/page/{page}/").text, 'html.parser')
        for el in soup.find_all("h2", class_="post-title"):
            try:
                print(f"Getting article #{counter+1}")
                articleSoup = bs4.BeautifulSoup(requests.get(el.find("a")['href']).text, 'html.parser')
                cur.execute("INSERT OR IGNORE INTO Clickhole (body, news_source) VALUES (?, ?)", (cleanupWhiteSpace(articleSoup.find('div', class_="post-content").text), "Clickhole"))
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

def scrapeAP(numArticles=50):
    counter = 0
    cur.execute("CREATE TABLE IF NOT EXISTS AP_News (id INTEGER PRIMARY KEY, body TEXT UNIQUE, news_source TEXT)")
    articleSoup = bs4.BeautifulSoup(requests.get("https://apnews.com/hub/world-news").text, 'html.parser')
    for el in articleSoup.find_all("div", class_='FeedCard'):
        try:
            path = el.find('a')['href']
            articleSoup = bs4.BeautifulSoup(requests.get(f'https://apnews.com{path}').text, 'html.parser')
            cur.execute("INSERT OR IGNORE INTO AP_News (body, news_source) VALUES (?, ?)", (cleanupWhiteSpace(articleSoup.find('div', class_="Article").text), "AP News"))
            print("Article gotten and stored. Waiting for a second before moving on to the next article")
        except Exception as e:
            print(f"Error getting article: {e}")
        finally:
            print("Sleeping for a second...")
            time.sleep(1)
        counter += 1
        if (counter == numArticles):
            print("Done with retrieving articles.")
            conn.commit()
            return
    conn.commit()
while True:
    try:
        choice = int(input("Select an operation:\n0. Drop Database\n1. Scrape Clickhole (Satire)\n2. Scrape AP (Real News)\n"))
        break
    except:
        print("Please enter an integer.")
if choice == 0:
    if (input("Are you sure you want to DROP the table? Y/N") == "Y"):
        dropArticles()
elif choice == 1:
    numToScrape = int(input("Enter the number of articles you would like to scrape:"))
    scrapeClickhole(numToScrape)
elif choice == 2:
    numToScrape = int(input("Enter the number of articles you would like to scrape (FOR AP, THIS WILL BE VERY LIMITED. IF YOU ENTER MORE THAN THE ARTICLES WE CAN GET, WE WILL GET THE MAXIMUM NUMBER OF ARITCLES POSSIBLE):"))
    scrapeAP(numToScrape)
