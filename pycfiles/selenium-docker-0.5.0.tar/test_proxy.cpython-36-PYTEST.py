# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/blake/code/vivint-selenium-docker/tests/test_proxy.py
# Compiled at: 2017-11-06 12:42:57
# Size of source mod 2**32: 797 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from selenium_docker.proxy import AbstractProxy, SquidProxy

def test_abstract_proxy():
    proxy = AbstractProxy.make_proxy('none')
    if not proxy:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(proxy) if 'proxy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(proxy) else 'proxy'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    @py_assert1 = proxy.http_proxy
    @py_assert4 = 'none'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.http_proxy\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(proxy) if 'proxy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(proxy) else 'proxy',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = proxy.httpProxy
    @py_assert5 = proxy.http_proxy
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.httpProxy\n} == %(py6)s\n{%(py6)s = %(py4)s.http_proxy\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(proxy) if 'proxy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(proxy) else 'proxy',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(proxy) if 'proxy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(proxy) else 'proxy',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    proxy = AbstractProxy.make_proxy('localhost', 3128, 'https-localhost')
    if not proxy:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(proxy) if 'proxy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(proxy) else 'proxy'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    @py_assert1 = proxy.http_proxy
    @py_assert4 = 'localhost:3128'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.http_proxy\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(proxy) if 'proxy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(proxy) else 'proxy',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = proxy.ssl_proxy
    @py_assert4 = 'https-localhost'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.ssl_proxy\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(proxy) if 'proxy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(proxy) else 'proxy',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_proxy_container(factory):
    proxy = SquidProxy(factory=factory)
    if not proxy:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(proxy) if 'proxy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(proxy) else 'proxy'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    @py_assert1 = proxy.container
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.container\n}') % {'py0':@pytest_ar._saferepr(proxy) if 'proxy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(proxy) else 'proxy',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    @py_assert0 = 'squid3'
    @py_assert4 = proxy.name
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.name\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(proxy) if 'proxy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(proxy) else 'proxy',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'unittest'
    @py_assert4 = proxy.container
    @py_assert6 = @py_assert4.name
    @py_assert2 = @py_assert0 in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.container\n}.name\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(proxy) if 'proxy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(proxy) else 'proxy',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'running'
    @py_assert4 = proxy.container
    @py_assert6 = @py_assert4.status
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.container\n}.status\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(proxy) if 'proxy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(proxy) else 'proxy',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    proxy.quit()