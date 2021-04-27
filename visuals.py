import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv

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
    ax.set_title("Mean Satire Score by News Source")
    ax.barh(labels, values)
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

idDict = cur.execute("SELECT id, news_source FROM News_Sources").fetchall()
idDict = {a[0]: a[1] for a in idDict}




postList = mostCommented()
print(postList)

mostCommScatter(postList)
realFakeByNetwork(idDict)
realSatireByNetwork(idDict)
plt.show()
