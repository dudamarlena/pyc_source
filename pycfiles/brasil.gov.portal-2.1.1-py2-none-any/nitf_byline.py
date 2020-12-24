# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idgb/src/brasil.gov.portal/src/brasil/gov/portal/browser/viewlets/nitf_byline.py
# Compiled at: 2017-07-07 17:23:19
from collective.nitf.browser import NITFBylineViewlet as CollectiveNITFBylineViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter

class NITFBylineViewlet(CollectiveNITFBylineViewlet):
    index = ViewPageTemplateFile('templates/nitf_byline.pt')

    def mostra_autor(self):
        u"""Verifica se a configuração do portal pede para mostrar o autor."""
        portal_settings = getMultiAdapter((self.context, self.context.REQUEST), name='portal_settings')
        return not portal_settings.get_esconde_autor()

    def mostra_data(self):
        u"""Verifica se a configuração do portal pede para mostrar a data."""
        portal_settings = getMultiAdapter((self.context, self.context.REQUEST), name='portal_settings')
        return not portal_settings.get_esconde_data()