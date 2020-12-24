# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/golem/db/resultlist.py
# Compiled at: 2008-08-22 15:02:55
"""Golem resultlist class.

Ties a series of results to the file they came from.

>>> x = resultlist(range(10), filename="test.xml")
>>> print x
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> print x.filename
test.xml
"""

class resultlist(list):
    __module__ = __name__

    def __init__(self, seq, filename=None):
        list.__init__(self, seq)
        self.filename = filename


def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _test()