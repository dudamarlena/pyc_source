# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gwik/dev/geventhttpclient/src/geventhttpclient/tests/test_url.py
# Compiled at: 2016-07-05 05:26:31
# Size of source mod 2**32: 3896 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, six
from geventhttpclient.url import URL
url_full = 'http://getgauss.com/subdir/file.py?param=value&other=true#frag'
url_path_only = '/path/to/something?param=value&other=true'

def test_simple_url():
    url = URL(url_full)
    @py_assert1 = url.path
    @py_assert4 = '/subdir/file.py'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.path\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = url.host
    @py_assert4 = 'getgauss.com'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.host\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = url.port
    @py_assert4 = 80
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.port\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = url['param']
    @py_assert3 = 'value'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = url['other']
    @py_assert3 = 'true'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert1 = url.fragment
    @py_assert4 = 'frag'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.fragment\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_path_only():
    url = URL(url_path_only)
    @py_assert1 = url.host
    @py_assert4 = ''
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.host\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = url.port
    @py_assert4 = None
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.port\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = url.path
    @py_assert4 = '/path/to/something'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.path\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = url['param']
    @py_assert3 = 'value'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = url['other']
    @py_assert3 = 'true'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_empty():
    url = URL()
    @py_assert1 = url.host
    @py_assert4 = ''
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.host\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = url.port
    @py_assert4 = 80
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.port\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = url.query
    @py_assert4 = {}
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.query\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = url.fragment
    @py_assert4 = ''
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.fragment\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = url.netloc
    @py_assert4 = ''
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.netloc\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert2 = str(url)
    @py_assert5 = 'http:///'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py1': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_empty_path():
    @py_assert1 = 'http://getgauss.com'
    @py_assert3 = URL(@py_assert1)
    @py_assert5 = @py_assert3.path
    @py_assert8 = ''
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}.path\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(URL) if 'URL' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(URL) else 'URL', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_consistent_reparsing():
    for surl in (url_full, url_path_only):
        url = URL(surl)
        reparsed = URL(str(url))
        for attr in URL.__slots__:
            @py_assert3 = getattr(reparsed, attr)
            @py_assert9 = getattr(url, attr)
            @py_assert5 = @py_assert3 == @py_assert9
            if not @py_assert5:
                @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py10)s\n{%(py10)s = %(py6)s(%(py7)s, %(py8)s)\n}',), (@py_assert3, @py_assert9)) % {'py7': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py0': @pytest_ar._saferepr(getattr) if 'getattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getattr) else 'getattr', 'py1': @pytest_ar._saferepr(reparsed) if 'reparsed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reparsed) else 'reparsed', 'py6': @pytest_ar._saferepr(getattr) if 'getattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getattr) else 'getattr', 'py2': @pytest_ar._saferepr(attr) if 'attr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr) else 'attr', 
                 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(attr) if 'attr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr) else 'attr', 'py4': @pytest_ar._saferepr(@py_assert3)}
                @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
                raise AssertionError(@pytest_ar._format_explanation(@py_format13))
            @py_assert3 = @py_assert5 = @py_assert9 = None


def test_redirection_abs_path():
    url = URL(url_full)
    updated = url.redirect('/test.html')
    @py_assert1 = updated.host
    @py_assert5 = url.host
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.host\n} == %(py6)s\n{%(py6)s = %(py4)s.host\n}', ), (@py_assert1, @py_assert5)) % {'py0': @pytest_ar._saferepr(updated) if 'updated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(updated) else 'updated', 'py4': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = updated.port
    @py_assert5 = url.port
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.port\n} == %(py6)s\n{%(py6)s = %(py4)s.port\n}', ), (@py_assert1, @py_assert5)) % {'py0': @pytest_ar._saferepr(updated) if 'updated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(updated) else 'updated', 'py4': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = updated.path
    @py_assert4 = '/test.html'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.path\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(updated) if 'updated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(updated) else 'updated', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = updated.query
    @py_assert4 = {}
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.query\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(updated) if 'updated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(updated) else 'updated', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = updated.fragment
    @py_assert4 = ''
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.fragment\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(updated) if 'updated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(updated) else 'updated', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_redirection_rel_path():
    url = URL(url_full)
    for redir in ('test.html?key=val', 'folder/test.html?key=val'):
        updated = url.redirect(redir)
        @py_assert1 = updated.host
        @py_assert5 = url.host
        @py_assert3 = @py_assert1 == @py_assert5
        if not @py_assert3:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.host\n} == %(py6)s\n{%(py6)s = %(py4)s.host\n}', ), (@py_assert1, @py_assert5)) % {'py0': @pytest_ar._saferepr(updated) if 'updated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(updated) else 'updated', 'py4': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = updated.port
        @py_assert5 = url.port
        @py_assert3 = @py_assert1 == @py_assert5
        if not @py_assert3:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.port\n} == %(py6)s\n{%(py6)s = %(py4)s.port\n}', ), (@py_assert1, @py_assert5)) % {'py0': @pytest_ar._saferepr(updated) if 'updated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(updated) else 'updated', 'py4': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = updated.path
        @py_assert3 = @py_assert1.startswith
        @py_assert5 = '/subdir/'
        @py_assert7 = @py_assert3(@py_assert5)
        if not @py_assert7:
            @py_format9 = ('' + 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.startswith\n}(%(py6)s)\n}') % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(updated) if 'updated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(updated) else 'updated', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = updated.path
        @py_assert3 = @py_assert1.endswith
        @py_assert5 = redir.split('?', 1)[0]
        @py_assert7 = @py_assert3(@py_assert5)
        if not @py_assert7:
            @py_format9 = ('' + 'assert %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.endswith\n}(%(py6)s)\n}') % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(updated) if 'updated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(updated) else 'updated', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = updated.query
        @py_assert4 = {'key': 'val'}
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.query\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(updated) if 'updated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(updated) else 'updated', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = updated.fragment
        @py_assert4 = ''
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.fragment\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(updated) if 'updated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(updated) else 'updated', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None


def test_redirection_full_path():
    url_full2_plain = 'http://google.de/index'
    url = URL(url_full)
    updated = url.redirect(url_full2_plain)
    url_full2 = URL(url_full2_plain)
    for attr in URL.__slots__:
        @py_assert3 = getattr(updated, attr)
        @py_assert9 = getattr(url_full2, attr)
        @py_assert5 = @py_assert3 == @py_assert9
        if not @py_assert5:
            @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py10)s\n{%(py10)s = %(py6)s(%(py7)s, %(py8)s)\n}',), (@py_assert3, @py_assert9)) % {'py7': @pytest_ar._saferepr(url_full2) if 'url_full2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url_full2) else 'url_full2', 'py0': @pytest_ar._saferepr(getattr) if 'getattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getattr) else 'getattr', 'py1': @pytest_ar._saferepr(updated) if 'updated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(updated) else 'updated', 'py6': @pytest_ar._saferepr(getattr) if 'getattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getattr) else 'getattr', 'py2': @pytest_ar._saferepr(attr) if 'attr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr) else 'attr', 
             'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(attr) if 'attr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr) else 'attr', 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert3 = @py_assert5 = @py_assert9 = None

    @py_assert2 = str(url_full2)
    @py_assert4 = @py_assert2 == url_full2_plain
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s',), (@py_assert2, url_full2_plain)) % {'py0': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py1': @pytest_ar._saferepr(url_full2) if 'url_full2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url_full2) else 'url_full2', 'py5': @pytest_ar._saferepr(url_full2_plain) if 'url_full2_plain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url_full2_plain) else 'url_full2_plain', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None


def test_set_safe_encoding():

    class SafeModURL(URL):
        quoting_safe = '*'

    surl = '/path/to/something?param=value&other=*'
    @py_assert1 = []
    @py_assert4 = URL(surl)
    @py_assert6 = @py_assert4.query_string
    @py_assert9 = 'other=%2A&param=value'
    @py_assert8 = @py_assert6 == @py_assert9
    @py_assert0 = @py_assert8
    if not @py_assert8:
        @py_assert16 = URL(surl)
        @py_assert18 = @py_assert16.query_string
        @py_assert21 = 'param=value&other=%2A'
        @py_assert20 = @py_assert18 == @py_assert21
        @py_assert0 = @py_assert20
    if not @py_assert0:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n}.query_string\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py3': @pytest_ar._saferepr(surl) if 'surl' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(surl) else 'surl', 'py2': @pytest_ar._saferepr(URL) if 'URL' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(URL) else 'URL'}
        @py_format13 = '%(py12)s' % {'py12': @py_format11}
        @py_assert1.append(@py_format13)
        if not @py_assert8:
            @py_format23 = @pytest_ar._call_reprcompare(('==', ), (@py_assert20,), ('%(py19)s\n{%(py19)s = %(py17)s\n{%(py17)s = %(py14)s(%(py15)s)\n}.query_string\n} == %(py22)s', ), (@py_assert18, @py_assert21)) % {'py22': @pytest_ar._saferepr(@py_assert21), 'py17': @pytest_ar._saferepr(@py_assert16), 'py14': @pytest_ar._saferepr(URL) if 'URL' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(URL) else 'URL', 'py19': @pytest_ar._saferepr(@py_assert18), 'py15': @pytest_ar._saferepr(surl) if 'surl' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(surl) else 'surl'}
            @py_format25 = '%(py24)s' % {'py24': @py_format23}
            @py_assert1.append(@py_format25)
        @py_format26 = @pytest_ar._format_boolop(@py_assert1, 1) % {}
        @py_format28 = 'assert %(py27)s' % {'py27': @py_format26}
        raise AssertionError(@pytest_ar._format_explanation(@py_format28))
    @py_assert0 = @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert16 = @py_assert18 = @py_assert20 = @py_assert21 = None
    @py_assert1 = []
    @py_assert4 = SafeModURL(surl)
    @py_assert6 = @py_assert4.query_string
    @py_assert9 = 'other=*&param=value'
    @py_assert8 = @py_assert6 == @py_assert9
    @py_assert0 = @py_assert8
    if not @py_assert8:
        @py_assert16 = SafeModURL(surl)
        @py_assert18 = @py_assert16.query_string
        @py_assert21 = 'param=value&other=*'
        @py_assert20 = @py_assert18 == @py_assert21
        @py_assert0 = @py_assert20
    if not @py_assert0:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n}.query_string\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py3': @pytest_ar._saferepr(surl) if 'surl' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(surl) else 'surl', 'py2': @pytest_ar._saferepr(SafeModURL) if 'SafeModURL' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SafeModURL) else 'SafeModURL'}
        @py_format13 = '%(py12)s' % {'py12': @py_format11}
        @py_assert1.append(@py_format13)
        if not @py_assert8:
            @py_format23 = @pytest_ar._call_reprcompare(('==', ), (@py_assert20,), ('%(py19)s\n{%(py19)s = %(py17)s\n{%(py17)s = %(py14)s(%(py15)s)\n}.query_string\n} == %(py22)s', ), (@py_assert18, @py_assert21)) % {'py22': @pytest_ar._saferepr(@py_assert21), 'py17': @pytest_ar._saferepr(@py_assert16), 'py14': @pytest_ar._saferepr(SafeModURL) if 'SafeModURL' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SafeModURL) else 'SafeModURL', 'py19': @pytest_ar._saferepr(@py_assert18), 'py15': @pytest_ar._saferepr(surl) if 'surl' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(surl) else 'surl'}
            @py_format25 = '%(py24)s' % {'py24': @py_format23}
            @py_assert1.append(@py_format25)
        @py_format26 = @pytest_ar._format_boolop(@py_assert1, 1) % {}
        @py_format28 = 'assert %(py27)s' % {'py27': @py_format26}
        raise AssertionError(@pytest_ar._format_explanation(@py_format28))
    @py_assert0 = @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert16 = @py_assert18 = @py_assert20 = @py_assert21 = None
    URL.quoting_safe = '*'
    @py_assert1 = []
    @py_assert4 = URL(surl)
    @py_assert6 = @py_assert4.query_string
    @py_assert9 = 'other=*&param=value'
    @py_assert8 = @py_assert6 == @py_assert9
    @py_assert0 = @py_assert8
    if not @py_assert8:
        @py_assert16 = URL(surl)
        @py_assert18 = @py_assert16.query_string
        @py_assert21 = 'param=value&other=*'
        @py_assert20 = @py_assert18 == @py_assert21
        @py_assert0 = @py_assert20
    if not @py_assert0:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n}.query_string\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py3': @pytest_ar._saferepr(surl) if 'surl' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(surl) else 'surl', 'py2': @pytest_ar._saferepr(URL) if 'URL' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(URL) else 'URL'}
        @py_format13 = '%(py12)s' % {'py12': @py_format11}
        @py_assert1.append(@py_format13)
        if not @py_assert8:
            @py_format23 = @pytest_ar._call_reprcompare(('==', ), (@py_assert20,), ('%(py19)s\n{%(py19)s = %(py17)s\n{%(py17)s = %(py14)s(%(py15)s)\n}.query_string\n} == %(py22)s', ), (@py_assert18, @py_assert21)) % {'py22': @pytest_ar._saferepr(@py_assert21), 'py17': @pytest_ar._saferepr(@py_assert16), 'py14': @pytest_ar._saferepr(URL) if 'URL' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(URL) else 'URL', 'py19': @pytest_ar._saferepr(@py_assert18), 'py15': @pytest_ar._saferepr(surl) if 'surl' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(surl) else 'surl'}
            @py_format25 = '%(py24)s' % {'py24': @py_format23}
            @py_assert1.append(@py_format25)
        @py_format26 = @pytest_ar._format_boolop(@py_assert1, 1) % {}
        @py_format28 = 'assert %(py27)s' % {'py27': @py_format26}
        raise AssertionError(@pytest_ar._format_explanation(@py_format28))
    @py_assert0 = @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = @py_assert16 = @py_assert18 = @py_assert20 = @py_assert21 = None
    URL.quoting_safe = ''


def test_equality():
    @py_assert1 = 'https://example.com/'
    @py_assert3 = URL(@py_assert1)
    @py_assert7 = 'http://example.com/'
    @py_assert9 = URL(@py_assert7)
    @py_assert5 = @py_assert3 != @py_assert9
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} != %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py0': @pytest_ar._saferepr(URL) if 'URL' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(URL) else 'URL', 'py6': @pytest_ar._saferepr(URL) if 'URL' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(URL) else 'URL', 'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = 'http://example.com/'
    @py_assert3 = URL(@py_assert1)
    @py_assert7 = 'http://example.com/'
    @py_assert9 = URL(@py_assert7)
    @py_assert5 = @py_assert3 == @py_assert9
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py0': @pytest_ar._saferepr(URL) if 'URL' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(URL) else 'URL', 'py6': @pytest_ar._saferepr(URL) if 'URL' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(URL) else 'URL', 'py2': @pytest_ar._saferepr(@py_assert1), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_pw():
    url = URL('http://asdf:dd@heise.de/index.php?aaaa=bbbbb')
    @py_assert1 = url.host
    @py_assert4 = 'heise.de'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.host\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = url.port
    @py_assert4 = 80
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.port\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = url.user
    @py_assert4 = 'asdf'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.user\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = url.password
    @py_assert4 = 'dd'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.password\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_pw_with_port():
    url = URL('http://asdf:dd@heise.de:90/index.php?aaaa=bbbbb')
    @py_assert1 = url.host
    @py_assert4 = 'heise.de'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.host\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = url.port
    @py_assert4 = 90
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.port\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = url.user
    @py_assert4 = 'asdf'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.user\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = url.password
    @py_assert4 = 'dd'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.password\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_ipv6():
    url = URL('http://[2001:db8:85a3:8d3:1319:8a2e:370:7348]/')
    @py_assert1 = url.host
    @py_assert4 = '2001:db8:85a3:8d3:1319:8a2e:370:7348'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.host\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = url.port
    @py_assert4 = 80
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.port\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = url.user
    @py_assert4 = None
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.user\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_ipv6_with_port():
    url = URL('https://[2001:db8:85a3:8d3:1319:8a2e:370:7348]:8080/')
    @py_assert1 = url.host
    @py_assert4 = '2001:db8:85a3:8d3:1319:8a2e:370:7348'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.host\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = url.port
    @py_assert4 = 8080
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.port\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = url.user
    @py_assert4 = None
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.user\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


if __name__ == '__main__':
    test_redirection_abs_path()
    test_redirection_rel_path()
    test_redirection_full_path()
    test_ipv6_with_port()