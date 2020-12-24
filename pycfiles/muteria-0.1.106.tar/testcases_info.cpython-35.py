# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfi/mytools/muteria/muteria/drivers/testgeneration/testcases_info.py
# Compiled at: 2019-10-01 07:30:49
# Size of source mod 2**32: 3186 bytes
from __future__ import print_function
import muteria.common.fs as common_fs, muteria.common.mix as common_mix
ERROR_HANDLER = common_mix.ErrorHandler

class TestcasesInfoObject(object):
    __doc__ = ' This class represent the test case informations data structure\n    '
    DATA_KEY = 'DATA'
    SUMMARY_KEY = 'SUMMARY'
    CUSTOM_KEY = 'CUSTOM'

    def __init__(self):
        self.data = {self.DATA_KEY: {}, 
         self.SUMMARY_KEY: None, 
         self.CUSTOM_KEY: None}

    def load_from_file(self, file_path):
        self.data = common_fs.loadJSON(file_path)

    def write_to_file(self, file_path):
        common_fs.dumpJSON(self.data, file_path, pretty=True)

    def add_test(self, test_name, **kwargs):
        ERROR_HANDLER.assert_true(not self.has_test(test_name), 'Test is already present in this: {}'.format(test_name), __file__)
        self.data[self.DATA_KEY][test_name] = kwargs

    def has_test(self, test_name):
        return test_name in self.data[self.DATA_KEY]

    def get_tests_list(self):
        return list(self.data[self.DATA_KEY].keys())

    def update_using(self, toolname, old2new_tests, old_test_info_obj):
        for old_test_name, new_test_name in list(old2new_tests.items()):
            ERROR_HANDLER.assert_true(old_test_info_obj.has_test(old_test_name), 'Test not present in old_test_info_obj: {}'.format(old_test_name), __file__)
            ERROR_HANDLER.assert_true(not self.has_test(new_test_name), 'Test is already present in this: {}'.format(new_test_name), __file__)
            self.data[self.DATA_KEY][new_test_name] = old_test_info_obj.data[self.DATA_KEY][old_test_name]

        if self.data[self.SUMMARY_KEY] is None:
            self.data[self.SUMMARY_KEY] = {}
        self.data[self.SUMMARY_KEY][toolname] = old_test_info_obj.data[self.SUMMARY_KEY]
        if self.data[self.CUSTOM_KEY] is None:
            self.data[self.CUSTOM_KEY] = {}
        self.data[self.CUSTOM_KEY][toolname] = old_test_info_obj.data[self.CUSTOM_KEY]

    def remove_test(self, test_name):
        ERROR_HANDLER.assert_true(self.has_test(test_name), 'Removing an unexisting test: {}'.format(test_name), __file__)
        del self.data[self.DATA_KEY][test_name]

    def get_summary(self):
        return self.data[self.SUMMARY_KEY]

    def get_custom(self):
        return self.data[self.CUSTOM_KEY]