# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncqlio/orm/schema/types.py
# Compiled at: 2017-11-29 06:02:28
# Size of source mod 2**32: 8417 bytes
import abc, datetime, typing
from asyncqlio.exc import DatabaseException
from asyncqlio.orm import operators as md_operators
from asyncqlio.orm.schema import column as md_column, table as md_table

class ColumnValidationError(DatabaseException):
    __doc__ = '\n    Raised when a column fails validation.\n    '


class ColumnType(abc.ABC):
    __doc__ = '\n    Implements some underlying mechanisms for a :class:`.Column`.\n\n    The only method that is required to be implemented on children is :meth:`.ColumnType.sql` -\n    which is used in CREATE TABLE declarations, etc. :meth:`.ColumnType.on_set`,\n    :meth:`.ColumnType.on_get` and so on are not required to be implemented - the defaults will\n    work fine.\n\n    The ColumnType is responsible for actually loading the data from the row\'s internal storage\n    and to the user code.\n\n    .. code-block:: python3\n\n        # we hate fun\n        def on_get(self, row, column):\n            return "lol"\n\n        ...\n\n        # row is a random row object\n        # load the `fun` column which has this weird type\n        value = row.fun\n        print(value)  # "lol", regardless of what was stored in the database.\n\n    Accordingly, it is also responsible for storing the data into the row\'s internal storage.\n\n    .. code-block:: python3\n\n        def on_set(*args, **kwargs):\n            return None\n\n        row.not_fun = 1\n        print(row.not_fun)  # None - no value was stored in the row\n\n    To actually insert a value into the row\'s storage table, use :meth:`.ColumnType.store_value`.\n    Correspondingly, loading a value from the row\'s storage table can be achieved with\n    :meth:`.ColumnType.load_value`. These functions should be used, as they are guarenteed to work\n    across all versions.\n\n    Columns will proxy bad attribute accesses from the Column object to this type object - meaning\n    types can implement custom operators, if applicable.\n\n    .. code-block:: python3\n\n        class User(Table):\n            id = Column(MyWeirdType())\n\n        ...\n\n        # MyWeirdType implements `.contains`\n        # the contains call is proxied to (MyWeirdType instance).contains("heck")\n        q = await sess.select(User).where(User.id.contains("heck")).first()\n\n    '
    __slots__ = ('column', )

    def __init__(self):
        self.column = None

    @abc.abstractmethod
    def sql(self) -> str:
        """
        :return: The str SQL name of this type.
        """
        pass

    def validate_set(self, row: 'md_table.Table', value: typing.Any) -> bool:
        """
        Validates that the item being set is valid.
        This is called by the default ``on_set``.

        :param row: The row being set.
        :param value: The value to set.
        :return: A bool indicating if this is valid or not.
        """
        return True

    def store_value(self, row: 'md_table.Table', value: typing.Any):
        """
        Stores a value in the row's storage table.

        This is for internal usage only.

        :param row: The row to store in.
        :param value: The value to store in the row.
        """
        row.store_column_value(self.column, value)

    def on_set(self, row: 'md_table.Table', value: typing.Any) -> typing.Any:
        """
        Called when a value is a set on this column.

        This is the default method - it will call :meth:`.ColumnType.validate_set` to validate the
        type before storing it. This is useful for simple column types.

        :param row: The row this value is being set on.
        :param value: The value being set.
        """
        if value is not None:
            valid = self.validate_set(row, value)
            if not valid:
                raise ColumnValidationError('Value {} failed to validate in type {}'.format(value, type(self).__name__))
        self.store_value(row, value)

    def on_get(self, row: 'md_table.Table') -> typing.Any:
        """
        Called when a value is retrieved from this column.

        :param row: The row that is being retrieved.
        :return: The value of the row's internal storage.
        """
        return row.get_column_value(self.column)

    @classmethod
    def create_default(cls) -> 'ColumnType':
        """
        Creates the default object for this table in the event that a type is passed to a column,
        instead of an instance.
        """
        return cls()

    def in_(self, *args) -> 'md_operators.In':
        """
        Returns an IN operator, checking if a value in this column is in a tuple of items.

        :param args: The items to check.
        """
        if len(args) <= 0:
            raise ValueError('Must provide at least one argument to in_')
        return md_operators.In(self.column, args)


class String(ColumnType):
    __doc__ = '\n    Represents a VARCHAR() type.\n    '

    def __init__(self, size=-1):
        super().__init__()
        self.size = size

    def sql(self):
        if self.size >= 0:
            return 'VARCHAR({})'.format(self.size)
        else:
            return 'VARCHAR'

    def validate_set(self, row, value: typing.Any):
        if self.size < 0:
            return True
        else:
            if len(value) > self.size:
                raise ColumnValidationError('Value {} is more than {} chars long'.format(value, self.size))
            return True

    def like(self, other: str) -> 'md_operators.Like':
        """
        Returns a LIKE operator, checking if this column is LIKE another string.

        :param other: The other string to check.
        """
        return md_operators.Like(self.column, other)

    def ilike(self, other: str) -> 'typing.Union[md_operators.ILike, md_operators.HackyILike]':
        """
        Returns an ILIKE operator, checking if this column is case-insensitive LIKE another string.

        .. warning::
            This is not supported in all DB backends.

        :param other: The other string to check.
        """
        if self.column.table._bind.dialect.has_ilike:
            return md_operators.ILike(self.column, other)
        else:
            return md_operators.HackyILike(self.column, other)


class Text(String):
    __doc__ = '\n    Represents a TEXT type.\n    TEXT type columns are very similar to String type objects, except that they have no size limit.\n\n    .. note::\n        This is preferable to the String type in some databases.\n\n    .. warning::\n        This is deprecated in MSSQL.\n    '

    def __init__(self):
        super().__init__(size=(-1))

    def sql(self):
        return 'TEXT'


class Boolean(ColumnType):
    __doc__ = '\n    Represents a BOOL type.\n    '

    def sql(self):
        return 'BOOLEAN'

    def validate_set(self, row: 'md_table.Table', value: typing.Any):
        return value in (True, False)


class Integer(ColumnType):
    __doc__ = '\n    Represents an INTEGER type.\n\n    .. warning::\n        This represents a 32-bit integer (2**31-1 to -2**32)\n    '

    def sql(self):
        return 'INTEGER'

    def validate_set(self, row, value: typing.Any):
        """
        Checks if this int is in range for the type.
        """
        return -2147483648 < value < 2147483647

    def on_set(self, row, value):
        if not isinstance(value, int):
            raise ColumnValidationError('Value {} is not an int'.format(value))
        return super().on_set(row, value)


class SmallInt(Integer):
    __doc__ = '\n    Represents a SMALLINT type.\n    '

    def sql(self):
        return 'SMALLINT'

    def validate_set(self, row, value: typing.Any):
        return -32768 < value < 32767


class BigInt(Integer):
    __doc__ = '\n    Represents a BIGINT type.\n    '

    def sql(self):
        return 'BIGINT'

    def validate_set(self, row, value):
        return -9223372036854775808 < value < 9223372036854775807


class Timestamp(ColumnType):
    __doc__ = '\n    Represents a TIMESTAMP type.\n    '

    def sql(self):
        return 'TIMESTAMP'

    def validate_set(self, row, value):
        return isinstance(value, datetime.datetime)