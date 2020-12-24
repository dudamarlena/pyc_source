# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/pingtool/browser/ping.py
# Compiled at: 2009-03-31 04:47:30
from Acquisition import aq_inner
from zope.annotation.interfaces import IAnnotations
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from quintagroup.pingtool.interfaces import ISyndicationObject

class RunPingView(BrowserView):
    """A class with helper methods for use in views/templates.
    """
    __module__ = __name__

    def __call__(self):
        context = aq_inner(self.context)
        annotations = IAnnotations(self.context)
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        pp = getToolByName(portal, 'portal_pingtool', None)
        if pp:
            (status, message) = pp.pingFeedReader(context)
            portal_message, ping_message = message['portal_message'], message['return_message']
            annotations['ping_message'] = ping_message
            state = self.get_state(status)
            portal.plone_utils.addPortalMessage(portal_message, state)
            if state == 'warning':
                self.request.response.redirect(context.absolute_url() + '/base_edit')
            else:
                self.request.response.redirect('@@return_ping')
        return

    def get_state(self, status):
        if status == 'success':
            state = 'info'
        elif status == 'failed':
            state = 'warning'
        else:
            state = 'info'
        return state


class CanPingView(BrowserView):
    """A class with helper methods for use in views/templates.
    """
    __module__ = __name__

    def __call__(self):
        return ISyndicationObject.providedBy(self.context) and (hasattr(self.context, 'enable_ping') and self.context.enable_ping or False)


class ReturnPingView(BrowserView):
    """A class with helper methods for use in views/templates.
    """
    __module__ = __name__
    template = ViewPageTemplateFile('return_ping.pt')

    def __call__(self):
        annotations = IAnnotations(self.context)
        self.ping_message = annotations['ping_message']
        return self.template()