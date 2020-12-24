# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oaraque/git/gsi/gsitk/gsitk/preprocess/simple.py
# Compiled at: 2017-05-03 05:05:40
# Size of source mod 2**32: 1029 bytes
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
    return string.strip().lower()


def normalize_text(data):
    text_data = data['text'].apply(clean_str)
    text_data = text_data.str.split(' ')
    return text_data