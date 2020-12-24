# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/thesaurus/tests/test_incremental_search_select_widget.py
# Compiled at: 2008-10-06 10:31:07
import unittest
from icsemantic.thesaurus.Thesaurus import thesaurus_utility
from icsemantic.thesaurus.browser.admin import VerticalSelectTest
from icsemantic.thesaurus.browser.incrementalSearchSelectWidget import IncrementalSearchSelectAzax
from zope.app.component.hooks import setSite
import base

class TestIncrementalSearchSelectWidget(base.icSemanticTestCase):
    __module__ = __name__

    def testChooseSelectedConcept(self):
        print self.chooseSelectedConcept('formverticalSelect', 'amar@es, antoja')

    def testAutocompleteConcepts(self):
        print self.autocompleteConcepts('formverticalSelect', 'amar, temer')

    def testVerticalSelect(self):
        pass

    def openVerticalSelectTestPage(self):
        vertical_select = VerticalSelectTest(self.portal, self.app.REQUEST)()

    def autocompleteConcepts(self, widgetName, searchExpression):
        return self.incrementalSearchSelectAzax().autocompleteConcepts(widgetName, searchExpression)

    def chooseSelectedConcept(self, widgetName, searchExpression):
        return self.incrementalSearchSelectAzax().chooseSelectedConcept(widgetName, searchExpression)

    def incrementalSearchSelectAzax(self):
        return IncrementalSearchSelectAzax(self.portal, self.app.REQUEST)

    def afterSetUp(self):
        setSite(self.portal)
        self.login()
        self.setRoles(['Manager', 'Member'])
        self.portal.portal_languages.addSupportedLanguage('es')
        self.loadThesaurus('../pyThesaurus/pyThesaurus/tests/data/open_thesaurus_es.txt', language='es', format='Ding')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestIncrementalSearchSelectWidget))
    return suite