# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryan/DH/prosodic/lib/Coda.py
# Compiled at: 2012-12-06 15:11:04
from entity import entity

class Coda(entity):

    def __init__(self, phonemes, lang):
        self.feats = {}
        self.featpaths = {}
        self.lang = lang
        if phonemes:
            self.children = phonemes
        else:
            self.children = []

    def isBranching(self):
        return len(self.children) > 1