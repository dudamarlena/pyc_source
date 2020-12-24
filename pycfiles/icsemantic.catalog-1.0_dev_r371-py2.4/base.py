# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/catalog/tests/base.py
# Compiled at: 2008-10-06 10:31:12
"""Test setup for unit, integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of
Plone's products are loaded, and a Plone site will be created. This
happens at module level, which makes it faster to run each test, but
slows down test runner startup.
"""
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from zope.app.component.hooks import setSite
from icsemantic.thesaurus.Thesaurus import thesaurus_utility
from icsemantic.thesaurus.interfaces import IThesaurus
from icsemantic.catalog.config import *
from pyThesaurus.Concept import Concept
from icsemantic.langfallback.tests import utils
if not HAS_PLONE3:
    ztc.installProduct('PloneLanguageTool')
ztc.installProduct('LinguaPlone')
ztc.installProduct('pluggablecatalog')

@onsetup
def setup_icsemantic_catalog():
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
        ztc.installPackage('icsemantic.core')
        ztc.installPackage('icsemantic.langfallback')
        ztc.installPackage('icsemantic.thesaurus')
        ztc.installPackage(PROJECTNAME)

    return


setup_icsemantic_catalog()
ptc.setupPloneSite(products=[PROJECTNAME])

def add_test_thesaurus(context):
    """Fill the thesaurus local utility with some useful information"""
    setSite(context)
    t = thesaurus_utility()
    c = Concept(et=['fútbol@es', 'balón pie@es', 'soccer@en', 'football@en', 'football@fr'])
    t.append_concept(c)
    t.append_term('mundial@es', rt=['fútbol@es'], automatic=False)
    t.append_term('pelota@es', rt=['balón pie@es'], contexts=['publicidad'], automatic=False)


class ICSemanticCatalogTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code in here. This
    applies to unit test cases.
    """
    __module__ = __name__

    def afterSetUp(self):
        ptc.PloneTestCase.afterSetUp(self)
        try:
            add_test_thesaurus(self.portal)
        except:
            pass

        self.loginAsPortalOwner()
        langtool = getToolByName(self.portal, 'portal_languages')
        langtool.addSupportedLanguage('en')
        langtool.addSupportedLanguage('es')
        langtool.addSupportedLanguage('fr')
        langtool.setDefaultLanguage('en')
        self.add_member('member1', 'Member One', 'none1@test.com', ('Member', ), 'en')
        self.add_member('member2', 'Member Two', 'none2@test.com', ('Member', ), 'es')

    def add_member(self, username, fullname, email, roles, language):
        self.portal.portal_membership.addMember(username, 'secret', roles, [])
        member = self.portal.portal_membership.getMemberById(username)
        member.setMemberProperties({'fullname': fullname, 'email': email, 'language': language})


class ICSemanticCatalogFunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use
    doctest syntax. Again, we can put basic common utility or setup
    code in here.
    """
    __module__ = __name__

    def setUp(self):
        super(ptc.FunctionalTestCase, self).setUp()
        add_test_thesaurus(self.portal)