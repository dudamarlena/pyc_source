# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ameadows/PycharmProjects/etlTest/etltest/samples/output/DataMart/UsersDim.py
# Compiled at: 2014-08-29 10:43:52
# Size of source mod 2**32: 2709 bytes
import unittest, datetime
from os import path
from etltest.data_connector import DataConnector
from etltest.process_executor import ProcessExecutor
from etltest.utilities.settings_manager import SettingsManager

class DataMartUsersDimTest(unittest.TestCase):

    def setUp(self):
        DataConnector('etlUnitTest').insert_data('users', [1, 2])
        PDI_settings = SettingsManager().get_tool('PDI')
        PDI_code_path = SettingsManager().system_variable_replace(PDI_settings['code_path'])
        ProcessExecutor('PDI').execute_process('job', path.join(PDI_code_path, 'data_mart/user_dim_jb.kjb'))

    def tearDown(self):
        DataConnector('etlUnitTest').truncate_data('users')

    def testFirstNameNotLower(self):
        given_result = DataConnector('etlUnitTest').select_data('first_name', 'user_dim', 'user_id = 2')
        expected_result = [{'first_name': 'sarah'}]
        self.assertNotEqual(given_result, expected_result)

    def testFirstNameUpper(self):
        given_result = DataConnector('etlUnitTest').select_data('first_name', 'user_dim', 'user_id = 2')
        expected_result = [{'first_name': 'SARAH'}]
        self.assertEqual(given_result, expected_result)

    def testUserValidBirthday(self):
        given_result = DataConnector('etlUnitTest').select_data('birthday', 'user_dim', 'user_id IN (1, 2)')
        expected_result = [{'birthday': datetime.date(2000, 1, 4)}, {'birthday': datetime.date(2000, 2, 2)}]
        self.assertEqual(given_result, expected_result)

    def testIsActiveTrue(self):
        given_result = DataConnector('etlUnitTest').select_data('is_active', 'users', 'user_id = 2')
        self.assertTrue(given_result)

    def testIsActiveFalse(self):
        given_result = DataConnector('etlUnitTest').select_data('is_active', 'users', 'user_id = 1')
        self.assertFalse(given_result)


if __name__ == '__main__':
    unittest.main()