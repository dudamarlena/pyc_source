# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/easyapi/tests/test_reverse_relations.py
# Compiled at: 2014-07-20 14:15:27
import json, pytest
from easyapi.tests.factories import CompanyFactory, ProjectFactory
__author__ = 'mikhailturilin'

@pytest.skip
@pytest.mark.django_db
def test_model_property(staff_api_client):
    company = CompanyFactory()
    for i in range(3):
        ProjectFactory(company=company, budget=(i + 1) * 100)

    response = staff_api_client.get('/api/company/%d/projects' % company.pk)
    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert 'first_project' in response_data
    assert isinstance(response_data['first_project'], int)