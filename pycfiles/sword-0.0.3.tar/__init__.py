# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: buildpy\__init__.py
# Compiled at: 2019-10-04 19:13:24
import os

class CDefinitions(object):
    """
    This class acts as a collection of definitions for a C preprocessor
    """

    def __init__(self):
        self.dmap = {}

    def __len__(self):
        return len(self.dmap)

    def __list__(self):
        return [ (x, y) for x, y in self.dmap.items() ]