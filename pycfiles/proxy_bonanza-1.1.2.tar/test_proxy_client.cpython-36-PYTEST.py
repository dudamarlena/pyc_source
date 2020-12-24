# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/victormartinez/Workspace/python/python_proxy_bonanza/tests/test_proxy_client.py
# Compiled at: 2017-06-02 17:49:03
# Size of source mod 2**32: 12285 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from mock import MagicMock
from requests.models import Response, HTTPError
from proxy_bonanza.client import ProxyBonanzaClient

@pytest.fixture
def response_content():
    return '{"success":true,"data":{"id":48788,"login":"fakelogin","password":"qwerty123","expires":"2017-10-31T00:00:00+0000","bandwidth":1492664315943,"last_ip_change":"2016-08-23T00:00:00+0000","ippacks":[{"id":19316,"ip":"123.45.678.910","port_http":60099,"port_socks":61336,"active":true,"modified":"2016-05-22T06:44:24+0000","proxyserver":{"georegion_id":13,"georegion":{"name":"Sao Paulo","country":{"id":15,"isocode":"BR","name":"Brazil","flag_image":"br.gif","continent":"southamerica","eunion":false,"vat_rate":null}}}},{"id":19396,"ip":"321.45.876.999","port_http":60099,"port_socks":61336,"active":true,"modified":"2016-05-22T06:44:24+0000","proxyserver":{"georegion_id":13,"georegion":{"name":"Sao Paulo","country":{"id":15,"isocode":"BR","name":"Brazil","flag_image":"br.gif","continent":"southamerica","eunion":false,"vat_rate":null}}}}],"authips":[],"package":{"parent_id":null,"name":"International","bandwidth":10737418240,"price":36,"howmany_ips":10,"price_per_gig":1.5,"package_type":"geo","created":null,"modified":null}}}'


@pytest.fixture
def get_data_from_userpackage_id():
    return {'authips':[],  'bandwidth':1492664315943, 
     'expires':'2017-10-31T00:00:00+0000', 
     'id':48788, 
     'ippacks':[
      {'active':True, 
       'id':19316, 
       'ip':'123.45.678.910', 
       'modified':'2016-05-22T06:44:24+0000', 
       'port_http':60099, 
       'port_socks':61336, 
       'proxyserver':{'georegion':{'country':{'continent':'southamerica', 
          'eunion':False, 
          'flag_image':'br.gif', 
          'id':15, 
          'isocode':'BR', 
          'name':'Brazil', 
          'vat_rate':None}, 
         'name':'Sao Paulo'}, 
        'georegion_id':13}},
      {'active':True, 
       'id':19396, 
       'ip':'321.45.876.999', 
       'modified':'2016-05-22T06:44:24+0000', 
       'port_http':60099, 
       'port_socks':61336, 
       'proxyserver':{'georegion':{'country':{'continent':'southamerica', 
          'eunion':False, 
          'flag_image':'br.gif', 
          'id':15, 
          'isocode':'BR', 
          'name':'Brazil', 
          'vat_rate':None}, 
         'name':'Sao Paulo'}, 
        'georegion_id':13}}], 
     'last_ip_change':'2016-08-23T00:00:00+0000', 
     'login':'fakelogin', 
     'package':{'bandwidth':10737418240, 
      'created':None, 
      'howmany_ips':10, 
      'modified':None, 
      'name':'International', 
      'package_type':'geo', 
      'parent_id':None, 
      'price':36, 
      'price_per_gig':1.5}, 
     'password':'qwerty123'}


@pytest.fixture
def get_data_from_api():
    return [
     {'bandwidth':34192444911,  'expires':'2015-02-06T00:00:00+0000', 
      'id':212121, 
      'last_ip_change':'2014-11-10T00:00:00+0000', 
      'login':'fakelogin', 
      'package':{'bandwidth':10737418240, 
       'howmany_ips':1, 
       'name':'Special 3', 
       'package_type':'exclusive', 
       'price':5, 
       'price_per_gig':1}, 
      'password':'qwerty123'},
     {'bandwidth':3433019582, 
      'expires':'2015-01-01T00:00:00+0000', 
      'id':31313131, 
      'last_ip_change':'2014-07-28T00:00:00+0000', 
      'login':'fakelogin', 
      'package':{'bandwidth':2147483648, 
       'howmany_ips':2, 
       'name':'International', 
       'package_type':'geo', 
       'price':12, 
       'price_per_gig':2}, 
      'password':'fakelogin'}]


def test_error_when_api_key_is_not_provided():
    with pytest.raises(RuntimeError):
        ProxyBonanzaClient()


def test_getting_user_package_ids(monkeypatch, get_data_from_api):
    monkeypatch.setattr('proxy_bonanza.client.ProxyBonanzaClient._get_api_data', MagicMock(return_value=get_data_from_api))
    client = ProxyBonanzaClient(api_key='fake123api')
    ids = client.get_user_package_ids()
    @py_assert2 = [212121, 31313131]
    @py_assert1 = ids == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (ids, @py_assert2)) % {'py0':@pytest_ar._saferepr(ids) if 'ids' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ids) else 'ids',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_getting_proxies(monkeypatch, get_data_from_userpackage_id):
    monkeypatch.setattr('proxy_bonanza.client.ProxyBonanzaClient._get_api_data', MagicMock(return_value=get_data_from_userpackage_id))
    client = ProxyBonanzaClient(api_key='fake123api')
    proxies = client.get_proxies(212121)
    @py_assert2 = [{'active':True,  'id':19316,  'ip':'123.45.678.910',  'modified':'2016-05-22T06:44:24+0000',  'port_http':60099,  'port_socks':61336,  'proxyserver':{'georegion':{'country':{'continent':'southamerica',  'eunion':False,  'flag_image':'br.gif',  'id':15,  'isocode':'BR',  'name':'Brazil',  'vat_rate':None},  'name':'Sao Paulo'},  'georegion_id':13},  'login':'fakelogin',  'password':'qwerty123'}, {'active':True,  'id':19396,  'ip':'321.45.876.999',  'modified':'2016-05-22T06:44:24+0000',  'port_http':60099,  'port_socks':61336,  'proxyserver':{'georegion':{'country':{'continent':'southamerica',  'eunion':False,  'flag_image':'br.gif',  'id':15,  'isocode':'BR',  'name':'Brazil',  'vat_rate':None},  'name':'Sao Paulo'},  'georegion_id':13},  'login':'fakelogin',  'password':'qwerty123'}]
    @py_assert1 = proxies == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (proxies, @py_assert2)) % {'py0':@pytest_ar._saferepr(proxies) if 'proxies' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(proxies) else 'proxies',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_getting_data_with_bad_response(monkeypatch):
    response = Response()
    response.status_code = 401
    monkeypatch.setattr('requests.get', MagicMock(return_value=response))
    client = ProxyBonanzaClient(api_key='fake123api')
    with pytest.raises(HTTPError):
        client._get_api_data('www.abc.com.br')


def test_getting_data_with_successful_response(monkeypatch, response_content):
    response = Response()
    response.status_code = 202
    response._content = response_content
    monkeypatch.setattr('requests.get', MagicMock(return_value=response))
    client = ProxyBonanzaClient(api_key='fake123api')
    data = client._get_api_data('www.abc.com.br')
    @py_assert2 = {'authips':[],  'bandwidth':1492664315943,  'expires':'2017-10-31T00:00:00+0000',  'id':48788,  'ippacks':[{'active':True,  'id':19316,  'ip':'123.45.678.910',  'modified':'2016-05-22T06:44:24+0000',  'port_http':60099,  'port_socks':61336,  'proxyserver':{'georegion':{'country':{'continent':'southamerica',  'eunion':False,  'flag_image':'br.gif',  'id':15,  'isocode':'BR',  'name':'Brazil',  'vat_rate':None},  'name':'Sao Paulo'},  'georegion_id':13}}, {'active':True,  'id':19396,  'ip':'321.45.876.999',  'modified':'2016-05-22T06:44:24+0000',  'port_http':60099,  'port_socks':61336,  'proxyserver':{'georegion':{'country':{'continent':'southamerica',  'eunion':False,  'flag_image':'br.gif',  'id':15,  'isocode':'BR',  'name':'Brazil',  'vat_rate':None},  'name':'Sao Paulo'},  'georegion_id':13}}],  'last_ip_change':'2016-08-23T00:00:00+0000',  'login':'fakelogin',  'package':{'bandwidth':10737418240,  'created':None,  'howmany_ips':10,  'modified':None,  'name':'International',  'package_type':'geo',  'parent_id':None,  'price':36,  'price_per_gig':1.5},  'password':'qwerty123'}
    @py_assert1 = data == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (data, @py_assert2)) % {'py0':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None