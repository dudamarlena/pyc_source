# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/squidnet/squidtypereg.py
# Compiled at: 2010-04-07 08:54:00
"""
SquidType register that houses all of the different types in a global dictionary.
"""
__all__ = ('squidtypes', )

class SquidTypeRegister(object):
    mapping = {}

    def register(self, *squidtypes):
        for squidtype in squidtypes:
            self.mapping[squidtype.clssquidtype()] = squidtype


squidtypes = SquidTypeRegister()