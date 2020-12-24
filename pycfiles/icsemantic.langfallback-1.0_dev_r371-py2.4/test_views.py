# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/langfallback/tests/test_views.py
# Compiled at: 2008-10-06 10:31:06
import unittest
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase.layer import PloneSite
from icsemantic.langfallback.config import *
import base

class TestViews(base.icSemanticTestCase):
    """
    """
    __module__ = __name__

    def test_writer(self):
        """
        """
        pass


def test_suite():
    return unittest.TestSuite([unittest.makeSuite(TestViews), ztc.ZopeDocTestSuite(module=PACKAGENAME + '.browser.views', test_class=TestViews), ztc.FunctionalDocFileSuite('test_views_concepts.txt', optionflags=base.OPTIONFLAGS, package=PACKAGENAME + '.tests', test_class=base.icSemanticFunctionalTestCase), ztc.FunctionalDocFileSuite('test_views_custom_widgets.txt', optionflags=base.OPTIONFLAGS, package=PACKAGENAME + '.tests', test_class=base.icSemanticFunctionalTestCase), ztc.FunctionalDocFileSuite('test_views_set_language.txt', optionflags=base.OPTIONFLAGS, package=PACKAGENAME + '.tests', test_class=base.icSemanticFunctionalTestCase), ztc.FunctionalDocFileSuite('test_views.txt', optionflags=base.OPTIONFLAGS, package=PACKAGENAME + '.tests', test_class=base.icSemanticFunctionalTestCase)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')