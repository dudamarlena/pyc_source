# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redomino/advancedkeyword/tests/test_indexers.py
# Compiled at: 2013-05-08 04:41:18
from redomino.advancedkeyword.tests.base import TestCase

class TestIndexers(TestCase):
    """ Check if the customized plone indexer Subject works properly
    """

    def test_subjects1(self):
        """ redomino -> redomino"""
        front_page = self.portal['front-page']
        front_page.setSubject(['redomino'])
        front_page.reindexObject()
        self.assertEqual(self.portal.portal_catalog.uniqueValuesFor('Subject'), ('redomino', ))

    def test_subjects2(self):
        """ redomino.prodotti.recatalog -> redomino, redomino.prodotti, redomino.prodotti.recatalog"""
        front_page = self.portal['front-page']
        front_page.setSubject(['redomino.prodotti.recatalog'])
        front_page.reindexObject()
        self.assertEqual(set(self.portal.portal_catalog.uniqueValuesFor('Subject')), set(('redomino',
                                                                                          'redomino.prodotti',
                                                                                          'redomino.prodotti.recatalog')))

    def test_subjects3(self):
        """ redomino.prodotti.recatalog, redomino.prova -> redomino, redomino.prova, redomino.prodotti, redomino.prodotti.recatalog 
        """
        front_page = self.portal['front-page']
        front_page.setSubject(['redomino.prodotti.recatalog', 'redomino.prova'])
        front_page.reindexObject()
        self.assertEqual(set(self.portal.portal_catalog.uniqueValuesFor('Subject')), set(('redomino',
                                                                                          'redomino.prova',
                                                                                          'redomino.prodotti',
                                                                                          'redomino.prodotti.recatalog')))

    def test_subjects4(self):
        """ redomino, redomino. -> redomino"""
        front_page = self.portal['front-page']
        front_page.setSubject(['redomino', 'redomino.'])
        front_page.reindexObject()
        self.assertEqual(self.portal.portal_catalog.uniqueValuesFor('Subject'), ('redomino', ))

    def test_subjectsi5(self):
        """ redomino..pippo. -> redomino, pippo"""
        front_page = self.portal['front-page']
        front_page.setSubject(['redomino..pippo.'])
        front_page.reindexObject()
        self.assertEqual(self.portal.portal_catalog.uniqueValuesFor('Subject'), ('redomino',
                                                                                 'redomino.pippo'))

    def test_subjects6(self):
        """ colore.rosso spento -> colore, rosso spento"""
        front_page = self.portal['front-page']
        front_page.setSubject(['colore.rosso spento'])
        front_page.reindexObject()
        self.assertEqual(self.portal.portal_catalog.uniqueValuesFor('Subject'), ('colore',
                                                                                 'colore.rosso spento'))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestIndexers))
    return suite