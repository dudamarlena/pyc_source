# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/plomino/dominoimport/tests/tests.py
# Compiled at: 2009-07-06 10:06:10
import unittest, doctest
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    return unittest.TestSuite([ztc.ZopeDocFileSuite('tests/global_test.txt', package='plomino.dominoimport', test_class=ExampleFunctionalTestCase, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), ztc.ZopeDocFileSuite('tests/createDatabase.txt', package='plomino.dominoimport', test_class=ExampleFunctionalTestCase, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), ztc.ZopeDocFileSuite('tests/importDXL_basic.txt', package='plomino.dominoimport', test_class=ExampleFunctionalTestCase, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), ztc.ZopeDocFileSuite('tests/importDXL_formLayout.txt', package='plomino.dominoimport', test_class=ExampleFunctionalTestCase, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), ztc.ZopeDocFileSuite('tests/importDXL_fieldform.txt', package='plomino.dominoimport', test_class=ExampleFunctionalTestCase, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), ztc.ZopeDocFileSuite('tests/importDXL_documents.txt', package='plomino.dominoimport', test_class=ExampleFunctionalTestCase, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), ztc.ZopeDocFileSuite('tests/importDXL_binary.txt', package='plomino.dominoimport', test_class=ExampleFunctionalTestCase, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), ztc.ZopeDocFileSuite('tests/importDXL_formulas_scripts.txt', package='plomino.dominoimport', test_class=ExampleFunctionalTestCase, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)])


@onsetup
def setup_product():
    """Set up the package and its dependencies.
    
    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer. We could have created our
    own layer, but this is the easiest way for Plone integration tests.
    """
    ztc.installProduct('CMFPlomino')
    import Products.CMFPlomino
    from Products.Five import zcml
    zcml.load_config('configure.zcml', Products.CMFPlomino)


setup_product()
ptc.setupPloneSite(products=['CMFPlomino'])

class ExampleFunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use doctest
    syntax. Again, we can put basic common utility or setup code in here.
    """
    __module__ = __name__