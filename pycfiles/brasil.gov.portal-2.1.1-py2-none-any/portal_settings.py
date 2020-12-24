# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/browser/plone/portal_settings.py
# Compiled at: 2018-10-18 17:35:13
"""Views"""
from brasil.gov.portal.browser.plone.interfaces import IPortalSettingsView
from plone import api
from Products.Five import BrowserView
from zope.interface import implementer

@implementer(IPortalSettingsView)
class PortalSettingsView(BrowserView):
    """View para obter configurações do portal."""

    def get_esconde_autor(self):
        u"""Retorna o valor da configuração esconde_autor."""
        record = 'brasil.gov.portal.controlpanel.portal.ISettingsPortal.esconde_autor'
        return api.portal.get_registry_record(record)

    def get_esconde_data(self):
        u"""Retorna o valor da configuração esconde_data."""
        record = 'brasil.gov.portal.controlpanel.portal.ISettingsPortal.esconde_data'
        return api.portal.get_registry_record(record)