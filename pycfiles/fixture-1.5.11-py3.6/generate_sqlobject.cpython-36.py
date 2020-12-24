# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fixture/command/generate/generate_sqlobject.py
# Compiled at: 2017-10-02 03:31:12
# Size of source mod 2**32: 9395 bytes
"""support to generate SQLObject-based fixtures."""
from fixture.style import camel_to_under
from fixture import SQLObjectFixture
from fixture.command.generate import DataHandler, FixtureSet, register_handler, code_str, UnsupportedHandler, MisconfiguredHandler, NoData
try:
    import sqlobject
except ImportError:
    sqlobject = None

class SQLObjectHandler(DataHandler):
    loadable_fxt_class = SQLObjectFixture

    def __init__(self, *a, **kw):
        (DataHandler.__init__)(self, *a, **kw)
        from sqlobject import sqlhub, connectionForURI
        if self.options.dsn:
            self.connection = connectionForURI(self.options.dsn)
        else:
            raise MisconfiguredHandler('--dsn option is required by %s' % self.__class__)
        if len(self.options.env):
            raise NotImplementedError('sqlobject is not using --env; perhaps we just need to import the envs so that findClass knows about its objects?')

    def add_fixture_set(self, fset):
        from sqlobject.classregistry import findClass
        so_class = fset.obj_id()
        kls = findClass(so_class)
        self.template.add_import('from %s import %s' % (
         kls.__module__, so_class))

    def find(self, idval):
        self.rs = [
         self.obj.get(idval)]

    def findall(self, query):
        """gets record set for query."""
        self.rs = self.obj.select(query, connection=(self.connection))
        if not self.rs.count():
            raise NoData('no data for query "%s" on object %s' % (
             query, self.obj))

    def fxt_type(self):
        return 'SOFixture'

    @staticmethod
    def recognizes(object_path, obj=None):
        """returns True if obj is a SQLObject class.
        """
        if not sqlobject:
            raise UnsupportedHandler('sqlobject module not found')
        else:
            if obj is None:
                return False
            from sqlobject.declarative import DeclarativeMeta
            if type(obj) is DeclarativeMeta:
                if obj.__name__ not in ('SQLObject', 'sqlmeta', 'ManyToMany', 'OneToMany'):
                    return True

    def sets(self):
        """yields FixtureSet for each row in SQLObject."""
        for row in self.rs:
            yield SQLObjectFixtureSet(row, (self.obj), connection=(self.connection))


register_handler(SQLObjectHandler)

class SQLObjectFixtureSet(FixtureSet):
    __doc__ = 'a fixture set for a SQLObject row.'

    def __init__(self, data, model, connection=None):
        FixtureSet.__init__(self, data)
        self.connection = connection
        self.model = model
        self.meta = model.sqlmeta
        self.foreign_key_class = {}
        self.primary_key = None
        self.understand_columns()
        cols = [
         self.meta.style.idForTable(self.meta.table)]
        cols.extend([self.attr_to_db_col(c) for c in self.meta.columnList])
        vals = [
         getattr(self.data, 'id')]
        vals.extend([self.get_col_value(c.name) for c in self.meta.columnList])
        self.data_dict = dict(zip(cols, vals))

    def attr_to_db_col(self, col):
        if col.dbName is not None:
            return col.dbName
        else:
            return self.meta.style.pythonAttrToDBColumn(col.name)

    def get_col_value(self, colname):
        """transform column name into a value or a
        new set if it's a foreign key (recursion).
        """
        from sqlobject.classregistry import findClass
        value = getattr(self.data, colname)
        if value is None:
            return
        else:
            if self.foreign_key_class.has_key(colname):
                model = findClass(self.foreign_key_class[colname])
                rs = model.get(value, connection=(self.connection))
                return SQLObjectFixtureSet(rs, model, connection=(self.connection))
            return value

    def get_id_attr(self):
        meta = self.meta
        id_attr = meta.style.idForTable(meta.table)
        return id_attr

    def mk_var_name(self):
        """returns a variable name for the instance of the fixture class.
        """
        fxt_cls_name = self.obj_id()
        return '_'.join([camel_to_under(n) for n in fxt_cls_name.split('_')])

    def set_id(self):
        """returns id of this set (the primary key value)."""
        return getattr(self.data, 'id')

    def understand_columns(self):
        """get an understanding of what columns are what, foreign keys, etc."""
        from sqlobject.col import SOForeignKey
        for name, col in self.meta.columns.items():
            if isinstance(col, SOForeignKey):
                self.foreign_key_class[col.name] = col.foreignKey