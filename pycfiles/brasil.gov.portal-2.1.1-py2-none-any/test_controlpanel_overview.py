# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/tests/test_controlpanel_overview.py
# Compiled at: 2018-10-18 17:35:14
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
import unittest

class OverviewControlPanelTest(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_overview_controlpanel_view(self):
        """Validamos se o control panel esta acessivel"""
        view = api.content.get_view(name='overview-controlpanel', context=self.portal, request=self.request)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_overview_controlpanel_portal_padrao_version(self):
        u"""Validamos se temos a versão do Portal Padrão"""
        view = api.content.get_view(name='overview-controlpanel', context=self.portal, request=self.request)
        view = view.__of__(self.portal)
        content = view()
        self.assertIn('Portal Padrão 2.', content)