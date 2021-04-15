from keras.layers import *
from keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle
'''what version is this'''

num_words = 75000


onion, real = ()

x = np.concatenate([onion, real])
y = np.concatenate([np.ones(onion.shape), np.zeros(real.shape)])

print(x[15000])
# Assign the same random permutation to x (headlines) and y (labels)
p = np.random.permutation(len(x))
x = x[p]
y = y[p]

# Assign token to each word present in headlines
tokenizer = Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n\'`’‘\\')
tokenizer.fit_on_texts(x)
max_len = 200
trainX = tokenizer.texts_to_sequences(x)
trainX = pad_sequences(trainX, max_len)
indexLen = len(tokenizer.word_index)
with open('onion_tokenizer.pyc', 'wb') as pickleHand:
    pickle.dump(tokenizer, pickleHand)

# Define our deep learning model
model = Sequential([
    Embedding(indexLen+1, 20),
    LSTM(512, dropout=0.2, return_sequences=True),
    LSTM(256, dropout=0.2),
    Dense(1024, activation='relu'),
    Dropout(0.2),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(trainX, y, epochs=2, validation_split=0.2)
model.save('./onion_harvester_woah.h5')