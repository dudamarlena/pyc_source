# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/tests/unit/api/test_grade.py
# Compiled at: 2018-09-19 12:39:14
# Size of source mod 2**32: 811 bytes
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class GradeTests(APITestCase):
    fixtures = [
     'users', 'course1', 'course1_users', 'course1_teams',
     'course1_pa1', 'course1_pa1_registrations']

    def test_create_grade(self):
        user = User.objects.get(username='instructor1')
        self.client.force_authenticate(user=user)
        url = reverse('grade-list', args=['cmsc40100', 'student1-student2', 'pa1'])
        post_data = {'rubric_component_id': 1, 
         'points': 30}
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)