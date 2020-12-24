# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/collective/subrip2html/browser/view.py
# Compiled at: 2010-12-28 14:41:43
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

class SrtView(BrowserView):
    """View file content transformed in SRT"""
    __module__ = __name__

    @property
    def srt_content(self):
        context = self.context
        pt = getToolByName(context, 'portal_transforms')
        data = context.getFile().data
        if not type(data) == str:
            data = data.data
        html = pt.convert('srt_to_html', data).getData()
        return html