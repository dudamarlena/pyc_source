# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/releaser/tests/test_base.py
# Compiled at: 2008-04-29 08:14:25
""" base.py low-level tests
"""
import unittest, os
from iw.releaser.base import safe_input

class BaseTest(unittest.TestCase):
    __module__ = __name__

    def test_safe_input(self):

        def my_input(msg):
            return ''

        safe_input.func_globals['raw_input'] = my_input
        self.assertEquals(safe_input('value'), None)
        self.assertEquals(safe_input('value', 10), 10)
        return


def test_suite():
    """returns the test suite"""
    return unittest.makeSuite(BaseTest)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')