# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/tests/test_helper_view.py
# Compiled at: 2018-11-30 15:01:51
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
import base64, hashlib, unittest
FILENAME = 'box.png'
DATA = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x01\x03\x00\x00\x00%=m"\x00\x00\x00\x03PLTE\xf2\xf2\xf2d\x03\x8ak\x00\x00\x00\x0bIDAT\x08\xd7c \x11\x00\x00\x000\x00\x01ez\xd6|\x00\x00\x00\x00IEND\xaeB`\x82'
IMAGEB64 = ('filenameb64:{0};datab64:{1}').format(base64.b64encode(FILENAME), base64.b64encode(DATA))
CHECKSUM = hashlib.sha1(DATA).hexdigest()

class HelperViewTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    @staticmethod
    def set_image(value):
        from brasil.gov.portal.controlpanel.portal import ISettingsPortal
        name = ISettingsPortal.__identifier__ + '.background_image'
        api.portal.set_registry_record(name, value=value)

    def render(self):
        view = api.content.get_view('searchbox-background-media', self.portal, self.request)
        view()

    def test_headers_no_image(self):
        self.render()
        self.assertEqual(self.request.response.getStatus(), 410)

    def test_headers_no_match(self):
        self.set_image(IMAGEB64)
        self.render()
        headers = self.request.response.headers
        self.assertEqual(self.request.response.getStatus(), 200)
        self.assertEqual(headers['cache-control'], 'max-age=0, s-maxage=120')
        self.assertEqual(headers['etag'], CHECKSUM)

    def test_headers_match(self):
        self.set_image(IMAGEB64)
        self.request.environ['IF_NONE_MATCH'] = CHECKSUM
        self.render()
        headers = self.request.response.headers
        self.assertEqual(self.request.response.getStatus(), 304)
        self.assertEqual(headers['cache-control'], 'max-age=0, s-maxage=120')
        self.assertEqual(headers['etag'], CHECKSUM)