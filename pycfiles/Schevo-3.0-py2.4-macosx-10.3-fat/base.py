# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/test/base.py
# Compiled at: 2007-03-21 14:34:39
"""Test base classes.

For copyright, license, and warranty, see bottom of file.
"""
import os, sys
from schevo import database
from schevo.lib import module
import schevo.schema
from schevo.script.path import package_path
from textwrap import dedent
from StringIO import StringIO
PREAMBLE = 'from schevo.schema import *\nschevo.schema.prep(locals())\n'
SCHEMA = file(os.path.join(os.path.dirname(__file__), 'schema', 'schema_001.py'), 'U').read()

def raises(exc_type, fn, *args, **kw):
    try:
        fn(*args, **kw)
    except Exception, e:
        assert isinstance(e, exc_type)
        return True
    else:
        raise AssertionError('Call did not raise an exception')


_db_cache = {}
_cached_dbs = set()

class BaseTest(object):
    __module__ = __name__

    def setup_method(self, method):
        return self.setUp()

    def teardown_method(self, method):
        return self.tearDown()

    def assertRaises(self, *args, **kw):
        return raises(*args, **kw)

    def setUp(self):
        pass

    def tearDown(self):
        pass


class CreatesDatabase(BaseTest):
    """A mixin to provide test directory and Durus database creation
    and deletion per-method."""
    __module__ = __name__

    def setUp(self):
        self.suffixes = set()
        self.open()

    def tearDown(self):
        for suffix in list(self.suffixes):
            self.close(suffix)

    def close(self, suffix=''):
        """Close the database."""
        db_name = 'db' + suffix
        db = getattr(self, db_name)
        if db not in _cached_dbs:
            db.close()
        delattr(self, db_name)
        delattr(self, 'fp' + suffix)
        delattr(self, 'connection' + suffix)
        modname = self.__class__.__module__
        mod = sys.modules[modname]
        delattr(mod, db_name)
        self.suffixes.remove(suffix)

    def evolve(self, schema_source, version):
        db = self.reopen()
        database.evolve(db, schema_source, version)

    def _base_open(self, suffix='', schema_source=None):
        """Open and return the database, setting self.db if no suffix
        is given.

        May be called more than once in a series of open/close calls.
        """
        value = ''
        if hasattr(self, 'fpv' + suffix):
            value = getattr(self, 'fpv' + suffix)
        fp = StringIO(value)
        db = database.open(fp=fp, schema_source=schema_source)
        db_name = 'db' + suffix
        setattr(self, db_name, db)
        setattr(self, 'fp' + suffix, fp)
        setattr(self, 'connection' + suffix, db.connection)
        self.suffixes.add(suffix)
        modname = self.__class__.__module__
        mod = sys.modules[modname]
        setattr(mod, db_name, db)
        setattr(mod, 'ex', db.execute)
        return db

    def _open(self, suffix='', schema_source=None):
        return self._base_open(suffix, schema_source)

    def open(self):
        """Open the database and perform first-time operations, and
        return the database.

        Must be called only once per test method.
        """
        return self._open()

    def reopen(self, suffix=''):
        """Close and reopen self.db and return its new incarnation."""
        setattr(self, 'fpv' + suffix, getattr(self, 'fp' + suffix).getvalue())
        self.close(suffix)
        db = self._open(suffix)
        delattr(self, 'fpv' + suffix)
        return db

    def sync(self, schema_source):
        db = self.reopen()
        db._sync(schema_source)


class CreatesSchema(CreatesDatabase):
    """A mixin to provide test dir, Durus database, and schema
    creation/deletion per-method."""
    __module__ = __name__
    body = ''
    schema = SCHEMA
    _use_db_cache = True

    def _open(self, suffix=''):
        if self.body:
            schema = self.schema = PREAMBLE + dedent(self.body)
        else:
            schema = self.schema
        use_db_cache = self._use_db_cache
        db_name = 'db' + suffix
        ex_name = 'ex' + suffix
        fpv_name = 'fpv' + suffix
        if use_db_cache and (schema, suffix) in _db_cache and not hasattr(self, fpv_name):
            (db, fp, connection) = _db_cache[(schema, suffix)]
            setattr(self, 'fp' + suffix, fp)
            setattr(self, 'connection' + suffix, connection)
            if not hasattr(self, db_name):
                db._reset_all()
            setattr(self, db_name, db)
        else:
            for m in module.MODULES:
                module.forget(m)

            db = self._base_open(suffix, self.schema)
            if use_db_cache:
                fp = getattr(self, 'fp' + suffix)
                connection = getattr(self, 'connection' + suffix)
                _db_cache[(schema, suffix)] = (db, fp, connection)
                _cached_dbs.add(db)
        modname = self.__class__.__module__
        mod = sys.modules[modname]
        setattr(mod, db_name, db)
        setattr(mod, ex_name, db.execute)
        self.suffixes.add(suffix)
        return db

    def open(self):
        db = self._open()
        db.populate('unittest')
        return db


class EvolvesSchemata(CreatesDatabase):
    __module__ = __name__
    schemata = []
    _use_db_cache = True

    def _open(self, suffix=''):
        use_db_cache = self._use_db_cache
        db_name = 'db' + suffix
        ex_name = 'ex' + suffix
        fpv_name = 'fpv' + suffix
        schema = self.schemata[(-1)]
        if use_db_cache and (schema, suffix) in _db_cache and not hasattr(self, fpv_name):
            (db, fp, connection) = _db_cache[(schema, suffix)]
            setattr(self, 'fp' + suffix, fp)
            setattr(self, 'connection' + suffix, connection)
            if not hasattr(self, db_name):
                db._reset_all()
            setattr(self, db_name, db)
        else:
            for m in module.MODULES:
                module.forget(m)

            db = self._base_open(suffix, self.schemata[0])
            for i in xrange(1, len(self.schemata)):
                schema_source = self.schemata[i]
                database.evolve(db, schema_source, version=i + 1)

            if use_db_cache:
                fp = getattr(self, 'fp' + suffix)
                connection = getattr(self, 'connection' + suffix)
                _db_cache[(schema, suffix)] = (db, fp, connection)
                _cached_dbs.add(db)
        modname = self.__class__.__module__
        mod = sys.modules[modname]
        setattr(mod, db_name, db)
        setattr(mod, ex_name, db.execute)
        self.suffixes.add(suffix)
        return db

    def open(self):
        db = self._open()
        db.populate('unittest')
        return db

    @staticmethod
    def from_package(pkg_name, final_version):
        schemata = []
        schema_path = package_path(pkg_name)
        version = 0
        while True:
            if version == final_version:
                break
            version += 1
            try:
                source = schevo.schema.read(schema_path, version=version)
            except schevo.error.SchemaFileIOError:
                if final_version == 'latest':
                    break
                else:
                    raise

            schemata.append(source)

        return schemata


class DocTest(CreatesSchema):
    """Doctest-helping test class.

    Call directly to override body for one test::

      >>> from schevo.test.base import DocTest
      >>> t = DocTest('''
      ...     class Foo(E.Entity):
      ...         bar = f.integer()
      ...     ''')
      >>> t.db.extent_names()
      ['Foo']

    Call `done` method at end of test case::

      >>> t.done()

    Subclass to override body for several tests::

      >>> class test(DocTest):
      ...     body = '''
      ...     class Foo(E.Entity):
      ...         bar = f.integer()
      ...     '''
      >>> t = test()
      >>> t.db.extent_names()
      ['Foo']
      >>> t.done()
    """
    __module__ = __name__
    body = ''

    def __init__(self, body=None):
        super(DocTest, self).__init__()
        if body:
            self.body = body
        self.setUp()

    def done(self):
        """Test case is done; free up resources."""
        self.tearDown()

    def update(self, body):
        """Update database with new schema, keeping same schema version."""
        self.body = body
        schema_source = PREAMBLE + dedent(self.body)
        self.sync(schema_source)