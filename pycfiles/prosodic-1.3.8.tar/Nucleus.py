# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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