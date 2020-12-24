# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/kss/flygui/browser/delete.py
# Compiled at: 2008-05-01 14:12:35
from Products.Five.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile

class DeletePopup(BrowserView):
    render = ViewPageTemplateFile('templates/delete_popup.pt')

    def __init__(self, context, request, paths):
        super(DeletePopup, self).__init__(context, request)
        self.paths = paths