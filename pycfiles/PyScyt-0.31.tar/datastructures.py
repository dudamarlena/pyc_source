# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/scxml/datastructures.py
# Compiled at: 2011-11-01 15:53:09
__doc__ = '\nCreated on Jan 4, 2010\n\n@author: johan\n'

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