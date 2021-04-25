from keras.layers import *
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from process_data import DataProcessor
import tensorflow as tf
import numpy as np
import pickle

physical_devices = tf.config.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)


'''what version is this'''

num_words = 200000

dp = DataProcessor()

x, y = dp.getTrainingData()


# Assign token to each word present in headlines
tokenizer = Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n\'`’‘\\', num_words=num_words)
tokenizer.fit_on_texts(x)
max_len = dp.getMaxWords()
trainX = tokenizer.texts_to_sequences(x)
trainX = pad_sequences(trainX, max_len)
indexLen = len(tokenizer.word_index)
with open('onion_tokenizer.pyc', 'wb') as pickleHand:
    pickle.dump(tokenizer, pickleHand)

# Define our deep learning model
model = Sequential([
    Embedding(indexLen+1, 256),
    LSTM(512, dropout=0.2, return_sequences=True),
    LSTM(256, dropout=0.2),
    Dense(1024, activation='relu'),
    Dropout(0.2),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
checkpoint = ModelCheckpoint(
    'models/weights.{epoch:02d}.h5', monitor='val_loss'
)
model.fit(trainX, y, epochs=5, validation_split=0.2, callbacks=[checkpoint])
model.save('./onion_harvester_woah.h5')