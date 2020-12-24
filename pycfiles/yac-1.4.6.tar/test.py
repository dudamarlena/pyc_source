# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: yac/lib/test.py
# Compiled at: 2018-01-02 12:16:07
import os, datetime
from yac.lib.intrinsic import apply_custom_fxn
from yac.lib.variables import get_variable, set_variable
from yac.lib.file import get_localized_script_path, FileError
from yac.lib.artillery import ArtilleryDriver
from yac.lib.module import get_module
from yac.lib.stack import cp_file_to_s3

class IntegrationTests:

    def __init__(self, test_descriptor, service_parameters):
        self.target = get_variable(test_descriptor, 'target')
        self.tests = []
        if 'tests' in test_descriptor:
            self.tests = test_descriptor['tests']
        self.test_groups = []
        if 'test-groups' in test_descriptor:
            self.test_groups = test_descriptor['test-groups']
        self.service_parameters = service_parameters
        self.results_store = get_variable(test_descriptor, 'results-store')
        self.test_results = TestResults()

    def get_results(self):
        return self.test_results

    def get_tests(self):
        return self.tests

    def run(self):
        for test_name in self.tests:
            self._run_test(test_name, self.tests[test_name])

        for group_name in self.test_groups:
            self.run_group(group_name)

    def run_group(self, group_name):
        if group_name not in self.test_groups:
            self.test_results.failing_test(test_group, 'test group %s does not exist' % test_group)
        else:
            group_descriptor = self.test_groups[group_name]
            print 'running test group %s ...' % group_name
            if 'setup' in group_descriptor:
                print 'running setup script %s...' % group_descriptor['setup']
            sequence = []
            if 'sequence' in group_descriptor:
                sequence = group_descriptor['sequence']
            elif 'tests' in group_descriptor:
                sequence = group_descriptor['tests'].keys()
            for test_name in sequence:
                if test_name in group_descriptor['tests']:
                    self._run_test(test_name, group_descriptor['tests'][test_name])

        if 'cleanup' in group_descriptor:
            print 'running cleanup script %s...' % group_descriptor['cleanup']

    def _run_test(self, test_name, test):
        print 'running test: %s ...' % test_name
        if 'setup' in test:
            print 'running setup function ...'
            setup_source_file = get_variable(test, 'setup')
            _run_test_setup(setup_source_file)
        if 'artillery' in test:
            artillery_script = get_variable(test, 'artillery')
            artillery = ArtilleryDriver(test_name, self.target, artillery_script, test['assertions'], self.test_results)
            artillery.run()
        if 'custom' in test:
            print 'running custom test function ...'
            custom_test_source_file = get_variable(test, 'custom')
            run_custom_test(test_name, custom_test_source_file)
        if 'cleanup' in test:
            print 'running cleanup function ...'
            cleanup_source_file = get_variable(test, 'cleanup')
            _run_test_cleanup(cleanup_source_file)

    def _run_test_setup(self, module_rel_path):
        return_val = ''
        module = get_module(module_rel_path, self.service_parameters)
        if hasattr(module, 'test_setup'):
            return_val = module.test_setup(self.service_parameters)
        else:
            print 'setup module %s does not exist ' % module_rel_path + "or does not have a 'test_setup' function"

    def run_custom_test(self, test_name, custom_test_source_file):
        module = get_module(custom_test_source_file, self.service_parameters)
        if hasattr(module, 'test_driver'):
            return_val = module.test_driver(test_name, self.target, self.test_results)
        else:
            msg = 'custom test module %s does  ' % custom_test_source_file + "not exist or does not have a 'test_driver' function"
            self.test_results.append_fail_msg(msg)

    def _run_test_cleanup(self, module_rel_path):
        return_val = ''
        module = get_module(module_rel_path, self.service_parameters)
        if hasattr(module, 'test_cleanup'):
            return_val = module.test_cleanup(self.service_parameters)
        else:
            msg = 'setup module %s does not exist ' % module_rel_path + "or does not have a 'test_cleanup' function"
            self.test_results.append_fail_msg(msg)
        return return_val

    def process_test_results(self):
        exit_code = 0
        num_tests = self.test_results.get_num_tests()
        test_duration_sec = self.test_results.get_test_duration_sec()
        if len(self.test_results.get_failing_tests()) == 0:
            print self.get_stdout_divider('-')
            print 'Ran %s test in %s sec\n' % (num_tests, test_duration_sec)
            print 'OK'
        else:
            print self.get_stdout_divider('=')
            for failed_test in self.test_results.get_failing_tests():
                print 'FAIL: %s' % failed_test['test']
                print self.get_stdout_divider('-')
                print '%s\n' % failed_test['msg']

            print self.get_stdout_divider('-')
            print 'Ran %s test in %s sec\n' % (num_tests, test_duration_sec)
            print 'FAILED (failures=%s)' % len(test_results.get_failing_tests())
            exit_code = 1
        return exit_code

    def get_stdout_divider(self, character):
        divider = ''
        for i in range(0, 70):
            divider = divider + character

        return divider

    def save_test_results(self):
        if self.results_store:
            destination_path = self.results_store
            print 'saving results to results store ... '
            for result_file in self.test_results.get_results_files():
                file_name = os.path.basename(result_file)
                if 's3:' in destination_path:
                    try:
                        destination_s3_url = os.path.join(destination_path, file_name)
                        print 'saving %s to %s... ' % (result_file, destination_s3_url)
                        cp_file_to_s3(result_file, destination_s3_url)
                    except FileError as e:
                        print e.msg


class TestResults:

    def __init__(self):
        self.num_tests = 0
        self.passing_tests = []
        self.failing_tests = []
        self.results_files = []
        self.start_time = datetime.datetime.now()

    def get_failing_tests(self):
        return self.failing_tests

    def get_passing_tests(self):
        return self.passing_tests

    def get_num_tests(self):
        return len(self.passing_tests) + len(self.failing_tests)

    def get_results_files(self):
        return self.results_files

    def passing_test(self, test_name):
        self.passing_tests = self.passing_tests + [test_name]

    def failing_test(self, test_name, fail_msg):
        self.failing_tests = self.failing_tests + [
         {'test': test_name, 'msg': fail_msg}]

    def append_results_file(self, file_path):
        self.results_files = self.results_files + [file_path]

    def get_test_duration_sec(self):
        return (datetime.datetime.now() - self.start_time).seconds