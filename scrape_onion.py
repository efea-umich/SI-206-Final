from bs4 import BeautifulSoup
import requests
import time
import json
import sqlite3

#Uses the PushShift API to get the [num] most-commented-on posts from the specified subreddit posted in the last [days] days.
def getPosts(sub, days = 30, num = 25):
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
    "&size=" + str(num))

    r = requests.get(base + quer)

    #Load the JSON data into a Python object
    data = json.loads(r.text)
    print(type(data))
    return data

def redditDB(data):
    conn = sqlite3.Connection('static/onion_barn.db')
    cur = conn.cursor()
    
    #Creates a Reddit table with id, link, title, and numComments columns.
    #Prevents duplicates by making the link column unique values only.
    cur.execute("CREATE TABLE IF NOT EXISTS Reddit (id INTEGER PRIMARY KEY, link TEXT UNIQUE, title Text, numComments INTEGER)")
    for d in data['data']:
        link = d['url']
        title = d['title']
        numComments = d['num_comments']
        cur.execute("INSERT OR IGNORE INTO Reddit (link, title, numComments) VALUES (?,?,?)",
        (link, title, numComments))
    conn.commit()

def scrape(url):
    r = requests.get(url)
    soup = BeautifulSoup(r, 'html.parser')
    text = soup.find('p', class_='sc-77igqf-0 bOfvBY').text

data = getPosts('TheOnion', 30, 25)
redditDB(data)