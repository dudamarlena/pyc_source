# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/django_evolution/tests/test_database_sig.py
# Compiled at: 2018-06-14 23:17:51
from django.test.testcases import TestCase
from django_evolution.db import EvolutionOperationsMulti
from django_evolution.models import Evolution
from django_evolution.signature import create_database_sig

class DatabaseSigTests(TestCase):
    """Testing database signatures."""

    def setUp(self):
        self.database_sig = create_database_sig('default')
        self.evolver = EvolutionOperationsMulti('default').get_evolver()

    def test_initial_state(self):
        """Testing initial state of database_sig"""
        tables = self.database_sig.keys()
        self.assertTrue('auth_permission' in tables)
        self.assertTrue('auth_user' in tables)
        self.assertTrue('django_evolution' in tables)
        self.assertTrue('django_project_version' in tables)
        self.assertTrue('indexes' in self.database_sig['django_evolution'])
        index_name = self.evolver.get_default_index_name(Evolution._meta.db_table, Evolution._meta.get_field('version'))
        indexes = self.database_sig['django_evolution']['indexes']
        self.assertTrue(index_name in indexes)
        self.assertEqual(indexes[index_name], {'unique': False, 
           'columns': [
                     'version_id']})