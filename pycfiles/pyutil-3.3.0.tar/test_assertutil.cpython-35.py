# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/current/test_assertutil.py
# Compiled at: 2019-06-26 11:58:00
# Size of source mod 2**32: 968 bytes
import sys, unittest
from pyutil import assertutil

class AssertUtilTestCase(unittest.TestCase):

    def test_bad_precond(self):
        adict = 23
        try:
            assertutil.precondition(isinstance(adict, dict), 'adict is required to be a dict.', 23, adict=adict, foo=None)
        except AssertionError as le:
            if sys.version_info[0] == 2:
                self.assertEqual(le.args[0], "precondition: 'adict is required to be a dict.' <type 'str'>, 23 <type 'int'>, 'adict': 23 <type 'int'>, 'foo': None <type 'NoneType'>")
            else:
                self.assertEqual(le.args[0], "precondition: 'adict is required to be a dict.' <class 'str'>, 23 <class 'int'>, 'adict': 23 <class 'int'>, 'foo': None <class 'NoneType'>")