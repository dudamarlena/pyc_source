# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.activitystream/plonesocial/activitystream/browser/navigation.py
# Compiled at: 2014-01-17 04:33:08
from zope.interface import implements
from zope.viewlet.interfaces import IViewlet
from zope.publisher.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from plonesocial.activitystream.integration import PLONESOCIAL

class PloneSocialNavigation(BrowserView):
    """Provide toplevel navigation that spans plonesocial.activitystream
    and plonesocial.network.
    """
    implements(IViewlet)

    def __init__(self, context, request, view, manager):
        self.context = context
        self.request = request
        self.view = self.__parent__ = view
        self.manager = manager

    def update(self):
        pass

    render = ViewPageTemplateFile('templates/navigation.pt')

    def portal_url(self):
        portal_state = getMultiAdapter((
         self.context, self.request), name='plone_portal_state')
        return portal_state.portal_url()

    def items(self):
        menu = []
        m_context = PLONESOCIAL.context(self.context)
        if m_context:
            m_base = m_context.absolute_url() + '/'
            menu.extend([
             dict(url=m_base + '@@stream', title=m_context.Title() + ' updates', state='localstream')])
        base = self.portal_url() + '/'
        menu.extend([
         dict(url=base + '@@stream', title='Explore', state='explore')])
        if PLONESOCIAL.network:
            menu.extend([
             dict(url=base + '@@stream/network', title='My network', state='stream'),
             dict(url=base + '@@profile', title='My profile', state='profile')])
        for item in menu:
            if self.request.URL == item['url']:
                item['state'] = 'active'

        return menu