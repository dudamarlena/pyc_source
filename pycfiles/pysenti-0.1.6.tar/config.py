# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xuming06/Codes/sentiment-classifier-zh/pysenti/config.py
# Compiled at: 2019-09-21 00:48:26
"""
@author:XuMing（xuming624@qq.com)
@description:
"""
import os
pwd_path = os.path.abspath(os.path.dirname(__file__))
stopwords_path = os.path.join(pwd_path, 'data/stopwords.txt')
sentiment_model_path = os.path.join(pwd_path, 'data/sentiment_model.pkl')
sentiment_dict_path = os.path.join(pwd_path, 'data/sentiment_dict.txt')
conjunction_dict_path = os.path.join(pwd_path, 'data/conjunction_dict.txt')
adverb_dict_path = os.path.join(pwd_path, 'data/adverb_dict.txt')
denial_dict_path = os.path.join(pwd_path, 'data/denial_dict.txt')