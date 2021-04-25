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


print(avgPredVal('CNN'))
print(percentRF('CNN'))