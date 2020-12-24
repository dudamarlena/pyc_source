# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\db\tests\test_util.py
# Compiled at: 2010-12-23 17:42:43
"""
Test suite for DB utilities.
"""
from seishub.core.db import DEFAULT_PREFIX, util
from seishub.core.db.manager import meta
from seishub.core.test import SeisHubEnvironmentTestCase
from sqlalchemy import sql, Table, Column, Integer, String, ForeignKey, and_, or_
import unittest
test_meta = meta
users = Table(DEFAULT_PREFIX + 'users', test_meta, Column('id', Integer, primary_key=True), Column('name', String), Column('fullname', String))
addresses = Table(DEFAULT_PREFIX + 'addresses', test_meta, Column('id', Integer, primary_key=True), Column('user_id', None, ForeignKey(DEFAULT_PREFIX + 'users.id')), Column('email_address', String, nullable=False))

class DBUtilTest(SeisHubEnvironmentTestCase):
    """
    Test suite for DB utilities.
    """

    def setUp(self):
        self.db = self.env.db.engine
        test_meta.create_all(self.db, checkfirst=True)
        self.db.execute(users.insert(), [{'id': 1, 'name': 'jack', 'fullname': 'Jack Jones'}, {'id': 2, 'name': 'wendy', 'fullname': 'Wendy Williams'}, {'id': 3, 'name': 'fred', 'fullname': 'Fred Flintstone'}, {'id': 4, 'name': 'mary', 'fullname': 'Mary Contrary'}])
        self.db.execute(addresses.insert(), [{'user_id': 1, 'email_address': 'jack@yahoo.com'}, {'user_id': 1, 'email_address': 'jack@msn.com'}, {'user_id': 2, 'email_address': 'www@www.org'}, {'user_id': 2, 'email_address': 'wendy@aol.com'}])

    def tearDown(self):
        addresses.drop()
        users.drop()

    def test_compileStaticStatement(self):
        """
        Tests compiling of a static statement.
        """
        sql_auto = sql.select([
         (users.c.fullname + ', ' + addresses.c.email_address).label('title')], and_(users.c.id == addresses.c.user_id, users.c.name.between('m', 'z'), or_(addresses.c.email_address.like('%@aol.com'), addresses.c.email_address.like('%@msn.com'))))
        result = self.db.execute(sql_auto)
        result = result.fetchall()
        self.assertEquals(result, [('Wendy Williams, wendy@aol.com', )])
        sql_compiled = util.compileStatement(sql_auto)
        result = self.db.execute(sql.text(sql_compiled))
        result = result.fetchall()
        self.assertEquals(result, [('Wendy Williams, wendy@aol.com', )])

    def test_compileStatementFromText(self):
        sql_auto = sql.select([
         sql.text(DEFAULT_PREFIX + "users.fullname || ', ' || " + DEFAULT_PREFIX + 'addresses.email_address AS title')], and_(DEFAULT_PREFIX + 'users.id = ' + DEFAULT_PREFIX + 'addresses.user_id', DEFAULT_PREFIX + "users.name BETWEEN 'm' AND 'z'", '(' + DEFAULT_PREFIX + 'addresses.email_address LIKE :x OR ' + DEFAULT_PREFIX + 'addresses.email_address LIKE :y)'), from_obj=[
         DEFAULT_PREFIX + 'users', DEFAULT_PREFIX + 'addresses'])
        result = self.db.execute(sql_auto, x='%@aol.com', y='%@msn.com')
        result = result.fetchall()
        self.assertEquals(result, [('Wendy Williams, wendy@aol.com', )])
        sql_compiled = util.compileStatement(sql_auto, bind=self.db, x='%@aol.com', y='%@msn.com')
        result = self.db.execute(sql.text(sql_compiled))
        result = result.fetchall()
        self.assertEquals(result, [('Wendy Williams, wendy@aol.com', )])

    def test_compileStatementWithStringBindParameter(self):
        sql_auto = sql.select([users, addresses], users.c.name.like(sql.bindparam('name', type_=String) + sql.text("'%'")) | addresses.c.email_address.like(sql.bindparam('name', type_=String) + sql.text("'@%'")), from_obj=[
         users.outerjoin(addresses)])
        result = self.db.execute(sql_auto, name='jack')
        result = result.fetchall()
        self.assertEquals(result, [
         (1, 'jack', 'Jack Jones', 1, 1, 'jack@yahoo.com'),
         (1, 'jack', 'Jack Jones', 2, 1, 'jack@msn.com')])
        sql_compiled = util.compileStatement(sql_auto, name='jack')
        result = self.db.execute(sql.text(sql_compiled))
        result = result.fetchall()
        self.assertEquals(result, [
         (1, 'jack', 'Jack Jones', 1, 1, 'jack@yahoo.com'),
         (1, 'jack', 'Jack Jones', 2, 1, 'jack@msn.com')])

    def test_compileStatementWithIntegerBindParameter(self):
        sql_auto = sql.select([users], users.c.id == sql.bindparam('id', type_=Integer))
        result = self.db.execute(sql_auto, id=2)
        result = result.fetchall()
        self.assertEquals(result, [(2, 'wendy', 'Wendy Williams')])
        sql_compiled = util.compileStatement(sql_auto, id=2)
        result = self.db.execute(sql.text(sql_compiled))
        result = result.fetchall()
        self.assertEquals(result, [(2, 'wendy', 'Wendy Williams')])


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DBUtilTest, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')