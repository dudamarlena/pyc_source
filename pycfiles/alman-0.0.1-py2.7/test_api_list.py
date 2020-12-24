# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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