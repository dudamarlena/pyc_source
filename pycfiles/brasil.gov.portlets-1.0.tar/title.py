# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/browser/plone/title.py
# Compiled at: 2018-10-18 17:35:13
from six import iteritems
from plone.app.layout.viewlets.common import TitleViewlet as PloneTitleViewlet
from plone.memoize.view import memoize
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class TitleViewlet(PloneTitleViewlet):
    """Customize Plone TitleViewlet
    """
    index = ViewPageTemplateFile('templates/title.pt')

    @property
    @memoize
    def page_title(self):
        """
        Override default method to add the right page name (translated) for
        search and sitemap pages
        """
        alternative_titles = {'busca': 'Busca', 
           'mapadosite': 'Mapa do Site'}
        view_name = self.request.getURL()
        view_name = view_name.split('/')[(-1)]
        view_name = view_name.strip('@')
        view_name = view_name.split('?')[0]
        title = ''
        for k, v in iteritems(alternative_titles):
            if view_name == k:
                title = v

        if not title:
            title = PloneTitleViewlet.page_title.fget(self)
        return title