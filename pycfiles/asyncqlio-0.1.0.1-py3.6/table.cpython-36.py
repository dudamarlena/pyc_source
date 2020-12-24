# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncqlio/orm/schema/table.py
# Compiled at: 2017-11-29 06:02:28
# Size of source mod 2**32: 34188 bytes
import collections, itertools, logging, sys, typing
from collections import OrderedDict
from asyncqlio import db as md_db
from asyncqlio.exc import SchemaError
from asyncqlio.orm import inspection as md_inspection, session as md_session
from asyncqlio.orm.schema import column as md_column, relationship as md_relationship
from asyncqlio.sentinels import NO_DEFAULT, NO_VALUE
PY36 = sys.version_info[0:2] >= (3, 6)
logger = logging.getLogger(__name__)

class TableMetadata(object):
    __doc__ = '\n    The root class for table metadata.\n    This stores a registry of tables, and is responsible for calculating relationships etc.\n\n    .. code-block:: python3\n\n        meta = TableMetadata()\n        Table = table_base(metadata=meta)\n\n    '

    def __init__(self):
        self.tables = {}
        self.bind = None

    def register_table(self, tbl: 'TableMeta', *, autosetup_tables: bool=False) -> 'TableMeta':
        """
        Registers a new table object.

        :param tbl: The table to register.
        :param autosetup_tables: Should tables be setup again?
        """
        tbl.metadata = self
        self.tables[tbl.__tablename__] = tbl
        if autosetup_tables:
            self.setup_tables()
        return tbl

    def get_table(self, table_name: str) -> 'typing.Type[Table]':
        """
        Gets a table from the current metadata.

        :param table_name: The name of the table to get.
        :return: A :class:`.Table` object.
        """
        try:
            return self.tables[table_name]
        except KeyError:
            for table in self.tables.values():
                if table.__name__ == table_name:
                    return table
            else:
                return

    def setup_tables(self):
        """
        Sets up the tables for usage in the ORM.
        """
        self.resolve_floating_relationships()
        self.resolve_aliases()
        self.resolve_backrefs()

    def resolve_aliases(self):
        """
        Resolves all alias tables on relationship objects.
        """
        for tbl in self.tables.copy().values():
            if isinstance(tbl, AliasedTable):
                pass
            else:
                for relationship in tbl.iter_relationships():
                    if relationship._table_alias is None:
                        relationship._table_alias = 'r_{}_{}'.format(relationship.owner_table.__name__, relationship._name.lower())
                    if not isinstance(relationship._table_alias, AliasedTable):
                        relationship._table_alias = AliasedTable(relationship._table_alias, relationship.foreign_table)
                    self.tables[relationship._table_alias.alias_name] = relationship._table_alias

    def resolve_backrefs(self):
        """
        Resolves back-references.
        """
        for tbl in self.tables.values():
            if isinstance(tbl, AliasedTable):
                pass
            else:
                for relationship in tbl.iter_relationships():
                    if relationship.back_reference is None:
                        pass
                    else:
                        table, name = relationship.back_reference.split('.')
                        table = self.get_table(table)
                        new_rel = md_relationship.Relationship((relationship.right_column), (relationship.left_column),
                          load='joined',
                          use_iter=False)
                        new_rel.__set_name__(table, name)
                        table._relationships[name] = new_rel
                        relationship.back_reference = new_rel

    def resolve_floating_relationships(self):
        """
        Resolves any "floating" relationships - i.e any relationship/foreign keys that don't
        directly reference a column object.
        """
        for tbl in self.tables.values():
            if isinstance(tbl, AliasedTable):
                pass
            else:
                for column in tbl._columns.values():
                    if column.foreign_key is None:
                        pass
                    else:
                        foreignkey = column.foreign_key
                        if foreignkey.foreign_column is None:
                            table, column = foreignkey._f_name.split('.')
                            table_obb = self.get_table(table)
                            if table_obb is None:
                                raise SchemaError("No such table '{}' exists in FK {}".format(table, foreignkey))
                            col = table_obb.get_column(column)
                            if col is None:
                                raise SchemaError("No such column '{}' exists on table '{}'(from FK {})".format(column, table, foreignkey))
                            foreignkey.foreign_column = col

                for relation in tbl._relationships.values():
                    assert isinstance(relation, md_relationship.Relationship)
                    resolving_columns = [col for col in [relation.left_column, relation.right_column] if isinstance(col, str)]
                    for to_resolve in resolving_columns:
                        table, column = to_resolve.split('.')
                        table_obb = self.get_table(table)
                        if table_obb is None:
                            raise SchemaError("No such table '{}' exists(from relationship {})".format(table, relation))
                        col = table_obb.get_column(column)
                        if col is None:
                            raise SchemaError("No such column '{}' exists on table '{}'".format(table, column))
                        if (to_resolve == relation.left_column) is True:
                            relation.left_column = col
                            logger.debug('Resolved {} to {}'.format(to_resolve, col))
                        else:
                            if (to_resolve == relation.right_column) is True:
                                relation.right_column = col
                                logger.debug('Resolved {} to {}'.format(to_resolve, col))
                            else:
                                raise SchemaError("Could not resolve column '{}' - it did not match the left or right column!")


class TableMeta(type):
    __doc__ = '\n    The metaclass for a table object. This represents the "type" of a table class.\n    '

    def __prepare__(*args, **kwargs):
        return OrderedDict()

    def __new__(mcs, name: str, bases: tuple, class_body: dict, register: bool=True, *args, **kwargs):
        if register is False:
            return type.__new__(mcs, name, bases, class_body)
        else:
            columns = OrderedDict()
            relationships = OrderedDict()
            for col_name, value in class_body.copy().items():
                if isinstance(value, md_column.Column):
                    columns[col_name] = value
                    class_body.pop(col_name)
                else:
                    if isinstance(value, md_relationship.Relationship):
                        relationships[col_name] = value
                        class_body.pop(col_name)

            class_body['_columns'] = columns
            class_body['_relationships'] = relationships
            try:
                class_body['__tablename__'] = kwargs['table_name']
            except KeyError:
                class_body['__tablename__'] = name.lower()

            return type.__new__(mcs, name, bases, class_body)

    def __init__(self, tblname, tblbases, class_body, register=True, *args, **kwargs):
        """
        Creates a new Table instance.

        :param register: Should this table be registered in the TableMetadata?
        :param table_name: The name for this table.
        """
        super().__init__(tblname, tblbases, class_body)
        if register is False:
            return
        if not hasattr(self, 'metadata'):
            raise TypeError('Table {} has been created but has no metadata - did you subclass Table directly instead of a clone?'.format(tblname))
        it = itertools.chain(self._columns.items(), self._relationships.items())
        if not PY36:
            it = itertools.chain(class_body.items(), it)
        for name, value in it:
            if hasattr(value, '__set_name__'):
                value.__set_name__(self, name)

        self._columns = self._columns
        self._relationships = self._relationships
        self._primary_key = self._calculate_primary_key()
        logger.debug('Registered new table {}'.format(tblname))
        self.metadata.register_table(self)

    def __getattr__(self, item):
        if item.startswith('_'):
            raise AttributeError("'{}' object has no attribute {}".format(self.__name__, item))
        else:
            col = self.get_column(item)
            if col is None:
                try:
                    return next(filter(lambda tup: tup[0] == item, self._relationships.items()))[1]
                except StopIteration:
                    raise AttributeError(item) from None

            else:
                return col

    @property
    def _bind(self):
        return self.metadata._bind

    @property
    def __quoted_name__(self):
        return '"{}"'.format(self.__tablename__)

    @property
    def columns(self) -> 'typing.List[md_column.Column]':
        """
        :return: A list of :class:`.Column` this Table has.
        """
        return list(self.iter_columns())

    def __repr__(self):
        try:
            return "<Table object='{}' name='{}'>".format(self.__name__, self.__tablename__)
        except AttributeError:
            return super().__repr__()

    def iter_relationships(self) -> 'typing.Generator[md_relationship.Relationship, None, None]':
        """
        :return: A generator that yields :class:`.Relationship` objects for this table.
        """
        for rel in self._relationships.values():
            yield rel

    def iter_columns(self) -> 'typing.Generator[md_column.Column, None, None]':
        """
        :return: A generator that yields :class:`.Column` objects for this table.
        """
        for col in self._columns.values():
            yield col

    def get_column(self, column_name: str, *, raise_si: bool=False) -> 'typing.Union[md_column.Column, None]':
        """
        Gets a column by name.

        :param column_name: The column name to lookup.

            This can be one of the following:
                - The column's ``name``
                - The column's ``alias_name()`` for this table

        :return: The :class:`.Column` associated with that name, or None if no column was found.
        """
        try:
            return self._columns[column_name]
        except KeyError:
            for column in self._columns.values():
                alias = column.alias_name(table=self)
                if alias == column_name:
                    return column

    def get_relationship(self, relationship_name) -> 'typing.Union[md_relationship.Relationship, None]':
        """
        Gets a relationship by name.

        :param relationship_name: The name of the relationship to get.
        :return: The :class:`.Relationship` associated with that name, or None if it doesn't existr.
        """
        try:
            return self._relationships[relationship_name]
        except KeyError:
            return

    def _calculate_primary_key(self) -> typing.Union[('PrimaryKey', None)]:
        """
        Calculates the current primary key for a table, given all the columns.

        If no columns are marked as a primary key, the key will not be generated.
        """
        pk_cols = []
        for col in self.iter_columns():
            if col.primary_key is True:
                pk_cols.append(col)

        if pk_cols:
            pk = PrimaryKey(*pk_cols)
            pk.table = self
            logger.debug('Calculated new primary key {}'.format(pk))
            return pk

    @property
    def primary_key(self) -> 'PrimaryKey':
        """
        :getter: The :class:`.PrimaryKey` for this table.
        :setter: A new :class:`.PrimaryKey` for this table.

        .. note::
            A primary key will automatically be calculated from columns at define time, if any
            columns have ``primary_key`` set to True.
        """
        return self._primary_key

    @primary_key.setter
    def primary_key(self, key: 'PrimaryKey'):
        key.table = self
        self._primary_key = key

    def _internal_from_row(cls, values: dict, *, existed: bool=False):
        obb = object.__new__(cls)
        obb.__init__()
        setattr(obb, '_{}__existed'.format(cls.__name__), existed)
        (obb._init_row)(**values)
        return obb


class Table(metaclass=TableMeta, register=False):
    __doc__ = '\n    The "base" class for all tables. This class is not actually directly used; instead\n    :meth:`.table_base` should be called to get a fresh clone.\n    '

    def __init__(self, **kwargs):
        self.table = type(self)
        self._Table__existed = False
        self._Table__deleted = False
        self._session = None
        self._previous_values = {}
        self._relationship_mapping = collections.defaultdict(lambda : [])
        self._values = {}
        if kwargs:
            (self._init_row)(**kwargs)

    def _init_row(self, **values):
        """
        Initializes the rows for this table, setting the values of the object.

        :param values: The values to pass into this column.
        """
        for name, value in values.items():
            column = self.table.get_column(name)
            if column is None:
                raise TypeError("Unexpected row parameter: '{}'".format(name))
            self._values[column] = value

        return self

    def __repr__(self):
        gen = ('{}={}'.format(col.name, self.get_column_value(col)) for col in self.table.columns)
        return '<{} {}>'.format(self.table.__name__, ' '.join(gen))

    def __eq__(self, other):
        if not isinstance(other, Table):
            return NotImplemented
        else:
            if other.table != self.table:
                raise ValueError('Rows to compare must be on the same table')
            return self.primary_key == other.primary_key

    def __le__(self, other):
        if not isinstance(other, Table):
            return NotImplemented
        else:
            if other.table != self.table:
                raise ValueError('Rows to compare must be on the same table')
            return self.primary_key <= other.primary_key

    def __setattr__(self, key, value):
        try:
            object.__getattribute__(self, '_values')
        except AttributeError:
            return super().__setattr__(key, value)
        else:
            if key in self.__dict__:
                return super().__setattr__(key, value)
            else:
                col = self.table.get_column(column_name=key)
                if col is None:
                    return super().__setattr__(key, value)
                return col.type.on_set(self, value)

    @property
    def primary_key(self) -> typing.Union[(typing.Any, typing.Iterable[typing.Any])]:
        """
        Gets the primary key for this row.

        If this table only has one primary key column, this property will be a single value.
        If this table has multiple columns in a primary key, this property will be a tuple.
        """
        pk = self.table.primary_key
        result = []
        for col in pk.columns:
            val = self.get_column_value(col)
            result.append(val)

        if len(result) == 1:
            return result[0]
        else:
            return tuple(result)

    def __getattr__(self, item: str):
        obb = self._resolve_item(item)
        return obb

    __hash__ = object.__hash__

    def _get_insert_sql(self, emitter: typing.Callable[([], str)], session: 'md_session.Session'):
        """
        Gets the INSERT into statement SQL for this row.
        """
        if self._session is None:
            self._session = session
        q = 'INSERT INTO {} '.format(self.table.__quoted_name__)
        params = {}
        column_names = []
        sql_params = []
        for column in self.table.iter_columns():
            column_names.append(column.quoted_name)
            value = self.get_column_value(column)
            if value is NO_VALUE or value is None and column.default is NO_DEFAULT:
                sql_params.append('DEFAULT')
            else:
                name = emitter()
                param_name = session.bind.emit_param(name)
                params[name] = value
                sql_params.append(param_name)

        q += '({}) '.format(', '.join(column_names))
        q += 'VALUES '
        q += '({}) '.format(', '.join(sql_params))
        if session.bind.dialect.has_returns:
            columns_to_get = []
            for column in self.table.iter_columns():
                columns_to_get.append(column)

            to_return = ', '.join(column.quoted_name for column in columns_to_get)
            q += ' RETURNING {}'.format(to_return)
        q += ';'
        return (q, params)

    def _get_update_sql(self, emitter: typing.Callable[([], str)], session: 'md_session.Session'):
        """
        Gets the UPDATE statement SQL for this row.
        """
        if self._session is None:
            self._session = session
        params = {}
        base_query = 'UPDATE {} SET '.format(self.table.__quoted_name__)
        sets = []
        history = md_inspection.get_row_history(self)
        if not history:
            return (None, None)
        else:
            for col, d in history.items():
                if d['old'] == d['new']:
                    pass
                else:
                    p = emitter()
                    params[p] = d['new']
                    sets.append('{} = {}'.format(col.quoted_name, session.bind.emit_param(p)))

            if not sets:
                return (None, None)
            base_query += ', '.join(sets)
            wheres = []
            for col in self.table.primary_key.columns:
                p = emitter()
                params[p] = history[col]['old']
                wheres.append('{} = {}'.format(col.quoted_name, session.bind.emit_param(p)))

            base_query += ' WHERE ({});'.format(' AND '.join(wheres))
            return (
             base_query, params)

    def _get_delete_sql(self, emitter: typing.Callable[([], str)], session: 'md_session.Session') -> typing.Tuple[(str, typing.Any)]:
        """
        Gets the DELETE sql for this row.
        """
        if self._session is None:
            self._session = session
        query = 'DELETE FROM {} '.format(self.table.__quoted_name__)
        wheres = []
        params = {}
        for col, value in zip(self.table.primary_key.columns, md_inspection.get_pk(self, as_tuple=True)):
            name = emitter()
            params[name] = value
            wheres.append('{} = {}'.format(col.quoted_fullname, session.bind.emit_param(name)))

        query += 'WHERE ({}) '.format(' AND '.join(wheres))
        return (query, params)

    def _resolve_item(self, name: str):
        """
        Resolves an item on this row.

        This will check:

            - Functions decorated with :func:`.row_attr`
            - Non-column :class:`.Table` members
            - Columns

        :param name: The name to resolve.
        :return: The object returned, if applicable.
        """
        try:
            return self.get_relationship_instance(name)
        except ValueError:
            pass

        col = self.table.get_column(name)
        if col is None:
            raise AttributeError('{} was not a function or attribute on the associated table, and was not a column'.format(name)) from None
        return col.type.on_get(self)

    def get_old_value(self, column: 'md_column.Column'):
        """
        Gets the old value from the specified column in this row.
        """
        if column.table != self.table:
            raise ValueError('Column table must match row table')
        try:
            return self._previous_values[column]
        except KeyError:
            return NO_VALUE

    def get_column_value(self, column: 'md_column.Column', return_default: bool=True):
        """
        Gets the value from the specified column in this row.

        :param column: The column.
        :param return_default: If this should return the column default, or NO_VALUE.
        """
        if column.table != self.table:
            raise ValueError('Column table must match row table')
        try:
            return self._values[column]
        except KeyError:
            if return_default:
                default = column.default
                if default is NO_DEFAULT:
                    return
                else:
                    return default
            else:
                return NO_VALUE

    def store_column_value(self, column: 'md_column.Column', value: typing.Any, track_history: bool=True):
        """
        Updates the value of a column in this row.

        This will also update the history of the value, if applicable.
        """
        if self._Table__deleted:
            raise RuntimeError('This row is marked as deleted')
        if column not in self._previous_values:
            if track_history:
                if column in self._values:
                    self._previous_values[column] = self._values[column]
        self._values[column] = value
        return self

    def get_relationship_instance(self, relation_name: str):
        """
        Gets a 'relationship instance'.

        :param relation_name: The name of the relationship to load.
        """
        try:
            relation = next(filter(lambda relationship: relationship._name == relation_name, self.table.iter_relationships()))
        except StopIteration:
            raise ValueError("No such relationship '{}'".format(relation_name))

        rel = relation.get_instance(self, self._session)
        rel.set_rows(self._relationship_mapping[relation])
        rel._update_sub_relationships(self._relationship_mapping)
        return rel

    def _load_columns_using_table(self, table: 'TableMeta', record: dict, buckets: dict, seen: list):
        """
        Recursively organizes columns in a record into table buckets by scanning the
        relationships inside the table.

        :param table: The :class:`.TableMeta` to use to load the table.
        :param record: The dict-like record to read from.
        :param buckets: The dict of buckets to store tables in.
        :param seen: A list of relationships that have already been seen. This prevents infinite             loops.

            Outside of internal code, this should be passed in as an empty list.

        """
        for relationship in table.iter_relationships():
            if relationship in seen:
                pass
            else:
                seen.append(relationship)
                self._load_columns_using_relationship(relationship, record, buckets)
                self._load_columns_using_table(relationship.foreign_table, record, buckets, seen)

    def _load_columns_using_relationship(self, relationship, record: dict, buckets: dict):
        """
        Loads columns from a record dict using a relationship object.
        """
        if relationship not in buckets:
            buckets[relationship] = {}
        for cname, value in record.copy().items():
            column = relationship.foreign_table.get_column(cname)
            if column is not None:
                actual_name = column.name
                buckets[relationship][actual_name] = value
                record.pop(cname)

    def _update_relationships(self, record: dict):
        """
        Updates relationship data for this row, storing any extra rows that are needed.

        :param record: The dict record of extra data to store.
        """
        if self._Table__deleted:
            raise RuntimeError('This row is marked as deleted')
        if self.table not in self._relationship_mapping:
            self._relationship_mapping[self.table] = [
             self]
        buckets = {}
        seen = []
        self._load_columns_using_table(self.table, record, buckets, seen)
        for relationship, subdict in buckets.items():
            if all(i is None for i in subdict.values()):
                pass
            else:
                row = relationship.foreign_table._internal_from_row(subdict, existed=True)
                try:
                    next(filter(lambda r: r.primary_key == row.primary_key, self._relationship_mapping[relationship]))
                except StopIteration:
                    self._relationship_mapping[relationship].append(row)

                row._session = self._session

    def to_dict(self, *, include_attrs: bool=False) -> dict:
        """
        Converts this row to a dict, indexed by Column.

        :param include_attrs: Should this include row_attrs?
        """
        d = {col:self.get_column_value(col) for col in self.table.columns}
        return d


def table_base(name: str='Table', meta: 'TableMetadata'=None):
    """
    Gets a new base object to use for OO-style tables.
    This object is the parent of all tables created in the object-oriented style; it provides some
    key configuration to the relationship calculator and the DB object itself.

    To use this object, you call this function to create the new object, and subclass it in your
    table classes:

    .. code-block:: python3

        Table = table_base()

        class User(Table):
            ...

    Binding the base object to the database object is essential for querying:

    .. code-block:: python3

        # ensure the table is bound to that database
        db.bind_tables(Table)

        # now we can do queries
        sess = db.get_session()
        user = await sess.select(User).where(User.id == 2).first()

    Each Table object is associated with a database interface, which it uses for special querying
    inside the object, such as :meth:`.Table.get`.

    .. code-block:: python3

        class User(Table):
            id = Column(Integer, primary_key=True)
            ...

        db.bind_tables(Table)
        # later on, in some worker code
        user = await User.get(1)

    :param name: The name of the new class to produce. By default, it is ``Table``.
    :param meta: The :class:`.TableMetadata` to use as metadata.
    :return: A new Table class that can be used for OO tables.
    """
    if meta is None:
        meta = TableMetadata()
    clone = TableMeta.__new__(TableMeta, name, (Table,), {'metadata': meta}, register=False)
    return clone


class AliasedTable(object):
    __doc__ = '\n    Represents an "aliased table". This is a transparent proxy to a :class:`.TableMeta` table, and\n    will create the right Table objects when called.\n\n    .. code-block:: python3\n\n        class User(Table):\n            id = Column(Integer, primary_key=True, autoincrement=True)\n            username = Column(String, nullable=False, unique=True)\n            password = Column(String, nullable=False)\n\n        NotUser = AliasedTable("not_user", User)\n\n    '

    def __init__(self, alias_name: str, table: 'typing.Type[Table]'):
        """
        :param alias_name: The name of the alias for this table.
        :param table: The :class:`.TableMeta` used to alias this table.
        """
        self.alias_name = alias_name
        self.alias_table = table

    def __getattr__(self, item):
        return getattr(self.alias_table, item)

    def __call__(self, *args, **kwargs):
        return (self.alias_table)(*args, **kwargs)

    def __repr__(self):
        return '<Alias {} for {}>'.format(self.alias_name, self.alias_table)

    def get_column(self, column_name: str) -> 'md_column.Column':
        """
        Gets a column by name from the specified table.

        This will use the base :meth:`.TableMeta.get_column`, and then search for columns via
        their alias name using this table.
        """
        c = self.alias_table.get_column(column_name)
        if c is not None:
            return c
        for column in self.alias_table.iter_columns():
            if column.alias_name(self) == column_name:
                return column

    @property
    def __tablename__(self) -> str:
        return self.alias_name

    @property
    def __quoted_name__(self):
        return '"{}"'.format(self.alias_name)


class PrimaryKey(object):
    __doc__ = '\n    Represents the primary key of a table.\n\n    A primary key can be on any 1 to N columns in a table.\n\n    .. code-block:: python3\n\n        class Something(Table):\n            first_id = Column(Integer)\n            second_id = Column(Integer)\n\n        pkey = PrimaryKey(Something.first_id, Something.second_id)\n        Something.primary_key = pkey\n\n    Alternatively, the primary key can be automatically calculated by passing ``primary_key=True``\n    to columns in their constructor:\n\n    .. code-block:: python3\n\n        class Something(Table):\n            id = Column(Integer, primary_key=True)\n\n        print(Something.primary_key)\n\n    '

    def __init__(self, *cols: 'md_column.Column'):
        self.columns = list(cols)
        self.table = None

    def __repr__(self):
        return "<PrimaryKey table='{}' columns='{}'>".format(self.table, self.columns)