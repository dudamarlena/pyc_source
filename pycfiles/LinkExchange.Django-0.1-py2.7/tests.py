# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange_django/tests.py
# Compiled at: 2011-05-12 16:14:22
import unittest
from linkexchange.tests import MultiHashDriverTestMixin
from linkexchange_django.models import DBHash
from linkexchange_django.db_drivers import DjangoMultiHashDriver

class DBHashTest(unittest.TestCase):

    def setUp(self):
        self.hash = DBHash.objects.create(dbname='testdb', key='testkey')
        self.hash.save()

    def tearDown(self):
        self.hash.items.all().delete()
        self.hash.delete()

    def test_clear_items(self):
        self.hash.set_items([('k1', 'v1'), ('k2', 'v2')])
        self.hash.save()
        self.assertEqual(len(self.hash), 2)
        self.hash.clear_items()
        self.hash.save()
        self.assertEqual(len(self.hash), 0)

    def test_update_items(self):
        self.hash.set_items([('k1', 'v1'), ('k2', 'v2'), ('k3', 'v3')])
        self.hash.save()
        self.assertEqual(len(self.hash), 3)
        self.hash.update_items([('k3', 'v3x'), ('k4', 'v4')])
        self.hash.save()
        self.assertEqual(len(self.hash), 4)
        self.assertEqual(self.hash['k1'], 'v1')
        self.assertEqual(self.hash['k2'], 'v2')
        self.assertEqual(self.hash['k3'], 'v3x')
        self.assertEqual(self.hash['k4'], 'v4')

    def test_set_items(self):
        self.hash.set_items([('k1', 'v1'), ('k2', 'v2'), ('k3', 'v3')])
        self.hash.save()
        self.assertEqual(len(self.hash), 3)
        self.assertEqual(self.hash['k1'], 'v1')
        self.assertEqual(self.hash['k2'], 'v2')
        self.assertEqual(self.hash['k3'], 'v3')
        self.hash.set_items([('k1', 'v1'), ('k3', 'v3x'), ('k4', 'v4')])
        self.hash.save()
        self.assertEqual(len(self.hash), 3)
        self.assertEqual(self.hash['k1'], 'v1')
        self.assertEqual(self.hash['k3'], 'v3x')
        self.assertEqual(self.hash['k4'], 'v4')

    def test_delete_items(self):
        self.hash.set_items([('k1', 'v1'), ('k2', 'v2'), ('k3', 'v3')])
        self.hash.save()
        self.assertEqual(len(self.hash), 3)
        self.hash.delete_items(['k2', 'k3'])
        self.assertEqual(len(self.hash), 1)


class DjangoMultiHashDriverTest(MultiHashDriverTestMixin, unittest.TestCase):
    with_blocking = False

    def setUp(self):
        self.db = DjangoMultiHashDriver('testdb')

    def tearDown(self):
        for h in DBHash.objects.filter(dbname=self.db.dbname):
            h.items.all().delete()
            h.delete()

        del self.db