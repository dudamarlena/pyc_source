# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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