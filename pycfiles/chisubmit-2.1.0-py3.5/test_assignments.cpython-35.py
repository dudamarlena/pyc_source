# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/tests/unit/api/test_assignments.py
# Compiled at: 2018-09-19 12:39:14
# Size of source mod 2**32: 1450 bytes
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class AssignmentTests(APITestCase):
    fixtures = [
     'users', 'course1', 'course1_users', 'course1_pa1']

    def test_get_assignments(self):
        user = User.objects.get(username='instructor1')
        self.client.force_authenticate(user=user)
        url = reverse('assignment-list', args=['cmsc40100'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_assignment(self):
        user = User.objects.get(username='student1')
        self.client.force_authenticate(user=user)
        url = reverse('assignment-detail', args=['cmsc40100', 'pa1'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_assignment(self):
        user = User.objects.get(username='instructor1')
        self.client.force_authenticate(user=user)
        url = reverse('assignment-list', args=['cmsc40100'])
        post_data = {'assignment_id': 'pa3', 
         'name': 'Programming Assignment 3', 
         'deadline': '2042-02-04 20:00:00+00:00'}
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)