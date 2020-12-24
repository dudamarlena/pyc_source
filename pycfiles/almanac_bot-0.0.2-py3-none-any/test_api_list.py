# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/test/test_api_list.py
# Compiled at: 2015-08-31 22:18:14
import alman, unittest

class TestApiList(unittest.TestCase):

    def setUp(self):
        self.fake_resource = {'data': 'fake-data'}
        self.apilist = alman.apibits.ApiList(alman.apibits.ApiResource, [self.fake_resource])

    def test_setting_klass(self):
        self.assertEqual(alman.apibits.ApiResource, self.apilist.klass)

    def test_convert_data_to_klass_instances(self):
        self.assertIsInstance(self.apilist[0], alman.apibits.ApiResource)
        self.assertEqual(self.fake_resource, self.apilist[0].json)