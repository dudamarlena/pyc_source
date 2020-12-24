# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/Products/LinguaFace/tests/testCopyPast.py
# Compiled at: 2010-11-30 09:59:25
import transaction
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.tests.utils import makeTranslation
from base import LinguaFaceTestCase

class TestCopy(LinguaFaceTestCase):
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

    def testCopyCanonical(self):
        transaction.savepoint(optimistic=True)
        cp = self.folderA.manage_copyObjects(ids=['doc'])
        self.folderB.manage_pasteObjects(cb_copy_data=cp)
        listA = self.folderA.objectIds()
        listA.sort()
        listB = self.folderB.objectIds()
        listB.sort()
        self.assertEquals(listA, ['doc', 'doc-en', 'doc-es'])
        self.assertEquals(listB, ['doc', 'doc-en', 'doc-es'])
        for folder in [self.folderA, self.folderB]:
            canonical = getattr(folder, 'doc')
            self.assertEquals(canonical.isCanonical(), True)
            english = getattr(folder, 'doc-en')
            self.assertEquals(english.getCanonical(), canonical)
            spanish = getattr(folder, 'doc-es')
            self.assertEquals(spanish.getCanonical(), canonical)

    def testCopyTranslation(self):
        transaction.savepoint(optimistic=True)
        cp = self.folderA.manage_copyObjects(ids=['doc-en'])
        self.folderB.manage_pasteObjects(cb_copy_data=cp)
        listA = self.folderA.objectIds()
        listA.sort()
        listB = self.folderB.objectIds()
        listB.sort()
        self.assertEquals(listA, ['doc', 'doc-en', 'doc-es'])
        self.assertEquals(listB, ['doc', 'doc-en', 'doc-es'])
        for folder in [self.folderA, self.folderB]:
            canonical = getattr(folder, 'doc')
            self.assertEquals(canonical.isCanonical(), True)
            english = getattr(folder, 'doc-en')
            self.assertEquals(english.getCanonical(), canonical)
            spanish = getattr(folder, 'doc-es')
            self.assertEquals(spanish.getCanonical(), canonical)


class TestCopyNested(LinguaFaceTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.addLanguage('fr')
        self.addLanguage('en')
        self.addLanguage('es')
        self.addLanguage('de')
        self.setLanguage('fr')
        self.folderA = makeContent(self.folder, 'SimpleFolder', 'folderA')
        self.folderB = makeContent(self.folderA, 'SimpleFolder', 'folderB')
        self.french = makeContent(self.folderA, 'SimpleType', 'doc')
        self.french.setLanguage('fr')
        self.english = makeTranslation(self.french, 'en')
        self.spanish = makeTranslation(self.french, 'es')

    def testCopyCanonical(self):
        transaction.savepoint(optimistic=True)
        cp = self.folderA.manage_copyObjects(ids=['doc'])
        self.folderB.manage_pasteObjects(cb_copy_data=cp)
        listA = self.folderA.objectIds()
        listA.sort()
        listB = self.folderB.objectIds()
        listB.sort()
        self.assertEquals(listA, ['doc', 'doc-en', 'doc-es', 'folderB'])
        self.assertEquals(listB, ['doc', 'doc-en', 'doc-es'])
        for folder in [self.folderA, self.folderB]:
            canonical = getattr(folder, 'doc')
            self.assertEquals(canonical.isCanonical(), True)
            english = getattr(folder, 'doc-en')
            self.assertEquals(english.getCanonical(), canonical)
            spanish = getattr(folder, 'doc-es')
            self.assertEquals(spanish.getCanonical(), canonical)

    def testCopyTranslation(self):
        transaction.savepoint(optimistic=True)
        cp = self.folderA.manage_copyObjects(ids=['doc-en'])
        self.folderB.manage_pasteObjects(cb_copy_data=cp)
        listA = self.folderA.objectIds()
        listA.sort()
        listB = self.folderB.objectIds()
        listB.sort()
        self.assertEquals(listA, ['doc', 'doc-en', 'doc-es', 'folderB'])
        self.assertEquals(listB, ['doc', 'doc-en', 'doc-es'])
        for folder in [self.folderA, self.folderB]:
            canonical = getattr(folder, 'doc')
            self.assertEquals(canonical.isCanonical(), True)
            english = getattr(folder, 'doc-en')
            self.assertEquals(english.getCanonical(), canonical)
            spanish = getattr(folder, 'doc-es')
            self.assertEquals(spanish.getCanonical(), canonical)


class TestCopyInSameFolder(LinguaFaceTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.addLanguage('fr')
        self.addLanguage('en')
        self.addLanguage('es')
        self.addLanguage('de')
        self.setLanguage('fr')
        self.french = makeContent(self.folder, 'SimpleType', 'doc')
        self.french.setLanguage('fr')
        self.english = makeTranslation(self.french, 'en')
        self.spanish = makeTranslation(self.french, 'es')
        self.copy_prefix = 'copy_of_'

    def testCopyCanonical(self):
        copies = self.folder.objectIds()
        for id in self.folder.objectIds():
            copies.append(self.copy_prefix + id)

        copies.sort()
        transaction.savepoint(optimistic=True)
        cp = self.folder.manage_copyObjects(ids=['doc'])
        self.folder.manage_pasteObjects(cb_copy_data=cp)
        listIds = self.folder.objectIds()
        listIds.sort()
        self.assertEquals(listIds, copies)
        for prefix in ['', self.copy_prefix]:
            canonical = getattr(self.folder, '%sdoc' % prefix)
            self.assertEquals(canonical.isCanonical(), True)
            english = getattr(self.folder, '%sdoc-en' % prefix)
            self.assertEquals(english.getCanonical(), canonical)
            spanish = getattr(self.folder, '%sdoc-es' % prefix)
            self.assertEquals(spanish.getCanonical(), canonical)

    def testCopyTranslation(self):
        copies = self.folder.objectIds()
        for id in self.folder.objectIds():
            copies.append(self.copy_prefix + id)

        copies.sort()
        transaction.savepoint(optimistic=True)
        cp = self.folder.manage_copyObjects(ids=['doc-en'])
        self.folder.manage_pasteObjects(cb_copy_data=cp)
        listIds = self.folder.objectIds()
        listIds.sort()
        for prefix in ['', self.copy_prefix]:
            canonical = getattr(self.folder, '%sdoc' % prefix)
            self.assertEquals(canonical.isCanonical(), True)
            english = getattr(self.folder, '%sdoc-en' % prefix)
            self.assertEquals(english.getCanonical(), canonical)
            spanish = getattr(self.folder, '%sdoc-es' % prefix)
            self.assertEquals(spanish.getCanonical(), canonical)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCopy))
    suite.addTest(makeSuite(TestCopyInSameFolder))
    suite.addTest(makeSuite(TestCopyNested))
    return suite