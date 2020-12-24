# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/queryfilter.py
# Compiled at: 2015-10-11 07:17:06


class Op(object):

    def last(self):
        return

    def __str__(self):
        return self.__repr__()


class QueryFilter(Op):

    def __init__(self, lhs, operator=None, rhs=None):
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs

    def last(self):
        return self

    def __repr__(self):
        return ('{me.lhs} {me.operator} {me.rhs}').format(me=self)


class BitOp(Op):

    def __init__(self, children=None):
        if children is not None:
            self.children = children
        else:
            self.children = []
        return

    def append(self, _filter):
        self.children.append(_filter)

    def last(self):
        return self.children[(-1)].last()

    def __getitem__(self, i):
        return self.children[i]

    def __len__(self):
        return len(self.children)


class OrOp(BitOp):

    def __repr__(self):
        return (' or ').join(map(unicode, self.children))


class AndOp(BitOp):

    def __repr__(self):
        return (' and ').join(map(unicode, self.children))