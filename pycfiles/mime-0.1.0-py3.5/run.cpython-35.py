# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/tests/run.py
# Compiled at: 2016-08-03 22:31:30
# Size of source mod 2**32: 695 bytes
import os, sys
TEST_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(TEST_DIR)
sys.path.insert(0, ROOT_DIR)
from unittest import main, TestSuite, findTestCases

def get_test_module_names():
    file_names = os.listdir(os.curdir)
    for fn in file_names:
        if fn.startswith('test') and fn.endswith('.py'):
            yield 'tests.' + fn[:-3]


def suite():
    alltests = TestSuite()
    for module_name in get_test_module_names():
        module = __import__(module_name, fromlist=[module_name])
        alltests.addTest(findTestCases(module))

    return alltests


if __name__ == '__main__':
    main(defaultTest='suite')