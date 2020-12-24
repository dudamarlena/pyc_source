# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugojosebello/Documents/git-repos/sentiment-spanish/sentiment_analysis_spanish/sentiment_analysis.py
# Compiled at: 2020-04-14 11:53:02
# Size of source mod 2**32: 1168 bytes
from cleaner import Cleaner
from keras.preprocessing.sequence import pad_sequences
from keras.models import model_from_json
import pickle

class SentimentAnalysisSpanish:

    def __init__(self):
        self.cleaner = Cleaner()
        self.maxlen = 500
        self.tokenizer = None
        with open('tokenizer.pickle', 'rb') as (handle):
            self.tokenizer = pickle.load(handle)
        json_model_keras = open('model.json', 'r')
        loaded_model_json = json_model_keras.read()
        json_model_keras.close()
        self.loaded_model = model_from_json(loaded_model_json)
        self.loaded_model.load_weights('model.h5')
        self.loaded_model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae', 'accuracy'])

    def sentiment(self, text: str):
        x = self.tokenizer.texts_to_sequences([self.cleaner.clean_text(text)])
        x = pad_sequences(x, padding='post', maxlen=(self.maxlen))
        y_new = self.loaded_model.predict(x)
        return y_new[0][0]