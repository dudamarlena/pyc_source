# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/easyapi/tests/generate_data.py
# Compiled at: 2014-08-13 20:09:45
import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import pytest
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APIClient
from easyapi.tests.factories import CompanyFactory, ProjectFactory
from easyapi.tests.test_project.models import Company, Project
__author__ = 'mikhailturilin'

def staff_api_client():
    credentials = dict(username='ccc', password='ddd')
    try:
        User.objects.get(username=credentials['username'])
    except:
        User.objects.create_superuser(email='njnjn@njn.com', **credentials)

    client = APIClient()
    client.login(**credentials)
    return client


Company.objects.all().delete()
Project.objects.all().delete()
company = CompanyFactory()
companies = [ CompanyFactory() for i in range(4) ]
projects = [ ProjectFactory(company=company) for i in range(3) ]
response = staff_api_client().get('/api/company/')
assert response.status_code == HTTP_200_OK
response_data = json.loads(response.content)
print response.content