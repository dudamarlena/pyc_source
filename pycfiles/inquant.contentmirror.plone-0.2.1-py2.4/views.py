# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/inquant/contentmirror/plone/browser/views.py
# Compiled at: 2008-04-09 08:43:41
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 62294 $'
__version__ = '$Revision: 62294 $'[11:-2]
from zope import component
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from inquant.contentmirror.base.interfaces import IMirroredContentManager
from inquant.contentmirror.plone.utils import get_copy_objects

class MirrorAddView(BrowserView):
    """
    """
    __module__ = __name__

    def __init__(self, context, request):
        super(MirrorAddView, self).__init__(context, request)
        self.copy_objects = get_copy_objects(REQUEST=request)
        self.manager = component.getUtility(IMirroredContentManager)

    def __call__(self):
        added = []
        for o in self.copy_objects:
            self.manager.addMirror(o, self.context)
            added.append(o.getId())

        IStatusMessage(self.request).addStatusMessage('Added mirror(s) of %s' % (',').join(added), type='info')
        self.request.response.redirect(self.context.absolute_url())