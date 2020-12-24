# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\lquery\extras\mongodb.py
# Compiled at: 2018-08-01 12:20:52
# Size of source mod 2**32: 6537 bytes
from ..func import where, skip, take
from ..query import Query
from ..queryable import Queryable, QueryProvider
from ..expr import BinaryExpr, IndexExpr, ConstExpr, call, parameter, CallExpr, Expr, ParameterExpr, BuildDictExpr, BuildListExpr
from ..expr_builder import to_lambda_expr
from ..expr_utils import get_deep_indexes, require_argument
from ..iterable import PROVIDER as ITERABLE_PROVIDER
from ..iterable import IterableQuery

class MongoDbQuery(Queryable):

    def __init__(self, collection):
        super().__init__(None, PROVIDER)
        self._collection = collection

    @property
    def collection(self):
        return self._collection


class MongoDbQueryImpl:

    def __init__(self, queryable: Queryable):
        self._mongodb_query = queryable.src or queryable
        self._query = None
        self._always_empty = False
        self._filter = {}
        self._skip = None
        self._limit = None
        exprs = []
        for expr in queryable.query.exprs:
            if self._query is None:
                if not self._apply_call(expr):
                    self._build_query()
                if self._query is not None:
                    exprs.append(expr)

        query = self._query or self._build_query()
        self._query = ITERABLE_PROVIDER.create_query(query, Query(*exprs))

    def __iter__(self):
        return iter(self._query)

    def _build_query(self):
        if self._always_empty:
            cursor = []
        else:
            cursor = self._mongodb_query.collection.find(filter=(self._filter),
              skip=(self._skip or 0),
              limit=(self._limit or 0))
        self._query = IterableQuery(cursor)
        return self._query

    def _apply_call(self, expr: CallExpr) -> bool:
        func = expr.func
        if func is where:
            return self._apply_call_where(expr.args[1].value)
        if func is skip:
            return self._apply_call_skip(expr.args[1].value)
        else:
            if func is take:
                return self._apply_call_take(expr.args[1].value)
            return False

    def _apply_call_skip(self, value):
        if self._skip is None:
            self._skip = value
        else:
            self._skip += value
        return True

    def _apply_call_take(self, value):
        if value == 0:
            self._always_empty = True
        else:
            if self._limit is None:
                self._limit = value
            else:
                self._limit = min(self._limit, value)
        return True

    def _apply_call_where(self, predicate):
        if self._limit is not None or self._skip is not None:
            return False
        else:
            lambda_expr = to_lambda_expr(predicate)
            if lambda_expr:
                if len(lambda_expr.args) == 1:
                    return self._apply_call_where_by(lambda_expr.body)
            return False

    def _apply_call_where_by(self, body: Expr):
        if isinstance(body, BinaryExpr):
            return self._apply_call_where_binary(body)
        else:
            return False

    def _apply_call_where_binary(self, body: BinaryExpr):
        left, op, right = body.left, body.op, body.right
        if op == '&':
            if not self._apply_call_where_by(left):
                return False
            if not self._apply_call_where_by(right):
                return False
            return True
        else:
            return self._apply_call_where_compare(left, right, op)

    _SWAPABLE_OP_MAP = {'==':'==', 
     '>':'<=', 
     '<':'>=', 
     '>=':'<', 
     '<=':'>', 
     'in':'-in'}

    def _apply_call_where_compare(self, left, right, op):
        left_is_index_expr = isinstance(left, IndexExpr)
        right_is_index_expr = isinstance(right, IndexExpr)
        if not left_is_index_expr:
            if not right_is_index_expr:
                return False
        if left_is_index_expr:
            if right_is_index_expr:
                return False
        if not left_is_index_expr:
            swaped_op = self._SWAPABLE_OP_MAP.get(op)
            if swaped_op is None:
                return False
            else:
                return self._apply_call_where_compare(right, left, swaped_op)
        else:
            if isinstance(right, ConstExpr):
                value = right.value
            else:
                if isinstance(right, BuildDictExpr):
                    value = right.create()
                else:
                    if isinstance(right, BuildListExpr):
                        value = right.create()
                    else:
                        if isinstance(right, CallExpr):
                            if require_argument(right):
                                return False
                            value = right()
                        else:
                            return False
        if isinstance(value, tuple):
            value = list(value)
        if not isinstance(value, (str, int, dict, list)):
            return False
        value = self._from_op(value, op)
        if value is None:
            return False
        else:
            data = self._filter
            indexes, src_expr = get_deep_indexes(left)
            if not isinstance(src_expr, ParameterExpr):
                return False
            fname = '.'.join(indexes)
            if data.get(fname, value) != value:
                self._always_empty = True
            else:
                data[fname] = value
            return True

    _OP_MAP = {'<':'$lt', 
     '>':'$gt', 
     '<=':'$lte', 
     '>=':'$gte', 
     'in':'$in'}

    def _from_op(self, right_value, op):
        """
        get mongodb query object value by `value` and `op`.

        for example: `(3, '>')` => `{ '$gt': 3 }`
        """
        if op == '==' or op == '-in':
            return right_value
        op = self._OP_MAP.get(op)
        if op is not None:
            return {op: right_value}


class MongoDbQueryProvider(QueryProvider):

    def execute(self, queryable: Queryable):
        return MongoDbQueryImpl(queryable)


PROVIDER = MongoDbQueryProvider()