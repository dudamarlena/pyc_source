# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/tests/unit/api/test_teams.py
# Compiled at: 2018-09-19 12:39:14
# Size of source mod 2**32: 1308 bytes
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from pprint import pprint
from chisubmit.backend.api.models import Course

class TeamTests(APITestCase):
    fixtures = [
     'users', 'course1', 'course1_users', 'course1_teams']

    def test_get_teams_as_admin(self):
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)
        url = reverse('team-list', args=['cmsc40100'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_teams_as_instructor(self):
        user = User.objects.get(username='instructor1')
        self.client.force_authenticate(user=user)
        url = reverse('team-list', args=['cmsc40100'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_teams_as_student(self):
        user = User.objects.get(username='instructor1')
        self.client.force_authenticate(user=user)
        url = reverse('team-list', args=['cmsc40100'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)