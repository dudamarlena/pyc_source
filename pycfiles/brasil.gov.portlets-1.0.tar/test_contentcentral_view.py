# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/tests/test_contentcentral_view.py
# Compiled at: 2018-10-18 17:35:14
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
import unittest

class ContentCentralViewTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(self.portal, 'Folder', 'folder')
        self.view = self.folder.restrictedTraverse('centrais-de-conteudo')

    def test_action(self):
        action = 'centrais-de-conteudo'
        self.folder.setLayout(action)
        self.assertEqual(self.folder.getLayout(), action)

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
        view = self.folder.unrestrictedTraverse('centrais-de-conteudo')
        view.setup()
        self.assertIn('disable_border', self.request)

    def test_filter_types(self):
        self.assertEqual(self.view.filter_types([]), [
         'sc.embedder', 'Image', 'Audio', 'Infographic'])
        self.assertEqual(self.view.filter_types(['Image']), ['Image'])
        self.assertEqual(self.view.filter_types(['File']), [])

    def test_media(self):
        from collections import OrderedDict
        self.assertEqual(self.view.media(), OrderedDict())
        api.content.create(self.folder, 'Image', 'foo')
        api.content.create(self.folder, 'File', 'bar')
        self.assertEqual(self.view.media(), OrderedDict([('Image', 'Image')]))
        api.content.create(self.folder, 'Audio', 'baz')
        self.assertEqual(self.view.media(), OrderedDict([('Image', 'Image'), ('Audio', 'Audio')]))