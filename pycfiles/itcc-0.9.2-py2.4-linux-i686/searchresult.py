# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/ccs2/searchresult.py
# Compiled at: 2008-04-20 13:19:45
"""store CCS2 search result"""
__revision__ = '0.1'

class SearchResult:
    """store CCS2 search result, include mol, ene, opttimes"""
    __module__ = __name__

    def __init__(self, mol, ene, opttimes):
        self.mol = mol
        self.ene = ene
        self.opttimes = opttimes

    def __cmp__(self, other):
        return cmp(self.ene, other)