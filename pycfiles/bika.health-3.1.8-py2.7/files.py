# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/browser/patient/files.py
# Compiled at: 2015-11-03 03:53:39
from bika.lims import bikaMessageFactory as _
from plone.app.content.browser.interfaces import IFolderContentsView
from plone.app.layout.globals.interfaces import IViewView
from zope.interface import implements
from bika.lims.browser.multifile import MultifileView

class PatientMultifileView(MultifileView):
    implements(IFolderContentsView, IViewView)

    def __init__(self, context, request):
        super(PatientMultifileView, self).__init__(context, request)
        self.title = self.context.translate(_('Patient Attachments'))
        self.context_actions = {_('Add'): {'url': 'createObject?type_name=Multifile', 'icon': '++resource++bika.lims.images/add.png'}}