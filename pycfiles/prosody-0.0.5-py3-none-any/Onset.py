# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ryan/DH/prosodic/lib/Onset.py
# Compiled at: 2012-12-06 15:11:04
from entity import entity

class Onset(entity):

    def __init__(self, phonemes, lang):
        self.feats = {}
        self._p_changed = True
        self.featpaths = {}
        self.lang = lang
        if phonemes:
            self.children = phonemes
        else:
            self.children = []

    def isBranching(self):
        return len(self.children) > 1