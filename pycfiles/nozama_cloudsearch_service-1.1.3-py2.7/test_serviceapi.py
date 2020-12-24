# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/src/nozama-cloudsearch/nozama-cloudsearch-service/nozama/cloudsearch/service/tests/test_serviceapi.py
# Compiled at: 2013-12-03 06:00:21
"""
Tests to verify the REST interface of the nozama-cloudsearch-service.

Oisin Mulvihill
2013-08-22

"""
import pkg_resources

def test_service_is_running(test_server):
    """Test the service is running and the status it returns.
    """
    response = test_server.api.ping()
    pkg = pkg_resources.get_distribution('nozama-cloudsearch-service')
    assert response['status'] == 'ok'
    assert response['name'] == 'nozama-cloudsearch-service'
    assert response['version'] == pkg.version


def test_batch_document_upload_add(test_server):
    """Test the /documents/batch API.
    """
    test_server.api.remove_all()
    report = test_server.api.report()
    assert report['documents'] == []
    assert report['documents_removed'] == []
    doc = {'designer': '98', 
       'price': 1195, 
       'retailer': '', 
       'brand_id': [
                  7017], 
       'size': [], 'category': '', 
       'name': 'Pro Quad Clamp Purple', 
       'colour': [], 'brand': '98', 
       'created_at': 1376391294}
    example_sdf = [
     {'lang': 'en', 
        'fields': doc, 
        'version': 1376497963, 
        'type': 'add', 
        'id': 1246}]
    test_server.api.batch_upload(example_sdf)
    report = test_server.api.report()
    found = report['documents']
    assert len(found) == 1
    assert found[0]['id'] == '1246'
    assert found[0]['_id'] == '1246'
    assert found[0]['lang'] == 'en'
    assert 'type' not in found[0]
    assert found[0]['version'] == '1376497963'
    assert found[0]['fields']['name'] == 'Pro Quad Clamp Purple'
    test_server.api.remove_all()
    report = test_server.api.report()
    found = report['documents']
    assert len(found) == 0