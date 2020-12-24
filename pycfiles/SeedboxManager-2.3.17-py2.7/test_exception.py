# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/tests/db/test_exception.py
# Compiled at: 2015-06-14 13:30:57
from seedbox.db import exception
from seedbox.tests import test

class DbExceptionTest(test.BaseTestCase):

    def test_db_error(self):

        def gen_error(an_error):
            raise exception.DBError(an_error)

        err = self.assertRaises(exception.DBError, gen_error, ValueError)
        self.assertEqual(ValueError, err.inner_exception)

    def test_multiple_results_error(self):

        def gen_error(an_error):
            raise exception.MultipleResultsFound(an_error)

        err = self.assertRaises(exception.MultipleResultsFound, gen_error, RuntimeError)
        self.assertEqual(RuntimeError, err.inner_exception)

    def test_no_results_error(self):

        def gen_error(an_error):
            raise exception.NoResultFound(an_error)

        err = self.assertRaises(exception.NoResultFound, gen_error, RuntimeError)
        self.assertEqual(RuntimeError, err.inner_exception)

    def test_db_migration_error(self):

        def gen_error(an_error):
            raise exception.DbMigrationError(an_error)

        err = self.assertRaises(exception.DbMigrationError, gen_error, RuntimeError)
        self.assertEqual(RuntimeError, err.inner_exception)