from wordcloud import STOPWORDS, WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from process_data import DataProcessor
from PIL import Image

dp = DataProcessor()

real, fake = dp.getDatasets()

#realString = "".join([art for art in real])
fakeString = "".join([art for art in fake])

#print(realString == fakeString)

wc = WordCloud(stopwords=STOPWORDS, height=1080, width=1920)

#r_wc = wc.generate(realString)
f_wc = wc.generate(fakeString)
#r_wc.to_file('static/visualizations/realWordCloud.png')
f_wc.to_file('static/visualizations/fakeWordCloud.png')


