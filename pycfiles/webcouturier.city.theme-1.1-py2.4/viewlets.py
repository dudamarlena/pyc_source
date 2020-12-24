# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/webcouturier/city/theme/browser/viewlets.py
# Compiled at: 2008-06-29 10:06:05
from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class GlobalSectionsViewlet(common.GlobalSectionsViewlet):
    __module__ = __name__
    render = ViewPageTemplateFile('templates/webcouturier_sections.pt')


class SearchBoxViewlet(common.SearchBoxViewlet):
    __module__ = __name__
    render = ViewPageTemplateFile('templates/webcouturier_searchbox.pt')