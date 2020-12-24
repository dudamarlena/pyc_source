# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/lead/tests.py
# Compiled at: 2008-04-27 07:30:45
import os, unittest, transaction, sqlalchemy as sa
from sqlalchemy import orm, sql
from collective.lead import Database, tx
from collective.lead.interfaces import IDatabase, ITransactionAware
from zope.component import provideAdapter, provideUtility, getUtility
DB_NAME = 'collective.lead.tests.testlead'
LeadDataManager = tx.ThreadlocalDatabaseDataManager
provideAdapter(tx.ThreadlocalDatabaseTransactions, adapts=(Database,), provides=ITransactionAware)

class SimpleModel(object):
    __module__ = __name__

    def __init__(self, **kw):
        for (k, v) in kw.items():
            setattr(self, k, v)

    def asDict(self):
        return dict((k.startswith('_') or (k, v) for (k, v) in self.__dict__.items()))


class User(SimpleModel):
    __module__ = __name__


class Skill(SimpleModel):
    __module__ = __name__


class TestDatabase(Database):
    __module__ = __name__
    _url = os.environ.get('TEST_DSN', 'sqlite:///test')

    def _setup_tables(self, metadata, tables):
        tables['test_users'] = sa.Table('test_users', metadata, sa.Column('id', sa.Integer, primary_key=True), sa.Column('firstname', sa.Text), sa.Column('lastname', sa.Text))
        tables['test_skills'] = sa.Table('test_skills', metadata, sa.Column('id', sa.Integer, primary_key=True), sa.Column('user_id', sa.Integer), sa.Column('name', sa.Text), sa.ForeignKeyConstraint(('user_id', ), ('test_users.id', )))

    def _setup_mappers(self, tables, mappers):
        mappers['test_users'] = orm.mapper(User, tables['test_users'], properties={'skills': orm.relation(Skill, primaryjoin=tables['test_users'].columns['id'] == tables['test_skills'].columns['user_id'])})
        mappers['test_skills'] = orm.mapper(Skill, tables['test_skills'])


def setup_db():
    db = TestDatabase()
    provideUtility(db, IDatabase, name=DB_NAME)


setup_db()

class LeadTests(unittest.TestCase):
    __module__ = __name__

    @property
    def db(self):
        return getUtility(IDatabase, name=DB_NAME)

    def setUp(self):
        pass

    def tearDown(self):
        transaction.abort()

    def testAAA(self):
        ignore = self.db.session
        self.db._metadata.drop_all()
        self.db._metadata.create_all()
        transaction.commit()

    def testzzz(self):
        self.db._metadata.drop_all()
        transaction.commit()

    def testSimplePopulation(self):
        session = self.db.session
        query = session.query(User)
        rows = query.all()
        self.assertEqual(len(rows), 0)
        session.save(User(id=1, firstname='udo', lastname='juergens'))
        session.save(User(id=2, firstname='heino', lastname='n/a'))
        session.flush()
        rows = query.order_by(query.table.c.id).all()
        self.assertEqual(len(rows), 2)
        row1 = rows[0]
        d = row1.asDict()
        self.assertEqual(d, {'firstname': 'udo', 'lastname': 'juergens', 'id': 1})
        stmt = sql.select(query.table.columns).order_by('id')
        results = self.db.connection.execute(stmt)
        self.assertEqual(results.fetchall(), [(1, 'udo', 'juergens'), (2, 'heino', 'n/a')])
        transaction.abort()
        self.db._metadata.create_all()
        results = self.db.connection.execute(stmt)
        self.assertEqual(results.fetchall(), [])

    def testXXRelations(self):
        session = self.db.session
        session.save(User(id=1, firstname='foo', lastname='bar'))
        user = session.query(User).filter_by(firstname='foo')[0]
        user.skills.append(Skill(id=1, name='Zope'))
        session.flush()

    def testTransactionJoining(self):
        transaction.abort()
        t = transaction.get()
        self.failIf([ r for r in t._resources if r.__class__ is LeadDataManager ], 'Joined transaction too early')
        ignore = self.db.session
        self.failUnless([ r for r in t._resources if r.__class__ is LeadDataManager ], 'Not joined transaction')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(LeadTests))
    return suite