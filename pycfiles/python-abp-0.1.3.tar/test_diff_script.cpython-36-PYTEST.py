# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vkuznetsov/prog/devops/python-abp/tests/test_diff_script.py
# Compiled at: 2019-05-13 06:18:18
# Size of source mod 2**32: 4717 bytes
"""Functional tests for the diff script."""
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, subprocess, io, os, re
from test_differ import BASE, LATEST

@pytest.fixture
def rootdir(tmpdir):
    """Root directory for test files."""
    rootdir = tmpdir.join('root')
    rootdir.mkdir()
    rootdir.join('latest.txt').write_text(LATEST, encoding='utf8')
    return rootdir


@pytest.fixture
def archive_dir(rootdir):
    return rootdir.mkdir('archive')


@pytest.fixture
def diff_dir(rootdir):
    return rootdir.mkdir('diff')


@pytest.fixture
def archived_files(archive_dir):
    base2 = BASE + '&adnet=\n'
    base2 = re.sub('! Version: \\d+', '! Version: 112', base2)
    archive_dir.join('list111.txt').write_text(BASE, encoding='utf8')
    archive_dir.join('list112.txt').write_text(base2, encoding='utf8')
    return [str(x) for x in archive_dir.listdir()]


@pytest.fixture
def base_no_version(archive_dir):
    base = re.sub('! Version: \\d+', '! ', BASE)
    archive_dir.join('list113.txt').write_text(base, encoding='utf8')
    return [str(x) for x in archive_dir.listdir()]


def run_script(*args, **kw):
    """Run diff rendering script with given arguments and return its output."""
    cmd = [
     'fldiff'] + list(args)
    proc = (subprocess.Popen)(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, 
     stdin=subprocess.PIPE, **kw)
    stdout, stderr = proc.communicate()
    return (proc.returncode, stderr.decode('utf-8'), stdout.decode('utf-8'))


def test_diff_with_outfile(rootdir, archived_files, diff_dir):
    run_script(str(rootdir.join('latest.txt')), '-o', str(diff_dir), *archived_files)
    @py_assert2 = diff_dir.listdir
    @py_assert4 = @py_assert2()
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 2
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_diff_script.py', lineno=78)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.listdir\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(diff_dir) if 'diff_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(diff_dir) else 'diff_dir',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    for file in diff_dir.visit():
        with io.open((str(file)), encoding='utf-8') as (dst):
            result = dst.read()
        @py_assert0 = '- &ad.vid=$~xmlhttprequest'
        @py_assert2 = @py_assert0 in result
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_diff_script.py', lineno=82)
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, result)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = '+ &ad_channel=£'
        @py_assert2 = @py_assert0 in result
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_diff_script.py', lineno=83)
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, result)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = '! Version: 123'
        @py_assert2 = @py_assert0 in result
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_diff_script.py', lineno=84)
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, result)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None


def test_diff_no_outfile(rootdir, archived_files):
    os.chdir(str(rootdir))
    run_script(str(rootdir.join('latest.txt')), *archived_files)
    for file in ('diff111.txt', 'diff112.txt'):
        with io.open(file, encoding='utf-8') as (dst):
            result = dst.read()
        @py_assert0 = '- &ad.vid=$~xmlhttprequest'
        @py_assert2 = @py_assert0 in result
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_diff_script.py', lineno=93)
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, result)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = '+ &ad_channel=£'
        @py_assert2 = @py_assert0 in result
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_diff_script.py', lineno=94)
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, result)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = '! Version: 123'
        @py_assert2 = @py_assert0 in result
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_diff_script.py', lineno=95)
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, result)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None


def test_no_base_file(rootdir):
    code, err, _ = run_script(str(rootdir.join('latest.txt')))
    @py_assert2 = 2
    @py_assert1 = code == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_diff_script.py', lineno=100)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (code, @py_assert2)) % {'py0':@pytest_ar._saferepr(code) if 'code' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(code) else 'code',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert0 = 'usage: fldiff'
    @py_assert2 = @py_assert0 in err
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_diff_script.py', lineno=101)
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, err)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_wrong_file(rootdir):
    code, err, _ = run_script(str(rootdir.join('base.txt')), 'wrong.txt')
    @py_assert2 = 1
    @py_assert1 = code == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_diff_script.py', lineno=106)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (code, @py_assert2)) % {'py0':@pytest_ar._saferepr(code) if 'code' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(code) else 'code',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert0 = 'No such file or directory'
    @py_assert2 = @py_assert0 in err
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_diff_script.py', lineno=107)
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, err)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_diff_to_self(rootdir, diff_dir):
    run_script(str(rootdir.join('latest.txt')), '-o', str(diff_dir), str(rootdir.join('latest.txt')))
    @py_assert2 = diff_dir.listdir
    @py_assert4 = @py_assert2()
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 1
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_diff_script.py', lineno=113)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.listdir\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(diff_dir) if 'diff_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(diff_dir) else 'diff_dir',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    for file in diff_dir.visit():
        with io.open((str(file)), encoding='utf-8') as (dst):
            result = dst.read()
        @py_assert2 = '[Adblock Plus Diff]\n'
        @py_assert1 = result == @py_assert2
        if @py_assert1 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_diff_script.py', lineno=117)
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_no_version(rootdir, base_no_version):
    code, err, _ = run_script(str(rootdir.join('latest.txt')), '-o', str(diff_dir), *base_no_version)
    @py_assert2 = 1
    @py_assert1 = code == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_diff_script.py', lineno=123)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (code, @py_assert2)) % {'py0':@pytest_ar._saferepr(code) if 'code' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(code) else 'code',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert0 = 'Unable to find Version in '
    @py_assert2 = @py_assert0 in err
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_diff_script.py', lineno=124)
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, err)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_write_and_overwrite(rootdir, archived_files, diff_dir):
    test_diff_with_outfile(rootdir, archived_files, diff_dir)
    latest = re.sub('&act=ads_', '! ', BASE) + '&adurl=\n'
    rootdir.join('latest.txt').write_text(latest, encoding='utf8')
    run_script(str(rootdir.join('latest.txt')), '-o', str(diff_dir), *archived_files)
    @py_assert2 = diff_dir.listdir
    @py_assert4 = @py_assert2()
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 2
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_diff_script.py', lineno=133)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.listdir\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(diff_dir) if 'diff_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(diff_dir) else 'diff_dir',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    for file in diff_dir.visit():
        with io.open((str(file)), encoding='utf-8') as (dst):
            result = dst.read()
        @py_assert0 = '- &act=ads_'
        @py_assert2 = @py_assert0 in result
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_diff_script.py', lineno=137)
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, result)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = '+ &adurl='
        @py_assert2 = @py_assert0 in result
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_diff_script.py', lineno=138)
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, result)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = '- &ad.vid=$~xmlhttprequest'
        @py_assert2 = @py_assert0 not in result
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_diff_script.py', lineno=139)
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, result)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None