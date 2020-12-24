# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/tests/test_middlewares.py
# Compiled at: 2017-07-04 10:20:34
# Size of source mod 2**32: 1558 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, base64, pytest
from flask.wrappers import Response
from flask.ext.restframework.authentication_backend import SimpleBasicAuth
from flask.ext.restframework.middlewares import AuthenticationMiddleware
from flask.ext.restframework.tests.compat import mock

@pytest.mark.test_auth_middleware_with_basic_auth
def test_auth_middleware_with_basic_auth():
    am = AuthenticationMiddleware(mock.Mock(config={'BASIC_AUTH_LOGIN': '1', 
     'BASIC_AUTH_PASSWORD': '1'}))
    with mock.patch.object(AuthenticationMiddleware, 'get_view') as (m):
        m.return_value = mock.Mock(authentication_backends=[
         SimpleBasicAuth])
        with mock.patch('flask.globals.request') as (m):
            response = am.before_request()
        @py_assert0 = response.headers['WWW-Authenticate']
        @py_assert3 = 'Basic realm="User Visible Realm"'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert1 = response.status_code
        @py_assert4 = 401
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        with mock.patch('flask.globals.request', mock.Mock(authorization=mock.Mock(username='1', password='2'))):
            response = am.before_request()
            @py_assert0 = response.headers['WWW-Authenticate']
            @py_assert3 = 'Basic realm="User Visible Realm"'
            @py_assert2 = @py_assert0 == @py_assert3
            if not @py_assert2:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None
            @py_assert1 = response.status_code
            @py_assert4 = 401
            @py_assert3 = @py_assert1 == @py_assert4
            if not @py_assert3:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status_code\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert1 = @py_assert3 = @py_assert4 = None
        with mock.patch('flask.globals.request', mock.Mock(authorization=mock.Mock(username='1', password='1'))):
            response = am.before_request()
            @py_assert2 = None
            @py_assert1 = response == @py_assert2
            if not @py_assert1:
                @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (response, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(response) if 'response' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(response) else 'response'}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert2 = None