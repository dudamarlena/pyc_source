# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/forcontent/idgb/src/brasil.gov.portal/src/brasil/gov/portal/browser/viewlets/content.py
# Compiled at: 2017-07-07 17:23:19
__doc__ = 'Customiza DocumentBylineViewlet do plone.app.layout.'
from plone.app.layout.viewlets.content import DocumentBylineViewlet as DBLV
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter

class DocumentBylineViewlet(DBLV):
    u"""Customiza DocumentBylineViewlet do plone.app.layout, para considerar
    configurações do portal sobre esconder autor e esconder data de publicação.
    """
    index = ViewPageTemplateFile('templates/document_byline.pt')

    def mostra_autor(self):
        u"""Verifica se a configuração do portal pede para mostrar o autor."""
        portal_settings = getMultiAdapter((self.context, self.context.REQUEST), name='portal_settings')
        return not portal_settings.get_esconde_autor()

    def mostra_data(self):
        u"""Verifica se a configuração do portal pede para mostrar a data."""
        portal_settings = getMultiAdapter((self.context, self.context.REQUEST), name='portal_settings')
        return not portal_settings.get_esconde_data()