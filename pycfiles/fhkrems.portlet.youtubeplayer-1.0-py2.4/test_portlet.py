# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\fhkrems\portlet\youtubeplayer\tests\test_portlet.py
# Compiled at: 2010-07-20 08:14:57
from zope.component import getUtility, getMultiAdapter
from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer
from plone.app.portlets.storage import PortletAssignmentMapping
from fhkrems.portlet.youtubeplayer import youtubeplayerportlet
from fhkrems.portlet.youtubeplayer.tests.base import TestCase

class TestPortlet(TestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def test_portlet_type_registered(self):
        portlet = getUtility(IPortletType, name='fhkrems.portlet.youtubeplayer.YouTubePlayerPortlet')
        self.assertEquals(portlet.addview, 'fhkrems.portlet.youtubeplayer.YouTubePlayerPortlet')

    def test_interfaces(self):
        portlet = youtubeplayerportlet.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_add_view(self):
        portlet = getUtility(IPortletType, name='fhkrems.portlet.youtubeplayer.YouTubePlayerPortlet')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]

        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        addview.createAndAdd(data={})
        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0], youtubeplayerportlet.Assignment))

    def test_invoke_edit_view(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST
        mapping['foo'] = youtubeplayerportlet.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, youtubeplayerportlet.EditForm))

    def test_obtain_renderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = youtubeplayerportlet.Assignment()
        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, youtubeplayerportlet.Renderer))


class TestRenderer(TestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = assignment or youtubeplayerportlet.Assignment()
        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)

    def test_render(self):
        r = self.renderer(context=self.portal, assignment=youtubeplayerportlet.Assignment())
        r = r.__of__(self.folder)
        r.update()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    suite.addTest(makeSuite(TestRenderer))
    return suite