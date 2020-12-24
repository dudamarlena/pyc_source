# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_catalogs.py
# Compiled at: 2018-10-07 05:33:45
# Size of source mod 2**32: 3341 bytes
import os, datetime, pytest, responses
from findwatt.catalogs import Catalog, Catalogs, CatalogSchema
from findwatt.exceptions import DoesNotExist, APIError
DUMMY_DATA = {'id':'dummy-catalog', 
 'name':'Dummy Catalog', 
 'creationDate':datetime.datetime.utcnow().isoformat(), 
 'activeVersions':2}

def test_make_catalog():
    catalog = CatalogSchema().load(DUMMY_DATA).data
    assert isinstance(catalog, Catalog)


def test_to_json():
    catalog = CatalogSchema().load(DUMMY_DATA).data
    assert isinstance(catalog.to_json(), str)


def test_to_dict():
    catalog = CatalogSchema().load(DUMMY_DATA).data
    assert isinstance(catalog.to_dict(), dict)


def test_catalogs_properties():
    api_key = 'dummy-api-key'
    url = 'https://api.testing.findwatt.com'
    catalogs = Catalogs(api_key, url)
    if not catalogs.auth_header == f"Bearer {api_key}":
        raise AssertionError
    elif not catalogs.url == os.path.join(url, 'catalogs'):
        raise AssertionError


@responses.activate
def test_catalogs_get():
    catalogs = Catalogs('dummy-api-key', 'http://api.testing.findwatt.com')
    responses.add((responses.GET),
      (os.path.join(catalogs.url, 'dummy-catalog')),
      json=DUMMY_DATA,
      status=200)
    catalog = catalogs.get('dummy-catalog')
    assert isinstance(catalog, Catalog)


@responses.activate
def test_get_nonexistent_catalog():
    catalogs = Catalogs('dummy-api-key', 'http://api.testing.findwatt.com')
    responses.add((responses.GET),
      (os.path.join(catalogs.url, 'nonexistent-catalog')),
      json={'message': 'Does not exist'},
      status=404)
    with pytest.raises(DoesNotExist) as (err):
        catalogs.get('nonexistent-catalog')
        assert err


@responses.activate
def test_get_catalog_failed():
    for error_code in (500, 502):
        catalogs = Catalogs('dummy-api-key', 'http://api.testing.findwatt.com')
        responses.add((responses.GET),
          (os.path.join(catalogs.url, 'dummy-catalog')),
          json={}, status=error_code)
        with pytest.raises(APIError) as (err):
            catalogs.get('dummy-catalog')
            assert err


@responses.activate
def test_catalogs_list():
    resource = Catalogs('dummy-api-key', 'http://api.testing.findwatt.com')
    responses.add((responses.GET),
      (resource.url), json=[DUMMY_DATA, DUMMY_DATA], status=200)
    catalogs = resource.search()
    if not isinstance(catalogs, list):
        raise AssertionError
    elif not all(isinstance(elem, Catalog) for elem in catalogs):
        raise AssertionError


@responses.activate
def test_catalogs_filter():
    resource = Catalogs('dummy-api-key', 'http://api.testing.findwatt.com')
    mocked_url = f"{resource.url}?name=Dummy%20Catalog&limit=0&offset=0"
    print(f"MOCKED_URL: {mocked_url}")
    responses.add((responses.GET), mocked_url, json=[DUMMY_DATA], status=200)
    catalogs = resource.search(name='Dummy Catalog')
    if not isinstance(catalogs, list):
        raise AssertionError
    elif not all(isinstance(elem, Catalog) for elem in catalogs):
        raise AssertionError


@responses.activate
def test_list_catalogs_error():
    for error_code in (500, 502):
        resource = Catalogs('dummy-api-key', 'http://api.testing.findwatt.com')
        responses.add((responses.GET), (resource.url), json={}, status=error_code)
        with pytest.raises(APIError) as (err):
            resource.search()
            assert err