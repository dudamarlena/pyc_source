# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/easyapi/tests/test_meta.py
# Compiled at: 2014-07-29 21:05:52
import json, pytest
from rest_framework.status import HTTP_200_OK
from easyapi.tests.factories import CompanyFactory, ProjectFactory
__author__ = 'mikhailturilin'

@pytest.mark.django_db
def test_meta(staff_api_client):
    company = CompanyFactory()
    link = '/api/company/%d/' % company.id
    response = staff_api_client.get(link)
    assert response.status_code == HTTP_200_OK
    response_data = json.loads(response.content)
    meta = {'app': 'test_project', 
       'model': 'company'}
    assert response_data['_meta'] == meta