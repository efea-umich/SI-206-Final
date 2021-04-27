#import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re

class DataProcessor:
    fakeDB = None
    realDB = None
    maxWords = -1

    def __init__(self):
        fakeDB = pd.read_csv("static/Fake_Cleaned.csv")
        realDB = pd.read_csv("static/True_Cleaned.csv")

        mnrows = int(min(fakeDB.shape[0], realDB.shape[0]))
        mnrows = 6000
        self.fakeDB = fakeDB[:mnrows - 1]["text"]
        self.realDB = realDB[:mnrows - 1]["text"]
        self.maxWords = max(self.fakeDB.apply(lambda x: len(x.split())).max(), self.realDB.apply(lambda x: len(x.split())).max())

    # Gets maximum number of words
    def getMaxWords(self):
        return self.maxWords

    def getTrainingData(self):
        # Merge real and fake into one array and create labels
        x = np.concatenate([self.realDB.to_numpy(), self.fakeDB.to_numpy()])
        y = np.concatenate([np.zeros(self.realDB.shape[0]), np.ones(self.fakeDB.shape[0])])

        # Assign the same random permutation to x and y to mix up array
        p = np.random.permutation(len(x))
        x = x[p]
        y = y[p]
        return (x, y)

    def getDatasets(self):
        return self.realDB, self.fakeDB

if __name__ == "__main__":
    dp = DataProcessor()
    print(len(dp.getData()[0]))
    print(dp.getMaxWords())