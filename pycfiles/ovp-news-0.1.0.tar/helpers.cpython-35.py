# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-users/ovp_users/tests/helpers.py
# Compiled at: 2017-02-22 18:06:29
# Size of source mod 2**32: 1037 bytes
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

def create_user(email='validemail@gmail.com', password='validpassword'):
    data = {'name': 'Valid Name', 
     'email': email, 
     'password': password}
    client = APIClient()
    return client.post(reverse('user-list'), data, format='json')


def create_user_with_profile(email='validemail@gmail.com', password='validpassword', profile={}):
    data = {'name': 'Valid Name', 
     'email': email, 
     'password': password, 
     'profile': profile}
    client = APIClient()
    return client.post(reverse('user-list'), data, format='json')


def authenticate(email='test_can_login@test.com', password='validpassword'):
    data = {'email': email, 
     'password': password}
    client = APIClient()
    return client.post('/api-token-auth/', data, format='json')


def create_token(email='test@recovery.token'):
    data = {'email': email}
    client = APIClient()
    return client.post(reverse('recovery-token-list'), data, format='json')