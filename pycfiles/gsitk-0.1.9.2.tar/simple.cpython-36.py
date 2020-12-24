# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/app/gsitk/preprocess/simple.py
# Compiled at: 2018-02-19 13:25:50
# Size of source mod 2**32: 1050 bytes
"""
    Tokenization and string cleaning. Modified from:
    https://github.com/dennybritz/cnn-text-classification-tf/blob/master/data_helpers.py
"""
import re

def clean_str(string):
    string = re.sub("[^A-Za-z0-9().,!?\\'\\`]", ' ', string)
    string = re.sub('[0-9]+', ' num ', string)
    string = re.sub("\\'s", " 's", string)
    string = re.sub("\\'ve", " 've", string)
    string = re.sub("n\\'t", " n't", string)
    string = re.sub("\\'re", " 're", string)
    string = re.sub("\\'d", " 'd", string)
    string = re.sub("\\'ll", " 'll", string)
    string = re.sub('\\.', ' . ', string)
    string = re.sub(',', ' , ', string)
    string = re.sub('!', ' ! ', string)
    string = re.sub('\\(', ' ( ', string)
    string = re.sub('\\)', ' ) ', string)
    string = re.sub('\\?', ' ? ', string)
    string = re.sub('\\s{2,}', ' ', string)
    return string.strip().lower().split(' ')


def normalize_text(data):
    text_data = data['text'].apply(clean_str)
    return text_data


def preprocess(text):
    return clean_str(text)