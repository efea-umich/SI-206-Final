import pandas as pd
import re

def removeLinks(text):
    return re.sub("[^\.][A-Za-z\.\/:]+(?:\.com|\.org|\.gov|\.us|\.edu|\.net|\.co|\.be)\/[\w\/\?\-]+", "", text)

def removeFeaturedVia(text):
    #return re.sub('(\w+)\.(\w+)', '\1. \2', text)
    return re.sub(r'\.[^\.]*\.$', ".", text)

def removeMultSpc(text):
    return re.sub('\s+', ' ', text)

f = pd.read_csv('static/Fake.csv')
f["text"] = f["text"].apply(removeLinks).apply(removeFeaturedVia).apply(removeMultSpc)
f.to_csv('static/Fake_Cleaned.csv')