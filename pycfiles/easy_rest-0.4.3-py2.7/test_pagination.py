# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/easyapi/tests/test_pagination.py
# Compiled at: 2014-08-13 22:20:59
__author__ = 'mikhailturilin'
import json, pytest
from easyapi.tests.factories import CompanyFactory

@pytest.mark.django_db
def test_list_endpoint(staff_api_client):
    for i in range(37):
        CompanyFactory()

    response = staff_api_client.get('/custom-api/company-paginator/')
    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data['count'] == 37
    assert response_data['num_pages'] == 8
    assert response_data['number'] == 1
    results = response_data['results']
    company = results[0]
    assert company['name']
    assert company['category_id']
    assert company['company_type']
    assert company['country']
    assert company['_meta']['app'] == 'test_project'
    assert company['_meta']['model'] == 'company'