# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\collective\groupdelegation\tests.py
# Compiled at: 2009-06-18 07:02:52
import sys, unittest
from zope.testing import doctest
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_product():
    """
    Set up the package and its dependencies.
    """
    fiveconfigure.debug_mode = True
    import collective.groupdelegation
    zcml.load_config('configure.zcml', collective.groupdelegation)
    fiveconfigure.debug_mode = False
    ztc.installPackage('collective.groupdelegation')


setup_product()
ptc.setupPloneSite()

class TestCase(ptc.FunctionalTestCase):
    __module__ = __name__

    class layer(PloneSite):
        __module__ = __name__

        @classmethod
        def setUp(cls):
            try:
                iphook = sys.displayhook
                sys.displayhook = sys.__displayhook__
            except:
                pass

        @classmethod
        def tearDown(cls):
            try:
                sys.displayhook = iphook
            except:
                pass


OPTIONFLAGS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE

def test_suite():
    return unittest.TestSuite([ztc.FunctionalDocFileSuite('readme.txt', package='collective.groupdelegation', optionflags=OPTIONFLAGS, test_class=TestCase)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')