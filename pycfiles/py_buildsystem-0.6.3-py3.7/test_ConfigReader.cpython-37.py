# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\ConfigReader\test_ConfigReader.py
# Compiled at: 2019-06-09 09:37:17
# Size of source mod 2**32: 2250 bytes
import os, yaml, shutil, unittest
import py_buildsystem.ConfigReader.ConfigReader as ConfigReader
script_file_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
test_files_directory_name = 'test_files'
corrupted_test_file_name = 'corrupted_test_file.yaml'
test_file_name = 'test_file.yaml'
test_files_path = script_file_path + '/' + test_files_directory_name
test_file_with_path = test_files_path + '/' + test_file_name
corrupted_test_file_with_path = test_files_path + '/' + corrupted_test_file_name
test_data = {'string_field':'test_string', 
 'list_field':[
  'list_element_1', 'list_element2', 3], 
 'dictionary_field':{'key1':'value_1', 
  'key2':'value_2'}}

class MockConfigReader(ConfigReader):

    def _check_config(self):
        self._MockConfigReader__string_field = self.configuration['string_field']
        self._MockConfigReader__list_field = self.configuration['list_field']
        self._MockConfigReader__dictionary_field = self.configuration['dictionary_field']
        try:
            self._MockConfigReader__dictionary_field['key1']
        except KeyError:
            raise Exception('no key1 key in dictionary_field')

        self._MockConfigReader__dictionary_field['key2']


class TestConfigReader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.makedirs(test_files_path, exist_ok=True)
        with open(test_file_with_path, 'w') as (test_file):
            test_file.write(yaml.dump(test_data))
        with open(corrupted_test_file_with_path, 'w') as (corrupted_test_file):
            corrupted_test_file.write(yaml.dump(cls._corrupt_data(cls)))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(test_files_path, ignore_errors=True)

    def test_ConfigReader(self):
        MockConfigReader(test_file_with_path)
        with self.assertRaises(Exception):
            MockConfigReader(corrupted_test_file_with_path)
        with self.assertRaises(Exception):
            MockConfigReader(test_files_path + '/' + 'file_which_doesnt_exist.yaml')

    def _corrupt_data(self):
        corrupted_data = test_data.copy()
        corrupted_data['dictionary_field'].pop('key1')
        return corrupted_data