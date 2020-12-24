# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/dbsprockets/test/testMetadata.py
# Compiled at: 2008-06-30 11:43:30
from nose.tools import raises, eq_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbsprockets.metadata import Metadata, MetadataError, DatabaseMetadata, FieldsMetadata, FieldMetadata
from dbsprockets.saprovider import SAProvider
from dbsprockets.test.base import sortedTableList
from dbsprockets.iprovider import IProvider
import model
from model import *

def setup():
    engine = create_engine('sqlite://')
    metadata.bind = engine
    metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, autoflush=True, transactional=True)
    session = Session()
    u = User()
    u.user_name = 'asdf'
    u.password = 'asdf'
    u.email = 'asdf@asdf.com'
    session.save(u)
    g = Group(group_name='group', display_name='group')
    session.save(g)
    session.flush()


provider = SAProvider(metadata)

class TestMetadata:
    obj = Metadata
    provider = IProvider()

    def setup(self):
        self.metadata = self.obj(self.provider)

    def testCreate(self):
        pass

    @raises(TypeError)
    def _create(self, arg1):
        Metadata(arg1)

    def testCreateBad(self):
        badInput = (
         (), [], {}, 'a', 1, 1.2)
        for input in badInput:
            yield (
             self._create, input)

    @raises(NotImplementedError)
    def testPrimaryKeys(self):
        self.metadata.primaryKeys()

    @raises(NotImplementedError)
    def testSetItem(self):
        self.metadata['asdf'] = 'asdf'

    @raises(NotImplementedError)
    def testGetItem(self):
        value = self.metadata['asdf']

    @raises(NotImplementedError)
    def testKeys(self):
        value = self.metadata.keys()

    @raises(NotImplementedError)
    def testAutoIncrementFields(self):
        value = self.metadata.autoIncrementFields


class TestDatabaseMetadata(TestMetadata):

    def setup(self):
        self.metadata = DatabaseMetadata(provider)

    def testKeys(self):
        tables = sorted(self.metadata.keys())
        expected = sortedTableList
        assert tables == expected, 'expected: %s\n actual: %s' % (expected, tales)

    def testSetItem(self):
        self.metadata['asdf'] = 'asdf'

    def testGetItem(self):
        table = self.metadata['test_table']

    def testGetAddedInfo(self):
        self.metadata['asdf'] = 'asdf'
        assert self.metadata['asdf'] == 'asdf'

    @raises(MetadataError)
    def testSetItemBad(self):
        self.metadata['test_table'] = '1234'

    def testPrimaryKeys(self):
        assert [] == self.metadata.primaryKeys()

    def testGetForeignKeys(self):
        metadata = DatabaseMetadata(provider)
        pks = metadata.foreignKeys
        assert [] == pks, '%s' % pks


class TestFieldsMetadata(TestMetadata):

    def setup(self):
        self.metadata = FieldsMetadata(provider, 'test_table')

    def testGetItem(self):
        field = self.metadata['id']
        assert field.name == 'id'

    def testAutoIncrementFields(self):
        value = self.metadata.autoIncrementFields
        eq_(value, ['id', 'created', 'BLOB', 'BOOLEAN_', 'Binary',
         'Boolean', 'CHAR', 'CLOB', 'DATE_', 'DATETIME_',
         'DECIMAL', 'Date', 'DateTime', 'FLOAT_',
         'Float', 'INT', 'Integer', 'Numeric', 'PickleType',
         'SMALLINT', 'SmallInteger', 'String', 'TEXT', 'TIME_',
         'Time', 'TIMESTAMP', 'Unicode', 'VARCHAR', 'Password'])

    @raises(KeyError)
    def testGetItemKeyError(self):
        self.metadata['asdf']

    def testSetItem(self):
        self.metadata['asdf'] = '1234'
        assert self.metadata['asdf'] == '1234'

    @raises(MetadataError)
    def testSetItemBad(self):
        self.metadata['id'] = '1234'

    def testKeys(self):
        self.metadata['asdf'] = '1234'
        keys = sorted(self.metadata.keys())
        assert keys == ['BLOB', 'BOOLEAN_', 'Binary', 'Boolean', 'CHAR', 'CLOB', 'DATETIME_', 'DATE_', 'DECIMAL', 'Date', 'DateTime', 'FLOAT_', 'Float', 'INT', 'Integer', 'Numeric', 'Password', 'PickleType', 'SMALLINT', 'SmallInteger', 'String', 'TEXT', 'TIMESTAMP', 'TIME_', 'Time', 'Unicode', 'VARCHAR', 'asdf', 'created', 'id'], 'actual: %s' % keys

    def testPrimaryKeys(self):
        pks = self.metadata.primaryKeys()
        assert ['id'] == pks, '%s' % pks

    def testGetForeignKeys(self):
        metadata = FieldsMetadata(provider, 'tg_user')
        pks = metadata.foreignKeys
        assert ['town'] == pks, '%s' % pks