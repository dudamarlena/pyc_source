# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\collective\threecolorstheme\browser\viewlets.py
# Compiled at: 2008-10-12 05:15:37
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common
from Acquisition import aq_inner
from zope.app.component.hooks import getSite

class GlobalSectionsViewlet(common.ViewletBase):
    __module__ = __name__
    render = ViewPageTemplateFile('templates/dropdown-sections.pt')

    def ajaxinfos(self):
        """
        get the good ajaxurl and selected id
        """
        portal = getSite()
        context = aq_inner(self.context)
        request = self.request
        plone_url = portal.absolute_url()
        plone_url_splitted = plone_url.split('/')
        url_splitted = context.absolute_url().split('/')
        if len(url_splitted) > len(plone_url_splitted):
            selectedid = url_splitted[len(plone_url_splitted)]
        else:
            selectedid = 'index_html'
        ajaxurl = '%s/@@dropdownmenus' % plone_url
        if request.get('refresh-globalsections', ''):
            ajaxurl += '?refresh-globalsections=1'
        return {'ajaxurl': ajaxurl, 'selectedid': selectedid}