# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\lquery\empty.py
# Compiled at: 2018-08-03 12:18:43
# Size of source mod 2**32: 1330 bytes
from .func import NOT_QUERYABLE_FUNCS
from .queryable import Queryable, QueryProvider, ReduceInfo, EMPTY_QUERYS
from .iterable import IterableQueryProvider

class EmptyQuery(Queryable):

    def __init__(self, querys=EMPTY_QUERYS, reason='', **kwargs):
        (super().__init__)(None, PROVIDER, querys, **kwargs)
        self._reason = reason

    def __iter__(self):
        yield from ()
        if False:
            yield None

    @property
    def reason(self):
        return self._reason


class EmptyQueryProvider(IterableQueryProvider):

    def get_reduce_info(self, queryable: EmptyQuery) -> ReduceInfo:
        """
        get reduce info in console.
        """
        info = ReduceInfo(queryable)
        info.set_mode(ReduceInfo.MODE_EMPTY, queryable.reason)
        for expr in queryable.querys.exprs:
            info.add_node(ReduceInfo.TYPE_NOT_EXEC, expr)

        return info

    def execute(self, queryable, call_expr):
        if call_expr.func in NOT_QUERYABLE_FUNCS:
            return super().execute(queryable, call_expr)
        else:
            querys = queryable.querys.then(call_expr)
            return EmptyQuery(querys, queryable.reason)


PROVIDER = EmptyQueryProvider()