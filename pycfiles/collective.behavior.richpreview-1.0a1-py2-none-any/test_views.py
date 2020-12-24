# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/behavior.richpreview/src/collective/behavior/richpreview/tests/test_views.py
# Compiled at: 2018-04-05 17:11:05
from collective.behavior.richpreview.testing import INTEGRATION_TESTING
from plone import api
import json, unittest

class RichPreviewJsonViewTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.view = api.content.get_view('richpreview-json-view', self.portal, self.request)

    def test_view_no_url(self):
        self.view.setup()
        response = self.view()
        self.assertEqual(response, '')
        self.assertEqual(self.request.RESPONSE.getStatus(), 400)

    def test_view(self):
        self.request.form['url'] = 'http://www.plone.org'
        self.view.setup()
        expected = {'image': 'https://plone.org/logo.png', 
           'description': '', 
           'title': 'Plone CMS: Open Source Content Management'}
        response = self.view()
        content_type = response.getHeader('Content-Type')
        body = response.getBody()
        self.assertEqual(content_type, 'application/json')
        self.assertEqual(body, json.dumps(expected))