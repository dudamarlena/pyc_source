# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/tests/testBrain.py
# Compiled at: 2008-09-11 19:48:09
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Products.PloneTestCase import PloneTestCase
from Interface.Verify import verifyObject
import Products.Relations.interfaces as interfaces, Products.Relations.brain as brain, common
common.installWithinPortal()

class TestBrain(PloneTestCase.PloneTestCase):
    __module__ = __name__
    TYPES = ('SimpleFolder', 'SimpleType')

    def afterSetUp(self):
        self.objects = common.createObjects(self, self.TYPES)

    def testMakeBrainAggregate(self):
        portal = self.portal
        catalog = portal.uid_catalog

        def assertions(obj, b):
            self.assertEquals(b.getObject(), obj)
            self.assertEquals(b.UID, obj.UID())
            verifyObject(interfaces.IBrainAggregate, b)
            self.assertEquals(b.sources, ['portal_catalog'])
            self.failUnless(hasattr(b, 'EffectiveDate'))

        for obj in self.objects:
            b = brain.makeBrainAggregate(portal, obj.UID())
            assertions(obj, b)
            b = brain.makeBrainAggregate(portal, catalog(UID=obj.UID())[0])
            assertions(obj, b)
            b = brain.makeBrainAggregate(portal, b)
            assertions(obj, b)

    def testMakeBrainAggrFromBrainCatalogsArg(self):
        portal = self.portal
        catalog = portal.uid_catalog
        b = brain.makeBrainAggrFromBrain(portal, catalog(UID=self.objects[0].UID())[0], catalogs=[])
        self.assertEquals(b.sources, [])
        self.assertRaises(AttributeError, getattr, b, 'EffectiveDate')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestBrain))
    return suite


if __name__ == '__main__':
    framework()