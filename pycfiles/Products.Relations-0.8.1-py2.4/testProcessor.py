# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/tests/testProcessor.py
# Compiled at: 2008-09-11 19:48:09
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Products.PloneTestCase import PloneTestCase
import common
common.installWithinPortal()
import Products.Relations.processor as processor

class TestProcessor(PloneTestCase.PloneTestCase):
    __module__ = __name__
    TYPES = ('SimpleType', 'ComplexType')
    RULESETS = ('OneRuleset', 'AnotherRuleset')

    def afterSetUp(self):
        self.objs = common.createObjects(self, self.TYPES)
        self.rulesets = [ common.createRuleset(self, j) for j in self.RULESETS ]

    def testConnectAndDisconnect(self):
        triples = [ (self.objs[0].UID(), self.objs[1].UID(), ruleset.getId()) for ruleset in self.rulesets ]
        processor.process(self.portal, connect=triples)
        for ruleset in self.rulesets:
            self.assertEquals(self.objs[0].getRefs(ruleset.getId())[0], self.objs[1])

        processor.process(self.portal, disconnect=triples)
        self.assertEquals(len(self.objs[0].getRefs()), 0)
        self.assertEquals(len(self.objs[1].getBRefs()), 0)

    def testConnectAndDisconnectWithReferenceUIDs(self):
        triples = [ (self.objs[0].UID(), self.objs[1].UID(), ruleset.getId()) for ruleset in self.rulesets ]
        processor.process(self.portal, connect=triples)
        for ruleset in self.rulesets:
            self.assertEquals(self.objs[0].getRefs(ruleset.getId())[0], self.objs[1])

        refUIDs = [ ref.UID() for ref in self.objs[0].getReferenceImpl() ]
        self.assertEquals(len(refUIDs), 2)
        processor.process(self.portal, disconnect=refUIDs)
        self.assertEquals(len(self.objs[0].getRefs()), 0)
        self.assertEquals(len(self.objs[1].getBRefs()), 0)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProcessor))
    return suite


if __name__ == '__main__':
    framework()