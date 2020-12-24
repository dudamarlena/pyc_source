# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/ccs2/base.py
# Compiled at: 2008-04-20 13:19:45
__revision__ = '$Rev$'

class Base:
    __module__ = __name__

    def __init__(self, _=None):
        pass

    def getr6s(self, loopatoms, is_chain=False):
        if is_chain:
            doubleloop = tuple(loopatoms)
            count = len(doubleloop) - 6
        else:
            doubleloop = tuple(loopatoms) * 2
            count = len(doubleloop) / 2
        for i in range(count):
            yield tuple([ (x,) for x in doubleloop[i:i + 7] ])


def _test():
    base = Base()
    print tuple(base.getr6s(range(10)))


if __name__ == '__main__':
    _test()