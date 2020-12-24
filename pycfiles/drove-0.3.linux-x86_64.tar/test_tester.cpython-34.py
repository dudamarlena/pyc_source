# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/tests/util/test_tester.py
# Compiled at: 2015-01-20 05:42:58
# Size of source mod 2**32: 598 bytes
import os, unittest
from drove.util import temp
from drove.util import tester

class TestTemp(unittest.TestCase):

    def test_tester(self):
        """Testing util.tester.run_tests: basic behaviour"""
        with temp.variables({'sys.stderr': open(os.devnull, 'a')}):
            tester.run_tests(os.path.dirname(__file__))