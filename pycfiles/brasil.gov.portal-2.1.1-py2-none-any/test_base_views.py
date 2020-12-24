# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/tests/test_base_views.py
# Compiled at: 2018-10-18 17:35:14
from brasil.gov.portal.browser.plone.admin import Overview
from brasil.gov.portal.testing import FUNCTIONAL_TESTING
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser
import unittest

class OverviewViewFunctionalTestCase(unittest.TestCase):
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        self.request = self.layer['request']

    def test_overview_view(self):
        browser = Browser(self.layer['app'])
        browser.open(('{0}/plone-overview').format(self.app.absolute_url()))
        self.assertIn('<title>e-Government Digital Identity', browser.contents)


class OverviewViewIntegrationTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        self.request = self.layer['request']
        self.view = Overview(self.app, self.request)

    def test_overview_sites(self):
        sites = self.view.sites()
        self.assertEqual(len(sites), 1)
        self.assertEqual(sites[0], self.portal)

    def test_overview_can_manage(self):
        self.assertEqual(self.view.can_manage(), None)
        with api.env.adopt_roles(['Manager']):
            self.assertEqual(self.view.can_manage(), True)
        return

    def test_overview_upgrade_url(self):
        self.assertEqual(self.view.upgrade_url(self.portal), ('{0}/@@plone-root-login').format(self.app.absolute_url()))
        with api.env.adopt_roles(['Manager']):
            self.assertEqual(self.view.upgrade_url(self.portal), ('{0}/@@plone-upgrade').format(self.portal.absolute_url()))

    def test_overview_outdated(self):
        self.assertEqual(self.view.outdated(self.app), False)
        self.assertEqual(self.view.outdated(self.portal), False)


class AddSiteViewFunctionalTestCase(unittest.TestCase):
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        self.request = self.layer['request']

    def test_addsite_view(self):
        import base64
        browser = Browser(self.layer['app'])
        browser.handleErrors = False
        basic_auth = ('Basic {0}').format(base64.encodestring(('{0}:{1}').format(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)))
        browser.addHeader('Authorization', basic_auth)
        browser.open(('{0}/@@plone-addsite?site_id=site').format(self.app.absolute_url()))
        self.assertIn('"site"', browser.contents)
        self.assertIn('Name of Ministry or', browser.contents)