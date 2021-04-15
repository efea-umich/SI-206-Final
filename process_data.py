import matplotlib.pyplot as plt
import pandas as pd
import re

fakeDB = pd.read_csv("Fake.csv")
realDB = pd.read_csv("True.csv")

mnrows = min(fakeDB.shape()[0], realDB.shape()[0])
fakeDB = fakeDB.truncate(after=mnrows - 1)
realDB = realDB.truncate(after=mnrows - 1)

#loop through the tables here

for index, row in realDB.iterrows():
    start_header = "\w+ - \(\w+\)"
    re.sub(start_header, "", row)
