# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/tests/test_resultsfilter_view.py
# Compiled at: 2018-10-18 17:35:14
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
import unittest

class ResultsFilterViewTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        with api.env.adopt_roles(['Manager']):
            self.collection = api.content.create(self.portal, 'Collection', 'collection')
        self.view = self.collection.restrictedTraverse('filtro-de-resultados')

    def test_action(self):
        action = 'filtro-de-resultados'
        self.collection.setLayout(action)
        self.assertEqual(self.collection.getLayout(), action)

    def test_portlets_disabled(self):
        self.view.setup()
        self.assertIn('disable_plone.leftcolumn', self.request)
        self.assertIn('disable_plone.rightcolumn', self.request)

    def test_greenbar_authenticated(self):
        self.view.setup()
        self.assertNotIn('disable_border', self.request)

    def test_greenbar_anonymous(self):
        from plone.app.testing import logout
        logout()
        view = self.collection.unrestrictedTraverse('filtro-de-resultados')
        view.setup()
        self.assertIn('disable_border', self.request)