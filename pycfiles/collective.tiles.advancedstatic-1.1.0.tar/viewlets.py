# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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