import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re

def removeArticleStart(text):
    return re.sub(r'^[\S +]+ \(\w+\) - ', "", text)


class DataProcessor:
    fakeDB = None
    realDB = None
    maxWords = -1

    def __init__(self):
        fakeDB = pd.read_csv("static/Fake.csv")
        realDB = pd.read_csv("static/True.csv")

        mnrows = min(fakeDB.shape[0], realDB.shape[0])
        self.fakeDB = fakeDB.truncate(after=mnrows - 1)["text"].apply(removeArticleStart).apply(lambda x: x[:400])
        self.realDB = realDB.truncate(after=mnrows - 1)["text"].apply(removeArticleStart).apply(lambda x: x[:400])
        self.maxWords = max(fakeDB["text"].apply(lambda x: len(x.split())).max(), realDB["text"].apply(lambda x: len(x.split())).max())

    def getMaxWords(self):
        return self.maxWords

    def getDatasets(self):
        return (self.realDB, self.fakeDB)

    def getTrainingData(self):
        # Merge real and fake into one array and create labels
        x = np.concatenate([self.realDB.to_numpy(), self.fakeDB.to_numpy()])
        y = np.concatenate([np.zeros(self.realDB.shape[0]), np.ones(self.fakeDB.shape[0])])

        # Assign the same random permutation to x and y to mix up array
        p = np.random.permutation(len(x))
        x = x[p]
        y = y[p]
        return (x, y)



