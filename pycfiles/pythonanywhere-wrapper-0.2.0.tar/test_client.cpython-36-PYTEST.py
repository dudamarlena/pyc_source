# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trevor/projects/pythonanywhere-wrapper/source/tests/test_client.py
# Compiled at: 2017-10-21 10:41:04
# Size of source mod 2**32: 7725 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, responses
from pythonanywhere_wrapper import API_ENDPOINT
from pythonanywhere_wrapper.client import PythonAnywhereError

class PythonAnywhereTestCase(object):
    API_ENDPOINT = API_ENDPOINT.format('testuser')

    def asserts(self, expected_url, method='GET', data=None):
        @py_assert2 = responses.calls
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.calls\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(responses) if 'responses' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(responses) else 'responses',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        call = responses.calls[0]
        @py_assert1 = call.response
        @py_assert3 = @py_assert1.url
        @py_assert7 = self.get_url
        @py_assert10 = @py_assert7(expected_url)
        @py_assert5 = @py_assert3 == @py_assert10
        if not @py_assert5:
            @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.response\n}.url\n} == %(py11)s\n{%(py11)s = %(py8)s\n{%(py8)s = %(py6)s.get_url\n}(%(py9)s)\n}', ), (@py_assert3, @py_assert10)) % {'py0':@pytest_ar._saferepr(call) if 'call' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(call) else 'call',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(self) if 'self' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(self) else 'self',  'py8':@pytest_ar._saferepr(@py_assert7),  'py9':@pytest_ar._saferepr(expected_url) if 'expected_url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_url) else 'expected_url',  'py11':@pytest_ar._saferepr(@py_assert10)}
            @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
            raise AssertionError(@pytest_ar._format_explanation(@py_format14))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert10 = None
        @py_assert1 = call.request
        @py_assert3 = @py_assert1.method
        @py_assert5 = @py_assert3 == method
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.request\n}.method\n} == %(py6)s', ), (@py_assert3, method)) % {'py0':@pytest_ar._saferepr(call) if 'call' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(call) else 'call',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(method) if 'method' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(method) else 'method'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        if data:
            for argument in data:
                @py_assert3 = call.response
                @py_assert5 = @py_assert3.request
                @py_assert7 = @py_assert5.body
                @py_assert1 = argument in @py_assert7
                if not @py_assert1:
                    @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.response\n}.request\n}.body\n}', ), (argument, @py_assert7)) % {'py0':@pytest_ar._saferepr(argument) if 'argument' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(argument) else 'argument',  'py2':@pytest_ar._saferepr(call) if 'call' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(call) else 'call',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
                    @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format11))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None

    def get_url(self, url):
        return self.API_ENDPOINT + url


class TestMakeRequest(PythonAnywhereTestCase):

    @responses.activate
    def test_make_request(self, api_client):
        responses.add(responses.GET, self.get_url('consoles/'))
        api_client.consoles()
        @py_assert2 = responses.calls
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.calls\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(responses) if 'responses' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(responses) else 'responses',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        call = responses.calls[0]
        headers = call.request.headers
        @py_assert0 = headers['Authorization']
        @py_assert3 = 'Token api_key'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = headers['User-Agent']
        @py_assert3 = 'PythonAnywhere Python Client'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert1 = call.response
        @py_assert3 = @py_assert1.ok
        @py_assert6 = True
        @py_assert5 = @py_assert3 is @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.response\n}.ok\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(call) if 'call' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(call) else 'call',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None

    @responses.activate
    def test_make_request_not_okay(self, api_client):
        responses.add((responses.GET), (self.get_url('console/')), status=404)
        with pytest.raises(PythonAnywhereError):
            api_client.console()


class TestConstructConsoles(PythonAnywhereTestCase):

    @responses.activate
    def test_consoles(self, api_client):
        url_path = 'consoles/'
        responses.add(responses.GET, self.get_url(url_path))
        api_client.consoles()
        self.asserts(url_path)

    @responses.activate
    def test_consoles_shared_with_you(self, api_client):
        url_path = 'consoles/shared_with_you/'
        responses.add(responses.GET, self.get_url(url_path))
        api_client.consoles.shared_with_you()
        self.asserts(url_path)

    @responses.activate
    def test_consoles_console_id(self, api_client):
        url_path = 'consoles/123/'
        responses.add(responses.GET, self.get_url(url_path))
        api_client.consoles(console_id=123)
        self.asserts(url_path)

    @responses.activate
    def test_consoles_delete_console_id(self, api_client):
        url_path = 'consoles/123/'
        responses.add(responses.DELETE, self.get_url(url_path))
        api_client.consoles.delete(console_id=123)
        self.asserts(url_path, 'DELETE')


class TestConstructFiles(PythonAnywhereTestCase):

    @responses.activate
    def test_files_create(self, api_client):
        url_path = 'files/sharing/'
        responses.add(responses.POST, self.get_url(url_path))
        api_client.files.sharing.create(data={'path': 'test/path'})
        self.asserts(url_path, 'POST', [
         'path=test%2Fpath'])

    @responses.activate
    def test_files_sharing(self, api_client):
        url_path = 'files/sharing/?path=test%2Fpath'
        responses.add(responses.GET, self.get_url(url_path))
        api_client.files.sharing(path='test/path')
        self.asserts(url_path)

    @responses.activate
    def test_files_sharing_delete(self, api_client):
        url_path = 'files/sharing/?path=test%2Fpath'
        responses.add(responses.DELETE, self.get_url(url_path))
        api_client.files.sharing.delete(path='test/path')
        self.asserts(url_path, 'DELETE')

    @responses.activate
    def test_files_tree(self, api_client):
        url_path = 'files/tree/?path=test%2Fpath'
        responses.add(responses.GET, self.get_url(url_path))
        api_client.files.tree(path='test/path')
        self.asserts(url_path)


class TestConstructWebapps(PythonAnywhereTestCase):

    @responses.activate
    def test_webapps(self, api_client):
        url_path = 'webapps/'
        responses.add(responses.GET, self.get_url(url_path))
        api_client.webapps()
        self.asserts(url_path)

    @responses.activate
    def test_webapps_create(self, api_client):
        url_path = 'webapps/'
        responses.add(responses.POST, self.get_url(url_path))
        api_client.webapps.create(data={'domain_name':'www.test.com', 
         'python_version':'python27'})
        self.asserts(url_path, 'POST', [
         'domain_name=www.test.com', 'python_version=python27'])

    @responses.activate
    def test_webapps_get_by_domain_name(self, api_client):
        url_path = 'webapps/test.com/'
        responses.add(responses.GET, self.get_url(url_path))
        api_client.webapps(domain_name='test.com')
        self.asserts(url_path)

    @responses.activate
    def test_webapps_update_by_domain_name(self, api_client):
        url_path = 'webapps/test.com/'
        responses.add(responses.PUT, self.get_url(url_path))
        api_client.webapps.update(domain_name='test.com',
          data={'python_version': 'python27'})
        self.asserts(url_path, 'PUT', ['python_version=python27'])

    @responses.activate
    def test_webapps_delete_by_domain_name(self, api_client):
        url_path = 'webapps/test.com/'
        responses.add(responses.DELETE, self.get_url(url_path))
        api_client.webapps.delete(domain_name='test.com')
        self.asserts(url_path, 'DELETE')

    @responses.activate
    def test_webapps_reload(self, api_client):
        url_path = 'webapps/test.com/reload/'
        responses.add(responses.POST, self.get_url(url_path))
        api_client.webapps.reload(domain_name='test.com')
        self.asserts(url_path, 'POST')


class TestConstructWebappsStaicFiles(PythonAnywhereTestCase):

    @responses.activate
    def test_webapps_static_files(self, api_client):
        url_path = 'webapps/test.com/static_files/'
        responses.add(responses.GET, self.get_url(url_path))
        api_client.webapps.static_files(domain_name='test.com')
        self.asserts(url_path)

    @responses.activate
    def test_webapps_static_files_create(self, api_client):
        url_path = 'webapps/test.com/static_files/'
        responses.add(responses.POST, self.get_url(url_path))
        api_client.webapps.static_files.create(domain_name='test.com',
          data={'url':'/static/', 
         'path':'/test/path/'})
        self.asserts(url_path, 'POST', ['url=%2Fstatic%2F', 'path=%2Ftest%2Fpath%2F'])

    @responses.activate
    def test_webapps_static_files_get_by_static_id(self, api_client):
        url_path = 'webapps/test.com/static_files/123/'
        responses.add(responses.GET, self.get_url(url_path))
        api_client.webapps.static_files(domain_name='test.com',
          static_id=123)
        self.asserts(url_path)

    @responses.activate
    def test_webapps_static_files_update_by_static_id(self, api_client):
        url_path = 'webapps/test.com/static_files/123/'
        responses.add(responses.PUT, self.get_url(url_path))
        api_client.webapps.static_files.update(domain_name='test.com',
          static_id=123,
          data={'url':'/static/', 
         'path':'/test/path/'})
        self.asserts(url_path, 'PUT', ['url=%2Fstatic%2F', 'path=%2Ftest%2Fpath%2F'])

    @responses.activate
    def test_webapps_static_files_delete_by_static_id(self, api_client):
        url_path = 'webapps/test.com/static_files/123/'
        responses.add(responses.DELETE, self.get_url(url_path))
        api_client.webapps.static_files.delete(domain_name='test.com',
          static_id=123)
        self.asserts(url_path, 'DELETE')