# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/Products/LinguaFace/tests/testCutPast.py
# Compiled at: 2010-11-30 09:59:25
import transaction
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.tests.utils import makeTranslation
from base import LinguaFaceTestCase

class TestCut(LinguaFaceTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.addLanguage('fr')
        self.addLanguage('en')
        self.addLanguage('es')
        self.setLanguage('fr')
        self.folderA = makeContent(self.folder, 'SimpleFolder', 'folderA')
        self.folderB = makeContent(self.folder, 'SimpleFolder', 'folderB')
        self.french = makeContent(self.folderA, 'SimpleType', 'doc')
        self.french.setLanguage('fr')
        self.english = makeTranslation(self.french, 'en')
        self.spanish = makeTranslation(self.french, 'es')

    def testCutCanonical(self):
        transaction.savepoint(optimistic=True)
        cp = self.folderA.manage_cutObjects(ids=['doc'])
        self.folderB.manage_pasteObjects(cb_copy_data=cp)
        listA = self.folderA.objectIds()
        listB = self.folderB.objectIds()
        listB.sort()
        self.assertEquals(listA, [])
        self.assertEquals(listB, ['doc', 'doc-en', 'doc-es'])
        canonicalB = getattr(self.folderB, 'doc')
        englishB = getattr(self.folderB, 'doc-en')
        self.assertEquals(englishB.getCanonical(), canonicalB)

    def testCutTranslation(self):
        transaction.savepoint(optimistic=True)
        cp = self.folderA.manage_cutObjects(ids=['doc-en'])
        self.folderB.manage_pasteObjects(cb_copy_data=cp)
        listA = self.folderA.objectIds()
        listB = self.folderB.objectIds()
        listB.sort()
        self.assertEquals(listA, [])
        self.assertEquals(listB, ['doc', 'doc-en', 'doc-es'])
        canonical = getattr(self.folderB, 'doc')
        spanish = getattr(self.folderB, 'doc-es')
        self.assertEquals(spanish.getCanonical(), canonical)


class TestCutNested(LinguaFaceTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.addLanguage('fr')
        self.addLanguage('en')
        self.addLanguage('es')
        self.setLanguage('fr')
        self.folderA = makeContent(self.folder, 'SimpleFolder', 'folderA')
        self.folderB = makeContent(self.folderA, 'SimpleFolder', 'folderB')
        self.french = makeContent(self.folderA, 'SimpleType', 'doc')
        self.french.setLanguage('fr')
        self.english = makeTranslation(self.french, 'en')
        self.spanish = makeTranslation(self.french, 'es')

    def testCutCanonical(self):
        transaction.savepoint(optimistic=True)
        cp = self.folderA.manage_cutObjects(ids=['doc'])
        self.folderB.manage_pasteObjects(cb_copy_data=cp)
        listA = self.folderA.objectIds()
        listB = self.folderB.objectIds()
        listB.sort()
        self.assertEquals(listA, ['folderB'])
        self.assertEquals(listB, ['doc', 'doc-en', 'doc-es'])
        canonicalB = getattr(self.folderB, 'doc')
        englishB = getattr(self.folderB, 'doc-en')
        self.assertEquals(englishB.getCanonical(), canonicalB)

    def testCutTranslation(self):
        transaction.savepoint(optimistic=True)
        cp = self.folderA.manage_cutObjects(ids=['doc-en'])
        self.folderB.manage_pasteObjects(cb_copy_data=cp)
        listA = self.folderA.objectIds()
        listB = self.folderB.objectIds()
        listB.sort()
        self.assertEquals(listA, ['folderB'])
        self.assertEquals(listB, ['doc', 'doc-en', 'doc-es'])
        canonicalB = getattr(self.folderB, 'doc')
        englishB = getattr(self.folderB, 'doc-en')
        self.assertEquals(englishB.getCanonical(), canonicalB)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCut))
    suite.addTest(makeSuite(TestCutNested))
    return suite