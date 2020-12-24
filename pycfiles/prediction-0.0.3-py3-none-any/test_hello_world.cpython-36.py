# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/omri/code/prediction/scoring/tests/test_hello_world.py
# Compiled at: 2017-12-26 08:40:28
# Size of source mod 2**32: 854 bytes
"""
This module will hold our hello world api test
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class LeadsTest(APITestCase):

    def setUp(self):
        self.base_uri = reverse('hello-world')

    def test_get_hello_world_without_required_params(self):
        """
        Should return a 400 Bad request.
        """
        resp = self.client.get(path=(self.base_uri))
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_hello_world(self):
        """
        Should return a 200 OK.
        """
        query_params = {'hello':'hello', 
         'world':'world'}
        resp = self.client.get(path=(self.base_uri), data=query_params)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['hello'], 'world')