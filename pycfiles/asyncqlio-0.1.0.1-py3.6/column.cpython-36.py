# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncqlio/orm/schema/column.py
# Compiled at: 2017-11-29 06:02:28
# Size of source mod 2**32: 11223 bytes
import functools, inspect, logging, typing
from cached_property import cached_property
from asyncqlio.meta import proxy_to_getattr
from asyncqlio.orm import operators as md_operators
from asyncqlio.orm.schema import relationship as md_relationship, table as md_table, types as md_types
from asyncqlio.sentinels import NO_DEFAULT
logger = logging.getLogger(__name__)

def _wrap(self, i):
    if not inspect.ismethod(i):
        return i
    else:

        def _wrapper(*args, **kwargs):
            result = i(*args, **kwargs)
            if not isinstance(result, md_operators.ColumnValueMixin):
                return result
            else:
                result.column = self
                return result

        return _wrapper


@proxy_to_getattr('__eq__', '__neq__', '__gt__', '__lt__', '__gte__', '__lte__')
class AliasedColumn(object):
    __doc__ = '\n    Represents a column on an aliased table.\n    '

    def __init__(self, alias_table: 'md_table.AliasedTable', column: 'Column'):
        """
        :param alias_table: The alias table this column is a member of.
        :param column: The Column object this aliased column proxies.
        """
        self.alias_table = alias_table
        self.column = column

    @property
    def quoted_fullname(self):
        return '"{}"."{}"'.format(self.alias_table.alias_name, self.column.name)

    def __hash__(self):
        return self.column.__hash__()

    def __getattr__(self, item):
        i = getattr(self.column, item)
        return _wrap(self, i)


@proxy_to_getattr('__contains__', '__getitem__', '__setitem__')
class Column(object):
    __doc__ = '\n    Represents a column in a table in a database.\n\n    .. code-block:: python3\n\n        class MyTable(Table):\n            id = Column(Integer, primary_key=True)\n\n    The ``id`` column will mirror the ID of records in the table when fetching, etc. and can be set\n    on a record when storing in a table.\n\n    .. code-block:: python3\n\n        sess = db.get_session()\n        user = await sess.select(User).where(User.id == 2).first()\n\n        print(user.id)  # 2\n\n    '

    def __init__(self, type_: 'typing.Union[md_types.ColumnType, typing.Type[md_types.ColumnType]]', *, primary_key: bool=False, nullable: bool=True, default: typing.Any=NO_DEFAULT, autoincrement: bool=False, index: bool=True, unique: bool=False, foreign_key: 'md_relationship.ForeignKey'=None):
        """
        :param type_:
            The :class:`.ColumnType` that represents the type of this column.

        :param primary_key:
            Is this column the table's Primary Key (the unique identifier that identifies each row)?

        :param nullable:
            Can this column be NULL?

        :param default:
            The client-side default for this column. If no value is provided when inserting, this
            value will automatically be added to the insert query.

        :param autoincrement:
            Should this column auto-increment? This will create a serial sequence.

        :param index:
            Should this column be indexed?

        :param unique:
            Is this column unique?

        :param foreign_key:
            The :class:`.ForeignKey` associated with this column.
        """
        self.name = None
        self.table = None
        self.type = type_
        if not isinstance(self.type, md_types.ColumnType):
            self.type = self.type.create_default()
        self.type.column = self
        self.default = default
        self.primary_key = primary_key
        self.nullable = nullable
        self.autoincrement = autoincrement
        self.indexed = index
        self.unique = unique
        self.foreign_key = foreign_key
        if self.foreign_key is not None:
            self.foreign_key.column = self

    def __repr__(self):
        return '<Column table={} name={} type={}>'.format(self.table, self.name, self.type.sql())

    def __hash__(self):
        return super().__hash__()

    def __set_name__(self, owner, name):
        """
        Called to update the table and the name of this Column.

        :param owner: The :class:`.Table` this Column is on.
        :param name: The str name of this table.
        """
        logger.debug('Column created with name {} on {}'.format(name, owner))
        self.name = name
        self.table = owner

    def __getattr__(self, item):
        try:
            i = getattr(self.type, item)
        except AttributeError:
            raise AttributeError("Column object '{}' has no attribute '{}'".format(self.name, item)) from None

        if inspect.isfunction(i):
            return functools.partial(i, self)
        else:
            return i

    def __eq__(self, other: typing.Any) -> 'typing.Union[md_operators.Eq, bool]':
        if isinstance(other, Column):
            return self.table == other.table and self.name == other.name
        else:
            return md_operators.Eq(self, other)

    def __ne__(self, other) -> 'typing.Union[md_operators.NEq, bool]':
        if isinstance(other, Column):
            return self.table != other.table or self.name != other.name
        else:
            return md_operators.NEq(self, other)

    def __lt__(self, other) -> 'md_operators.Lt':
        return md_operators.Lt(self, other)

    def __gt__(self, other) -> 'md_operators.Gt':
        return md_operators.Gt(self, other)

    def __le__(self, other) -> 'md_operators.Lte':
        return md_operators.Lte(self, other)

    def __ge__(self, other) -> 'md_operators.Gte':
        return md_operators.Gte(self, other)

    def eq(self, other) -> 'md_operators.Eq':
        """
        Checks if this column is equal to something else.

        .. note::

            This is the easy way to check if a column equals another column in a WHERE clause,
            because the default __eq__ behaviour returns a bool rather than an operator.
        """
        return md_operators.Eq(self, other)

    def ne(self, other) -> 'md_operators.NEq':
        """
        Checks if this column is not equal to something else.

        .. note::

            This is the easy way to check if a column doesn't equal another column in a WHERE
            clause, because the default __ne__ behaviour returns a bool rather than an operator.
        """
        return md_operators.NEq(self, other)

    def asc(self) -> 'md_operators.AscSorter':
        """
        Returns the ascending sorter operator for this column.
        """
        return md_operators.AscSorter(self)

    def desc(self) -> 'md_operators.DescSorter':
        """
        Returns the descending sorter operator for this column.
        """
        return md_operators.DescSorter(self)

    def set(self, value: typing.Any) -> 'md_operators.ValueSetter':
        """
        Sets this column in a bulk update.
        """
        return md_operators.ValueSetter(self, value)

    def incr(self, value: typing.Any) -> 'md_operators.IncrementSetter':
        """
        Increments this column in a bulk update.
        """
        return md_operators.IncrementSetter(self, value)

    def __add__(self, other):
        """
        Magic method for incr()
        """
        return self.incr(other)

    def decr(self, value: typing.Any) -> 'md_operators.DecrementSetter':
        """
        Decrements this column in a bulk update.
        """
        return md_operators.DecrementSetter(self, value)

    def __sub__(self, other):
        """
        Magic method for decr()
        """
        return self.decr(other)

    def quoted_fullname_with_table(self, table: 'md_table.TableMeta') -> str:
        """
        Gets the quoted fullname with a table.
        This is used for columns with alias tables.

        :param table: The :class:`.Table` or :class:`.AliasedTable` to use.
        :return:
        """
        return '"{}"."{}"'.format(table.__tablename__, self.name)

    @cached_property
    def quoted_name(self) -> str:
        """
        Gets the quoted name for this column.

        This returns the column name in "column" format.
        """
        return '"{}"'.format(self.name)

    @cached_property
    def quoted_fullname(self) -> str:
        """
        Gets the full quoted name for this column.

        This returns the column name in "table"."column" format.
        """
        return '"{}"."{}"'.format(self.table.__tablename__, self.name)

    @property
    def foreign_column(self) -> 'Column':
        """
        :return: The foreign :class:`.Column` this is associated with, or None otherwise.
        """
        if self.foreign_key is None:
            return
        else:
            return self.foreign_key.foreign_column

    def alias_name(self, table=None, quoted: bool=False) -> str:
        """
        Gets the alias name for a column, given the table.

        This is in the format of `t_<table name>_<column_name>`.

        :param table: The :class:`.Table` to use to generate the alias name.             This is useful for aliased tables.
        :param quoted: Should the name be quoted?
        :return: A str representing the alias name.
        """
        if table is None:
            table = self.table
        fmt = 't_{}_{}'.format(table.__tablename__, self.name)
        if quoted:
            return '"{}"'.format(fmt)
        else:
            return fmt