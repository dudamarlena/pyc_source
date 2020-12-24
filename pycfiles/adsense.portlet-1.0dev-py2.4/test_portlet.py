# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/adsense/portlet/tests/test_portlet.py
# Compiled at: 2009-07-01 06:06:36
from zope.component import getUtility, getMultiAdapter
from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer
from plone.app.portlets.storage import PortletAssignmentMapping
from wwp.adsense.portlet import wwp_adsense
from wwp.adsense.portlet.tests.base import TestCase

class TestPortlet(TestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def test_portlet_type_registered(self):
        portlet = getUtility(IPortletType, name='wwp.adsense.portlet.wwp_adsense')
        self.assertEquals(portlet.addview, 'wwp.adsense.portlet.wwp_adsense')

    def test_interfaces(self):
        portlet = wwp_adsense.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_add_view(self):
        portlet = getUtility(IPortletType, name='wwp.adsense.portlet.wwp_adsense')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]

        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        addview.createAndAdd(data={})
        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0], wwp_adsense.Assignment))

    def test_invoke_edit_view(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST
        mapping['foo'] = wwp_adsense.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, wwp_adsense.EditForm))

    def test_obtain_renderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = wwp_adsense.Assignment()
        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, wwp_adsense.Renderer))


class TestRenderer(TestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = assignment or wwp_adsense.Assignment()
        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)

    def test_render(self):
        r = self.renderer(context=self.portal, assignment=wwp_adsense.Assignment())
        r = r.__of__(self.folder)
        r.update()
        output = r.render()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    suite.addTest(makeSuite(TestRenderer))
    return suite