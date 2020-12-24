# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/dataaccess/test_dataaccess.py
# Compiled at: 2020-03-21 10:42:53
# Size of source mod 2**32: 690 bytes
from unittest import TestCase
from tt.dataaccess.utils import *

class TestDataaccess(TestCase):

    def test_basic_json_datastore_creation(self):
        datastore = get_data_store()
        self.assertIsNotNone(datastore, 'Should not be none, but is')

    def test_loading_json_datastore(self):
        datastore = get_data_store()
        data = datastore.load()
        self.assertIsNotNone(data, 'Should not be none, but is')
        self.assertIsNotNone(data['work'], "Data should have empty work list, but doesn't")

    def test_wrong_datastore_type_generates_exception(self):
        with self.assertRaises(NonexistentDatasource):
            datastore = get_data_store('XML')