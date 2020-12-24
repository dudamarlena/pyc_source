# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/scxml/datastructures.py
# Compiled at: 2011-11-01 15:53:09
"""
Created on Jan 4, 2010

@author: johan
"""

class OrderedSet(list):

    def delete(self, elem):
        try:
            self.remove(elem)
        except ValueError:
            pass

    def member(self, elem):
        return elem in self

    def isEmpty(self):
        return len(self) == 0

    def add(self, elem):
        if elem not in self:
            self.append(elem)

    def clear(self):
        self.__init__()