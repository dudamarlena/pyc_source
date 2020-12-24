# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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