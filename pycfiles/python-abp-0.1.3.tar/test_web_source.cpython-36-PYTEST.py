# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vkuznetsov/prog/devops/python-abp/tests/test_web_source.py
# Compiled at: 2019-05-13 06:18:18
# Size of source mod 2**32: 2648 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, mock
try:
    from StringIO import StringIO
    from urllib2 import HTTPError
except ImportError:
    from io import BytesIO as StringIO
    from urllib.error import HTTPError

from abp.filters.sources import WebSource, NotFound

@pytest.fixture
def web_mock(request):
    """Replace urlopen with our test implementation."""
    patcher = mock.patch('abp.filters.sources.urlopen')
    ret = patcher.start()
    request.addfinalizer(patcher.stop)
    return ret


@pytest.fixture
def http_source():
    return WebSource('http')


def response_mock(encoding, data):
    """Make a fake response with specific encoding and content."""
    resp = StringIO(data)
    info = mock.Mock()
    info.get_param = mock.Mock(return_value=encoding)
    resp.info = mock.Mock(return_value=info)
    return resp


def test_fetch_file(web_mock, http_source):
    web_mock.return_value = response_mock(None, b'! Line 1\n! Line 2')
    @py_assert2 = http_source.get
    @py_assert4 = '//foo/bar.txt'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = list(@py_assert6)
    @py_assert11 = [
     '! Line 1', '! Line 2']
    @py_assert10 = @py_assert8 == @py_assert11
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_web_source.py', lineno=56)
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.get\n}(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(http_source) if 'http_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(http_source) else 'http_source',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_charset_handling(web_mock, http_source):
    web_mock.return_value = response_mock('latin-1', b'\xfc')
    @py_assert2 = http_source.get
    @py_assert4 = '//foo/bar.txt'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = list(@py_assert6)
    @py_assert11 = [
     'ü']
    @py_assert10 = @py_assert8 == @py_assert11
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_web_source.py', lineno=61)
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.get\n}(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(http_source) if 'http_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(http_source) else 'http_source',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    web_mock.return_value = response_mock('utf-8', b'\xc3\xbc')
    @py_assert2 = http_source.get
    @py_assert4 = '//foo/bar.txt'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = list(@py_assert6)
    @py_assert11 = [
     'ü']
    @py_assert10 = @py_assert8 == @py_assert11
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_web_source.py', lineno=63)
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.get\n}(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(http_source) if 'http_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(http_source) else 'http_source',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    web_mock.return_value = response_mock(None, b'\xc3\xbc')
    @py_assert2 = http_source.get
    @py_assert4 = '//foo/bar.txt'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = list(@py_assert6)
    @py_assert11 = [
     'ü']
    @py_assert10 = @py_assert8 == @py_assert11
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_web_source.py', lineno=65)
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.get\n}(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(http_source) if 'http_source' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(http_source) else 'http_source',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_404(web_mock, http_source):
    web_mock.side_effect = HTTPError('', 404, 'Not found', [], StringIO(b''))
    with pytest.raises(NotFound):
        list(http_source.get('//foo/bar.txt'))


def test_500(web_mock, http_source):
    web_mock.side_effect = HTTPError('', 500, 'Internal Server Error', [], StringIO(b''))
    with pytest.raises(HTTPError):
        list(http_source.get('//foo/bar.txt'))