import pandas as pd
import re



def removeLinks(text):
    return re.sub("[^\.][A-Za-z\.\/:]+(?:\.com|\.org|\.gov|\.us|\.edu|\.net|\.co|\.be)(?:\/[\w\/\?\-\!\#]+)?", "", text)

def removeFeaturedVia(text):
    #return re.sub('(\w+)\.(\w+)', '\1. \2', text)
    #return re.sub(r'\.[^\.]*\.$', ".", text)
    return re.sub('[Ff]eatured [Ii]m.+$', '', text)

def removeMultSpc(text):
    return re.sub('\s+', ' ', text)

def fixConctracs(text):
    return re.sub(r" (s|nt|t)\b", r"'\1", text)

f = pd.read_csv('static/Fake.csv')
f["text"] = f["text"].apply(removeLinks).apply(removeFeaturedVia).apply(fixConctracs).apply(removeMultSpc)
f.to_csv('static/Fake_Cleaned.csv')

def removeArticleStart(text):
    return re.sub('^(?:.+ )?\(\w+\) - ', "", text)

def removeReuters(text):
    return re.sub('.?(?:Reuters|REUTERS)(?:\/\w+.|.)', " ", text)

t = pd.read_csv('static/True.csv')
t["text"] = t["text"].apply(removeArticleStart).apply(removeReuters).apply(removeLinks).apply(removeFeaturedVia).apply(fixConctracs).apply(removeMultSpc)
t["title"] = t["title"].apply(removeReuters).apply(removeMultSpc)
t.to_csv('static/True_Cleaned.csv')