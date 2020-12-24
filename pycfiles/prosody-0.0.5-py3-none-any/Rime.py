# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ryan/DH/prosodic/lib/Rime.py
# Compiled at: 2012-12-06 15:11:04
from entity import entity

class Rime(entity):

    def __init__(self, nucleuscoda, lang):
        self.feats = {}
        self.nucleus = nucleuscoda[0]
        self.coda = nucleuscoda[1]
        self.featpaths = {}
        self.lang = lang
        self.children = []
        if self.nucleus:
            self.children.append(self.nucleus)
        else:
            self.broken = True
        if self.coda:
            self.children.append(self.coda)

    def isBranching(self):
        return self.hasCoda()

    def hasCoda(self):
        if self.coda.children:
            return True
        else:
            return False