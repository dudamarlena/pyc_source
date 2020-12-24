# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pygoogleearth\viewextents.py
# Compiled at: 2009-09-26 22:10:50


class ViewExtents(object):

    def __init__(self, comobject):
        self.ge_ve = comobject

    def __getattr__(self, name):
        if name == 'north':
            return self.ge_ve.North
        if name == 'south':
            return self.ge_ve.South
        if name == 'east':
            return self.ge_ve.East
        if name == 'west':
            return self.ge_ve.West
        raise AttributeError