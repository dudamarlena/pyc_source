# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/tests/tests_db.py
# Compiled at: 2013-11-10 14:30:06
import logging
from nose.tools import assert_equal, raises, assert_not_equal
from arango.exceptions import DatabaseAlreadyExist, DatabaseSystemError
from arango import create
from .tests_integraion_base import TestsIntegration
logger = logging.getLogger(__name__)

class TestsDB(TestsIntegration):

    def setUp(self):
        super(TestsDB, self).setUp()

    def tearDown(self):
        super(TestsDB, self).tearDown()
        create(db='test1').database.delete()

    def test_info(self):
        data = self.conn.database.info
        assert_equal(data['name'], 'test')
        assert_equal(data['isSystem'], False)

    def test_create(self):
        c = create(db='test1')
        assert_equal(c.database.info, {})
        c.database.create()
        assert_not_equal(c.database.info, {})
        c.database.delete()
        assert_equal(c.database.info, {})

    @raises(DatabaseAlreadyExist)
    def test_create_exist_database(self):
        c = create(db='test1')
        c.database.create()
        c.database.create(ignore_exist=False)

    @raises(DatabaseSystemError)
    def test_delete_exist_database(self):
        self.conn.database.delete(ignore_exist=False)
        self.conn.database.delete(ignore_exist=False)