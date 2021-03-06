# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tests/cache/test_cache.py
# Compiled at: 2017-08-21 17:11:07
import testtools
from column.api import backend

class TestLocalMemoryCache(testtools.TestCase):

    def setUp(self):
        super(TestLocalMemoryCache, self).setUp()
        self.store = backend.get_store()

    def test_add_runs(self):
        self.assertTrue(self.store.create_run('key1', {'id': '1'}))
        self.assertEqual({'id': '1'}, self.store.get_run('key1'))

    def test_update_run(self):
        self.store.create_run('key5', {'id': '5'})
        self.store.update_run('key5', {'id': '55'})
        self.assertEqual({'id': '55'}, self.store.get_run('key5'))