# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-odnoklassniki-api/odnoklassniki_api/tests.py
# Compiled at: 2016-02-11 11:23:36
from django.test import TestCase
from django.conf import settings
from social_api.api import override_api_context
import mock
from .api import api_call, OdnoklassnikiApi
GROUP_ID = 53038939046008
TOKEN = getattr(settings, 'SOCIAL_API_CALL_CONTEXT', {'odnoklassniki': {'token': None}})['odnoklassniki']['token']

class OdnoklassnikiApiTest(TestCase):

    def test_api_instance_singleton(self):
        self.assertEqual(id(OdnoklassnikiApi()), id(OdnoklassnikiApi()))

    def test_get_url_info(self):
        with override_api_context('odnoklassniki', token=TOKEN):
            response = api_call('url.getInfo', url='http://www.odnoklassniki.ru/apiok')
        self.assertEqual(response, {'objectId': GROUP_ID, 'type': 'GROUP'})

    @mock.patch('odnoklassniki.api.Odnoklassniki._request', side_effect=lambda *args, **kwargs: (200, {'error_data': None, 'error_code': 102, 'error_msg': 'PARAM_SESSION_EXPIRED : Session expired'}))
    @mock.patch('odnoklassniki_api.api.OdnoklassnikiApi.handle_error_code_102')
    def test_error_102(self, request, handle_error):
        api_call('url.getInfo', url='http://www.odnoklassniki.ru/apiok')
        self.assertTrue(handle_error.called)