# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/tests/testUtils.py
# Compiled at: 2008-09-11 19:48:09
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Products.PloneTestCase import PloneTestCase
import common
common.installWithinPortal()
from Products.Relations import brain
from Products.Relations import utils

class TestAdddeleteVocab(PloneTestCase.PloneTestCase):
    __module__ = __name__
    TYPES = ('SimpleFolder', 'SimpleType', 'ComplexType')

    def afterSetUp(self):
        self.objs = common.createObjects(self, self.TYPES)
        self.brains = [ brain.makeBrainAggregate(self.portal, obj.UID()) for obj in self.objs ]
        self.ruleset = common.createRuleset(self, 'ruleset')
        self.ruleset.invokeFactory('Type Constraint', 'tc')
        self.ruleset.tc.setAllowedTargetTypes(self.TYPES)

    def testNoPermissions(self):
        vocab = utils.adddeleteVocab(self.objs[0])
        self.assertEquals(len(vocab), 1)
        self.assertEquals(len(vocab[0]['tuples']), 3)
        self.logout()
        vocab = utils.adddeleteVocab(self.objs[0])
        self.assertEquals(len(vocab), 0)

    def testTestOnly(self):
        vocab = utils.adddeleteVocab(self.objs[0], test_only=1)
        self.failUnless(vocab)
        self.ruleset.tc.setAllowedTargetTypes(['Gorilla'])
        vocab = utils.adddeleteVocab(self.objs[0], test_only=1)
        self.failIf(vocab)

    def testRuleSetIds(self):
        self.ruleset2 = common.createRuleset(self, 'ruleset2')
        self.ruleset2.invokeFactory('Type Constraint', 'tc')
        self.ruleset2.tc.setAllowedTargetTypes(self.TYPES)
        vocab = utils.adddeleteVocab(self.objs[0])
        self.assertEquals(len(vocab), 2)
        self.failUnless(vocab[0]['id'] in ('ruleset', 'ruleset2'))
        self.failUnless(vocab[1]['id'] in ('ruleset', 'ruleset2'))
        vocab = utils.adddeleteVocab(self.objs[0], ruleset_ids=['ruleset'])
        self.assertEquals(len(vocab), 1)
        self.assertEquals(vocab[0]['id'], 'ruleset')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestAdddeleteVocab))
    return suite


if __name__ == '__main__':
    framework()