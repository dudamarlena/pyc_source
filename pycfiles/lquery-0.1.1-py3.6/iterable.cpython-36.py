# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\lquery\iterable.py
# Compiled at: 2018-08-03 12:12:24
# Size of source mod 2**32: 2379 bytes
from collections import Iterable
from typeguard import typechecked
from .func import NOT_QUERYABLE_FUNCS
from .queryable import Queryable, QueryProvider, IQueryable, ReduceInfo, EMPTY_QUERYS

def get_func(call_expr):
    expr = call_expr
    args = [expr.value for expr in expr.args[1:]]
    func = expr.func
    assert expr.args and not expr.kwargs

    def _func(src):
        return func(src, *args)

    return _func


class IterableQuery(Queryable):

    @typechecked
    def __init__(self, items):
        super().__init__(None, PROVIDER, EMPTY_QUERYS)
        self._items = items

    def __iter__(self):
        return iter(self._items)

    def __str__(self):
        return f"Queryable({str(self._items)})"


class IterableQuery2(Queryable):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._reduced_func = None

    def __iter__(self):
        reduced_func = self._compile()
        return iter(reduced_func(self.src))

    def _compile(self):
        """
        compile the query as memory call.
        """
        if self._reduced_func is None:
            self._reduced_func = get_func(self.expr)
        return self._reduced_func


class IterableQueryProvider(QueryProvider):

    def create_query(self, src, query=None):
        queryable = IterableQuery(src)
        if query:
            for expr in query.exprs:
                queryable = self.execute(queryable, expr)

        return queryable

    def get_reduce_info(self, queryable):
        """
        get reduce info in console.
        """
        info = super().get_reduce_info(queryable)
        if queryable.expr:
            info.add_node(ReduceInfo.TYPE_MEMORY, queryable.expr)
        return info

    def execute(self, queryable: IQueryable, call_expr):
        if call_expr.func in NOT_QUERYABLE_FUNCS:
            func = get_func(call_expr)
            return func(queryable)
        else:
            querys = queryable.querys.then(call_expr)
            return IterableQuery2(queryable, self, querys)


PROVIDER = IterableQueryProvider()