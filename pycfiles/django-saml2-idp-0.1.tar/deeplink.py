# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/abhinav/Dev/saml.py/django-saml2-idp/tests/deeplink.py
# Compiled at: 2013-12-12 09:30:47
"""
Tests for the demo AttributeProcessor and IdP-initiated deep-linking.
"""
import base64, base

class TestDeepLink(base.SamlTestCase):
    SP_CONFIG = {'acs_url': 'http://127.0.0.1:9000/sp/acs/', 
       'processor': 'saml2idp.demo.Processor', 
       'links': {'deeplink': 'http://127.0.0.1:9000/sp/%s/'}}
    DEEPLINK = 'http://127.0.0.1:8000/idp/init/deeplink/test/'
    EXPECTED_RELAY_STATE = 'http://127.0.0.1:9000/sp/test/'

    def test_deeplink(self):
        self._hit_saml_view(self.DEEPLINK)
        relaystate = self._html_soup.findAll('input', {'name': 'RelayState'})[0]
        self.assertEqual(self.EXPECTED_RELAY_STATE, relaystate['value'])


class TestDeepLinkWithAttributes(TestDeepLink):
    SP_CONFIG = {'acs_url': 'http://127.0.0.1:9000/sp/acs/', 
       'processor': 'saml2idp.demo.AttributeProcessor', 
       'links': {'attr': 'http://127.0.0.1:9000/sp/%s/'}}
    DEEPLINK = 'http://127.0.0.1:8000/idp/init/attr/test/'
    EXPECTED_RELAY_STATE = 'http://127.0.0.1:9000/sp/test/'

    def test_deeplink(self):
        super(TestDeepLinkWithAttributes, self).test_deeplink()
        attributes = self._saml_soup.findAll('saml:attribute')
        self.assertEqual(len(attributes), 1)
        self.assertEqual(attributes[0]['name'], 'foo')
        value = attributes[0].findAll('saml:attributevalue')[0]
        self.assertEqual(value.text, 'bar')