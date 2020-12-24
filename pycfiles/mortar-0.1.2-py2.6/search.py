# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mortar/search.py
# Compiled at: 2009-01-14 10:36:41
"""
Stuff to allow building of complicated search specs.
"""

class Operator:

    def __init__(self, *args):
        self.args = args

    def __repr__(self):
        return '<%s:%s>' % (self.__class__.__name__, (',').join([ repr(a) for a in self.args ]))


class AND(Operator):
    pass


class OR(Operator):
    pass


class BinaryOperator:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '<%r %s %r>' % (self.x, self.__class__.__name__, self.y)


class OR(Operator):
    pass


class EQ(Operator):
    pass


class NE(Operator):
    pass


class LT(Operator):
    pass


class GT(Operator):
    pass