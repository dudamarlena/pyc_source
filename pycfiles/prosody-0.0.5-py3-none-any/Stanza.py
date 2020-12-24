# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: lib/Stanza.py
# Compiled at: 2019-06-02 18:11:38
from entity import entity
from Line import Line

class Stanza(entity):

    def givebirth(self):
        line = Line()
        line.ignoreMe = False
        return line

    def __repr__(self):
        num = self.parent.children.index(self) + 1
        return '<Stanza ' + str(num) + '> (' + str(len(self.children)) + ' lines)'