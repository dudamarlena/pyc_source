# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/textrankr/sentence.py
# Compiled at: 2019-07-20 08:55:20
# Size of source mod 2**32: 417 bytes
from collections import Counter
from konlpy.tag import Okt

class Sentence(object):
    okt = Okt()

    def __init__(self, text, index=0):
        self.index = index
        self.text = text.strip()
        self.tokens = self.okt.phrases(self.text)
        self.bow = Counter(self.tokens)

    def __str__(self):
        return self.text

    def __hash__(self):
        return self.index