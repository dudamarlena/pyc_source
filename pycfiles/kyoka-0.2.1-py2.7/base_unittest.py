# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/base_unittest.py
# Compiled at: 2016-12-01 23:40:36
import unittest

class BaseUnitTest(unittest.TestCase):

    def eq(self, expected, target):
        return self.assertEqual(expected, target)

    def almosteq(self, expected, target, tolerance):
        if isinstance(expected, list):
            curry = lambda zipped: self.almosteq(zipped[0], zipped[1], tolerance)
            map(curry, zip(expected, target))
        else:
            match = expected - tolerance <= target <= expected + tolerance
            if not match:
                return self.fail('%s and %s do not match with tolerance=%f' % (expected, target, tolerance))

    def neq(self, expected, target):
        return self.assertNotEqual(expected, target)

    def true(self, target):
        return self.assertTrue(target)

    def false(self, target):
        return self.assertFalse(target)

    def include(self, target, source):
        return self.assertIn(target, source)

    def not_include(self, target, source):
        return self.assertNotIn(target, source)

    def debug(self):
        from nose.tools import set_trace
        set_trace()