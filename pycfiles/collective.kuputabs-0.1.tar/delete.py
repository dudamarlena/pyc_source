# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/kss/flygui/browser/delete.py
# Compiled at: 2008-05-01 14:12:35
from Products.Five.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile

class DeletePopup(BrowserView):
    render = ViewPageTemplateFile('templates/delete_popup.pt')

    def __init__(self, context, request, paths):
        super(DeletePopup, self).__init__(context, request)
        self.paths = paths