import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv

from wordcloud import STOPWORDS, WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

conn = sqlite3.Connection('static/onion_barn.db')
cur = conn.cursor()

def avgPredVal(id):
    df = pd.read_sql_query(f"SELECT predVal FROM Preds WHERE news_source = ?", conn, params=(id,))
    return df['predVal'].mean()

def percentRF(id):
    df = pd.read_sql_query(f"SELECT prediction FROM Preds WHERE news_source = ?", conn, params=(id,))
    
    reals = df[df['prediction'] == 'Real']

    percentR = reals.shape[0] * 100 /df.shape[0]
    percentF = 100 - percentR

    return percentR, percentF

def mostCommented():

    postList = []

    # 3 Joins Should Have Read The Rubric Beforehand Lol
    cur.execute("""SELECT Reddit.title, Reddit.num_comments, Preds.prediction, Preds.predVal FROM Preds 
    JOIN The_Onion ON Preds.article = The_Onion.body 
    JOIN Reddit ON The_Onion.link = Reddit.link
    ORDER BY Reddit.num_comments DESC""")

    for c in cur:
        postList.append(c)

    return postList

def mostCommScatter(postList):
    comments = [i[1] for i in postList]
    values = [i[3] for i in postList]

    fig, ax = plt.subplots()
    ax.scatter(comments, values)

    ax.set_xlabel('Number of Comments')
    ax.set_ylabel('Predicted Satire Level')
    ax.set_title('Reddit Comments vs.Predicted Satire Level')


def realSatireByNetwork(idDict):
    labels = list(map(lambda x: x[1], idDict.items()))
    values = []

    for key in idDict:
        values.append(avgPredVal(key))

    fig, ax = plt.subplots()
    ax.set_title("Mean Onion Score by News Source")
    ax.barh(labels, values)
    ax.set_xlabel('Onion Score')
    ax.set_ylabel('Networks')
    ax.set_yticklabels(labels)
    fig.savefig('static/visuals/satire_by_network.svg')

def realFakeByNetwork(idDict):
    labels = list(map(lambda x: x[1], idDict.items()))
    values = []

    for key in idDict:
        values.append(percentRF(key)[1])

    fig, ax = plt.subplots()
    ax.set_title("% Fake Articles by News Source")
    ax.barh(labels, values)
    ax.set_xlabel('% Fake Articles')
    ax.set_ylabel('News Source')
    ax.set_yticklabels(labels)
    fig.savefig('static/visuals/percent_fake_articles_by_network.svg')


def writeCalculations(idDict):
    with open('static/calculations.csv', 'w', encoding='utf-8') as csv_file:
        #create a dictionary to store the values for each news source.
        #Will make writing the CSV file easier.
        data = []

        for k in idDict:
            temp = {}
            temp['News Source'] = idDict[k]
            temp['Average Predicted Satire Value'] = avgPredVal(k)
            r, f = percentRF(k)
            temp['Percent Predicted Real'] = r
            temp['Percent Predicted Fake'] = f

            data.append(temp)

        cols = list(data[0].keys())

        csv_writer = csv.DictWriter(csv_file, fieldnames=cols)

        csv_writer.writeheader()

    for d in data:
        csv_writer.writerow(d)

def makeWordcloud(df, name):

    fakeString = "".join([art for art in df['article']])

    wc = WordCloud(stopwords=STOPWORDS, height=1080, width=1920)

    f_wc = wc.generate(fakeString)

    f_wc.to_file(f'static/visuals/{name}WordCloud.png')


idDict = cur.execute("SELECT id, news_source FROM News_Sources").fetchall()
idDict = {a[0]: a[1] for a in idDict}

real = pd.read_sql_query(f"SELECT article FROM Preds WHERE prediction = 'Real'", conn)

fake = pd.read_sql_query(f"SELECT article FROM Preds WHERE prediction = 'Fake'", conn)

postList = mostCommented()

mostCommScatter(postList)
realFakeByNetwork(idDict)
realSatireByNetwork(idDict)
makeWordcloud(fake, 'fake')
makeWordcloud(real, 'real')

plt.show()