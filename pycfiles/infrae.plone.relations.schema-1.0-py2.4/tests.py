# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/infrae/plone/relations/schema/tests.py
# Compiled at: 2008-06-11 03:54:55
__author__ = 'sylvain@infrae.com'
__format__ = 'plaintext'
__version__ = '$Id: tests.py 29099 2008-06-11 07:54:54Z sylvain $'
import unittest
from zope.testing import doctest
from Testing.ZopeTestCase import ZopeDocFileSuite
from Products.PloneTestCase import ptc
from five.intid.site import add_intids
from plone.app.relations.utils import add_relations
from five.intid.lsm import USE_LSM
from Products.Five import zcml

class TestCase(ptc.PloneTestCase):
    __module__ = __name__

    def afterSetUp(self):
        from infrae.plone.relations import schema
        zcml.load_config('configure.zcml', schema)
        if not USE_LSM:
            from Products.Five.site.metaconfigure import classSiteHook
            from Products.Five.site.localsite import FiveSite
            from zope.interface import classImplements
            from zope.app.component.interfaces import IPossibleSite
            klass = self.portal.__class__
            classSiteHook(klass, FiveSite)
            classImplements(klass, IPossibleSite)
        add_intids(self.portal)
        add_relations(self.portal)


OPTIONS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE

def test_suite():
    (
     ptc.setupPloneSite(),)
    return unittest.TestSuite((ZopeDocFileSuite('README.EXT.txt', test_class=TestCase, optionflags=OPTIONS), ZopeDocFileSuite('README.txt', test_class=TestCase, optionflags=OPTIONS)))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')