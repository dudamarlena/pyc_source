# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/thesaurus/tests/base.py
# Compiled at: 2008-10-06 10:31:07
"""Test setup for integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of Plone's
products are loaded, and a Plone site will be created. This happens at module
level, which makes it faster to run each test, but slows down test runner
startup.
"""
import os, sys
from App import Common
from zope.app.component.hooks import setSite
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from icsemantic.thesaurus.Thesaurus import thesaurus_utility
from icsemantic.thesaurus.interfaces import IThesaurus
from icsemantic.thesaurus.config import *
from pyThesaurus.Concept import Concept
from icsemantic.core.tests import utils
from icsemantic.thesaurus.config import *
ztc.installProduct('GenericSetup')
ztc.installProduct('PloneLanguageTool')
ztc.installProduct('LinguaPlone')

@onsetup
def setup_icsemantic_thesaurus():
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
        ztc.installPackage(PROJECTNAME)

    return


setup_icsemantic_thesaurus()
ptc.setupPloneSite(products=[PROJECTNAME])

def add_test_thesaurus(context):
    """Fill the thesaurus local utility with some useful information"""
    setSite(context)
    t = thesaurus_utility()
    c = Concept(et=['fútbol@es', 'balón pie@es', 'soccer@en', 'football@en', 'football@fr'])
    t.append_concept(c)
    t.append_term('mundial@es', rt=['fútbol@es'], automatic=False)
    t.append_term('pelota@es', rt=['balón pie@es'], contexts=['publicidad'], automatic=False)


class icSemanticTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit
    test cases.
    """
    __module__ = __name__

    def loadThesaurus(self, filename, language='en', format='SKOSCore', encoding='latin1'):
        self.thesaurus_utility().clean()
        self.thesaurus_utility().load(filename, language, format=format, encoding=encoding)

    def thesaurus_utility(self):
        return thesaurus_utility()

    def _where_are_different(self, aString, anotherString):
        if aString == anotherString:
            print 'Both strings are equal.'
        else:
            print 'String 1:'
            print aString
            print 'String 2:'
            print anotherString
            print 'length 1: %d' % len(aString)
            print 'length 2: %d' % len(anotherString)
            for i in range(min(len(aString), len(anotherString))):
                if aString[i] != anotherString[i]:
                    print 'first difference at: %d' % i
                    print "character 1: '%c'" % aString[i]
                    print "character 2: '%c'" % anotherString[i]
                    break


class icSemanticFunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use doctest
    syntax. Again, we can put basic common utility or setup code in here.
    """
    __module__ = __name__

    def setUp(self):
        super(ptc.FunctionalTestCase, self).setUp()
        add_test_thesaurus(self.portal)