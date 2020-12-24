# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/evaluation/test/test_evalfactory.py
# Compiled at: 2019-08-19 15:09:29
"""Test for taurus.core.evaluation.test.test_evalfactory..."""
import re, taurus, unittest
from taurus.test import insertTest

@insertTest(helper_name='checkAttributeName', model='eval://1', oldstyle=True)
@insertTest(helper_name='checkAttributeName', model='a=2;a*3')
@insertTest(helper_name='checkAttributeName', model='1')
@insertTest(helper_name='checkAttributeID', model='eval://1', oldstyle=True)
@insertTest(helper_name='checkAttributeID', model='a=2;a*3')
@insertTest(helper_name='checkAttributeID', model='1')
@insertTest(helper_name='checkAttributeID', model='eval:1')
class EvaluationFactoryTestCase(unittest.TestCase):
    fragments = ['#', '#label', '#units']

    def setUp(self):
        self.f = taurus.Factory('eval')

    def convert2oldstyle(self, fragment):
        if fragment == '#':
            return '?configuration'
        return re.sub('#(?=.+)', '?configuration=', fragment)

    def checkAttributeID(self, model, oldstyle=False):
        """Helper for test the attributes (by ID) when some different models
        of the same attribute are given (adding fragments in the models)
        """
        attr = self.f.getAttribute(model)
        for fragment in self.fragments:
            if oldstyle:
                fragment = self.convert2oldstyle(fragment)
            attr2 = self.f.getAttribute(model + fragment)
            msg = '%s and %s has different id' % (attr.getFullName(),
             attr2.getFullName())
            self.assertTrue(id(attr) == id(attr2), msg)

    def checkAttributeName(self, model, oldstyle=False):
        """Helper for test the attribute names of the same attribute
        with different models (adding fragments in the models)
        """
        attr = self.f.getAttribute(model)
        for fragment in self.fragments:
            if oldstyle:
                fragment = self.convert2oldstyle(fragment)
            attr2 = self.f.getAttribute(model + fragment)
            msg = '%s and %s has different ' % (attr.getFullName(),
             attr2.getFullName())
            self.assertTrue(attr.getFullName() == attr2.getFullName(), msg + 'fullname')
            self.assertTrue(attr.getNormalName() == attr2.getNormalName(), msg + 'normalname')
            self.assertTrue(attr.getSimpleName() == attr2.getSimpleName(), msg + 'simplename')