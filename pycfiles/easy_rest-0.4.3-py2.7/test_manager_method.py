# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/easyapi/tests/test_manager_method.py
# Compiled at: 2015-05-27 18:59:53
import json
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from easyapi.tests.factories import CompanyFactory, ProjectFactory
__author__ = 'mikhailturilin'
import pytest

@pytest.mark.django_db
def test_manager_method(staff_api_client):
    country = 'Prussia'
    for i in range(3):
        CompanyFactory(country=country)

    for i in range(6):
        CompanyFactory()

    response = staff_api_client.get('/api/company-manager/select_by_country/', data={'country': country})
    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert len(response_data) == 3


@pytest.mark.django_db
def test_manager_method_embedded(staff_api_client):
    country = 'Prussia'
    for i in range(3):
        c = CompanyFactory(country=country)
        for j in range(4):
            ProjectFactory(company=c)

    for i in range(6):
        CompanyFactory()

    response = staff_api_client.get('/api/company-manager/select_by_country/', data={'country': country, '_embedded': 'projects'})
    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert len(response_data) == 3
    assert len(response_data[0]['_embedded']['projects']) == 4


@pytest.mark.django_db
def test_manager_method_embedded_default(staff_api_client):
    project = ProjectFactory()
    response = staff_api_client.get('/auto-list/test_project/manager-manager/by_id/?id=%d' % project.manager.id)
    assert response.status_code == HTTP_200_OK
    response_data = json.loads(response.content)
    assert len(response_data['_embedded']['projects']) == 1


@pytest.mark.django_db
def test_manager_method_detect_required(staff_api_client):
    response = staff_api_client.get('/auto-list/test_project/manager-manager/plus/?a=1')
    assert response.status_code == HTTP_400_BAD_REQUEST
    response_data = json.loads(response.content)
    assert 'Param "b" is required' == response_data['detail']