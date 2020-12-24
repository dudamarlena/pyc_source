# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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