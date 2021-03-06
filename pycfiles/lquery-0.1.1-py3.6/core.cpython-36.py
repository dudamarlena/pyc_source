# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\lquery\extras\mongodb\core.py
# Compiled at: 2018-08-03 15:13:20
# Size of source mod 2**32: 7525 bytes
import copy
from ...func import where, skip, take
from ...queryable import Queryable, QueryProvider, ReduceInfo, Querys, EMPTY_QUERYS
from ...expr import BinaryExpr, IndexExpr, ValueExpr, CallExpr, Expr, AttrExpr, ParameterExpr, BuildDictExpr, BuildListExpr
from ...expr.builder import to_func_expr
from ...expr.utils import get_deep_names, require_argument
from ...expr.visitor import DefaultExprVisitor
from ...empty import PROVIDER as EMPTY_PROVIDER
from ...empty import EmptyQuery
from ...iterable import PROVIDER as ITERABLE_PROVIDER
from ...iterable import IterableQuery
from .._common import NotSupportError, AlwaysEmptyError
from .options import QueryOptions, QueryOptionsUpdater
VISITOR = DefaultExprVisitor()

class MongoDbQuery(Queryable):

    def __init__(self, collection, *, src=None, query_options=None, querys=EMPTY_QUERYS):
        super().__init__(src, PROVIDER, querys)
        self._collection = collection
        self._query_options = query_options or QueryOptions()

    def __str__(self):
        return f"Queryable({self._collection})"

    def __iter__(self):
        cursor = self._query_options.get_cursor(self._collection)
        yield from cursor
        if False:
            yield None

    @property
    def collection(self):
        return self._collection

    @property
    def query_options(self):
        return self._query_options


class MongoDbQueryImpl:

    def __init__(self, query_options):
        self._accept_sql_query = True
        self._query = None
        self._always_empty = False
        self._query_options = query_options

    @property
    def always_empty(self):
        return self._always_empty

    def apply_call(self, expr: CallExpr) -> bool:
        func = expr.func
        try:
            if func is where:
                self._apply_call_where(expr.args[1].value)
            else:
                if func is skip:
                    self._apply_call_skip(expr.args[1].value)
                elif func is take:
                    self._apply_call_take(expr.args[1].value)
            return True
        except NotSupportError:
            return False
        except AlwaysEmptyError as always_empty:
            self._always_empty = always_empty
            return False

    def _apply_call_skip(self, value):
        QueryOptionsUpdater.add_skip(value).apply(self._query_options)

    def _apply_call_take(self, value):
        if value == 0:
            raise AlwaysEmptyError(f"only take {value} item")
        QueryOptionsUpdater.add_limit(value).apply(self._query_options)

    def _apply_call_where(self, predicate):
        if self._query_options.limit is not None or self._query_options.skip is not None:
            raise NotSupportError
        lambda_expr = to_func_expr(predicate)
        if lambda_expr:
            if len(lambda_expr.args) == 1:
                updater = self._get_updater_by_call_where(lambda_expr.body)
                updater.apply(self._query_options)
                return
        raise NotSupportError

    def _get_updater_by_call_where(self, body: Expr):
        if isinstance(body, BinaryExpr):
            return self._get_updater_by_call_where_binary(body)
        raise NotSupportError

    def _get_updater_by_call_where_binary(self, body: BinaryExpr):
        left, op, right = body.left.accept(VISITOR), body.op, body.right.accept(VISITOR)
        if op in ('&', 'and'):
            lupdater = self._get_updater_by_call_where(left)
            rupdater = self._get_updater_by_call_where(right)
            return lupdater & rupdater
        else:
            return self._get_updater_by_call_where_compare(left, right, op)

    _SWAPABLE_OP_MAP = {'==':'==', 
     '>':'<', 
     '<':'>', 
     '>=':'<=', 
     '<=':'>=', 
     'in':'-in'}

    def _get_updater_by_call_where_compare(self, left, right, op):
        left_is_prop_expr = isinstance(left, (IndexExpr, AttrExpr))
        right_is_prop_expr = isinstance(right, (IndexExpr, AttrExpr))
        if not left_is_prop_expr:
            if not right_is_prop_expr:
                raise NotSupportError
        if left_is_prop_expr:
            if right_is_prop_expr:
                raise NotSupportError
        if not left_is_prop_expr:
            swaped_op = self._SWAPABLE_OP_MAP.get(op)
            if swaped_op is None:
                raise NotSupportError
            return self._get_updater_by_call_where_compare(right, left, swaped_op)
        else:
            if isinstance(right, ValueExpr):
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
                                raise NotSupportError
                            value = right()
                        else:
                            raise NotSupportError
                        if isinstance(value, tuple):
                            value = list(value)
                        if not isinstance(value, (str, int, dict, list)):
                            raise NotSupportError
                    value = self._from_op(value, op)
                    if value is None:
                        raise NotSupportError
                indexes, src_expr = get_deep_names(left)
                if not isinstance(src_expr, ParameterExpr):
                    raise NotSupportError
            fname = '.'.join(indexes)
            updater = QueryOptionsUpdater.add_filter_field(fname, value)
            return updater

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
        else:
            op = self._OP_MAP.get(op)
            if op is None:
                raise NotSupportError
            return {op: right_value}


class MongoDbQueryProvider(QueryProvider):

    def get_reduce_info(self, queryable):
        """
        get reduce info in console.
        """
        info = super().get_reduce_info(queryable)
        if queryable.expr:
            info.add_node(ReduceInfo.TYPE_SQL, queryable.expr)
        return info

    def execute(self, queryable, query_expr):
        if query_expr.func in (where, skip, take):
            query_options = copy.deepcopy(queryable.query_options)
            querys = queryable.querys.then(query_expr)
            impl = MongoDbQueryImpl(query_options)
            apply = impl.apply_call(query_expr)
            if impl.always_empty:
                return EmptyQuery(querys, impl.always_empty.reason)
            if apply:
                return MongoDbQuery((queryable.collection), src=queryable, query_options=query_options, querys=querys)
        return super().execute(queryable, query_expr)


PROVIDER = MongoDbQueryProvider()