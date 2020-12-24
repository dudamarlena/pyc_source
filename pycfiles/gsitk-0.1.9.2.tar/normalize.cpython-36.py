# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/app/gsitk/preprocess/normalize.py
# Compiled at: 2018-02-19 12:06:36
# Size of source mod 2**32: 559 bytes
"""
Normalize text
"""
import string
from nltk import word_tokenize
from gsitk.preprocess.pprocess_twitter import tokenize
noise = set(string.punctuation) - set('¡!¿?,.:')
noise = {ord(c):None for c in noise}

def _normalize_text(text):
    t = tokenize(text)
    t = t.lower().translate(noise)
    return word_tokenize(t)


def normalize_text(data):
    text_data = data['text'].apply(_normalize_text)
    return text_data


def preprocess(text):
    return _normalize_text(text)