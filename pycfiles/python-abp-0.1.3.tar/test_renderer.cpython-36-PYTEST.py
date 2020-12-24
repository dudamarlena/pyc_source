# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vkuznetsov/prog/devops/python-abp/tests/test_renderer.py
# Compiled at: 2019-06-05 11:48:03
# Size of source mod 2**32: 3891 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, mock, time
from abp.filters import render_filterlist, MissingHeader, IncludeError

@pytest.fixture()
def gmtime(request):
    """Patch time.gmtime to freeze timestamps."""
    patcher = mock.patch('time.gmtime')
    gmtime_mock = patcher.start()
    request.addfinalizer(patcher.stop)
    gmtime_mock.return_value = time.struct_time([2001] + [1] * 8)
    return gmtime_mock


@pytest.fixture()
def head(gmtime):
    """Typical start of the rendered list."""
    version = time.strftime('%Y%m%d%H%M', gmtime())
    return '[Adblock]\n! Version: {}\n'.format(version)


class MockSource(object):

    def __init__(self, **kw):
        self.is_inheritable = kw.get('is_inheritable', True)
        self.files = kw

    def get(self, filename):
        return self.files[filename].split('\n')


def render_str(*args, **kw):
    return '\n'.join(l.to_string() for l in render_filterlist(*args, **kw))


def test_simple_render(head):
    src = MockSource(fl='[Adblock]\n! Comment.')
    got = render_str('fl', {}, src)
    @py_assert3 = '! Comment.'
    @py_assert5 = head + @py_assert3
    @py_assert1 = got == @py_assert5
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_renderer.py', lineno=59)
    if not @py_assert1:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == (%(py2)s + %(py4)s)', ), (got, @py_assert5)) % {'py0':@pytest_ar._saferepr(got) if 'got' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(got) else 'got',  'py2':@pytest_ar._saferepr(head) if 'head' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(head) else 'head',  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_include(head):
    src = MockSource(fl='[Adblock]\n%include src:inc%', inc='!:foo=bar')
    got = render_str('src:fl', {'src': src})
    @py_assert1 = got.startswith
    @py_assert4 = '! *** src:inc ***\n! :foo=bar'
    @py_assert6 = head + @py_assert4
    @py_assert7 = @py_assert1(@py_assert6)
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_renderer.py', lineno=65)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.startswith\n}((%(py3)s + %(py5)s))\n}' % {'py0':@pytest_ar._saferepr(got) if 'got' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(got) else 'got',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(head) if 'head' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(head) else 'head',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_include2(head):
    src1 = MockSource(fl='[Adblock]\n%include inc1%', inc1='%include src2:inc2%')
    src2 = MockSource(inc2='%include inc3%', inc3='Included')
    got = render_str('src1:fl', {'src1':src1,  'src2':src2})
    expect = head + '! *** inc1 ***\n! *** src2:inc2 ***\n! *** inc3 ***\nIncluded'
    @py_assert1 = got.startswith
    @py_assert4 = @py_assert1(expect)
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_renderer.py', lineno=76)
    if not @py_assert4:
        @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.startswith\n}(%(py3)s)\n}' % {'py0':@pytest_ar._saferepr(got) if 'got' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(got) else 'got',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(expect) if 'expect' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expect) else 'expect',  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None


def test_circular_includes():
    src = MockSource(fl='[Adblock]\n%include src:fl%')
    with pytest.raises(IncludeError):
        render_str('src:fl', {'src': src})


def test_timestamp(gmtime):
    src = MockSource(fl='[Adblock]\n! Last modified: %timestamp%')
    got = render_str('fl', {}, src)
    @py_assert1 = time.strftime
    @py_assert3 = 'Last modified: %d %b %Y %H:%M UTC'
    @py_assert6 = gmtime()
    @py_assert8 = @py_assert1(@py_assert3, @py_assert6)
    @py_assert10 = @py_assert8 in got
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_renderer.py', lineno=88)
    if not @py_assert10:
        @py_format12 = @pytest_ar._call_reprcompare(('in', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py2)s\n{%(py2)s = %(py0)s.strftime\n}(%(py4)s, %(py7)s\n{%(py7)s = %(py5)s()\n})\n} in %(py11)s', ), (@py_assert8, got)) % {'py0':@pytest_ar._saferepr(time) if 'time' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(time) else 'time',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(gmtime) if 'gmtime' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(gmtime) else 'gmtime',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(got) if 'got' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(got) else 'got'}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = None


def test_wrong_source():
    src = MockSource(fl='[Adblock]\n%include missing:fl%')
    with pytest.raises(IncludeError):
        render_str('fl', {}, src)


def test_missing_top_source():
    with pytest.raises(IncludeError):
        render_str('fl', {})


def test_deduplication():
    src = MockSource(fl='[Adblock]\n! Title: foo\n%include inc1%',
      inc1='[Adblock]\n! Title: bar\nfilter')
    got = render_str('fl', {}, src)
    @py_assert0 = '! Title: foo\n! *** inc1 ***\nfilter'
    @py_assert2 = @py_assert0 in got
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_renderer.py', lineno=107)
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, got)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(got) if 'got' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(got) else 'got'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_source_non_inheritance():
    src1 = MockSource(fl='[Adblock]\n%include src2:inc1%')
    src2 = MockSource(is_inheritable=False, inc1='%include inc2%',
      inc2='Included')
    with pytest.raises(IncludeError):
        render_str('src1:fl', {'src1':src1,  'src2':src2})


def test_missing_header():
    src = MockSource(fl='! No header')
    with pytest.raises(MissingHeader):
        render_str('fl', {}, src)


def test_remove_checksum(head):
    src = MockSource(fl='[Adblock]\n! Comment\n! Checksum: foo')
    got = render_str('fl', {}, src)
    @py_assert3 = '! Comment'
    @py_assert5 = head + @py_assert3
    @py_assert1 = got == @py_assert5
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_renderer.py', lineno=127)
    if not @py_assert1:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == (%(py2)s + %(py4)s)', ), (got, @py_assert5)) % {'py0':@pytest_ar._saferepr(got) if 'got' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(got) else 'got',  'py2':@pytest_ar._saferepr(head) if 'head' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(head) else 'head',  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = None