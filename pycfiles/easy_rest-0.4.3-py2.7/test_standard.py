# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/easyapi/tests/test_standard.py
# Compiled at: 2014-08-29 21:03:29
import json, pytest
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from easyapi.tests.factories import CompanyFactory, ProjectFactory, ManagerFactory
__author__ = 'mikhailturilin'

@pytest.mark.django_db
def test_foreign_keys_end_with_id(staff_api_client):
    company = CompanyFactory()
    projects = [ ProjectFactory(company=company) for i in range(3) ]
    response = staff_api_client.get('/api/project/')
    assert response.status_code == HTTP_200_OK
    response_data = json.loads(response.content)
    for proj_dict in response_data:
        assert 'company_id' in proj_dict
        assert proj_dict['company_id'] == company.id


@pytest.mark.django_db
def test_create_with_foreign_keys_end_with_id(staff_api_client):
    company = CompanyFactory()
    manager = ManagerFactory()
    response = staff_api_client.post('/api/project/', {'name': 'aaaa', 'company_id': company.id, 'manager_id': manager.id, 'start_date': '2014-05-19', 
       'scope': 'Company'})
    assert response.status_code == HTTP_201_CREATED
    response_data = json.loads(response.content)
    proj_dict = response_data
    assert 'company_id' in proj_dict
    assert proj_dict['company_id'] == company.id