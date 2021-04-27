import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv

conn = sqlite3.Connection('static/onion_barn.db')
cur = conn.cursor()

def avgPredVal(db):
    df = pd.read_sql_query(f"SELECT predVal FROM {db}", conn)
    
    return df['predVal'].mean()

def percentRF(db):
    df = pd.read_sql_query(f"SELECT pred FROM {db}", conn)
    
    reals = df[df['pred'] == 'Real']

    percentR = reals.shape[0] * 100 /df.shape[0]
    percentF = 100 - percentR

    return percentR, percentF

def mostCommented():

    postList = []

    cur.execute("""SELECT Reddit.title, Reddit.num_comments, The_Onion.pred, The_Onion.predVal FROM Reddit 
    JOIN The_ONION ON Reddit.link = The_Onion.link 
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

    plt.show()

#Selecting all tables in the database that aren't named 'Reddit'
def getNewsTables(cur, conn):
    tablesList = []

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'Reddit' AND name NOT LIKE 'RF' AND name NOT LIKE 'News_Sources'")
    for c in cur:
        tablesList.append(c[0])
    print(tablesList)
    return tablesList

tablesList = getNewsTables(cur, conn)

with open('static/caulculations.csv', 'w', encoding='utf-8') as csv_file:
    #create a dictionary to store the values for each news source.
    #Will make writing the CSV file easier.
    data = []
    
    for t in range(len(tablesList)):
        temp = {}
        temp['News Source'] = tablesList[t]
        temp['Average Predicted Satire Value'] = avgPredVal(tablesList[t])
        r, f = percentRF(tablesList[t])
        temp['Percent Predicted Real'] = r
        temp['Percent Predicted Fake'] = f

        data.append(temp)

    cols = list(data[0].keys())

    csv_writer = csv.DictWriter(csv_file, fieldnames=cols)
    
    csv_writer.writeheader()
    
    for d in data:
        csv_writer.writerow(d)


postList = mostCommented()
print(postList)

mostCommScatter(postList)