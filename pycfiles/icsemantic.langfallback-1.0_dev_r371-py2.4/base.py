# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/langfallback/tests/base.py
# Compiled at: 2008-10-06 10:31:06
"""Test setup for integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of Plone's
products are loaded, and a Plone site will be created. This happens at module
level, which makes it faster to run each test, but slows down test runner
startup.
"""
import os, sys
from App import Common
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr
from icsemantic.langfallback.config import *
import utils, doctest
OPTIONFLAGS = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
if HAS_PLONE3:
    ztc.installProduct('plone.browserlayer')
ztc.installProduct('GenericSetup')
ztc.installProduct('PloneLanguageTool')
ztc.installProduct('LinguaPlone')

@onsetup
def setup_icsemantic_langfallback():
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
        ztc.installPackage(PROJECTNAME)

    return


setup_icsemantic_langfallback()
ptc.setupPloneSite(products=[PROJECTNAME])

class icSemanticTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit
    test cases.
    """
    __module__ = __name__


class icSemanticFunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use doctest
    syntax. Again, we can put basic common utility or setup code in here.
    """
    __module__ = __name__

    def afterSetUp(self):
        setup_tool = getToolByName(self.portal, 'portal_setup')
        profile_name = 'profile-' + PROJECTNAME + ':tests'
        if shasattr(setup_tool, 'runAllImportStepsFromProfile'):
            setup_tool.runAllImportStepsFromProfile(profile_name)
        else:
            old_context = setup_tool.getImportContextID()
            setup_tool.setImportContext(profile_name)
            setup_tool.runAllImportSteps()
            setup_tool.setImportContext(old_context)
        super(icSemanticFunctionalTestCase, self).afterSetUp()