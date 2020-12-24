# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redomino/advancedkeyword/tests/test_portlet.py
# Compiled at: 2013-05-08 04:41:18
from zope.component import getUtility, getMultiAdapter
from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer
from plone.app.portlets.storage import PortletAssignmentMapping
from redomino.advancedkeyword.portlets import keywordportlet
from redomino.advancedkeyword.tests.base import TestCase

class TestPortlet(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))
        self.portal.invokeFactory('Document', 'doc-tag1')
        self.portal.invokeFactory('Document', 'doc-tag2')
        doc1 = self.portal['doc-tag1']
        doc2 = self.portal['doc-tag2']
        doc1.setSubject(['1.11', '1.12', '1.12.121'])
        doc2.setSubject(['2.21', '1.11'])
        doc1.reindexObject()
        doc2.reindexObject()

    def test_portlet_type_registered(self):
        portlet = getUtility(IPortletType, name='redomino.advancedkeyword.KeywordPortlet')
        self.assertEquals(portlet.addview, 'redomino.advancedkeyword.KeywordPortlet')

    def test_interfaces(self):
        portlet = keywordportlet.Assignment('myportlet', '1')
        self.assertTrue(IPortletAssignment.providedBy(portlet))
        self.assertTrue(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_add_view(self):
        portlet = getUtility(IPortletType, name='redomino.advancedkeyword.KeywordPortlet')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]

        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        addview.form_instance.createAndAdd(data={})
        self.assertEquals(len(mapping), 1)
        self.assertTrue(isinstance(mapping.values()[0], keywordportlet.Assignment))

    def test_invoke_edit_view(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST
        mapping['foo'] = keywordportlet.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.assertTrue(isinstance(editview, keywordportlet.EditFormView))

    def test_obtain_renderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = keywordportlet.Assignment('myportlet', '1')
        renderer = getMultiAdapter((
         context, request, view, manager, assignment), IPortletRenderer)
        self.assertTrue(isinstance(renderer, keywordportlet.Renderer))
        childrenTags = [ item[0] for item in renderer.getChildrenTags() ]
        self.assertTrue('1.11' in childrenTags)
        self.assertTrue('1.12' in childrenTags)
        self.assertFalse('1.12.121' in childrenTags)
        self.assertFalse('2.21' in childrenTags)


class TestRenderer(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))
        self.portal.invokeFactory('Document', 'doc-tag1')
        self.portal.invokeFactory('Document', 'doc-tag2')
        doc1 = self.portal['doc-tag1']
        doc2 = self.portal['doc-tag2']
        doc1.setSubject(['1.11', '1.12', '1.11.111', '1.11.112'])
        doc2.setSubject(['2.21', '2.22'])
        doc1.reindexObject()
        doc2.reindexObject()

    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = assignment or keywordportlet.Assignment()
        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)

    def test_render(self):
        r = self.renderer(context=self.portal, assignment=keywordportlet.Assignment('myportlet', '1'))
        r = r.__of__(self.folder)
        r.update()
        output = r.render()
        self.assertTrue('Subject=1' in output)
        self.assertTrue('Subject=1.11' in output)
        self.assertTrue('Subject=1.12' in output)
        self.assertFalse('Subject=2.21' in output)
        self.assertFalse('Subject=2.22' in output)
        self.assertFalse('Subject=1.11.111' in output)
        self.assertFalse('Subject=1.11.112' in output)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    suite.addTest(makeSuite(TestRenderer))
    return suite