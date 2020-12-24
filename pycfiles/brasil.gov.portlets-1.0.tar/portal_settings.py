# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/browser/plone/portal_settings.py
# Compiled at: 2018-10-18 17:35:13
__doc__ = 'Views'
from brasil.gov.portal.browser.plone.interfaces import IPortalSettingsView
from plone import api
from Products.Five import BrowserView
from zope.interface import implementer

@implementer(IPortalSettingsView)
class PortalSettingsView(BrowserView):
    u"""View para obter configurações do portal."""

    def get_esconde_autor(self):
        u"""Retorna o valor da configuração esconde_autor."""
        record = 'brasil.gov.portal.controlpanel.portal.ISettingsPortal.esconde_autor'
        return api.portal.get_registry_record(record)

    def get_esconde_data(self):
        u"""Retorna o valor da configuração esconde_data."""
        record = 'brasil.gov.portal.controlpanel.portal.ISettingsPortal.esconde_data'
        return api.portal.get_registry_record(record)