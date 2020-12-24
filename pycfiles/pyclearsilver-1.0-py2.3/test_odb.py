# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyclearsilver/test_odb.py
# Compiled at: 2005-10-10 17:59:17
"""
usage: %(progname)s [args]
"""
import os, sys, string, time, getopt
from log import *
import odb, unittest

def TEST_MYSQL(output=warn):
    output('------ TESTING MySQLdb ---------')
    import odb_mysql
    conn = odb_mysql.Connection(host='localhost', user='root', passwd='', db='test')
    db = odb.Database(conn)
    return db


def TEST_SQLITE(output=warn):
    output('------ TESTING sqlite2 ----------')
    import odb_sqlite
    conn = odb_sqlite.Connection('/tmp/test2.db', autocommit=1)
    db = odb.Database(conn)
    return db


def TEST_SQLITE3(output=warn):
    output('------ TESTING sqlite3 ----------')
    import odb_sqlite3
    conn = odb_sqlite3.Connection('/tmp/test3.db', autocommit=1)
    db = odb.Database(conn)
    return db


def TEST_POSTGRES(output=warn):
    output('------ TESTING postgres ----------')
    import odb_postgres
    conn = odb_postgres.Connection(database='test')
    db = odb.Database(conn)
    return db


def setupDB(dbType='sqlite3'):
    if dbType == 'sqlite3':
        db = TEST_SQLITE3()
    elif dbType == 'sqlite2':
        db = TEST_SQLITE()
    elif dbType == 'mysql':
        db = TEST_MYSQL()
    elif dbType == 'postgres':
        db = TEST_POSTGRES()
    db.enabledCompression()
    db.addTable('agents', 'agents', AgentsTable)
    try:
        db.agents.dropTable()
    except:
        pass

    db.addTable('roles', 'roles', TestTable)
    try:
        db.test.dropTable()
    except:
        pass

    db.createTables()
    db.createIndices()
    return db


class AgentsTable(odb.Table):
    __module__ = __name__

    def _defineRows(self):
        self.d_addColumn('agent_id', odb.kInteger, None, primarykey=1, autoincrement=1)
        self.d_addColumn('login', odb.kVarString, 200, notnull=1)
        self.d_addColumn('ext_email', odb.kVarString, 200, notnull=1, indexed=1)
        self.d_addColumn('hashed_pw', odb.kVarString, 20, notnull=1)
        self.d_addColumn('name', odb.kBigString, compress_ok=1)
        self.d_addColumn('auth_level', odb.kInteger, None)
        self.d_addColumn('ticket_count', odb.kIncInteger, None)
        self.d_addColumn('data', odb.kBlob, None, compress_ok=1)
        self.d_addValueColumn()
        self.d_addVColumn('columnA', odb.kInteger, None)
        self.d_hasMany('roles')
        return


class TestTable(odb.Table):
    __module__ = __name__

    def _defineRows(self):
        self.d_addColumn('oid', odb.kInteger, None, primarykey=1, autoincrement=1)
        self.d_addColumn('agent_id', odb.kInteger)
        self.d_addColumn('a', odb.kInteger)
        self.d_addColumn('b', odb.kInteger)
        self.d_belongsTo('agents', foreign_key='agent_id')
        return


class Test_Database(unittest.TestCase):
    __module__ = __name__

    def __init__(self, methodName='runTest', db=None):
        unittest.TestCase.__init__(self, methodName=methodName)
        self.db = db
        if self.db is None:
            self.db = gDB
        self.TEST_INSERT_COUNT = 5
        return

    def setUp(self):
        self.db.agents.deleteAllRows()

    def test_fetchRow(self):
        try:
            a_row = self.db.agents.fetchRow(('agent_id', 1000))
            self.fail('fetchRow eNoMatchingRows')
        except odb.eNoMatchingRows:
            pass

    def test_rowCreation(self):
        for n in range(self.TEST_INSERT_COUNT):
            new_id = n + 1
            newrow = self.db.agents.newRow()
            newrow.name = 'name #%d' % new_id
            newrow.login = 'name%d' % new_id
            newrow.ext_email = '%d@name' % new_id
            newrow.hashed_pw = 'hashedpw'
            newrow.save()
            msg = 'new insert id (%d) does not match expected value (%d)' % (newrow.agent_id, new_id)
            self.assertEqual(newrow.agent_id, new_id, msg=msg)

    def test_fetchRow_One(self):
        row = self.db.agents.newRow()
        row.name = 'name #1'
        row.login = 'name #2'
        row.ext_email = 'name #2'
        row.hashed_pw = 'lsjdf'
        row.save()
        a_row = self.db.agents.fetchRow(('agent_id', 1))
        self.assertEqual(a_row.name, 'name #1')
        return a_row

    def test_save(self):
        a_row = self.test_fetchRow_One()
        try:
            a_row.save(cursor='dummy cursor')
        except AttributeError, reason:
            self.fail('row tried to access cursor on save() when no changes were made!')

    def test_save(self):
        a_row = self.test_fetchRow_One()
        a_row.auth_level = 10
        a_row.save()
        b_row = self.db.agents.fetchRow(('agent_id', 1))
        self.assertEqual(b_row.auth_level, 10, 'save and load failed')

    def misc(self):
        pass

    def test_unknownAttribute(self):
        a_row = self.test_fetchRow_One()
        try:
            a = a_row.UNKNOWN_ATTRIBUTE
            self.fail('unknown attribute')
        except AttributeError, reason:
            pass
        except odb.eNoSuchColumn, reason:
            pass

    def test_unknownAttribute2(self):
        a_row = self.test_fetchRow_One()
        try:
            a_row.UNKNOWN_ATTRIBUTE = 1
            self.fail('unknown attribute')
        except AttributeError, reason:
            pass
        except odb.eNoSuchColumn, reason:
            pass

    def test_unknownAttribute3(self):
        a_row = self.test_fetchRow_One()
        try:
            a = a_row['UNKNOWN_ATTRIBUTE']
            self.fail('unknown attribute')
        except KeyError, reason:
            pass
        except odb.eNoSuchColumn, reason:
            pass

    def test_unknownAttribute3(self):
        a_row = self.test_fetchRow_One()
        try:
            a_row['UNKNOWN_ATTRIBUTE'] = 1
            self.fail('unknown attribute')
        except KeyError, reason:
            pass
        except odb.eNoSuchColumn, reason:
            pass

    def misc2(self):
        pass

    def test_fetchRows(self):
        arow = self.test_fetchRow_One()
        rows = self.db.agents.fetchRows(('agent_id', 1))
        self.assertEqual(len(rows), 1)

    def test_fetchRows(self):
        arow = self.test_rowCreation()
        rows = self.db.agents.fetchAllRows()
        self.assertEqual(len(rows), self.TEST_INSERT_COUNT)

    def test_deleteObject(self):
        arow = self.test_fetchRow_One()
        row = self.db.agents.fetchRow(('agent_id', 1))
        row.delete()
        try:
            row = self.db.agents.fetchRow(('agent_id', 1))
            self.fail()
        except odb.eNoMatchingRows:
            pass

    def test_deleteRow(self):
        self.test_rowCreation()
        row = self.db.agents.fetchRow(('agent_id', 2))
        self.db.agents.deleteRow(('agent_id', 2))
        try:
            row = self.db.agents.fetchRow(('agent_id', 2))
            self.fail()
        except odb.eNoMatchingRows:
            pass

    def test_datasize(self):
        self.test_rowCreation()
        row = self.db.agents.fetchRow(('agent_id', 3))
        if row.databaseSizeForColumn('name') != len(row.name):
            self.fail()

    def test_primarykey(self):
        self.test_rowCreation()
        row = self.db.agents.fetchRowUsingPrimaryKey(3)
        if row.agent_id != 3:
            self.fail()

    def test_lookup(self):
        self.test_rowCreation()
        row = self.db.agents.lookup(agent_id=3)
        if row.agent_id != 3:
            self.fail()

    def test_lookupCreate(self):
        row = self.db.agents.lookupCreate(agent_id=2)
        if row.isClean():
            self.fail()
        row.login = 1
        row.ext_email = 'hassan@dotfunk.com'
        row.hashed_pw = 'sdfj'
        row.save()

    def misc3(self):
        pass

    def test_virtualColumns(self):
        self.test_rowCreation()
        try:
            b_row = self.db.agents.fetchRow(('agent_id', 5))
        except odb.eNoMatchingRows:
            self.fail()

        b_row.columnA = 'hello'
        b_row.save()
        b_row = self.db.agents.fetchRow(('agent_id', 5))
        self.assertEqual(b_row.columnA, 'hello')

    def test_compression(self):
        self.test_rowCreation()
        try:
            b_row = self.db.agents.fetchRow(('agent_id', 5))
        except odb.eNoMatchingRows:
            self.fail()

        d = 'hello\x00hello' * 100
        b_row.data = d
        b_row.save()
        b_row = self.db.agents.fetchRow(('agent_id', 5))
        self.assertEqual(b_row.data, d)

    def test_relations(self):
        self.test_rowCreation()
        row = self.db.roles.newRow()
        row.agent_id = 2
        row.a = '1'
        row.b = '2'
        row.save()
        row2 = self.db.roles.lookup(oid=row.oid)


def test():
    pass


def usage(progname):
    print __doc__ % vars()


def main(argv, stdout, environ):
    global gDB
    progname = argv[0]
    (optlist, args) = getopt.getopt(argv[1:], '', ['help', 'test', 'debug'])
    testflag = 0
    for (field, val) in optlist:
        if field == '--help':
            usage(progname)
            return
        elif field == '--debug':
            debugfull()
        elif field == '--test':
            testflag = 1

    if testflag:
        test()
        return
    gDB = setupDB('sqlite3')
    unittest.main()
    return
    for arg in args:
        if arg == 'sqlite2':
            TEST_SQLITE()
        elif arg == 'sqlite3':
            TEST_SQLITE3()
        elif arg == 'mysql':
            TEST_MYSQL()
        elif arg == 'postgres':
            TEST_POSTGRES()


if __name__ == '__main__':
    main(sys.argv, sys.stdout, os.environ)