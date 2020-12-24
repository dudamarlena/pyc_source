# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/tests/db_firebird.py
# Compiled at: 2018-07-11 18:15:31
from django.db import models
from south.db import db
from south.tests import unittest, skipUnless

class FirebirdTests(unittest.TestCase):
    """
    Tests firebird related issues
    """

    def setUp(self):
        print '=' * 80
        print 'Begin Firebird test'

    def tearDown(self):
        print 'End Firebird test'
        print '=' * 80

    @skipUnless(db.backend_name == 'firebird', 'Firebird-only test')
    def test_firebird_double_index_creation_1317(self):
        """
        Tests foreign key creation, especially uppercase (see #61)
        """
        Test = db.mock_model(model_name='Test', db_table='test5a', db_tablespace='', pk_field_name='ID', pk_field_type=models.AutoField, pk_field_args=[])
        db.create_table('test5a', [('ID', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True))])
        db.create_table('test5b', [
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'UNIQUE', models.ForeignKey(Test))])
        db.execute_deferred_sql()