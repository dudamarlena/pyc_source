# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/geats/tests/test_dummy_database.py
# Compiled at: 2013-12-22 08:50:12
import unittest
from ..databases.dummydatabase import DummyDatabase

class DummyDatabaseTest(unittest.TestCase):

    def setUp(self):
        self.db = DummyDatabase({})
        self.vmdef = {'vm_type': 'dummy', 
           'name': 'vm001', 
           'description': 'vm001 / appserver 001'}

    def test_create_vm(self):
        self.db.create('vm001', self.vmdef)

    def test_list(self):
        self.db.create('vm001', self.vmdef)
        vms = self.db.list()
        self.assertEqual(vms, ['vm001'])

    def test_get_definition(self):
        self.db.create('vm001', self.vmdef)
        vmdef = self.db.get_definition('vm001')
        self.assertEqual(vmdef, self.vmdef)