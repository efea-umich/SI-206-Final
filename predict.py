from keras.layers import *
from keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pandas as pd
import numpy as np
import json
import pickle
import keras
import tensorflow as tf
from process_data import DataProcessor
import sqlite3
from utils import processData
import csv

def getPreds(df, out=None):
    # GPU won't work without the next three lines
    physical_devices = tf.config.list_physical_devices('GPU')
    if len(physical_devices) > 0:
        tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)
    dp = DataProcessor()

    test_articles = processData(df, ['body']).to_numpy()
    test_articles = list(map(lambda x: x[0], test_articles))

    test_articles_raw = df.to_numpy()
    test_articles_raw = list(map(lambda x: x[0], test_articles_raw))

    with open('./onion_tokenizer.pyc', 'rb') as pickleHand:
        tokenizer = pickle.load(pickleHand)
    assert isinstance(tokenizer, Tokenizer)

    seqs = test_articles
    max_len = dp.getMaxWords()
    seqs = tokenizer.texts_to_sequences(seqs)
    seqs = pad_sequences(seqs, max_len)
    model = keras.models.load_model('static/onion_connoisseur.h5')
    assert isinstance(model, keras.models.Model)
    print(test_articles)
    predVals = model.predict(seqs)
    preds = list(map(lambda x: "Real" if x < 0.75 else "Fake", predVals))
    print(preds)
    if out:
        with open('predictions.csv', 'w', encoding='utf-8') as outHand:
            out = csv.writer(outHand)
            for i in range(0, len(preds)):
                out.writerow([test_articles_raw[i], preds[i], predVals[i]])
    
    return [preds, predVals]

if __name__ == '__main__':
    conn = sqlite3.Connection('static/onion_barn.db')
    df = pd.read_sql_query("SELECT body FROM The_Onion", conn)
    
    getPreds(df)