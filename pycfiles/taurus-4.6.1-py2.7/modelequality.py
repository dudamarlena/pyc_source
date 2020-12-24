# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/test/modelequality.py
# Compiled at: 2019-08-19 15:09:29
from builtins import object
import functools
from taurus import Device, Attribute
from taurus.test import insertTest

class TaurusModelEqualityTestCase(object):
    """Base class for taurus model equality testing."""

    def modelsEqual(self, models, class_, equal=True):
        """A helper method to create tests that checks equality (or inequality)
        of taurus objects e.g. TaurusAttribute.

        :param models: (seq<str>): a sequence of two taurus models
        :param class_: (function) model factory function
        :param equal: (bool) If True, check equality. Else check inequality
        """
        name1, name2 = models
        obj1 = class_(name1)
        obj2 = class_(name2)
        if equal:
            msg = 'models for %s and %s are not equal (they should)' % (
             name1, name2)
            self.assertIs(obj1, obj2, msg)
        else:
            msg = 'models for %s and %s are equal (they should not)' % (
             name1, name2)
            self.assertIsNot(obj1, obj2, msg)


testDeviceModelEquality = functools.partial(insertTest, helper_name='modelsEqual', class_=Device, test_method_name='testDeviceModelEquality')
testAttributeModelEquality = functools.partial(insertTest, helper_name='modelsEqual', class_=Attribute, test_method_name='testAttributeModelEquality')