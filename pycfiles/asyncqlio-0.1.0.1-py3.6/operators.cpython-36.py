# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncqlio/orm/operators.py
# Compiled at: 2017-11-29 06:02:28
# Size of source mod 2**32: 9914 bytes
"""
Classes for operators returned from queries.
"""
import abc, functools, itertools, typing
from asyncqlio.orm.schema import column as md_column

class OperatorResponse:
    __doc__ = '\n    A storage class for the generated SQL from an operator.\n    '
    __slots__ = ('sql', 'parameters')

    def __init__(self, sql: str, parameters: dict):
        """
        :param sql: The generated SQL for this operator.
        :param parameters: A dict of parameters to use for this response.
        """
        self.sql = sql
        self.parameters = parameters
        if self.parameters is None:
            self.parameters = {}


def requires_bop(func) -> 'typing.Callable[[BaseOperator, BaseOperator], typing.Any]':
    """
    A decorator that marks a magic method as requiring another BaseOperator.

    :param func: The function to decorate.
    :return: A function that returns NotImplemented when the class required isn't specified.
    """

    @functools.wraps(func)
    def inner(self, other):
        if not isinstance(other, BaseOperator):
            return NotImplemented
        else:
            return func(self, other)

    return inner


class BaseOperator(abc.ABC):
    __doc__ = '\n    The base operator class.\n    '

    def get_param(self, emitter: typing.Callable[([str], str)], counter: itertools.count) -> typing.Tuple[(str, str)]:
        """
        Gets the next parameter.

        :param emitter: A function that emits a parameter name that can be formatted in a SQL query.
        :param counter: The counter for parameters.
        """
        name = 'param_{}'.format(next(counter))
        return (emitter(name), name)

    @abc.abstractmethod
    def generate_sql(self, emitter: typing.Callable[([str], str)], counter: itertools.count) -> OperatorResponse:
        """
        Generates the SQL for an operator.

        Parameters must be generated using the emitter callable.

        :param emitter: A callable that can be used to generate param placeholders in a query.
        :param counter: The current "parameter number".
        :return: A :class:`.OperatorResponse` representing the result.

        .. warning::
            The param name and the param can be empty if none is to be returned.
        """
        pass

    @requires_bop
    def __and__(self, other: 'BaseOperator'):
        if isinstance(self, And):
            self.operators.append(other)
            return self
        else:
            if isinstance(other, And):
                other.operators.append(self)
                return other
            return And(self, other)

    @requires_bop
    def __or__(self, other: 'BaseOperator'):
        if isinstance(self, Or):
            self.operators.append(other)
            return self
        else:
            if isinstance(other, Or):
                other.operators.append(self)
                return other
            return Or(self, other)

    __rand__ = __and__
    __ror__ = __or__


class And(BaseOperator):
    __doc__ = '\n    Represents an AND operator in a query.\n\n    This will join multiple other :class:`.BaseOperator` objects together.\n    '

    def __init__(self, *ops: 'BaseOperator'):
        self.operators = list(ops)

    def generate_sql(self, emitter: typing.Callable[([str], str)], counter: itertools.count):
        final = []
        vals = {}
        for op in self.operators:
            response = op.generate_sql(emitter, counter)
            final.append(response.sql)
            vals.update(response.parameters)

        fmt = '({})'.format(' AND '.join(final))
        res = OperatorResponse(fmt, vals)
        return res


class Or(BaseOperator):
    __doc__ = '\n    Represents an OR operator in a query.\n\n    This will join multiple other :class:`.BaseOperator` objects together.\n    '

    def __init__(self, *ops: 'BaseOperator'):
        self.operators = list(ops)

    def generate_sql(self, emitter: typing.Callable[([str], str)], counter: itertools.count):
        final = []
        vals = {}
        for op in self.operators:
            response = op.generate_sql(emitter, counter)
            final.append(response.sql)
            vals.update(response.parameters)

        fmt = '({})'.format(' OR '.join(final))
        return OperatorResponse(fmt, vals)


class Sorter(BaseOperator, metaclass=abc.ABCMeta):
    __doc__ = '\n    A generic sorter operator, for use in ORDER BY.\n    '

    def __init__(self, *columns: 'md_column.Column'):
        self.cols = columns

    @property
    @abc.abstractmethod
    def sort_order(self):
        """
        The sort order for this row; ASC or DESC.
        """
        pass

    def generate_sql(self, emitter: typing.Callable[([str], str)], counter: itertools.count):
        names = ', '.join(col.alias_name(quoted=True) for col in self.cols)
        sql = '{} {}'.format(names, self.sort_order)
        return OperatorResponse(sql, {})


class AscSorter(Sorter):
    sort_order = 'ASC'


class DescSorter(Sorter):
    sort_order = 'DESC'


class ColumnValueMixin(object):
    __doc__ = '\n    A mixin that specifies that an operator takes both a Column and a Value as arguments.\n\n    .. code-block:: python3\n\n        class MyOp(BaseOperator, ColumnValueMixin):\n            ...\n\n        # myop is constructed MyOp(col, value)\n    '

    def __init__(self, column: 'md_column.Column', value: typing.Any):
        self.column = column
        self.value = value


class BasicSetter(BaseOperator, ColumnValueMixin, metaclass=abc.ABCMeta):
    __doc__ = '\n    Represents a basic setting operation. Used for bulk queries.\n    '

    @property
    @abc.abstractmethod
    def set_operator(self) -> str:
        """
        :return: The "setting" operator to use when generating the SQL.
        """
        pass

    def generate_sql(self, emitter: typing.Callable[([str], str)], counter: itertools.count):
        param_name, name = self.get_param(emitter, counter)
        params = {name: self.value}
        sql = '{0} = {0} {1} {2}'.format(self.column.quoted_name, self.set_operator, param_name)
        return OperatorResponse(sql, params)


class ValueSetter(BasicSetter):
    __doc__ = '\n    Represents a value setter (``col = 1``).\n    '
    set_operator = '='

    def generate_sql(self, emitter: typing.Callable[([str], str)], counter: itertools.count):
        param_name, name = self.get_param(emitter, counter)
        params = {name: self.value}
        sql = '{0} = {1}'.format(self.column.quoted_name, param_name)
        return OperatorResponse(sql, params)


class IncrementSetter(BasicSetter):
    __doc__ = '\n    Represents an increment setter. (``col = col + 1``)\n    '
    set_operator = '+'


class DecrementSetter(BasicSetter):
    __doc__ = '\n    Represents a decrement setter.\n    '
    set_operator = '-'


class In(BaseOperator, ColumnValueMixin):

    def generate_sql(self, emitter: typing.Callable[([str], str)], counter: itertools.count):
        params = {}
        l = []
        for item in self.value:
            emitted, name = self.get_param(emitter, counter)
            params[name] = item
            l.append(emitted)

        sql = '{} IN ({})'.format(self.column.quoted_fullname, ', '.join(l))
        return OperatorResponse(sql, params)


class ComparisonOp(ColumnValueMixin, BaseOperator):
    __doc__ = '\n    A helper class that implements easy generation of comparison-based operators.\n\n    To customize the operator provided, set the value of ``operator`` in the class body.\n    '
    operator = None

    def generate_sql(self, emitter: typing.Callable[([str], str)], counter: itertools.count):
        params = {}
        if isinstance(self.value, md_column.Column):
            sql = '{} {} {}'.format(self.column.quoted_fullname, self.operator, self.value.quoted_fullname)
        else:
            param_name, name = self.get_param(emitter, counter)
            sql = '{} {} {}'.format(self.column.quoted_fullname, self.operator, param_name)
            params[name] = self.value
        res = OperatorResponse(sql, params)
        return res


class Eq(ComparisonOp):
    __doc__ = '\n    Represents an equality operator.\n    '
    operator = '='


class NEq(ComparisonOp):
    __doc__ = '\n    Represents a non-equality operator.\n    '
    operator = '!='


class Lt(ComparisonOp):
    __doc__ = '\n    Represents a less than operator.\n    '
    operator = '<'


class Gt(ComparisonOp):
    __doc__ = '\n    Represents a more than operator.\n    '
    operator = '>'


class Lte(ComparisonOp):
    __doc__ = '\n    Represents a less than or equals to operator.\n    '
    operator = '<='


class Gte(ComparisonOp):
    __doc__ = '\n    Represents a more than or equals to operator.\n    '
    operator = '>='


class Like(ComparisonOp):
    __doc__ = '\n    Represents a LIKE operator.\n    '
    operator = 'LIKE'


class ILike(ComparisonOp):
    __doc__ = "\n    Represents an ILIKE operator.\n\n    .. warning::\n        This operator is not natively supported on all dialects. If used on a dialect that\n        doesn't support it, it will fallback to a lowercase LIKE.\n    "
    operator = 'ILIKE'


class HackyILike(BaseOperator, ColumnValueMixin):
    __doc__ = '\n    A "hacky" ILIKE operator for databases that do not support it.\n    '

    def generate_sql(self, emitter: typing.Callable[([str], str)], counter: itertools.count):
        params = {}
        if isinstance(self.value, md_column.Column):
            param_name = 'LOWER({})'.format(self.value.quoted_fullname)
        else:
            param_name, name = self.get_param(emitter, counter)
            params[name] = self.value
        sql = 'LOWER({}) LIKE {}'.format(self.column.quoted_fullname, param_name)
        res = OperatorResponse(sql, params)
        return res