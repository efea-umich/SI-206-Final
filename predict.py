from keras.layers import *
from keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pandas as pd
import numpy as np
import json
import pickle
import keras

# GPU won't work without the next three lines
physical_devices = tf.config.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)


with open('./onion_tokenizer.pyc', 'rb') as pickleHand:
    tokenizer = pickle.load(pickleHand)
assert isinstance(tokenizer, Tokenizer)

seqs = ["More than 44 million Americans share a collective $1.5 trillion in student debt, and that number only continues to grow due to skyrocketing tuition prices and high interest rates. Fortunately, President Biden just signed an executive order that’s going to make life a lot easier for Americans seeking college degrees: the government will now give every American a free minor in Digital Humanities from SUNY Oswego.  Awesome!   In a press conference earlier today, Biden announced that all U.S. citizens over the age of 18 will soon receive a diploma certifying the completion of 18 Digital Humanities credits at SUNY Oswego. With millions of Americans struggling to make payments on their student loans, a free minor that shows they’ve completed courses such as Digital Imagery Fundamentals and Ethics And Social Policy In The Digital Age will prevent our next generation from getting stuck with the kind of crippling debt that the generation before them endured.   “Students who would have taken out thousands of dollars in loans for a college education can now save their money instead and use their Digital Humanities minor to help secure job opportunities involving skills such as digital text analysis, digital mapping, and web design,” said the president. “At the very least, these minors should qualify all Americans for professional internships, which, while not full time jobs, would definitely provide the on-the-job experience and networking necessary to build a career in the field.”  If this wasn’t already great enough, Biden went on to say that he’ll be helping out those who’ve already amassed college debt by giving them a Dean’s List certificate stating that their cumulative GPA in their Digital Humanities minor was at least a 3.8, and by presenting an award called “The Mark C. Heller Prize For Outstanding Work In Digital Humanities” to Americans with more than $100,000 in student loans.  This is so great! A free Digital Humanities minor from one of the top SUNY satellite campuses is going to go such a long way towards helping the many Americans who would have otherwise gone to college only to find themselves saddled with terrible credit scores and payments they just couldn’t make. Well done, President Biden!"]
max_len = 200

seqs = tokenizer.texts_to_sequences(seqs)
seqs = pad_sequences(seqs, max_len)
model = keras.models.load_model('./onion_harvester_woah.h5')
assert isinstance(model, keras.models.Model)

print(model.predict(seqs))