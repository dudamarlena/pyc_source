# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toster/runner.py
# Compiled at: 2014-08-26 05:16:05
# Size of source mod 2**32: 1863 bytes
from argparse import ArgumentParser
import unittest
from .manager import TestManager

class TestRunner(object):

    def __init__(self):
        self.manager = TestManager(self)
        self.loader = unittest.TestLoader()
        self.verbosity = 1
        self.args = None

    def create_suite(self):
        test_cases = [self.loader.loadTestsFromTestCase(test_case) for test_case in self.get_tests()]
        return unittest.TestSuite(test_cases)

    def get_tests(self):
        if self.args.case:
            return self.manager.get_by_name(self.args.case)
        else:
            if self.args.group:
                return self.manager.get_by_group(self.args.group)
            return self.manager.get_all()

    def create_parser(self):
        if self.args is not None:
            return
        self.parser = ArgumentParser(description='Run some tests.')
        self.parser.add_argument('-c', '--case', dest='case', help='specify which test case')
        self.parser.add_argument('-g', '--group', dest='group', help='specify which group to run')
        self.parser.add_argument('-l', '--list', dest='list', action='store_true', help='list all tests and groups')
        self.args = self.parser.parse_args()

    def run(self):
        suite = self.create_suite()
        unittest.TextTestRunner(verbosity=self.verbosity).run(suite)

    def print_list(self):
        print('Cases:')
        print('\t' + '\n\t'.join(self.manager.tests.keys()))
        print('Groups:')
        print('\t' + '\n\t'.join(self.manager.groups.keys()))

    def __call__(self):
        self.create_parser()
        if self.args.list:
            self.print_list()
        else:
            self.run()