# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/test/basevalidator.py
# Compiled at: 2019-08-19 15:09:29
"""Test util module for creating test cases for name validators"""
from builtins import object
from functools import partial
from taurus.test import insertTest
from taurus.core.taurusvalidator import TaurusAttributeNameValidator
__docformat__ = 'restructuredtext'
valid = partial(insertTest, helper_name='isValid')
invalid = partial(insertTest, helper_name='isInvalid')
names = partial(insertTest, helper_name='getNames')

class AbstractNameValidatorTestCase(object):
    """A util class to create test cases for name validators"""
    validator = None

    def isValid(self, name=None, groups=None, strict=True):
        msg = '%s should be valid (with strict=%s)' % (name, strict)
        self.assertTrue(self.validator().isValid(name, strict=strict), msg)
        if groups is not None:
            returned = self.validator().getUriGroups(name, strict=strict)
            for k, v in groups.items():
                msg = '"%s" not in %s.getUriGroups("%s"). Returned %s' % (
                 k, self.validator.__name__, name, returned)
                self.assertIn(k, returned, msg=msg)
                msg = ('%s.getUriGroups("%s")["%s"] should be "%s". ' + 'Returned "%s"\nGroups: %s') % (self.validator.__name__,
                 name, k, v, returned[k],
                 str(returned))
                self.assertEqual(v, returned[k], msg=msg)

        return

    def isInvalid(self, name=None, groups=None, strict=True, exceptionType=None):
        try:
            valid = self.validator().isValid(name, strict=strict)
            groups = self.validator().getUriGroups(name, strict=strict)
            msg = '%s should be invalid. Matched: %s' % (name, groups)
            self.assertFalse(valid, msg)
        except exceptionType:
            pass
        else:
            msg = '%s should raise %s' % (name, exceptionType)
            self.assertTrue(exceptionType is None, msg)

        return

    def test_singleton(self):
        """Check that the validator is a singleton"""
        self.assertIs(self.validator(), self.validator())

    def getNames(self, name=None, out=None):
        v = self.validator()
        if isinstance(v, TaurusAttributeNameValidator):
            fragment = len(out) > 3
            names = v.getNames(name, fragment=fragment)
        else:
            names = v.getNames(name)
        self.assertEqual(names, out)