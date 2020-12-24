# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redomino/advancedkeyword/tests/test_viewlets.py
# Compiled at: 2013-05-08 04:41:18
from redomino.advancedkeyword.tests.base import FunctionalTestCase
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewlet, IViewletManager

class TestViewlets(FunctionalTestCase):
    """ Verifichiamo se la viewlet visualizza correttamente le keyword
    """

    def afterSetUp(self):
        super(TestViewlets, self).afterSetUp()
        portal = self.portal
        fp = portal['front-page']
        request = self.portal.REQUEST
        view = portal.restrictedTraverse('@@plone')
        from plone.app.layout.globals.interfaces import IViewView
        from zope.interface import alsoProvides
        alsoProvides(view, IViewView)
        manager = getMultiAdapter((fp, request, view), IViewletManager, name='plone.belowcontent')
        viewlet = getMultiAdapter((fp, request, view, manager), IViewlet, name='plone.belowcontenttitle.keywordstest')
        self.fp = fp
        self.viewlet = viewlet

    def test_right_viewlet(self):
        """ Test right viewlet """
        from redomino.advancedkeyword.browser.viewlets import KeywordsViewlet
        self.assertTrue(isinstance(self.viewlet, KeywordsViewlet))

    def test_keyword1(self):
        """ 'redomino' -> 'redomino' """
        fp = self.fp
        viewlet = self.viewlet
        fp.setSubject(['redomino'])
        fp.reindexObject()
        viewlet.update()
        self.assertEquals(set(['redomino']), set(viewlet.subjects))

    def test_keyword2(self):
        """ 'redomino','pippo.prova' -> 'redomino', 'pippo', 'pippo.prova' """
        fp = self.fp
        viewlet = self.viewlet
        fp.setSubject(['redomino', 'pippo.prova'])
        fp.reindexObject()
        viewlet.update()
        self.assertEquals(set(['redomino', 'pippo', 'pippo.prova']), set(viewlet.subjects))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestViewlets))
    return suite