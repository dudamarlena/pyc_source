# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/omer/Projects/DjangoProjects/basitapi/basitapi/tests/response_tests.py
# Compiled at: 2013-04-25 13:58:27
from django.test import TestCase
from basitapi.response import ApiResponse
from basitapi.exception import ApiException

class ResponseTest(TestCase):

    def test_error_codes(self):
        self.assertEquals(200, ApiResponse.okay().status)
        self.assertEquals(201, ApiResponse.created().status)
        self.assertEquals(202, ApiResponse.accepted().status)
        self.assertEquals(400, ApiResponse.bad_request().status)
        self.assertEquals(401, ApiResponse.unauthorized().status)
        self.assertEquals(402, ApiResponse.payment_required().status)
        self.assertEquals(403, ApiResponse.forbidden().status)
        self.assertEquals(404, ApiResponse.not_found().status)
        self.assertEquals(405, ApiResponse.method_not_allowed().status)

    def test_init(self):
        response = ApiResponse(content={'data': 1}, status=200)
        self.assertIsInstance(response.content, dict)
        self.assertEquals(response.to_object().data, 1)
        self.assertEqual(response.status, 200)

    def test_to_json(self):
        response = ApiResponse(content={'data': 1}, status=200)
        self.assertEqual(response.to_json(), '{"data": 1}')

    def test_to_object(self):
        response = ApiResponse(content={'data': 1}, status=200)
        self.assertEqual(response.to_object().data, 1)