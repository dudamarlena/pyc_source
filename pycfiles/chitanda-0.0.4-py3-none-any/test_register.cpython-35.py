# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/tests/unit/api/test_register.py
# Compiled at: 2018-09-19 12:39:14
# Size of source mod 2**32: 5348 bytes
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class RegisterTests(APITestCase):
    fixtures = [
     'users', 'course1', 'course1_users', 'course1_pa1']

    def test_register_single_student(self):
        user = User.objects.get(username='student1')
        self.client.force_authenticate(user=user)
        url = reverse('register', args=['cmsc40100', 'pa1'])
        post_data = {'students': ['student1', 'student2']}
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_full_team(self):
        user = User.objects.get(username='student1')
        self.client.force_authenticate(user=user)
        url = reverse('register', args=['cmsc40100', 'pa1'])
        post_data = {'students': ['student1', 'student2']}
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='student2')
        self.client.force_authenticate(user=user)
        post_data = {'students': ['student1', 'student2']}
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_full_team_redundant(self):
        user = User.objects.get(username='student1')
        self.client.force_authenticate(user=user)
        url = reverse('register', args=['cmsc40100', 'pa1'])
        post_data = {'students': ['student1', 'student2']}
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='student2')
        self.client.force_authenticate(user=user)
        post_data = {'students': ['student1', 'student2']}
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(username='student1')
        self.client.force_authenticate(user=user)
        url = reverse('register', args=['cmsc40100', 'pa1'])
        post_data = {'students': ['student1', 'student2']}
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_non_student(self):
        user = User.objects.get(username='instructor1')
        self.client.force_authenticate(user=user)
        url = reverse('register', args=['cmsc40100', 'pa1'])
        post_data = {'students': ['student1', 'student2']}
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class RegisterErrorTests(APITestCase):
    fixtures = [
     'users', 'course1', 'course1_users', 'course1_pa1']

    def test_register_other_students(self):
        user = User.objects.get(username='student1')
        self.client.force_authenticate(user=user)
        url = reverse('register', args=['cmsc40100', 'pa1'])
        post_data = {'students': ['student2', 'student3']}
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_student_in_other_class(self):
        user = User.objects.get(username='student1')
        self.client.force_authenticate(user=user)
        url = reverse('register', args=['cmsc40100', 'pa1'])
        post_data = {'students': ['student1', 'student5']}
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_wrong_number_of_students(self):
        user = User.objects.get(username='student1')
        self.client.force_authenticate(user=user)
        url = reverse('register', args=['cmsc40100', 'pa1'])
        post_data = {'students': ['student1', 'student2', 'student3']}
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RegisterExistingTeamErrorTests(APITestCase):
    fixtures = [
     'users', 'course1', 'course1_users', 'course1_pa1', 'course1_teams']

    def test_register_in_different_groups(self):
        user = User.objects.get(username='student1')
        self.client.force_authenticate(user=user)
        url = reverse('register', args=['cmsc40100', 'pa1'])
        post_data = {'students': ['student1', 'student2']}
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='student2')
        self.client.force_authenticate(user=user)
        post_data = {'students': ['student2', 'student3']}
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)