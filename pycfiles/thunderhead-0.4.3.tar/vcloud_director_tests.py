# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/errr/programs/python/thunderhead/tests/vcloud_director_tests.py
# Compiled at: 2015-03-05 16:14:12
import vcr, tests
from thunderhead.builder import vcloud_director

class VcloudDirectorTests(tests.VCRBasedTests):

    @vcr.use_cassette('create_vcd_success.yaml', cassette_library_dir=tests.fixtures_path, record_mode='once')
    def test_create_vcd_success(self):
        vcd_info = {'hostname': '10.12.254.111', 
           'username': 'administrator', 
           'password': 'password'}
        vcd = vcloud_director.create_vcd_server(tests.CONNECTION, vcd_info)
        self.assertIsInstance(vcd, dict)