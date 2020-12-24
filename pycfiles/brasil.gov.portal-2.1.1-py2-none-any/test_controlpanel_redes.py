# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/tests/test_controlpanel_redes.py
# Compiled at: 2018-06-11 09:46:52
from brasil.gov.portal.controlpanel import socialnetworks
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
import unittest

class ControlPanelTest(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.adapter = socialnetworks.SocialNetworksPanelAdapter(self.portal)

    def test_controlpanel_view(self):
        """ Validamos se o control panel esta acessivel """
        view = api.content.get_view(name='brasil.gov.portal-social', context=self.portal, request=self.portal.REQUEST)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_protected(self):
        """ Acesso a view nao pode ser feito por usuario anonimo """
        from AccessControl import Unauthorized
        with api.env.adopt_roles(['Anonymous']):
            self.assertRaises(Unauthorized, self.portal.restrictedTraverse, '@@brasil.gov.portal-social')

    def test_configlet_install(self):
        """ Validamos se o control panel foi registrado """
        controlpanel = api.portal.get_tool('portal_controlpanel')
        installed = [ a.getAction(self)['id'] for a in controlpanel.listActions()
                    ]
        self.assertTrue('social-config' in installed)

    def test_site_accounts(self):
        adapter = self.adapter
        adapter.accounts_info = []
        self.assertEqual(len(adapter.accounts_info), 0)
        info = socialnetworks.SocialNetworksPair
        twitter = info(site='twitter', info='plone')
        adapter.accounts_info = [twitter]
        self.assertEqual(len(adapter.accounts_info), 1)
        self.assertEqual(adapter.accounts_info[0].site, 'twitter')