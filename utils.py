import pandas as pd
import re

def removeFeaturedVia(text):
    return re.sub(r'\.[^\.]*\.$', ".", text)

f = pd.read_csv('static/Fake.csv')
f["text"] = f["text"].apply(removeFeaturedVia)
f.to_csv('static/Fake_No_Endings.csv')