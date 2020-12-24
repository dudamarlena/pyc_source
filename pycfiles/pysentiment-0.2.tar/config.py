# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/xuming06/Codes/sentiment-classifier-zh/pysenti/config.py
# Compiled at: 2019-09-21 00:48:26
__doc__ = '\n@author:XuMing（xuming624@qq.com)\n@description:\n'
import os
pwd_path = os.path.abspath(os.path.dirname(__file__))
stopwords_path = os.path.join(pwd_path, 'data/stopwords.txt')
sentiment_model_path = os.path.join(pwd_path, 'data/sentiment_model.pkl')
sentiment_dict_path = os.path.join(pwd_path, 'data/sentiment_dict.txt')
conjunction_dict_path = os.path.join(pwd_path, 'data/conjunction_dict.txt')
adverb_dict_path = os.path.join(pwd_path, 'data/adverb_dict.txt')
denial_dict_path = os.path.join(pwd_path, 'data/denial_dict.txt')