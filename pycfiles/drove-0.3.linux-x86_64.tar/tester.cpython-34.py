# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/util/tester.py
# Compiled at: 2015-01-20 05:42:58
# Size of source mod 2**32: 563 bytes
import os, unittest

def run_tests(path):
    """Run tests find in path and return a list of
    :class:`TesterResult` objects"""
    ret = []
    for test_path in [os.path.join(path, 'tests'), os.path.join(path, 'test')]:
        if os.path.isdir(test_path):
            suite = unittest.TestSuite()
            suite.addTests(unittest.TestLoader().discover(test_path))
            result = unittest.TestResult()
            suite.run(result)
            ret.append(result)
            continue

    return ret