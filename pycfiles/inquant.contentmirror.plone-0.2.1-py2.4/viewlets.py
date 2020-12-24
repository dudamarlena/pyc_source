# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/inquant/contentmirror/plone/browser/viewlets.py
# Compiled at: 2008-04-09 08:43:41
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 62294 $'
__version__ = '$Revision: 62294 $'[11:-2]
from zope import component
from zope.interface import implements
from zope.viewlet.interfaces import IViewlet
from Acquisition import aq_inner, aq_parent
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from inquant.contentmirror.base.interfaces import IMirroredContent
from inquant.contentmirror.base.interfaces import IMirroredContentManager
from inquant.contentmirror.base.interfaces import IMirrorReferenceManager

class MirrorInfoViewlet(BrowserView):
    """ Viewlet to show some info if the ccurrent context is a mirror. Also allows to remove the mirror.
    """
    __module__ = __name__
    implements(IViewlet)
    render = ViewPageTemplateFile('mirror-info.pt')

    def __init__(self, context, request, view, manager):
        super(MirrorInfoViewlet, self).__init__(context, request)
        self.__parent__ = view
        self.view = view
        self.container = aq_parent(aq_inner(self.context))
        self.manager = component.getUtility(IMirroredContentManager)
        self.refmgr = IMirrorReferenceManager(self.context)

    def update(self):
        if not self.available():
            return
        if self.request.has_key('inquant.contentmirror.plone.remove'):
            self.manager.removeMirror(self.context, self.container)
            IStatusMessage(self.request).addStatusMessage('Removed mirror.', type='info')
            self.request.response.redirect(self.container.absolute_url())

    def available(self):
        if not IMirroredContent.providedBy(self.context):
            return False
        return self.refmgr.isMirror(self.context, self.container)

    def original_url(self):
        return self.refmgr.getOriginal().absolute_url()