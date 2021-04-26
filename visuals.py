import sqlite3
import pandas as pd

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

    cur.execute("""SELECT Reddit.title, The_Onion.pred, The_Onion.predVal FROM Reddit 
    JOIN The_ONION ON Reddit.link = Onion.link 
    ORDER BY Reddit.num_comments DESC""")

    for c in cur:
        postList.append(c)

    return postList[:20]


print(avgPredVal('CNN'))
print(percentRF('CNN'))
print(mostCommented())