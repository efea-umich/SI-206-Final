import pandas as pd
import re
import nltk

progress = 0
# Removing all links from the article text.
def removeLinks(text):
    return re.sub("[^\.][A-Za-z\.\/:]+(?:\.com|\.org|\.gov|\.us|\.edu|\.net|\.co|\.be)(?:\/[\w\/\?\-\!\#]+)?", "", text)


# Removing the 'Featured Via' blurb tahat sometimes appears at the end of Onion articles.
def removeFeaturedVia(text):
    t = re.sub('[Pp]hoto by.+$', '', text)
    return re.sub('[Ff]eatured [Ii]m.+$', '', t)


# Fixes all occurences of multi-spaces, replacing them with a single space.
def removeMultSpc(text):
    return re.sub('\s+', ' ', text)


# The dataset had contractions with a space in the middle instead of an apostrophe.
# This function replaces the space in a contraction with an apostrophe.
def fixConctracs(text):
    return re.sub(r" (s|nt|t)\b", r"'\1", text)


# Reads the data from Fake.csv and applies the transformations.
f = pd.read_csv('static/Fake.csv')
f["text"] = f["text"].apply(removeLinks).apply(removeFeaturedVia).apply(fixConctracs).apply(removeMultSpc)

# Writes a new .csv file of the cleaned data.
f.to_csv('static/Fake_Cleaned.csv')


# Many of the real news articles start with a blurb that includes (REUTERS) -
# This gets rid of it to avoid giving the ML algorithm any giveaways.
def removeArticleStart(text):
    return re.sub('^(?:.+ )?\(\w+\) [-——] ', "", text)


# Removes all occurences of the word Reuters that were not previously removed.
def removeReuters(text):
    return re.sub('.?(?:Reuters|REUTERS)(?:\/\w+.|.)', " ", text)

def removeParens(text):
    return re.sub('\(.+\)', ' ', text)

def stemmize(text):
    global progress
    t = text.split()
    ws = []
    stemmer = nltk.PorterStemmer()
    for w in t:
        ws.append(stemmer.stem(w))
    progress += 1
    print(f'Stemmizing element {progress}', end='\r')
    return ' '.join(ws)


# Reads the data from True.csv and applies the transformations.
t = pd.read_csv('static/True.csv')
print(len(t))
# This time, to the titles as well, since many have Reuters in them.


def processData(df, col, out=None):
    df[col] = df[col].apply(removeArticleStart).apply(removeReuters).apply(removeLinks).apply(removeFeaturedVia).apply(
        fixConctracs).apply(removeMultSpc).apply(removeReuters).apply(removeMultSpc).apply(removeParens).apply(stemmize)
    if out:
        df.to_csv(out)
    return df
# Writes a new .csv file of the cleaned data.
#processData(t, 'text', 'static/True_Cleaned.csv')
