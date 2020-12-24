# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fixture/command/generate/generate_sqlalchemy.py
# Compiled at: 2017-10-02 03:31:12
# Size of source mod 2**32: 14791 bytes
import sys, inspect
from six import reraise
from fixture.command.generate import DataHandler, register_handler, FixtureSet, NoData, UnsupportedHandler
from fixture import SQLAlchemyFixture
try:
    import sqlalchemy
except ImportError:
    sqlalchemy = False

class TableEnv(object):
    __doc__ = 'a shared environment of sqlalchemy Table instances.\n    \n    can be initialized with python paths to objects or objects themselves\n    '

    def __init__(self, *objects):
        self.objects = objects
        self.tablemap = {}
        for obj in self.objects:
            module = None
            if isinstance(obj, basestring):
                modpath = obj
                if modpath not in sys.modules:
                    try:
                        if '.' in modpath:
                            cut = modpath.rfind('.')
                            names = [modpath[cut + 1:]]
                            parent = __import__(modpath[0:cut], globals(), locals(), names)
                            module = getattr(parent, names[0])
                        else:
                            module = __import__(modpath)
                    except:
                        etype, val, tb = sys.exc_info()
                        reraise(ImportError, ImportError('%s: %s (while importing %s)' % (
                         etype, val, modpath)))

                else:
                    module = sys.modules[modpath]
                    obj = module
            if module is None:
                module = inspect.getmodule(obj)
            self._find_objects(obj, module)

    def __contains__(self, key):
        return key in self.tablemap

    def __getitem__(self, table):
        try:
            return self.tablemap[table]
        except KeyError:
            reraise(LookupError, LookupError("Could not locate original declaration of Table %s (looked in: %s)  You might need to add --env='path.to.module'?" % (
             table, ', '.join([repr(p) for p in self.objects]))))

    def _find_objects(self, obj, module):
        from sqlalchemy.schema import Table
        if not hasattr(obj, 'items'):

            def getitems():
                for name in dir(obj):
                    yield (
                     name, getattr(obj, name))

        else:
            getitems = obj.items
        for name, o in getitems():
            if isinstance(o, Table):
                self.add_table(o, name=name, module=module)

    def add_table(self, table_obj, name=None, module=None):
        if not name:
            name = table_obj.fullname
        self.tablemap.setdefault(table_obj, {})
        self.tablemap[table_obj]['name'] = name
        self.tablemap[table_obj]['module'] = module

    def get_real_table(self, table):
        return getattr(self[table]['module'], self[table]['name'])


class SQLAlchemyHandler(DataHandler):
    __doc__ = 'handles genration of fixture code from a sqlalchemy data source.'
    loadable_fxt_class = SQLAlchemyFixture

    class RecordSetAdapter(object):
        __doc__ = 'adapts a sqlalchemy record set object for use in a \n        SQLAlchemyFixtureSet.'
        columns = None

        def __init__(self, obj):
            raise NotImplementedError('not a concrete implementation')

        def primary_key_from_instance(self, data):
            raise NotImplementedError

    def __init__(self, object_path, options, connection=None, **kw):
        from sqlalchemy import MetaData, create_engine
        from sqlalchemy.orm import sessionmaker, scoped_session
        self.engine = None
        self.connection = connection
        (super(SQLAlchemyHandler, self).__init__)(object_path, options, **kw)
        if not self.connection:
            if not self.options.dsn:
                raise MisconfiguredHandler('--dsn option is required by %s' % self.__class__)
            self.engine = create_engine(self.options.dsn)
            self.connection = self.engine
            self.meta = MetaData(bind=(self.engine))
            if self.options.dsn.startswith('postgres'):
                import psycopg2.extensions
                self.connection.raw_connection().set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        Session = scoped_session(sessionmaker(autoflush=True, transactional=False, bind=(self.engine)))
        self.session = Session()
        self.env = TableEnv(*[self.obj.__module__] + self.options.env)

    def add_fixture_set(self, fset):
        t = self.env[fset.obj.table]
        self.template.add_import('from %s import %s' % (
         t['module'].__name__, t['name']))

    def begin(self, *a, **kw):
        (DataHandler.begin)(self, *a, **kw)

    def commit(self):
        pass

    def rollback(self):
        pass

    def find(self, idval):
        self.rs = [
         self.obj.get(idval)]
        return self.rs

    def findall(self, query=None):
        """gets record set for query."""
        session = self.session
        if query:
            self.rs = session.query(self.obj).filter(query)
        else:
            self.rs = session.query(self.obj).all()
        if not self.rs.count():
            raise NoData('no data for query "%s" on %s, handler=%s' % (query, self.obj, self.__class__))
        return self.rs

    @staticmethod
    def recognizes(object_path, obj=None):
        """returns True if obj is not None.
        
        this method is just a starting point for sqlalchemy handlers.
        """
        if not sqlalchemy:
            raise UnsupportedHandler('sqlalchemy module not found')
        if obj is None:
            return False
        else:
            return True

    def sets(self):
        """yields FixtureSet for each row in SQLObject."""
        for row in self.rs:
            yield SQLAlchemyFixtureSet(row, (self.obj), (self.connection), (self.env), adapter=(self.RecordSetAdapter))


class SQLAlchemyMappedClassBase(SQLAlchemyHandler):

    class RecordSetAdapter(SQLAlchemyHandler.RecordSetAdapter):

        def __init__(self, obj):
            self.columns = obj.c
            from sqlalchemy.orm.mapper import object_mapper
            self.mapper = object_mapper(obj())
            if self.mapper.local_table:
                self.table = self.mapper.local_table
            else:
                if self.mapper.select_table:
                    self.table = self.mapper.select_table
                else:
                    raise LookupError('not sure how to get a table from mapper %s' % self.mapper)
            self.id_attr = self.table.primary_key.columns.keys()

        def primary_key_from_instance(self, data):
            return self.mapper.primary_key_from_instance(data)

    def __init__(self, *args, **kw):
        (super(SQLAlchemyMappedClassBase, self).__init__)(*args, **kw)
        from sqlalchemy.orm.mapper import class_mapper
        self.mapper = class_mapper(self.obj)
        if self.mapper.local_table:
            self.table = self.mapper.local_table
        else:
            if self.mapper.select_table:
                self.table = self.mapper.select_table
            else:
                raise LookupError('not sure how to get a table from mapper %s' % self.mapper)

    def find(self, idval):
        q = self.session.query(self.obj)
        primary_keys = self.table.primary_key.columns.keys()
        try:
            len(idval)
        except TypeError:
            idval = [
             idval]

        assert len(primary_keys) == len(idval), "length of idval did not match length of the table's primary keys (%s ! %s)" % (
         primary_keys, idval)
        table_cols = self.table.c
        for i, keyname in enumerate(primary_keys):
            q = q.filter(getattr(table_cols, keyname) == idval[i])

        self.rs = q.all()
        return self.rs

    def findall(self, query=None):
        """gets record set for query."""
        session = self.session
        if query:
            self.rs = session.query(self.obj).filter(query)
        else:
            self.rs = session.query(self.obj)
        if not self.rs.count():
            raise NoData('no data for query "%s" on %s, handler=%s' % (query, self.obj, self.__class__))
        return self.rs


class SQLAlchemySessionMapperHandler(SQLAlchemyMappedClassBase):
    __doc__ = 'handles a scoped session mapper\n    \n    that is, one created with sqlalchemy.orm.scoped_session(sessionmaker(...)).mapper()\n    \n    '

    @staticmethod
    def recognizes(object_path, obj=None):
        if not SQLAlchemyHandler.recognizes(object_path, obj=obj):
            return False
        else:
            if not SQLAlchemyMappedClassHandler.recognizes(object_path, obj=obj):
                return False
            if hasattr(obj, 'query'):
                if getattr(obj.query, '__module__', '').startswith('sqlalchemy'):
                    return True
            return False


register_handler(SQLAlchemySessionMapperHandler)

class SQLAlchemyTableHandler(SQLAlchemyHandler):

    class RecordSetAdapter(SQLAlchemyHandler.RecordSetAdapter):

        def __init__(self, obj):
            self.table = obj
            self.columns = self.table.columns
            keys = [k for k in self.table.primary_key]
            if len(keys) != 1:
                raise ValueError('unsupported primary key type %s' % keys)
            self.id_attr = keys[0].key

        def primary_key_from_instance(self, data):
            key_str = []
            for k in self.table.primary_key:
                key_str.append(str(getattr(data, k.key)))

            return '_'.join(key_str)

    @staticmethod
    def recognizes(object_path, obj=None):
        if not SQLAlchemyHandler.recognizes(object_path, obj=obj):
            return False
        else:
            from sqlalchemy.schema import Table
            if isinstance(obj, Table):
                raise NotImplementedError('Generating data with a table object is not implemented.  Please use a mapped class or mapper object instead.  Or, consider submitting a patch to support this.')
                return True
            return False


register_handler(SQLAlchemyTableHandler)

class SQLAlchemyMappedClassHandler(SQLAlchemyMappedClassBase):

    @staticmethod
    def recognizes(object_path, obj=None):
        if not SQLAlchemyHandler.recognizes(object_path, obj=obj):
            return False
        else:
            from sqlalchemy.orm import class_mapper
            try:
                class_mapper(obj)
            except:
                return False
                return True

            return False


register_handler(SQLAlchemyMappedClassHandler)

class SQLAlchemyFixtureSet(FixtureSet):
    __doc__ = 'a fixture set for a sqlalchemy record set.'

    def __init__(self, data, obj, connection, env, adapter=None):
        FixtureSet.__init__(self, data)
        self.env = env
        self.connection = connection
        if adapter:
            self.obj = adapter(obj)
        else:
            self.obj = obj
        self.primary_key = None
        self.data_dict = {}
        for col in self.obj.columns:
            sendkw = {}
            for fk in col.foreign_keys:
                sendkw['foreign_key'] = fk

            val = (self.get_col_value)((col.name), **sendkw)
            self.data_dict[col.name] = val

    def attr_to_db_col(self, col):
        return col.name

    def get_col_value(self, colname, foreign_key=None):
        """transform column name into a value or a
        new set if it's a foreign key (recursion).
        """
        value = getattr(self.data, colname)
        if value is None:
            return
        else:
            if foreign_key:
                from sqlalchemy.ext.assignmapper import assign_mapper
                from sqlalchemy.ext.sqlsoup import class_for_table
                table = foreign_key.column.table
                stmt = table.select(getattr(table.c, foreign_key.column.key) == value)
                rs = self.connection.execute(stmt)
                subset = SQLAlchemyFixtureSet((rs.fetchone()),
                  table, (self.connection), (self.env), adapter=(SQLAlchemyTableHandler.RecordSetAdapter))
                return subset
            return value

    def get_id_attr(self):
        return self.obj.id_attr

    def obj_id(self):
        return self.env[self.obj.table]['name']

    def set_id(self):
        """returns id of this set (the primary key value)."""
        compid = self.obj.primary_key_from_instance(self.data)
        return '_'.join([str(i) for i in compid])