# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oaraque/git/gsi/gsitk/gsitk/preprocess/normalize.py
# Compiled at: 2017-02-22 09:48:52
# Size of source mod 2**32: 523 bytes
"""
Normalize text
"""
import string
from nltk import word_tokenize
from gsitk.preprocess.pprocess_twitter import tokenize

def normalize_text(data):
    noise = set(string.punctuation) - set('¡!¿?,.:')
    noise = {ord(c):None for c in noise}

    def _normalize_text(text):
        t = tokenize(text['text'])
        t = t.lower().translate(noise)
        return word_tokenize(t)

    text_data = data.apply(_normalize_text, axis=1)
    return text_data