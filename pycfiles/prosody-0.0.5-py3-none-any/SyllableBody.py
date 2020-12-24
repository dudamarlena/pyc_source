# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ryan/DH/prosodic/lib/SyllableBody.py
# Compiled at: 2012-12-06 15:11:04
from entity import entity
from Phoneme import Phoneme
from Syllable import Syllable

class SyllableBody(entity, Syllable):

    def __init__(self, onset, rime, lang):
        self.feats = {}
        self.onset = onset
        self.rime = rime
        self.children = []
        self.lang = lang
        self.token = ''
        if self.onset:
            self.children.append(self.onset)
        self.children.append(self.rime)
        self._p_changed = True
        self.featpaths = {}
        self.feat('shape', self.getShape())
        self.feat('prom.weight', self.isHeavy())
        self.feat('prom.vheight', self.rime.nucleus.feature('prom.vheight'))

    def settok(self, tok):
        self.token = tok

    def __repr__(self):
        return '<' + self.classname() + '> [' + str(self) + ']'

    def getShape(self):
        shape = ''
        for phoneme in self.phonemes():
            shape += phoneme.CorV()

        return shape

    def isHeavy(self):
        if not self.rime:
            return None
        else:
            if not self.rime.nucleus:
                return None
            return self.rime.isBranching() or self.rime.nucleus.isBranching()

    def newRimeForSuffix(self, phon):
        nuc = self.rime.nucleus
        if self.rime.coda:
            codaphons = self.rime.coda.phonemes()
        else:
            codaphons = []
        codaphons.append(phon)
        from Coda import Coda
        from Rime import Rime
        coda = Coda(codaphons)
        return Rime(nuc, coda)