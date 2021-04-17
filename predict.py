from keras.layers import *
from keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pandas as pd
import numpy as np
import json
import pickle
import keras
import tensorflow as tf
from process_data import DataProcessor

# GPU won't work without the next three lines
physical_devices = tf.config.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)

dp = DataProcessor()
real, fake = dp.getDatasets()

with open('./onion_tokenizer.pyc', 'rb') as pickleHand:
    tokenizer = pickle.load(pickleHand)
assert isinstance(tokenizer, Tokenizer)

seqs = [""]
max_len = dp.getMaxWords()

seqs = tokenizer.texts_to_sequences(seqs)
seqs = pad_sequences(seqs, max_len)
model = keras.models.load_model('static/onion_harvester_woah.h5')
assert isinstance(model, keras.models.Model)
print(model.predict(seqs))