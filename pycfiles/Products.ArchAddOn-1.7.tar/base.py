# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/AnonymousCommenting/tests/base.py
# Compiled at: 2009-01-12 11:29:41
import unittest
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from transaction import commit
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup
import Products.AnonymousCommenting
TEST_INSTALL = True
if not hasattr(ztc, 'installPackage'):
    TEST_INSTALL = False
ptc.setupPloneSite()

@onsetup
def setup_product():
    """Set up the additional products required for this package.
    
    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', Products.AnonymousCommenting)
    fiveconfigure.debug_mode = False
    if TEST_INSTALL:
        ztc.installPackage('Products.AnonymousCommenting')


setup_product()
ptc.setupPloneSite(products=['Products.AnonymousCommenting'])
Products.AnonymousCommenting.initialize(ztc.app)

class AnonymousCommentingTestCase(ptc.PloneTestCase):
    __module__ = __name__


def test_suite():
    return unittest.TestSuite([])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')