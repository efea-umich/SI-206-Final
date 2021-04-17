from wordcloud import STOPWORDS, WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from process_data import DataProcessor
from PIL import Image

dp = DataProcessor()

real, fake = dp.getDatasets()

fakeString = "".join([art for art in fake])

wc = WordCloud(stopwords=STOPWORDS, height=1080, width=1920)

f_wc = wc.generate(fakeString)

f_wc.to_file('static/visualizations/fakeWordCloud.png')

#Moving onto generate a wordcloud for the real articles
realString = "".join([art for art in real])

wc = WordCloud(stopwords=STOPWORDS, height=1080, width=1920)

r_wc = wc.generate(realString)

r_wc.to_file('static/visualizations/realWordCloud.png')