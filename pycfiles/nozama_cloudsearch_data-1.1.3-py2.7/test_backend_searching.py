# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nozama/cloudsearch/data/tests/test_backend_searching.py
# Compiled at: 2013-12-03 06:00:21
"""
"""
from nozama.cloudsearch.data import document

def test_search_with_no_content(logger, mongodb, elastic):
    """Test search an empty system doesn't raise exceptions.
    """
    assert document.all() == []
    results = document.search()
    assert results['hits']['found'] == 0


def test_basic_search(logger, mongodb, elastic):
    """Test searching the documents stored in mongodb.
    """
    assert document.all() == []
    doc = {'designer': 'GearPro', 
       'price': 12.6, 
       'retailer': 'MyShoppe', 
       'brand_id': [
                  7017], 
       'size': [], 'category': '', 
       'name': 'Pro Quad Clamp Purple', 
       'colour': [], 'brand': '98', 
       'created_at': 1376391294}
    doc2 = {'designer': 'GearPro', 
       'price': 12.6, 
       'retailer': 'MyShoppe', 
       'brand_id': [
                  7016], 
       'size': [], 'category': '', 
       'name': 'Bike Pump Purple', 
       'colour': [], 'brand': '98', 
       'created_at': 1376391294}
    example_sdf = [
     {'lang': 'en', 
        'fields': doc, 
        'version': 1376497963, 
        'type': 'add', 
        'id': 1246},
     {'lang': 'en', 
        'fields': doc2, 
        'version': 1376497963, 
        'type': 'add', 
        'id': 1247}]
    rc = document.load(example_sdf)
    assert rc['status'] == 'ok'
    assert rc['adds'] == 2
    results = document.search()
    assert results['hits']['found'] == 2
    c = [{'id': '1247'}, {'id': '1246'}]
    c.sort()
    results['hits']['hit'].sort()
    assert results['hits']['hit'] == c
    query = dict(q='pro')
    results = document.search(query)
    assert results['hits']['found'] == 1
    assert results['hits']['hit'] == [{'id': '1246'}]
    query = dict(q='myshop')
    results = document.search(query)
    assert results['hits']['found'] == 2
    c.sort()
    results['hits']['hit'].sort()
    assert results['hits']['hit'] == c
    query = dict(q='not in any string')
    results = document.search(query)
    assert results['hits']['found'] == 0