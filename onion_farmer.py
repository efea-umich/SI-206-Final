from bs4 import BeautifulSoup
import requests
import sqlite3
import re
import time
import json
from predict import getPreds
import pandas as pd

conn = sqlite3.Connection('static/onion_barn.db')
cur = conn.cursor()

def cleanupWhiteSpace(text):
    return re.sub("\s+", ' ', text)

def dropArticles():
    cur.execute("DROP TABLE IF EXISTS Clickhole")
    cur.execute("DROP TABLE IF EXISTS AP_News")
    cur.execute("DROP TABLE IF EXISTS CNN")
    cur.execute("DROP TABLE IF EXISTS Fox_News")
    cur.execute("DROP TABLE IF EXISTS The_Onion")


def insertPreds(table_name):
    conn.commit()
    print("Running predictions for articles")
    df = pd.read_sql_query(f"SELECT body FROM {table_name} WHERE pred IS NULL AND predVal IS NULL", conn)
    bodies = list(map(lambda x: x[0], df.to_numpy()))
    preds, predVals = getPreds(df)
    predVals = list(map(lambda x: float(x[0]), predVals))
    for i in range(len(preds)):
        cur.execute(f"UPDATE {table_name} SET pred = (?), predVal = (?) WHERE body = ?", (preds[i], predVals[i], bodies[i]))
    conn.commit()


def scrapeClickhole(numArticles=2, page=1, verbose=False):
    counter = 0
    cur.execute("CREATE TABLE IF NOT EXISTS Clickhole (id INTEGER PRIMARY KEY, body TEXT UNIQUE, news_source TEXT, pred TEXT, predVal NUMERIC)")
    while counter < numArticles:
        soup = BeautifulSoup(requests.get(f"https://clickhole.com/category/news/page/{page}/").text, 'html.parser')
        for el in soup.find_all("h2", class_="post-title"):
            try:
                if verbose:
                    print(f"Getting article #{counter+1}")
                else:
                    print(f"Getting articles... {int(counter / numArticles * 100)}%", end='\r')
                
                articleSoup = BeautifulSoup(requests.get(el.find("a")['href']).text, 'html.parser')
                articleBody = cleanupWhiteSpace(articleSoup.find('div', class_="post-content").text)

                cur.execute("INSERT OR IGNORE INTO Clickhole (body, news_source) VALUES (?, ?)", (articleBody, "Clickhole"))
                
                if verbose:
                    print("Article gotten and stored. Waiting for a second before moving on to the next article")
            except:
                print("Error getting article. Moving on to the next article.")
            finally:
                time.sleep(0.5)
            counter += 1
            if counter == numArticles:
                conn.commit()
                break
        if verbose:
            print("Waiting for 2 seconds before moving on to the next page")
        time.sleep(2)
        page += 1

        insertPreds("Clickhole")

def scrapeAP(numArticles=50, verbose=False):
    counter = 0
    cur.execute("CREATE TABLE IF NOT EXISTS AP_News (id INTEGER PRIMARY KEY, body TEXT UNIQUE, news_source TEXT, pred TEXT, predVal NUMERIC)")
    articleSoup = BeautifulSoup(requests.get("https://apnews.com/hub/world-news").text, 'html.parser')
    for el in articleSoup.find_all("div", class_='FeedCard'):
        try:
            path = el.find('a')['href']
            articleSoup = BeautifulSoup(requests.get(f'https://apnews.com{path}').text, 'html.parser')
            cur.execute("INSERT OR IGNORE INTO AP_News (body, news_source) VALUES (?, ?)", (cleanupWhiteSpace(articleSoup.find('div', class_="Article").text), "AP News"))
            if verbose:
                print("Article gotten and stored. Waiting for a second before moving on to the next article")
            else:
                print(f"Getting articles... {int(counter / numArticles * 100)}%", end='\r')
        except:
            print(f"Error getting article")
        finally:
            if verbose:
                print("Sleeping for half a second...")
            time.sleep(0.5)
        counter += 1
        if (counter == numArticles):
            print("Done with retrieving articles.")
            conn.commit()
            break
    conn.commit()
    insertPreds("AP_News")


def scrapeCNN(numArticles=50, verbose=False):
    counter = 0
    cur.execute("CREATE TABLE IF NOT EXISTS CNN (id INTEGER PRIMARY KEY, body TEXT UNIQUE, news_source TEXT, pred TEXT, predVal NUMERIC)")
    articleSoup = BeautifulSoup(requests.get("http://rss.cnn.com/rss/cnn_topstories.rss").text, 'xml')
    for el in articleSoup.find_all("item"):
        try:
            path = el.find('link').text
            articleSoup = BeautifulSoup(requests.get(path).text, 'html.parser')
            cur.execute("INSERT OR IGNORE INTO CNN (body, news_source) VALUES (?, ?)", (cleanupWhiteSpace(articleSoup.find('section', class_='zn-body-text').text), "CNN"))
            if verbose:
                print("Article gotten and stored. Waiting for a second before moving on to the next article")
            else:
                print(f"Getting articles... {int(counter / numArticles * 100)}%", end='\r')
        except:
            print(f"Error getting article")
        finally:
            if verbose:
                print("Sleeping for half a second...")
            time.sleep(0.5)
        counter += 1
        if (counter == numArticles):
            print("Done with retrieving articles.")
            conn.commit()
            break
    conn.commit()
    insertPreds("CNN")


def scrapeFox(numArticles=50, verbose=False):
    counter = 0
    cur.execute("CREATE TABLE IF NOT EXISTS Fox_News (id INTEGER PRIMARY KEY, body TEXT UNIQUE, news_source TEXT, pred TEXT, predVal NUMERIC)")
    articleSoup = BeautifulSoup(requests.get("https://www.foxnews.com/").text, 'html.parser')
    for el in articleSoup.find_all("article"):
        try:
            path = el.find('a')['href']
            if re.search('video\.foxnews', path):
                continue
            articleSoup = BeautifulSoup(requests.get(path).text, 'html.parser')
            cur.execute("INSERT OR IGNORE INTO Fox_News (body, news_source) VALUES (?, ?)", (cleanupWhiteSpace(articleSoup.find('div', class_="article-body").text), "Fox News"))
            if verbose:
                print("Article gotten and stored. Waiting for a second before moving on to the next article")
            else:
                print(f"Getting articles... {int(counter / numArticles * 100)}%", end='\r')
        except:
            print(f"Error getting article")
        finally:
            if verbose:
                print("Sleeping for half a second...")
            time.sleep(0.5)
        counter += 1
        if (counter == numArticles):
            print("Done with retrieving articles.")
            conn.commit()
            break
    conn.commit()
    insertPreds("Fox_News")


def redditDB(sub, days=30, num_articles=25, verbose=False):
    conn = sqlite3.Connection('static/onion_barn.db')
    cur = conn.cursor()
    counter = 0
    cur.execute("CREATE TABLE IF NOT EXISTS The_Onion (id INTEGER PRIMARY KEY, body TEXT UNIQUE, news_source TEXT, pred TEXT, predVal NUMERIC)")
#Getting the current time (UNIX format)
    curr = int(time.time())

    #PushShift API query
    #This query will:
    # -Get [num] submissions(posts) from the specified subreddit that satisfy these conditions:
    # -Posted in the last [days] days from when this function is called
    # -Sorted by descending order of number of comments

    base = 'https://api.pushshift.io'

    quer = ("/reddit/search/submission/?subreddit=" + sub +
            "&sort=desc&sort_type=num_comments"
            "&after=" + str(curr - (days * 24 * 60 * 60)) +
            "&before=" + str(curr) +
            "&size=" + str(num_articles))

    r = requests.get(base + quer)

    #Load the JSON data into a Python object
    data = json.loads(r.text)

    #Creates a Reddit table with id, link, title, and numComments columns.
    #Prevents duplicates by making the link column unique values only.
    #cur.execute("CREATE TABLE IF NOT EXISTS Reddit (id INTEGER PRIMARY KEY, link TEXT UNIQUE, title Text, numComments INTEGER)")

    for d in data['data']:
        link = d['url']
        title = d['title']
        numComments = d['num_comments']
        try:
            r = requests.get(link)
            soup = BeautifulSoup(r.text, 'html.parser')
            text = soup.find('p', class_='sc-77igqf-0 bOfvBY').text
            cur.execute("INSERT OR IGNORE INTO The_Onion (body, news_source) VALUES (?, ?)", (cleanupWhiteSpace(text), "The Onion"))
            if verbose:
                print("Article gotten and stored. Waiting for a second before moving on to the next article")
            else:
                print(f"Getting articles... {int(counter / num_articles * 100)}%", end='\r')
        except Exception as e:
            print(f"Error getting article")
        finally:
            if verbose:
                print("Sleeping for half a second...")
            time.sleep(0.5)
        counter += 1
        if (counter == num_articles):
            print("Done with retrieving articles.")
            conn.commit()
            break
    conn.close()

    insertPreds("The_Onion")




while True:
    try:
        command = input("Select an operation (-v for verbose):\n0. Drop Database\n1. Scrape Clickhole (Satire)\n2. Scrape AP (Real News)\n3. Scrape CNN\n4. Scrape Fox\n5. Scrape The Onion\n").split()
        choice = int(command[0])
        break
    except:
        print("Please enter an integer.")
if choice == 0:
    if (input("Are you sure you want to DROP the table? Y/N") == "Y"):
        dropArticles()
elif choice == 1:
    numToScrape = int(input("Enter the number of articles you would like to scrape:"))
    if len(command) > 1 and command[1] == '-v':
        scrapeClickhole(numToScrape, verbose=True)
    else:
        scrapeClickhole(numToScrape)
elif choice == 2:
    numToScrape = int(input("Enter the number of articles you would like to scrape (FOR AP, THIS WILL BE VERY LIMITED. IF YOU ENTER MORE THAN THE ARTICLES WE CAN GET, WE WILL GET THE MAXIMUM NUMBER OF ARITCLES POSSIBLE):"))
    if len(command) > 1 and command[1] == '-v':
        scrapeAP(numToScrape, verbose=True)
    else:
        scrapeAP(numToScrape)
elif choice == 3:
    numToScrape = int(input("Enter the number of articles you would like to scrape:"))
    if len(command) > 1 and command[1] == '-v':
        scrapeCNN(numToScrape, verbose=True)
    else:
        scrapeCNN(numToScrape)
elif choice == 4:
    numToScrape = int(input("Enter the number of articles you would like to scrape:"))
    if len(command) > 1 and command[1] == '-v':
        scrapeFox(numToScrape, verbose=True)
    else:
        scrapeFox(numToScrape)
elif choice == 5:
    numToScrape = int(input("Enter the number of articles you would like to scrape:"))
    if len(command) > 1 and command[1] == '-v':
        redditDB('theOnion', verbose=True)
    else:
        redditDB('theOnion')


