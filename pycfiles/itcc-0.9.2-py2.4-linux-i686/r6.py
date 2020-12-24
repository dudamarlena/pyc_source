# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/ccs2/r6.py
# Compiled at: 2008-04-20 13:19:45
from itertools import chain
__all__ = [
 'R6']
__revision__ = '$Rev$'

class R6:
    __module__ = __name__

    def __init__(self, data):
        assert len(data) == 7
        self.data = tuple(data)

    def kind(self):
        return tuple([ len(node) for node in self.data ])

    def needshakenodes(self):
        return tuple(chain(*self.data[1:-1]))