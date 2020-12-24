# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/forcontent/idgb/src/brasil.gov.portal/src/brasil/gov/portal/browser/viewlets/portal_head.py
# Compiled at: 2017-11-02 19:53:49
from plone import api
from plone.app.layout.viewlets import ViewletBase
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class PortalHeadViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/portal_head.pt')

    def update(self):
        """Prepara/Atualiza os valores utilizados pelo Viewlet"""
        super(PortalHeadViewlet, self).update()
        portal = api.portal.get()
        self.pprop = getToolByName(portal, 'portal_properties')
        configs = getattr(self.pprop, 'brasil_gov', None)
        self.url_orgao = configs.getProperty('url_orgao', '')
        return