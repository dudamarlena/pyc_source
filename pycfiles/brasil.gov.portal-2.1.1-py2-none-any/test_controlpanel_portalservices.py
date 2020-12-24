# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/tests/test_controlpanel_portalservices.py
# Compiled at: 2018-10-18 17:35:14
"""Testa o controlpanel de configuração do Portal Padrão."""
from brasil.gov.portal.controlpanel.portal import ISettingsPortal
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
import unittest

class ControlPanelTestCase(unittest.TestCase):
    """Testes de configuração do Portal Padrão."""
    layer = INTEGRATION_TESTING

    def setUp(self):
        """Configura ambiente de teste antes de cada teste."""
        self.portal = self.layer['portal']
        self.controlpanel = api.portal.get_tool('portal_controlpanel')

    def test_controlpanel_has_view(self):
        u"""Verifica se a view de configuração existe."""
        request = self.layer['request']
        view = api.content.get_view('portal-services-settings', self.portal, request)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        with api.env.adopt_roles(['Anonymous']):
            self.assertRaises(Unauthorized, self.portal.restrictedTraverse, '@@portal-services-settings')

    def test_controlpanel_installed(self):
        u"""Verifica se o configlet do controlpanel está instalado."""
        actions = [ a.getAction(self)['id'] for a in self.controlpanel.listActions()
                  ]
        self.assertIn('portal-services-settings', actions)

    def test_controlpanel_permissions(self):
        u"""Testa a permissão de acesso ao configlet."""
        roles = [
         'Manager', 'Site Administrator']
        for r in roles:
            with api.env.adopt_roles([r]):
                configlets = self.controlpanel.enumConfiglets(group='Products')
                configlets = [ a['id'] for a in configlets ]
                self.assertIn('portal-services-settings', configlets, 'configlet not listed for ' + r)


class RegistryTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal-services-settings']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISettingsPortal)