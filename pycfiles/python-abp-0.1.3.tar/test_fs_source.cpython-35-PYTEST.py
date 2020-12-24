# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vkuznetsov/prog/devops/python-abp/tests/test_fs_source.py
# Compiled at: 2019-05-13 06:18:18
# Size of source mod 2**32: 1585 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from abp.filters.sources import FSSource, NotFound

@pytest.fixture
def fssource_dir(tmpdir):
    tmpdir.mkdir('root')
    not_in_source = tmpdir.join('not-in-source.txt')
    not_in_source.write('! secret')
    root = tmpdir.join('root')
    root.mkdir('foo')
    foobar = root.join('foo', 'bar.txt')
    foobar.write('! foo/bar.txt\n! end')
    return str(root)


@pytest.fixture
def fssource(fssource_dir):
    return FSSource(fssource_dir)


def test_read_file(fssource):
    @py_assert2 = fssource.get
    @py_assert4 = 'foo/bar.txt'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert8 = list(@py_assert6)
    @py_assert11 = [
     '! foo/bar.txt', '! end']
    @py_assert10 = @py_assert8 == @py_assert11
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_fs_source.py', lineno=39)
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.get\n}(%(py5)s)\n})\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py1': @pytest_ar._saferepr(fssource) if 'fssource' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fssource) else 'fssource', 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py12': @pytest_ar._saferepr(@py_assert11), 'py9': @pytest_ar._saferepr(@py_assert8), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_escape_source(fssource):
    with pytest.raises(ValueError):
        list(fssource.get('../not-in-source.txt'))


def test_read_missing_file(fssource):
    with pytest.raises(NotFound):
        list(fssource.get('foo/baz.txt'))


def test_fssource_get_err(fssource):
    with pytest.raises(IOError):
        list(fssource.get(''))