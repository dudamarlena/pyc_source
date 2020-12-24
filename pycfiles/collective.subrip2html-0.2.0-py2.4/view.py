# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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