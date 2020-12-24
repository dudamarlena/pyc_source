# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/test_python2.py
# Compiled at: 2019-11-28 13:06:29
import sys, unittest
sys.dont_write_bytecode = True

class Python2Tests(unittest.TestSuite):
    """
    Test suite aggregating all tests that should be executed when using Python 2
    (runexecutor supports Python 2, the rest does not).
    """

    def __init__(self):
        loader = unittest.TestLoader()
        super(Python2Tests, self).__init__([
         loader.loadTestsFromName('benchexec.test_cgroups'),
         loader.loadTestsFromName('benchexec.test_runexecutor'),
         loader.loadTestsFromName('benchexec.test_util')])