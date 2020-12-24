# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/iccommunity/mediawiki/tests/base.py
# Compiled at: 2008-10-06 10:31:13
"""Test setup for unit, integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of Plone's
products are loaded, and a Plone site will be created. This happens at module
level, which makes it faster to run each test, but slows down test runner
startup.
"""
import os, sys
from App import Common
from zope.component import queryUtility
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from iccommunity.mediawiki.config import *
from iccommunity.core.tests import utils
if not HAS_PLONE3:
    ztc.installProduct('PloneLanguageTool')

@onsetup
def setup_iccommunity_mediawiki():
    ztc.installProduct('Five')
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', PACKAGE)
    fiveconfigure.debug_mode = False
    try:
        from Products.Five import pythonproducts
        pythonproducts.setupPythonProducts(None)
        import App
        App.ApplicationManager.ApplicationManager.Five = utils.Five
        ztc.zopedoctest.functional.http = utils.http
    except ImportError:
        ztc.installPackage('iccommunity.core')
        ztc.installPackage(PROJECTNAME)

    return


setup_iccommunity_mediawiki()
ptc.setupPloneSite(products=[PROJECTNAME])

class MediawikiTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit
    test cases.
    """
    __module__ = __name__

    def setUp(self):
        super(ptc.PloneTestCase, self).setUp()


class MediawikiFunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use doctest
    syntax. Again, we can put basic common utility or setup code in here.
    """
    __module__ = __name__

    def setUp(self):
        super(ptc.FunctionalTestCase, self).setUp()