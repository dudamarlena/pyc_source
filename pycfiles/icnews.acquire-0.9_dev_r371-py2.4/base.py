# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icnews/acquire/tests/base.py
# Compiled at: 2008-10-06 10:31:17
"""Test setup for integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of
Plone's products are loaded, and a Plone site will be created. This
happens at module level, which makes it faster to run each test, but
slows down test runner startup.
"""
import os, sys
from App import Common
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from icnews.acquire.config import *
import icnews.acquire
from icnews.core.tests import utils
test_home = os.path.dirname(__file__)
if not HAS_PLONE3:
    ztc.installProduct('PloneLanguageTool')
ztc.installProduct('LinguaPlone')

@onsetup
def setup_icnews_adqnews():
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', icnews.acquire)
    fiveconfigure.debug_mode = False
    try:
        from Products.Five import pythonproducts
        pythonproducts.setupPythonProducts(None)
        import App
        App.ApplicationManager.ApplicationManager.Five = utils.Five
        ztc.zopedoctest.functional.http = utils.http
    except ImportError:
        ztc.installPackage('icnews.core')
        ztc.installPackage(PROJECTNAME)

    return


setup_icnews_adqnews()
ptc.setupPloneSite(products=[PROJECTNAME])

class ICNewsAcquireTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code in here. This
    applies to unit test cases.
    """
    __module__ = __name__


class ICNewsAcquireFunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use
    doctest syntax. Again, we can put basic common utility or setup
    code in here.
    """
    __module__ = __name__