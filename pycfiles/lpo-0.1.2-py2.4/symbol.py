# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/lpo/symbol.py
# Compiled at: 2008-07-30 12:52:46
from sqlalchemy import orm
import tables as ta

class Symbol(object):
    """
    A symbol object.
    Has a name and an arity.

    >>> symbol = Symbol('one', 2)
    >>> symbol.name
    'one'
    >>> symbol.arity
    2
    """
    __module__ = __name__

    def __init__(self, name, arity):
        """
        """
        self.name = name
        self.arity = arity


orm.mapper(Symbol, ta.symbols)