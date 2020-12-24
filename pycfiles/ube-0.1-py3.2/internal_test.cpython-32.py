# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ube/concerns/tests/internal_test.py
# Compiled at: 2013-09-01 17:36:06
"""
Created on Nov 18, 2012

@author: Nicklas Boerjesson
"""
import unittest
from ube.concerns.internal import not_implemented

class concern_internal_tests(unittest.TestCase):

    @not_implemented
    def _not_implemented(self):
        pass

    def test_not_implemented(self):
        try:
            self._not_implemented()
        except Exception as Ex:
            if str(Ex) != 'Internal error in "_not_implemented": Not implemented.':
                raise Exception('The @not_implemented decorator does not produce the expected output.')
            else:
                return

        raise Exception('The @not_implemented decorator does not raise an exception.')


if __name__ == '__main__':
    unittest.main()