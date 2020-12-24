# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncqlio/orm/schema/relationship.py
# Compiled at: 2017-11-29 06:02:28
# Size of source mod 2**32: 18278 bytes
"""
Relationship helpers.
"""
import typing
from cached_property import cached_property
from asyncqlio.orm import query as md_query
from asyncqlio.orm.schema import column as md_column, table as md_table
from asyncqlio.sentinels import NO_VALUE
from asyncqlio.utils import iter_to_aiter

class ForeignKey(object):
    __doc__ = '\n    Represents a foreign key object in a column. This allows linking multiple tables together\n    relationally.\n\n    .. code-block:: python3\n\n        class Server(Table):\n            id = Column(Integer, primary_key=True, autoincrement=True)\n            name = Column(String)\n\n            owner_id = Column(Integer, foreign_key=ForeignKey("User.id")\n    '

    def __init__(self, foreign_column: 'typing.Union[md_column.Column, str]'):
        """
        :param foreign_column: Either a :class:`.Column` representing the foreign column, or a str             in the format ``<table object name>.<column name>``.
        """
        self.foreign_column = None
        if isinstance(foreign_column, md_column.Column):
            self.foreign_column = foreign_column
            self._f_name = None
        else:
            self._f_name = foreign_column
        self.column = None

    def __repr__(self):
        return "<ForeignKey owner='{}' foreign='{}'>".format(self.column, self.foreign_column)


class Relationship(object):
    __doc__ = '\n    Represents a relationship to another table object.\n\n    This object provides an easy, object-oriented interface to a foreign key relationship between\n    two tables, the left table and the right table.\n    The left table is the "parent" table, and the right table is the "child" table; effectively\n    creating a one to many/many to one relationship between the two tables.\n\n    To create a relationship, there must be a column in the child table that represents the primary\n    key of a parent table; this is the foreign key column, and will be used to load the other table.\n\n    .. code-block:: python3\n\n        class User(Table):\n            # id is the primary key of the parent table\n            id = Column(Integer, auto_increment=True)\n            name = Column(String)\n\n            # this is the relationship joiner; it uses id as the left key, and user_id as the right\n            # this will create a join between the two tables\n            inventory = Relationship(left=id, right="InventoryItem.user_id")\n\n        class InventoryItem(Table):\n            id = Column(BigInteger, auto_increment=True)\n\n            # user_id is the "foreign key" - it references the column User.id\n            user_id = Column(Integer, foreign_key=ForeignKey(User.id)\n\n    Once created, the new relationship object can be used to iterate over the child objects, using\n    ``async for``:\n\n    .. code-block:: python3\n\n        user = await sess.select.from_(User).where(User.id == 1).first()\n        async for item in user.inventory:\n            ...\n\n    By default, the relationship will use a SELECT query to load the items; this can be changed to\n    a joined query when loading any table rows, by changing the ``load`` param.\n    The possible values of this param are:\n\n        - ``select`` - Emits a SELECT query to load child items.\n        - ``joined`` - Emits a join query to load child items.\n\n    For all possible options, see :ref:`Relationship Loading`.\n\n    '

    def __init__(self, left: 'typing.Union[md_column.Column, str]', right: 'typing.Union[md_column.Column, str]', *, load: str='select', use_iter: bool=True, back_ref: str=None, table_alias: str=None):
        """
        :param left: The left-hand column (the Column on this table) in this relationship.

        :param right: The right-hand column (the Column on the foreign table) in this relationship.

        :param load: The way to load this relationship.

            The default is "select" - this means that a separate select statement will be issued
            to iterate over the rows of the relationship.

            For all possible options, see :ref:`Relationship Loading`.

        :param use_iter: Should this relationship use the iterable format?

            This controls if this relationship is created as one to many, or as a many to one/one to
            one relationship.

        :param back_ref: The "back reference" to add to the right table.

            This will automatically add a relationship to the right table with the specified name,
            and automatically fill it when querying over said relationship.

        :param table_alias: The table alias to use when joining.

            This will rename the joined table to allow selecting specific rows in tables with
            multiple relationships to the same table.
        """
        self.left_column = left
        self.right_column = right
        self.load_type = load
        self.use_iter = use_iter
        self.owner_table = None
        self._name = None
        self.back_reference = back_ref
        self._table_alias = table_alias
        if self.use_iter is False:
            self.load_type = 'joined'

    def __getattr__(self, item):
        column = self.foreign_table.get_column(item)
        if column is not None:
            return md_column.AliasedColumn(self._table_alias, column)
        relationship = self.foreign_table.get_relationship(item)
        if relationship is not None:
            return relationship
        raise AttributeError(item)

    def __set_name__(self, owner, name):
        self.owner_table = owner
        self._name = name

    def __repr__(self):
        try:
            o_name = '{}.{}'.format(self.our_column.table.__tablename__, self.our_column.name)
        except AttributeError:
            o_name = '<unknown>'

        try:
            f_name = '{}.{}'.format(self.foreign_column.table.__tablename__, self.foreign_column.name)
        except AttributeError:
            f_name = '<unknown>'

        return "<Relationship '{}' <-> '{}'>".format(o_name, f_name)

    def _get_join_query(self, parent: 'Relationship'):
        """
        Gets the join part of a SELECT query for this relationship.

        """
        fmt = 'LEFT OUTER JOIN {} {} '.format(self.foreign_table.alias_table.__quoted_name__, self.foreign_table.__quoted_name__)
        if parent is not None:
            left = self.our_column.quoted_fullname_with_table(parent.foreign_table)
        else:
            left = self.our_column.quoted_fullname_with_table(self.owner_table)
        right = self.foreign_column.quoted_fullname_with_table(self.foreign_table)
        fmt += 'ON {} = {}'.format(left, right)
        return fmt

    @cached_property
    def our_column(self) -> 'md_column.Column':
        """
        Gets the local column this relationship refers to.
        """
        if self.left_column == self.owner_table:
            return self.left_column
        else:
            return self.right_column

    @property
    def foreign_column(self) -> 'md_column.Column':
        """
        Gets the foreign column this relationship refers to.
        """
        if self.left_column.table == self.owner_table:
            return self.right_column
        else:
            return self.left_column

    @property
    def foreign_table(self):
        if isinstance(self._table_alias, md_table.AliasedTable):
            return self._table_alias
        else:
            return self.foreign_column.table

    @property
    def join_columns(self) -> typing.Tuple[('md_column.Column', 'md_column.Column')]:
        """
        Gets the "join" columns of this relationship, i.e the columns that link the two columns.
        """
        return (
         self.our_column, self.foreign_column)

    def get_instance(self, row: 'md_table.Table', session):
        """
        Gets a new "relationship" instance.
        """
        if self.load_type == 'select':
            return SelectLoadedRelationship(self, row, session or row._session)
        else:
            if self.load_type == 'joined':
                if self.use_iter is False:
                    return JoinLoadedOTORelationship(self, row, session or row._session)
                else:
                    return JoinLoadedOTMRelationship(self, row, session or row._session)
            else:
                raise NotImplementedError('Unknown load type {}'.format(self.load_type))


class BaseLoadedRelationship(object):
    __doc__ = '\n    Provides some common methods for specific relationship type subclasses.\n    '

    def __init__(self, rel: 'Relationship', row: 'md_table.Table', session):
        """
        :param rel: The :class:`.Relationship` that lies underneath this object.
        :param row: The :class:`.TableRow` this is being loaded from.
        :param session: The :class:`.Session` this object is attached to.
        """
        self.relationship = rel
        self.row = row
        self.session = session or row._session

    def _it_stored_rows(self):
        raise NotImplementedError

    async def _add_row(self, row: 'md_table.Table'):
        """
        An overridable method called when a row is added.
        """
        pass

    async def add(self, row: 'md_table.Table'):
        """
        Adds a row to this relationship.

        .. warning::
            This will run an immediate insert/update of this row; if the parent row for this
            relationship is not inserted it will run an immediate insert on the parent.

        :param row: The :class:`.TableRow` object to add to this relationship.
        """
        if not self.row._TableRow__existed:
            self.row = await self.session.insert_now(row)
        our_column = self.relationship.our_column
        data = self.row.get_column_value(our_column)
        f_column = self.relationship.foreign_column
        row.store_column_value(f_column, data)
        row = await self.session.add(row)
        await self._add_row(row)
        return row

    async def _remove_row(self, row: 'md_table.Table'):
        """
        An overridable method called when a row is removed.
        """
        pass

    async def remove(self, row: 'md_table.Table'):
        """
        Removes a row from this query.

        .. warning::
            This will run an immediate UPDATE of this row to remove the foreign key.

        :param row: The :class:`.TableRow` object to remove from this relationship.
        """
        f_column = self.relationship.foreign_column
        if row.get_column_value(f_column, return_default=False) is NO_VALUE:
            raise ValueError("The row '{}' is not in this relationship".format(row))
        row.store_column_value(f_column, None)
        row = await self.session.add(row)
        await self._remove_row(row)
        return row

    def set_rows(self, rows: 'typing.List[md_table.Table]'):
        """
        Sets the rows for this relationship.
        This is an internal method, and not to be used in user code.
        """
        pass

    def _update_sub_relationships(self, mapping):
        """
        Updates relationship mappings for this relationship automatically, if applicable.
        """
        if isinstance(self, SelectLoadedRelationship):
            return
        for row in self._it_stored_rows():
            for relationship in row.table.iter_relationships():
                if relationship not in mapping:
                    pass
                else:
                    rows = mapping[relationship]
                    for nrow in rows:
                        if row.get_column_value(relationship.our_column) == nrow.get_column_value(relationship.foreign_column):
                            row._relationship_mapping[relationship].append(nrow)

    def __iter__(self):
        raise TypeError('This cannot be iterated over normally')

    def __anext__(self):
        raise TypeError('This is not an async iterator')


class SelectLoadedRelationship(BaseLoadedRelationship):
    __doc__ = '\n    A relationship object that uses a separate SELECT statement to load follow-on tables.\n    '

    def _it_stored_rows(self):
        return []

    @property
    def query(self) -> 'md_query.SelectQuery':
        """
        Gets the query for this relationship, allowing further customization.
        For example, to change the order of the rows returned:

        .. code-block:: python3

            async for child in parent.children.query.order_by(Child.age):
                ...
        """
        columns = self.relationship.join_columns
        query = md_query.SelectQuery(self.row._session)
        query.set_table(self.relationship.foreign_table)
        query.add_condition(columns[1] == self.row.get_column_value(columns[0]))
        return query

    async def first(self):
        rows = await self._load()
        return await rows.next()

    def __await__(self):
        return self._load().__await__()

    def __aiter__(self):
        return self._load()

    async def _load(self):
        """
        Loads the rows for this session.
        """
        return await self.query.all()


@iter_to_aiter
class JoinLoadedOTMRelationship(BaseLoadedRelationship):
    __doc__ = '\n    Represents a join-loaded one to many relationship.\n    '

    def __init__(self, rel, row, session):
        """
        :param rel: The :class:`.Relationship` that lies underneath this object.
        :param row: The :class:`.TableRow` this is being loaded from.
        :param session: The :class:`.Session` this object is attached to.
        """
        super().__init__(rel, row, session)
        self._row_storage = []

    def _it_stored_rows(self):
        return self._row_storage

    def __repr__(self):
        return '<JoinLoadedOTMRelationship {}>'.format(repr(self._row_storage))

    def __iter__(self):
        return iter(self._row_storage)

    async def _add_row(self, row: 'md_table.Table'):
        self._row_storage.append(row)

    async def _remove_row(self, row: 'md_table.Table'):
        self._row_storage.remove(row)

    def set_rows(self, rows: 'typing.List[md_table.Table]'):
        self._row_storage = rows


class JoinLoadedOTORelationship(BaseLoadedRelationship):
    __doc__ = '\n    Represents a joined one<-to->one relationship.\n    '

    def __init__(self, rel, row, session):
        """
        :param rel: The :class:`.Relationship` that lies underneath this object.
        :param row: The :class:`.TableRow` this is being loaded from.
        :param session: The :class:`.Session` this object is attached to.
        """
        super().__init__(rel, row, session)
        self._rel_row = None

    def _it_stored_rows(self):
        return [
         self._rel_row]

    def __repr__(self):
        return "<JoinLoadedOTORelationship row='{}'>".format(self._rel_row)

    def set_rows(self, rows: 'typing.List[md_table.Table]'):
        try:
            self._rel_row = next(iter(rows))
        except StopIteration:
            return

    def add(self, row: 'md_table.Table'):
        raise NotImplementedError('This method does not work on one to one relationships')

    def remove(self, row: 'md_table.Table'):
        raise NotImplementedError('This method not work on one to one relationships')

    def __getattr__(self, item):
        if self._rel_row is None:
            raise AttributeError('Cannot load from empty row')
        else:
            return getattr(self._rel_row, item)

    async def set(self, row: 'md_table.Table'):
        """
        Sets the row for this one-to-one relationship.

        .. warning::
            This will run an immediate insert/update of this row; if the parent row for this
            relationship is not inserted it will run an immediate insert on the parent.

        :param row: The :class:`.TableRow` to set.
        """
        if not self.row._TableRow__existed:
            self.row = await self.session.insert_now(row)
        our_column = self.relationship.our_column
        data = self.row.get_column_value(our_column)
        f_column = self.relationship.foreign_column
        row.store_column_value(f_column, data)
        row = await self.session.add(row)
        self._rel_row = row
        return row