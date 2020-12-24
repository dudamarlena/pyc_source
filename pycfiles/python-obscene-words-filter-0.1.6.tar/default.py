# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/asyncee/python-obscene-words-filter/obscene_words_filter/default.py
# Compiled at: 2017-01-24 07:20:43
from . import conf
from .words_filter import ObsceneWordsFilter

def get_default_filter():
    return ObsceneWordsFilter(conf.bad_words_re, conf.good_words_re)