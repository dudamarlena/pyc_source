# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/tests/common/base_test.py
# Compiled at: 2018-03-12 09:48:15
# Size of source mod 2**32: 3725 bytes
"""UtilTest class"""
import unittest
from ...common.base import Base

class BaseTest(unittest.TestCase):

    def test_load_json_from_str(self):
        json_01 = Base.load_json_from_str('')
        self.assertEqual(json_01, {})
        json_02 = Base.load_json_from_str('{"hello": "world"}')
        self.assertEqual(json_02, {'hello': 'world'})

    def test_response_success(self):
        res = Base.response_success('MOD_01', 'CREATE', '{content hash}')
        expected_res = {'success':True,  'info':'MOD_01 created successfully',  'app_info':{},  'data':'{content hash}'}
        self.assertEqual(res, expected_res)
        res = Base.response_success('MOD_02', 'UPDATE', '{content hash}')
        expected_res = {'success':True,  'info':'MOD_02 updated successfully',  'app_info':{},  'data':'{content hash}'}
        self.assertEqual(res, expected_res)
        res = Base.response_success('MOD_03', 'GET', '{content hash}')
        expected_res = {'success':True,  'info':'Got MOD_03 successfully',  'app_info':{},  'data':'{content hash}'}
        self.assertEqual(res, expected_res)
        res = Base.response_success('MOD_04', 'DELETE', '{content hash}')
        expected_res = {'success':True,  'info':'MOD_04 deleted successfully',  'app_info':{},  'data':'{content hash}'}
        self.assertEqual(res, expected_res)
        res = Base.response_success('MOD_05', 'SET', '{content hash}')
        expected_res = {'success':True,  'info':'MOD_05 set successfully',  'app_info':{},  'data':'{content hash}'}
        self.assertEqual(res, expected_res)
        res = Base.response_success('MOD_06', 'OTHER_ACTION', '{content hash}')
        expected_res = {'success':False,  'info':'ACTION is not correct!',  'app_info':'{content hash}', 
         'data':{}}
        self.assertEqual(res, expected_res)

    def test_response_error(self):
        res = Base.response_error('MOD_01', 'CREATE', 'Error 01')
        expected_res = {'success':False,  'info':'Error creating MOD_01',  'app_info':'Error 01', 
         'data':{}}
        self.assertEqual(res, expected_res)
        res = Base.response_error('MOD_02', 'UPDATE', 'Error 02')
        expected_res = {'success':False,  'info':'Error updating MOD_02',  'app_info':'Error 02', 
         'data':{}}
        self.assertEqual(res, expected_res)
        res = Base.response_error('MOD_03', 'GET', 'Error 03')
        expected_res = {'success':False,  'info':'MOD_03 not found!',  'app_info':'Error 03', 
         'data':{}}
        self.assertEqual(res, expected_res)
        res = Base.response_error('MOD_04', 'DELETE', 'Error 04')
        expected_res = {'success':False,  'info':'Error deleting MOD_04',  'app_info':'Error 04', 
         'data':{}}
        self.assertEqual(res, expected_res)
        res = Base.response_error('MOD_05', 'SET', 'Error 05')
        expected_res = {'success':False,  'info':'Error setting MOD_05',  'app_info':'Error 05', 
         'data':{}}
        self.assertEqual(res, expected_res)
        res = Base.response_error('MOD_06', 'OTHER_ACTION', 'Error 06')
        expected_res = {'success':False,  'info':'ACTION is not correct!',  'app_info':'Error 06', 
         'data':{}}
        self.assertEqual(res, expected_res)


if __name__ == '__main__':
    unittest.main()