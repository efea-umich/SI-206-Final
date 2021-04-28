import pandas as pd
import re
import nltk

progress = 0
# Removing all links from the article text.
def removeLinks(text):
    return re.sub("[^\.][A-Za-z\.\/:]+(?:\.com|\.org|\.gov|\.us|\.edu|\.net|\.co|\.be)(?:\/[\w\/\?\-\!\#]+)?", "", text)


# Removing the 'Featured Via' blurb that sometimes appears at the end of Onion articles.
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

# Removes quoted material from text.
def removeQuotes(text):
    return re.sub(r"\".+\"", "", text)



# Many of the real news articles start with a blurb that includes (REUTERS) -
# This gets rid of it to avoid giving the ML algorithm any giveaways.
def removeArticleStart(text):
    return re.sub('^(?:.+ )?\(\w+\) [-——] ', "", text)


# Removes all occurences of the word Reuters that were not previously removed.
def removeReuters(text):
    return re.sub('.?(?:Reuters|REUTERS)(?:\/\w+.|.)', " ", text)
# Removes anything inside of parantheses.
def removeParens(text):
    return re.sub('\(.+\)', ' ', text)

# Removes weird quotes that are due to formatting and sometimes cause annoying situations.
def removeWeirdQuotes(text):
    return re.sub('[’“‘”\.—–_]', " ", text)

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






def processData(df, cols, out=None):
    for col in cols:
        df[col] = df[col].apply(removeArticleStart).apply(removeQuotes).apply(removeReuters).apply(removeLinks).apply(removeFeaturedVia).apply(
            fixConctracs).apply(removeMultSpc).apply(removeReuters).apply(removeMultSpc).apply(removeParens).apply(stemmize).apply(removeWeirdQuotes)
    if out:
        df.to_csv(out)
    return df
if __name__ == "__main__":
    choice = int(input("Choose an operation\n1. Process both real and fake articles\n2. Process real articles\n3. Process fake articles"))
    if choice == 1:
        t = pd.read_csv('static/Fake.csv')
        processData(t, 'text', 'static/Fake_Cleaned.csv')
        t = pd.read_csv('static/True.csv')
        processData(t, 'text', 'static/True_Cleaned.csv')
    elif choice == 2:
        t = pd.read_csv('static/True.csv')
        processData(t, 'text', 'static/True_Cleaned.csv')
    elif choice == 3:
        t = pd.read_csv('static/Fake.csv')
        processData(t, 'text', 'static/Fake_Cleaned.csv')


