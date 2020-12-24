# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/collective/listjs/tests/base.py
# Compiled at: 2011-11-01 10:41:40
__doc__ = "Test setup for integration and functional tests.\n\nWhen we import PloneTestCase and then call setupPloneSite(), all of Plone's\nproducts are loaded, and a Plone site will be created. This happens at module\nlevel, which makes it faster to run each test, but slows down test runner\nstartup.\n"
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_product():
    """Set up the package and its dependencies.
    
    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer. We could have created our
    own layer, but this is the easiest way for Plone integration tests.
    """
    fiveconfigure.debug_mode = True
    import collective.listjs
    zcml.load_config('configure.zcml', collective.listjs)
    fiveconfigure.debug_mode = False
    ztc.installPackage('collective.listjs')


setup_product()
ptc.setupPloneSite(products=['collective.listjs'])

class ExampleTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit 
    test cases.
    """


class ExampleFunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use doctest
    syntax. Again, we can put basic common utility or setup code in here.
    """