# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/ccs2/crown.py
# Compiled at: 2008-04-20 13:19:45
"""Crown ether"""
from itcc.CCS2.tors import TorsSet
__revision__ = '$Rev$'

class TSCrown(TorsSet):
    __module__ = __name__

    def vary(item):
        doubledata = item * 2
        minusdoubledata = tuple([ -x for x in doubledata ])
        size = len(item)
        for i in range(0, size, 3):
            yield doubledata[i:i + size]
            yield doubledata[i + size:i:-1]
            yield minusdoubledata[i:i + size]
            yield minusdoubledata[i + size:i:-1]

    vary = staticmethod(vary)