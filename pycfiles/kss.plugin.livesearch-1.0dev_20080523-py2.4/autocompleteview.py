# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kss/plugin/livesearch/autocompleteview.py
# Compiled at: 2008-05-23 06:03:39
"""Support of keyword autocomplete widget for Plone / Archetypes
"""
from livesearchview import LiveSearchView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.CMFCore.utils import getToolByName

class AutoCompleteView(LiveSearchView):
    __module__ = __name__
    emptyResult = False

    def update(self, q, limit=10):
        fieldname = self.request.fieldname
        cat = getToolByName(self.context, 'portal_catalog')
        words = cat.uniqueValuesFor('Subject')
        term = q.strip()
        self.results = results = []
        if not term:
            return
        for w in words:
            if w.startswith(term):
                if len(results) < limit:
                    results.append(w)
                else:
                    self.showMore = True
                    break

    renderHtml = ZopeTwoPageTemplateFile('autocompleteview.pt')