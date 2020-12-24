# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vagoth/tests/test_dict_registry.py
# Compiled at: 2013-12-28 16:01:48
"""
Test vagoth.registry.couch_registry.CouchRegistry
"""
import unittest
from ..registry.dict_registry import DictRegistry
import uuid, couchdb
from .. import exceptions
from registry_mixin import RegistryMixin
NO_DEFAULT = uuid.uuid4()

class testDictRegistry(unittest.TestCase, RegistryMixin):

    def setUp(self):
        self.registry = DictRegistry(None, {})
        self.mixin_setUp()
        return

    def test_dict_initial_object(self):
        self.assertEqual(len(self.registry.nodes), 1)
        self.assertTrue('0xdeadbeef' in self.registry.nodes)
        self.assertEqual(len(self.registry.unique), 2)
        self.assertIn('VAGOTH_NAME_node001.example.com', self.registry.unique)
        self.assertIn('node001_uniquekey', self.registry.unique)