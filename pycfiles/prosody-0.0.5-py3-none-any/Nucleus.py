# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ryan/DH/prosodic/lib/Nucleus.py
# Compiled at: 2012-12-06 15:11:04
from entity import entity

class Nucleus(entity):

    def __init__(self, phonemes, lang):
        self.feats = {}
        self._p_changed = True
        self.featpaths = {}
        self.lang = lang
        if phonemes:
            self.children = phonemes
        else:
            self.children = []
        self.feat('prom.vheight', self.isHigh())

    def isBranching(self):
        return self.isDipthong() or self.isLong()

    def isDipthong(self):
        for phon in self.children:
            if phon.isDipthong():
                return True

        return False

    def isHigh(self):
        for phon in self.children:
            if phon.isHigh():
                return True

        return False

    def isLong(self):
        for phon in self.children:
            if phon.isLong():
                return True

        return False