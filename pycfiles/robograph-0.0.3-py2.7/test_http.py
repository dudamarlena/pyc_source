# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/tests/test_http.py
# Compiled at: 2016-07-13 17:51:17
from robograph.datamodel.nodes.lib import http
QUERY = dict(pippo='1', pluto='ciao')
HEADERS = {'X-Custom': 'value'}
MIME_TYPE = 'application/json'
FORM_DATA = dict(a='x', b='y', c='z')

def test_get():
    url = 'https://httpbin.org/get'
    expected_reqs = ['url', 'headers', 'auth', 'timeout_secs', 'verify_ssl',
     'query', 'mime_type']
    instance = http.Get(url=url, query=QUERY, mime_type=MIME_TYPE, headers=HEADERS, verify_ssl=False)
    assert instance.requirements == expected_reqs
    result = instance.output()
    assert url in result['url']
    assert result['args'] == QUERY
    assert ('X-Custom', 'value') in result['headers'].items()


def test_post():
    url = 'https://httpbin.org/post'
    expected_reqs = ['url', 'headers', 'auth', 'timeout_secs', 'verify_ssl',
     'post_data', 'files', 'mime_type']
    instance = http.Post(url=url, mime_type=MIME_TYPE, headers=HEADERS, verify_ssl=False, post_data=FORM_DATA)
    assert instance.requirements == expected_reqs
    result = instance.output()
    assert result['form'] == FORM_DATA
    assert len(result['files']) == 0
    assert result['url'] == url
    assert ('X-Custom', 'value') in result['headers'].items()


def test_put():
    url = 'https://httpbin.org/put'
    expected_reqs = ['url', 'headers', 'auth', 'timeout_secs', 'verify_ssl',
     'put_data', 'mime_type']
    instance = http.Put(url=url, mime_type=MIME_TYPE, headers=HEADERS, verify_ssl=False, put_data=FORM_DATA)
    assert instance.requirements == expected_reqs
    result = instance.output()
    assert result['form'] == FORM_DATA
    assert result['url'] == url
    assert ('X-Custom', 'value') in result['headers'].items()


def test_delete():
    url = 'https://httpbin.org/put'
    expected_reqs = ['url', 'headers', 'auth', 'timeout_secs', 'verify_ssl',
     'delete_data', 'mime_type']
    instance = http.Delete(url=url, mime_type=MIME_TYPE, headers=HEADERS, verify_ssl=False, delete_data=FORM_DATA)
    assert instance.requirements == expected_reqs
    result = instance.output()
    assert result['form'] == FORM_DATA
    assert result['url'] == url
    assert ('X-Custom', 'value') in result['headers'].items()


def test_status_code():
    url = 'https://httpbin.org/status/418'
    expected_reqs = ['response']
    response = http.RawGet(url=url, verify_ssl=False).output()
    instance = http.StatusCode(response=response)
    assert instance.requirements == expected_reqs
    assert instance.output() == 418


def test_status_code_ok():
    url_ok = 'https://httpbin.org/status/200'
    url_ko = 'https://httpbin.org/status/418'
    expected_reqs = ['response']
    response_ok = http.RawGet(url=url_ok, verify_ssl=False).output()
    instance = http.StatusCodeOk(response=response_ok)
    assert instance.requirements == expected_reqs
    assert instance.output()
    response_ko = http.RawGet(url=url_ko, verify_ssl=False).output()
    instance = http.StatusCodeOk(response=response_ko)
    assert not instance.output()