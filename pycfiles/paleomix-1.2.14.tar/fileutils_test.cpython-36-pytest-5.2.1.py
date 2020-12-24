# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py
# Compiled at: 2019-10-16 12:05:38
# Size of source mod 2**32: 25936 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, errno, os, stat
from unittest.mock import ANY, call, DEFAULT, Mock, patch
import pytest
from paleomix.common.testing import SetWorkingDirectory
from paleomix.common.fileutils import add_postfix, swap_ext, reroot_path, create_temp_dir, missing_files, is_executable, which_executable, executable_exists, missing_executables, make_dirs, move_file, copy_file, open_ro, try_remove, try_rmtree, describe_files, describe_paired_files

def test_dir():
    return os.path.dirname(os.path.dirname(__file__))


def test_file(*args):
    return (os.path.join)(test_dir(), 'data', *args)


def test_add_postfix__no_postfix():
    @py_assert1 = 'name.foo'
    @py_assert3 = ''
    @py_assert5 = add_postfix(@py_assert1, @py_assert3)
    @py_assert8 = 'name.foo'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=73)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(add_postfix) if 'add_postfix' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(add_postfix) else 'add_postfix',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_add_postfix__dot_postfix():
    @py_assert1 = 'name.foo'
    @py_assert3 = '.pf'
    @py_assert5 = add_postfix(@py_assert1, @py_assert3)
    @py_assert8 = 'name.pf.foo'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=77)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(add_postfix) if 'add_postfix' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(add_postfix) else 'add_postfix',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_add_postfix__underscore_postfix():
    @py_assert1 = 'name.foo'
    @py_assert3 = '_pf'
    @py_assert5 = add_postfix(@py_assert1, @py_assert3)
    @py_assert8 = 'name_pf.foo'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=81)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(add_postfix) if 'add_postfix' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(add_postfix) else 'add_postfix',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_add_postfix__no_ext__no_postfix():
    @py_assert1 = 'name'
    @py_assert3 = ''
    @py_assert5 = add_postfix(@py_assert1, @py_assert3)
    @py_assert8 = 'name'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=85)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(add_postfix) if 'add_postfix' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(add_postfix) else 'add_postfix',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_add_postfix__no_ext__dot_postfix():
    @py_assert1 = 'name'
    @py_assert3 = '.pf'
    @py_assert5 = add_postfix(@py_assert1, @py_assert3)
    @py_assert8 = 'name.pf'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=89)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(add_postfix) if 'add_postfix' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(add_postfix) else 'add_postfix',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_add_postfix__no_ext__underscore_postfix():
    @py_assert1 = 'name'
    @py_assert3 = '_pf'
    @py_assert5 = add_postfix(@py_assert1, @py_assert3)
    @py_assert8 = 'name_pf'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=93)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(add_postfix) if 'add_postfix' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(add_postfix) else 'add_postfix',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_swap_ext__has_ext_vs_empty_ext():
    @py_assert1 = 'name.foo'
    @py_assert3 = ''
    @py_assert5 = swap_ext(@py_assert1, @py_assert3)
    @py_assert8 = 'name'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=102)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(swap_ext) if 'swap_ext' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(swap_ext) else 'swap_ext',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_swap_ext__empty_ext_vs_empty_ext():
    @py_assert1 = 'name'
    @py_assert3 = ''
    @py_assert5 = swap_ext(@py_assert1, @py_assert3)
    @py_assert8 = 'name'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=106)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(swap_ext) if 'swap_ext' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(swap_ext) else 'swap_ext',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_swap_ext__has_ext_vs_dot_ext():
    @py_assert1 = 'name.foo'
    @py_assert3 = '.'
    @py_assert5 = swap_ext(@py_assert1, @py_assert3)
    @py_assert8 = 'name'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=110)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(swap_ext) if 'swap_ext' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(swap_ext) else 'swap_ext',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_swap_ext__dot_ext_vs_dot_ext():
    @py_assert1 = 'name.'
    @py_assert3 = '.'
    @py_assert5 = swap_ext(@py_assert1, @py_assert3)
    @py_assert8 = 'name'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=114)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(swap_ext) if 'swap_ext' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(swap_ext) else 'swap_ext',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_swap_ext__multiple__has_ext_vs_empty_ext():
    @py_assert1 = 'name.foo.bar'
    @py_assert3 = ''
    @py_assert5 = swap_ext(@py_assert1, @py_assert3)
    @py_assert8 = 'name.foo'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=118)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(swap_ext) if 'swap_ext' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(swap_ext) else 'swap_ext',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_swap_ext__multiple__has_ext_vs_dot_ext():
    @py_assert1 = 'name.foo.bar'
    @py_assert3 = '.'
    @py_assert5 = swap_ext(@py_assert1, @py_assert3)
    @py_assert8 = 'name.foo'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=122)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(swap_ext) if 'swap_ext' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(swap_ext) else 'swap_ext',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_swap_ext__multiple__dot_ext_vs_dot_ext():
    @py_assert1 = 'name.foo.'
    @py_assert3 = '.'
    @py_assert5 = swap_ext(@py_assert1, @py_assert3)
    @py_assert8 = 'name.foo'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=126)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(swap_ext) if 'swap_ext' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(swap_ext) else 'swap_ext',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_swap_ext__has_ext_vs_new_ext():
    @py_assert1 = 'name.foo'
    @py_assert3 = 'bar'
    @py_assert5 = swap_ext(@py_assert1, @py_assert3)
    @py_assert8 = 'name.bar'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=130)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(swap_ext) if 'swap_ext' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(swap_ext) else 'swap_ext',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_swap_ext__has_ext_vs_new_dot_ext():
    @py_assert1 = 'name.foo'
    @py_assert3 = '.bar'
    @py_assert5 = swap_ext(@py_assert1, @py_assert3)
    @py_assert8 = 'name.bar'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=134)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(swap_ext) if 'swap_ext' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(swap_ext) else 'swap_ext',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_swap_ext__empty_ext_vs_new_ext():
    @py_assert1 = 'name'
    @py_assert3 = 'bar'
    @py_assert5 = swap_ext(@py_assert1, @py_assert3)
    @py_assert8 = 'name.bar'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=138)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(swap_ext) if 'swap_ext' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(swap_ext) else 'swap_ext',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_swap_ext__dot_ext_vs_new_dot_ext():
    @py_assert1 = 'name'
    @py_assert3 = '.bar'
    @py_assert5 = swap_ext(@py_assert1, @py_assert3)
    @py_assert8 = 'name.bar'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=142)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(swap_ext) if 'swap_ext' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(swap_ext) else 'swap_ext',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_reroot_path__empty_root():
    @py_assert1 = ''
    @py_assert3 = '/etc/apt/sources.list'
    @py_assert5 = reroot_path(@py_assert1, @py_assert3)
    @py_assert8 = 'sources.list'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=151)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(reroot_path) if 'reroot_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reroot_path) else 'reroot_path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_reroot_path__empty_path():
    @py_assert1 = '/etc/apt'
    @py_assert3 = ''
    @py_assert5 = reroot_path(@py_assert1, @py_assert3)
    @py_assert8 = '/etc/apt/'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=155)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(reroot_path) if 'reroot_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reroot_path) else 'reroot_path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_reroot_path__abs_abs__wo_final_dash():
    @py_assert1 = '/etc/apt'
    @py_assert3 = '/tmp/sources.list'
    @py_assert5 = reroot_path(@py_assert1, @py_assert3)
    @py_assert8 = '/etc/apt/sources.list'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=159)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(reroot_path) if 'reroot_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reroot_path) else 'reroot_path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_reroot_path__abs_abs__w_final_dash():
    @py_assert1 = '/etc/apt/'
    @py_assert3 = '/tmp/sources.list'
    @py_assert5 = reroot_path(@py_assert1, @py_assert3)
    @py_assert8 = '/etc/apt/sources.list'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=163)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(reroot_path) if 'reroot_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reroot_path) else 'reroot_path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_reroot_path__abs_rel__wo_final_dash():
    @py_assert1 = '/etc/apt'
    @py_assert3 = 'tmp/sources.list'
    @py_assert5 = reroot_path(@py_assert1, @py_assert3)
    @py_assert8 = '/etc/apt/sources.list'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=167)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(reroot_path) if 'reroot_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reroot_path) else 'reroot_path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_reroot_path__abs_rel__w_final_dash():
    @py_assert1 = '/etc/apt/'
    @py_assert3 = 'tmp/sources.list'
    @py_assert5 = reroot_path(@py_assert1, @py_assert3)
    @py_assert8 = '/etc/apt/sources.list'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=171)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(reroot_path) if 'reroot_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reroot_path) else 'reroot_path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_reroot_path__rel_abs__wo_final_dash():
    @py_assert1 = 'etc/apt'
    @py_assert3 = '/tmp/sources.list'
    @py_assert5 = reroot_path(@py_assert1, @py_assert3)
    @py_assert8 = 'etc/apt/sources.list'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=175)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(reroot_path) if 'reroot_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reroot_path) else 'reroot_path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_reroot_path__rel_abs__w_final_dash():
    @py_assert1 = 'etc/apt/'
    @py_assert3 = '/tmp/sources.list'
    @py_assert5 = reroot_path(@py_assert1, @py_assert3)
    @py_assert8 = 'etc/apt/sources.list'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=179)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(reroot_path) if 'reroot_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reroot_path) else 'reroot_path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_reroot_path__rel_rel__wo_final_dash():
    @py_assert1 = 'etc/apt'
    @py_assert3 = 'tmp/sources.list'
    @py_assert5 = reroot_path(@py_assert1, @py_assert3)
    @py_assert8 = 'etc/apt/sources.list'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=183)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(reroot_path) if 'reroot_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reroot_path) else 'reroot_path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_reroot_path__rel_rel__w_final_dash():
    @py_assert1 = 'etc/apt/'
    @py_assert3 = 'tmp/sources.list'
    @py_assert5 = reroot_path(@py_assert1, @py_assert3)
    @py_assert8 = 'etc/apt/sources.list'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=187)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(reroot_path) if 'reroot_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reroot_path) else 'reroot_path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_create_temp_dir__create(tmp_path):
    tmp_dir_1 = create_temp_dir(tmp_path)
    tmp_dir_2 = create_temp_dir(tmp_path)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = @py_assert3(tmp_dir_1)
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=198)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py5)s)\n}' % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(tmp_dir_1) if 'tmp_dir_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_dir_1) else 'tmp_dir_1',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.exists
    @py_assert6 = @py_assert3(tmp_dir_2)
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=199)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py5)s)\n}' % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(tmp_dir_2) if 'tmp_dir_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_dir_2) else 'tmp_dir_2',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None


def test_create_temp_dir__empty(tmp_path):
    tmp_dir = create_temp_dir(tmp_path)
    contents = os.listdir(tmp_dir)
    @py_assert1 = not contents
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=205)
    if not @py_assert1:
        @py_format2 = 'assert not %(py0)s' % {'py0': @pytest_ar._saferepr(contents) if 'contents' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(contents) else 'contents'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert1 = None


def test_create_temp_dir__permissions(tmp_path):
    tmp_dir = create_temp_dir(tmp_path)
    stats = os.stat(tmp_dir)
    @py_assert1 = stats.st_mode
    @py_assert3 = 0
    @py_assert5 = @py_assert1 & @py_assert3
    @py_assert7 = 0
    @py_assert6 = @py_assert5 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=211)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('(%(py2)s\n{%(py2)s = %(py0)s.st_mode\n} & %(py4)s) == %(py8)s', ), (@py_assert5, @py_assert7)) % {'py0':@pytest_ar._saferepr(stats) if 'stats' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stats) else 'stats',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = @py_assert7 = None


def test_create_temp_dir__creation_preempted(tmp_path):
    makedirs = os.makedirs
    mock = Mock(wraps=makedirs)
    mock.side_effect = [
     OSError(errno.EEXIST, 'dir exists'), DEFAULT]
    with patch('os.makedirs', mock):
        work_dir = create_temp_dir(tmp_path)
    @py_assert1 = work_dir.startswith
    @py_assert5 = str(tmp_path)
    @py_assert7 = @py_assert1(@py_assert5)
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=222)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.startswith\n}(%(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n})\n}' % {'py0':@pytest_ar._saferepr(work_dir) if 'work_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(work_dir) else 'work_dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert5 = @py_assert7 = None
    @py_assert1 = mock.mock_calls
    @py_assert4 = [
     call(ANY, mode=488), call(ANY, mode=488)]
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=225)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.mock_calls\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    call_1, call_2 = mock.mock_calls
    @py_assert0 = call_1[1]
    @py_assert3 = call_2[1]
    @py_assert2 = @py_assert0 != @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=227)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert2,), ('%(py1)s != %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_create_temp_dir__permission_denied():
    with patch('os.makedirs') as (mock):
        mock.side_effect = OSError(errno.EACCES, 'Simulated premission denied')
        with pytest.raises(OSError, match='Simulated premission denied'):
            create_temp_dir('/tmp')


def test_missing_files__file_exists():
    @py_assert1 = [
     test_file('empty_file_1')]
    @py_assert3 = missing_files(@py_assert1)
    @py_assert6 = []
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=244)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(missing_files) if 'missing_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(missing_files) else 'missing_files',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_missing_files__file_doesnt_exist():
    @py_assert1 = [
     test_file('missing_file_1')]
    @py_assert3 = missing_files(@py_assert1)
    @py_assert6 = [
     test_file('missing_file_1')]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=248)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(missing_files) if 'missing_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(missing_files) else 'missing_files',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_missing_files__mixed_files():
    files = [
     test_file('missing_file_1'), test_file('empty_file_1')]
    result = [test_file('missing_file_1')]
    @py_assert2 = missing_files(files)
    @py_assert4 = @py_assert2 == result
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=255)
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, result)) % {'py0':@pytest_ar._saferepr(missing_files) if 'missing_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(missing_files) else 'missing_files',  'py1':@pytest_ar._saferepr(files) if 'files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(files) else 'files',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None


def test_is_executable__full_path__is_executable():
    @py_assert1 = '/bin/ls'
    @py_assert3 = is_executable(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=264)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(is_executable) if 'is_executable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_executable) else 'is_executable',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_is_executable__full_path__is_non_executable():
    @py_assert1 = '/etc/fstab'
    @py_assert3 = is_executable(@py_assert1)
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=268)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(is_executable) if 'is_executable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_executable) else 'is_executable',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_is_executable__full_path__folder_is_non_executable():
    @py_assert1 = '/etc'
    @py_assert3 = is_executable(@py_assert1)
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=272)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(is_executable) if 'is_executable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_executable) else 'is_executable',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_is_executable__rel_path__is_executable():
    @py_assert2 = os.path
    @py_assert4 = @py_assert2.join
    @py_assert7 = test_dir()
    @py_assert9 = 'setup.sh'
    @py_assert11 = @py_assert4(@py_assert7, @py_assert9)
    @py_assert13 = is_executable(@py_assert11)
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=276)
    if not @py_assert13:
        @py_format15 = 'assert %(py14)s\n{%(py14)s = %(py0)s(%(py12)s\n{%(py12)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.path\n}.join\n}(%(py8)s\n{%(py8)s = %(py6)s()\n}, %(py10)s)\n})\n}' % {'py0':@pytest_ar._saferepr(is_executable) if 'is_executable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_executable) else 'is_executable',  'py1':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(test_dir) if 'test_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_dir) else 'test_dir',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None


def test_is_executable__rel_path__is_non_executable():
    @py_assert2 = 'empty_file_1'
    @py_assert4 = test_file(@py_assert2)
    @py_assert6 = is_executable(@py_assert4)
    @py_assert8 = not @py_assert6
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=280)
    if not @py_assert8:
        @py_format9 = 'assert not %(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n}' % {'py0':@pytest_ar._saferepr(is_executable) if 'is_executable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_executable) else 'is_executable',  'py1':@pytest_ar._saferepr(test_file) if 'test_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_file) else 'test_file',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None


def test_which_executable__executable():
    @py_assert0 = '/bin/ls'
    @py_assert4 = 'ls'
    @py_assert6 = which_executable(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=289)
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(which_executable) if 'which_executable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(which_executable) else 'which_executable',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None


def test_which_executable__non_executable():
    @py_assert0 = None
    @py_assert4 = 'lsxxxx'
    @py_assert6 = which_executable(@py_assert4)
    @py_assert2 = @py_assert0 is @py_assert6
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=293)
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(which_executable) if 'which_executable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(which_executable) else 'which_executable',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None


def test_which_executable__executable__but_no_path():
    path = os.environ.pop('PATH')
    try:
        @py_assert0 = None
        @py_assert4 = 'ls'
        @py_assert6 = which_executable(@py_assert4)
        @py_assert2 = @py_assert0 is @py_assert6
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=299)
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(which_executable) if 'which_executable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(which_executable) else 'which_executable',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    finally:
        os.environ['PATH'] = path


def test_which_executable__executable__but_empty_path():
    path = os.environ.pop('PATH')
    try:
        os.environ['PATH'] = ''
        @py_assert0 = None
        @py_assert4 = 'ls'
        @py_assert6 = which_executable(@py_assert4)
        @py_assert2 = @py_assert0 is @py_assert6
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=308)
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(which_executable) if 'which_executable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(which_executable) else 'which_executable',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    finally:
        os.environ['PATH'] = path


def test_which_executable__executable__by_path_order_1():
    path = os.environ.pop('PATH')
    try:
        path_1 = test_dir()
        path_2 = os.path.join(os.getcwd(), path_1)
        os.environ['PATH'] = ':'.join((path_1, path_2))
        @py_assert1 = os.path
        @py_assert3 = @py_assert1.join
        @py_assert6 = 'setup.sh'
        @py_assert8 = @py_assert3(path_1, @py_assert6)
        @py_assert12 = 'setup.sh'
        @py_assert14 = which_executable(@py_assert12)
        @py_assert10 = @py_assert8 == @py_assert14
        if @py_assert10 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=320)
        if not @py_assert10:
            @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.join\n}(%(py5)s, %(py7)s)\n} == %(py15)s\n{%(py15)s = %(py11)s(%(py13)s)\n}', ), (@py_assert8, @py_assert14)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(path_1) if 'path_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path_1) else 'path_1',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(which_executable) if 'which_executable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(which_executable) else 'which_executable',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
            @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
            raise AssertionError(@pytest_ar._format_explanation(@py_format18))
        @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    finally:
        os.environ['PATH'] = path


def test_which_executable__executable__by_path_order_2():
    path = os.environ.pop('PATH')
    try:
        path_1 = test_dir()
        path_2 = os.path.join(os.getcwd(), path_1)
        os.environ['PATH'] = ':'.join((path_2, path_1))
        @py_assert1 = os.path
        @py_assert3 = @py_assert1.join
        @py_assert6 = 'setup.sh'
        @py_assert8 = @py_assert3(path_2, @py_assert6)
        @py_assert12 = 'setup.sh'
        @py_assert14 = which_executable(@py_assert12)
        @py_assert10 = @py_assert8 == @py_assert14
        if @py_assert10 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=332)
        if not @py_assert10:
            @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.join\n}(%(py5)s, %(py7)s)\n} == %(py15)s\n{%(py15)s = %(py11)s(%(py13)s)\n}', ), (@py_assert8, @py_assert14)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(path_2) if 'path_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path_2) else 'path_2',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(which_executable) if 'which_executable' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(which_executable) else 'which_executable',  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
            @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
            raise AssertionError(@pytest_ar._format_explanation(@py_format18))
        @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None
    finally:
        os.environ['PATH'] = path


def test_executable_exists__executable():
    @py_assert1 = 'ls'
    @py_assert3 = executable_exists(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=343)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(executable_exists) if 'executable_exists' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(executable_exists) else 'executable_exists',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_executable_exists__non_executable():
    @py_assert1 = 'lsxxxx'
    @py_assert3 = executable_exists(@py_assert1)
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=347)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(executable_exists) if 'executable_exists' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(executable_exists) else 'executable_exists',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_executable_exists__full_path__is_executable():
    @py_assert1 = '/bin/ls'
    @py_assert3 = executable_exists(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=351)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(executable_exists) if 'executable_exists' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(executable_exists) else 'executable_exists',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_executable_exists__full_path__is_non_executable():
    @py_assert1 = '/etc/fstab'
    @py_assert3 = executable_exists(@py_assert1)
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=355)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(executable_exists) if 'executable_exists' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(executable_exists) else 'executable_exists',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_executable_exists__rel_path__is_executable():
    @py_assert2 = os.path
    @py_assert4 = @py_assert2.join
    @py_assert7 = test_dir()
    @py_assert9 = 'setup.sh'
    @py_assert11 = @py_assert4(@py_assert7, @py_assert9)
    @py_assert13 = executable_exists(@py_assert11)
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=359)
    if not @py_assert13:
        @py_format15 = 'assert %(py14)s\n{%(py14)s = %(py0)s(%(py12)s\n{%(py12)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.path\n}.join\n}(%(py8)s\n{%(py8)s = %(py6)s()\n}, %(py10)s)\n})\n}' % {'py0':@pytest_ar._saferepr(executable_exists) if 'executable_exists' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(executable_exists) else 'executable_exists',  'py1':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(test_dir) if 'test_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_dir) else 'test_dir',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None


def test_executable_exists__rel_path__is_non_executable():
    @py_assert2 = 'empty_file_1'
    @py_assert4 = test_file(@py_assert2)
    @py_assert6 = executable_exists(@py_assert4)
    @py_assert8 = not @py_assert6
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=363)
    if not @py_assert8:
        @py_format9 = 'assert not %(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n}' % {'py0':@pytest_ar._saferepr(executable_exists) if 'executable_exists' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(executable_exists) else 'executable_exists',  'py1':@pytest_ar._saferepr(test_file) if 'test_file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_file) else 'test_file',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None


def test_missing_executables__executable():
    @py_assert1 = [
     'ls']
    @py_assert3 = missing_executables(@py_assert1)
    @py_assert6 = []
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=372)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(missing_executables) if 'missing_executables' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(missing_executables) else 'missing_executables',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_missing_executables__non_executable():
    @py_assert1 = [
     'lsxxxx']
    @py_assert3 = missing_executables(@py_assert1)
    @py_assert6 = [
     'lsxxxx']
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=376)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(missing_executables) if 'missing_executables' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(missing_executables) else 'missing_executables',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_missing_executables__mixed():
    @py_assert1 = [
     'lsxxxx', 'ls']
    @py_assert3 = missing_executables(@py_assert1)
    @py_assert6 = [
     'lsxxxx']
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=380)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(missing_executables) if 'missing_executables' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(missing_executables) else 'missing_executables',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_make_dirs__create_dir(tmp_path):
    @py_assert1 = os.listdir
    @py_assert4 = @py_assert1(tmp_path)
    @py_assert6 = not @py_assert4
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=389)
    if not @py_assert6:
        @py_format7 = 'assert not %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py3)s)\n}' % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert4 = @py_assert6 = None
    @py_assert2 = os.path
    @py_assert4 = @py_assert2.join
    @py_assert7 = 'test123'
    @py_assert9 = @py_assert4(tmp_path, @py_assert7)
    @py_assert11 = make_dirs(@py_assert9)
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=390)
    if not @py_assert11:
        @py_format13 = 'assert %(py12)s\n{%(py12)s = %(py0)s(%(py10)s\n{%(py10)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.path\n}.join\n}(%(py6)s, %(py8)s)\n})\n}' % {'py0':@pytest_ar._saferepr(make_dirs) if 'make_dirs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_dirs) else 'make_dirs',  'py1':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert1 = os.listdir
    @py_assert4 = @py_assert1(tmp_path)
    @py_assert7 = [
     'test123']
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=391)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_make_dirs__return_values(tmp_path):
    @py_assert2 = os.path
    @py_assert4 = @py_assert2.join
    @py_assert7 = 'test234'
    @py_assert9 = @py_assert4(tmp_path, @py_assert7)
    @py_assert11 = make_dirs(@py_assert9)
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=395)
    if not @py_assert11:
        @py_format13 = 'assert %(py12)s\n{%(py12)s = %(py0)s(%(py10)s\n{%(py10)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.path\n}.join\n}(%(py6)s, %(py8)s)\n})\n}' % {'py0':@pytest_ar._saferepr(make_dirs) if 'make_dirs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_dirs) else 'make_dirs',  'py1':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert2 = os.path
    @py_assert4 = @py_assert2.join
    @py_assert7 = 'test234'
    @py_assert9 = @py_assert4(tmp_path, @py_assert7)
    @py_assert11 = make_dirs(@py_assert9)
    @py_assert13 = not @py_assert11
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=396)
    if not @py_assert13:
        @py_format14 = 'assert not %(py12)s\n{%(py12)s = %(py0)s(%(py10)s\n{%(py10)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.path\n}.join\n}(%(py6)s, %(py8)s)\n})\n}' % {'py0':@pytest_ar._saferepr(make_dirs) if 'make_dirs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_dirs) else 'make_dirs',  'py1':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None


def test_make_dirs__subdirs_return_values(tmp_path):
    @py_assert2 = os.path
    @py_assert4 = @py_assert2.join
    @py_assert7 = 'test'
    @py_assert9 = @py_assert4(tmp_path, @py_assert7)
    @py_assert11 = make_dirs(@py_assert9)
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=400)
    if not @py_assert11:
        @py_format13 = 'assert %(py12)s\n{%(py12)s = %(py0)s(%(py10)s\n{%(py10)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.path\n}.join\n}(%(py6)s, %(py8)s)\n})\n}' % {'py0':@pytest_ar._saferepr(make_dirs) if 'make_dirs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_dirs) else 'make_dirs',  'py1':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert2 = os.path
    @py_assert4 = @py_assert2.join
    @py_assert7 = 'test'
    @py_assert9 = '234'
    @py_assert11 = @py_assert4(tmp_path, @py_assert7, @py_assert9)
    @py_assert13 = make_dirs(@py_assert11)
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=401)
    if not @py_assert13:
        @py_format15 = 'assert %(py14)s\n{%(py14)s = %(py0)s(%(py12)s\n{%(py12)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.path\n}.join\n}(%(py6)s, %(py8)s, %(py10)s)\n})\n}' % {'py0':@pytest_ar._saferepr(make_dirs) if 'make_dirs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_dirs) else 'make_dirs',  'py1':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None
    @py_assert2 = os.path
    @py_assert4 = @py_assert2.join
    @py_assert7 = 'test'
    @py_assert9 = '234'
    @py_assert11 = @py_assert4(tmp_path, @py_assert7, @py_assert9)
    @py_assert13 = make_dirs(@py_assert11)
    @py_assert15 = not @py_assert13
    if @py_assert15 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=402)
    if not @py_assert15:
        @py_format16 = 'assert not %(py14)s\n{%(py14)s = %(py0)s(%(py12)s\n{%(py12)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.path\n}.join\n}(%(py6)s, %(py8)s, %(py10)s)\n})\n}' % {'py0':@pytest_ar._saferepr(make_dirs) if 'make_dirs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_dirs) else 'make_dirs',  'py1':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None


def test_make_dirs__sub_directories(tmp_path):
    @py_assert1 = os.listdir
    @py_assert4 = @py_assert1(tmp_path)
    @py_assert6 = not @py_assert4
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=406)
    if not @py_assert6:
        @py_format7 = 'assert not %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py3)s)\n}' % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert4 = @py_assert6 = None
    @py_assert2 = os.path
    @py_assert4 = @py_assert2.join
    @py_assert7 = 'test'
    @py_assert9 = '123'
    @py_assert11 = @py_assert4(tmp_path, @py_assert7, @py_assert9)
    @py_assert13 = make_dirs(@py_assert11)
    if @py_assert13 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=407)
    if not @py_assert13:
        @py_format15 = 'assert %(py14)s\n{%(py14)s = %(py0)s(%(py12)s\n{%(py12)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.path\n}.join\n}(%(py6)s, %(py8)s, %(py10)s)\n})\n}' % {'py0':@pytest_ar._saferepr(make_dirs) if 'make_dirs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_dirs) else 'make_dirs',  'py1':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None
    @py_assert1 = os.listdir
    @py_assert4 = @py_assert1(tmp_path)
    @py_assert7 = [
     'test']
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=408)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert1 = os.listdir
    @py_assert4 = os.path
    @py_assert6 = @py_assert4.join
    @py_assert9 = 'test'
    @py_assert11 = @py_assert6(tmp_path, @py_assert9)
    @py_assert13 = @py_assert1(@py_assert11)
    @py_assert16 = [
     '123']
    @py_assert15 = @py_assert13 == @py_assert16
    if @py_assert15 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=409)
    if not @py_assert15:
        @py_format18 = @pytest_ar._call_reprcompare(('==', ), (@py_assert15,), ('%(py14)s\n{%(py14)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py12)s\n{%(py12)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.path\n}.join\n}(%(py8)s, %(py10)s)\n})\n} == %(py17)s', ), (@py_assert13, @py_assert16)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py8':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py17':@pytest_ar._saferepr(@py_assert16)}
        @py_format20 = 'assert %(py19)s' % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert16 = None


def test_make_dirs__permissions(tmp_path):
    work_dir = tmp_path / 'test_1'
    @py_assert2 = 329
    @py_assert4 = make_dirs(work_dir, mode=@py_assert2)
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=414)
    if not @py_assert4:
        @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, mode=%(py3)s)\n}' % {'py0':@pytest_ar._saferepr(make_dirs) if 'make_dirs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_dirs) else 'make_dirs',  'py1':@pytest_ar._saferepr(work_dir) if 'work_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(work_dir) else 'work_dir',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    stats = work_dir.stat()
    @py_assert2 = stats.st_mode
    @py_assert4 = 511
    @py_assert6 = @py_assert2 & @py_assert4
    @py_assert7 = oct(@py_assert6)
    @py_assert11 = 329
    @py_assert13 = oct(@py_assert11)
    @py_assert9 = @py_assert7 == @py_assert13
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=416)
    if not @py_assert9:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s((%(py3)s\n{%(py3)s = %(py1)s.st_mode\n} & %(py5)s))\n} == %(py14)s\n{%(py14)s = %(py10)s(%(py12)s)\n}', ), (@py_assert7, @py_assert13)) % {'py0':@pytest_ar._saferepr(oct) if 'oct' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(oct) else 'oct',  'py1':@pytest_ar._saferepr(stats) if 'stats' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stats) else 'stats',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(oct) if 'oct' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(oct) else 'oct',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None


def test_make_dirs__creation_preemted(tmp_path):
    makedirs = os.makedirs

    def _wrap_os_makedirs(*args, **kwargs):
        makedirs(*args, **kwargs)
        makedirs(*args, **kwargs)

    with patch('os.makedirs', _wrap_os_makedirs):
        work_folder = tmp_path / 'test'
        @py_assert2 = make_dirs(work_folder)
        @py_assert4 = not @py_assert2
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=429)
        if not @py_assert4:
            @py_format5 = 'assert not %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}' % {'py0':@pytest_ar._saferepr(make_dirs) if 'make_dirs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_dirs) else 'make_dirs',  'py1':@pytest_ar._saferepr(work_folder) if 'work_folder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(work_folder) else 'work_folder',  'py3':@pytest_ar._saferepr(@py_assert2)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert2 = @py_assert4 = None
        @py_assert1 = os.path
        @py_assert3 = @py_assert1.exists
        @py_assert6 = @py_assert3(work_folder)
        if @py_assert6 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=430)
        if not @py_assert6:
            @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.exists\n}(%(py5)s)\n}' % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(work_folder) if 'work_folder' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(work_folder) else 'work_folder',  'py7':@pytest_ar._saferepr(@py_assert6)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert6 = None
        @py_assert1 = os.listdir
        @py_assert4 = @py_assert1(tmp_path)
        @py_assert7 = [
         'test']
        @py_assert6 = @py_assert4 == @py_assert7
        if @py_assert6 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=431)
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_make_dirs__permission_denied(tmp_path):
    mode = os.stat(tmp_path).st_mode
    ro_mode = mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
    os.chmod(tmp_path, ro_mode)
    with pytest.raises(OSError):
        make_dirs(os.path.join(tmp_path, 'foo'))


def test_make_dirs__empty_directory():
    with pytest.raises(ValueError, match='Empty directory passed to make_dirs'):
        make_dirs('')


def test_move_file__simple_move(tmp_path):
    file_1 = tmp_path / 'file_1'
    file_2 = tmp_path / 'file_2'
    @py_assert1 = os.listdir
    @py_assert4 = @py_assert1(tmp_path)
    @py_assert7 = []
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=457)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
    file_1.write_text('1')
    @py_assert1 = os.listdir
    @py_assert4 = @py_assert1(tmp_path)
    @py_assert7 = [
     'file_1']
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=459)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
    move_file(file_1, file_2)
    @py_assert1 = os.listdir
    @py_assert4 = @py_assert1(tmp_path)
    @py_assert7 = [
     'file_2']
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=461)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert1 = file_2.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = '1'
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=462)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file_2) if 'file_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_2) else 'file_2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_move_file__simple_move_in_cwd(tmp_path):
    with SetWorkingDirectory(tmp_path):
        @py_assert1 = os.listdir
        @py_assert3 = '.'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = []
        @py_assert7 = @py_assert5 == @py_assert8
        if @py_assert7 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=467)
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        (tmp_path / 'file_1').write_text('1')
        @py_assert1 = os.listdir
        @py_assert3 = '.'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = [
         'file_1']
        @py_assert7 = @py_assert5 == @py_assert8
        if @py_assert7 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=469)
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        move_file('file_1', 'file_2')
        @py_assert1 = os.listdir
        @py_assert3 = '.'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = [
         'file_2']
        @py_assert7 = @py_assert5 == @py_assert8
        if @py_assert7 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=471)
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        @py_assert1 = 'file_2'
        @py_assert3 = tmp_path / @py_assert1
        @py_assert4 = @py_assert3.read_text
        @py_assert6 = @py_assert4()
        @py_assert9 = '1'
        @py_assert8 = @py_assert6 == @py_assert9
        if @py_assert8 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=472)
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).read_text\n}()\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_move_dirs__permission_denied(tmp_path):
    dst_folder = tmp_path / 'dst'
    file_1 = tmp_path / 'file'
    file_2 = dst_folder / 'file'
    file_1.write_text('1')
    @py_assert2 = 'dst'
    @py_assert4 = tmp_path / @py_assert2
    @py_assert5 = make_dirs(@py_assert4)
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=482)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py0)s((%(py1)s / %(py3)s))\n}' % {'py0':@pytest_ar._saferepr(make_dirs) if 'make_dirs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_dirs) else 'make_dirs',  'py1':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    mode = os.stat(dst_folder).st_mode
    ro_mode = mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
    os.chmod(dst_folder, ro_mode)
    with pytest.raises(IOError):
        move_file(file_1, file_2)


def test_move_file__move_to_existing_folder(tmp_path):
    @py_assert2 = 'src'
    @py_assert4 = tmp_path / @py_assert2
    @py_assert5 = make_dirs(@py_assert4)
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=493)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py0)s((%(py1)s / %(py3)s))\n}' % {'py0':@pytest_ar._saferepr(make_dirs) if 'make_dirs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_dirs) else 'make_dirs',  'py1':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert2 = 'dst'
    @py_assert4 = tmp_path / @py_assert2
    @py_assert5 = make_dirs(@py_assert4)
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=494)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py0)s((%(py1)s / %(py3)s))\n}' % {'py0':@pytest_ar._saferepr(make_dirs) if 'make_dirs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_dirs) else 'make_dirs',  'py1':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    file_1 = tmp_path / 'src' / 'file_1'
    file_2 = tmp_path / 'dst' / 'file_2'
    file_1.write_text('2')
    move_file(file_1, file_2)
    @py_assert1 = os.listdir
    @py_assert4 = file_1.parent
    @py_assert6 = @py_assert1(@py_assert4)
    @py_assert9 = []
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=500)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py5)s\n{%(py5)s = %(py3)s.parent\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(file_1) if 'file_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_1) else 'file_1',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = os.listdir
    @py_assert4 = file_2.parent
    @py_assert6 = @py_assert1(@py_assert4)
    @py_assert9 = [
     'file_2']
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=501)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py5)s\n{%(py5)s = %(py3)s.parent\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(file_2) if 'file_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_2) else 'file_2',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = file_2.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = '2'
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=502)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file_2) if 'file_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_2) else 'file_2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_move_file__move_to_new_folder(tmp_path):
    @py_assert2 = 'src'
    @py_assert4 = tmp_path / @py_assert2
    @py_assert5 = make_dirs(@py_assert4)
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=506)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py0)s((%(py1)s / %(py3)s))\n}' % {'py0':@pytest_ar._saferepr(make_dirs) if 'make_dirs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_dirs) else 'make_dirs',  'py1':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    file_1 = tmp_path / 'src' / 'file_1'
    file_2 = tmp_path / 'dst' / 'file_2'
    file_1.write_text('2')
    move_file(file_1, file_2)
    @py_assert1 = os.listdir
    @py_assert4 = file_1.parent
    @py_assert6 = @py_assert1(@py_assert4)
    @py_assert9 = []
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=513)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py5)s\n{%(py5)s = %(py3)s.parent\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(file_1) if 'file_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_1) else 'file_1',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = os.listdir
    @py_assert4 = file_2.parent
    @py_assert6 = @py_assert1(@py_assert4)
    @py_assert9 = [
     'file_2']
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=514)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py5)s\n{%(py5)s = %(py3)s.parent\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(file_2) if 'file_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_2) else 'file_2',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = file_2.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = '2'
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=515)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file_2) if 'file_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_2) else 'file_2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_move_file__move_to_different_folder(tmp_path):
    (tmp_path / 'file_1').write_text('3')
    with SetWorkingDirectory(tmp_path):
        move_file('file_1', 'dst/file_1')
    @py_assert1 = os.listdir
    @py_assert4 = @py_assert1(tmp_path)
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=524)
    if not @py_assert4:
        @py_format6 = (@pytest_ar._format_assertmsg(['dst']) + '\n>assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py3)s)\n}') % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    @py_assert1 = os.listdir
    @py_assert4 = 'dst'
    @py_assert6 = tmp_path / @py_assert4
    @py_assert7 = @py_assert1(@py_assert6)
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=525)
    if not @py_assert7:
        @py_format9 = (@pytest_ar._format_assertmsg(['file_1']) + '\n>assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}((%(py3)s / %(py5)s))\n}') % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert1 = 'dst'
    @py_assert3 = tmp_path / @py_assert1
    @py_assert4 = 'file_1'
    @py_assert6 = @py_assert3 / @py_assert4
    @py_assert7 = @py_assert6.read_text
    @py_assert9 = @py_assert7()
    @py_assert12 = '3'
    @py_assert11 = @py_assert9 == @py_assert12
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=526)
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = ((%(py0)s / %(py2)s) / %(py5)s).read_text\n}()\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None


def test_move_file__overwrite(tmp_path):
    (tmp_path / 'file_1').write_text('4')
    (tmp_path / 'file_2').write_text('5')
    with SetWorkingDirectory(tmp_path):
        move_file('file_1', 'file_2')
    @py_assert1 = os.listdir
    @py_assert4 = @py_assert1(tmp_path)
    @py_assert7 = [
     'file_2']
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=536)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert1 = 'file_2'
    @py_assert3 = tmp_path / @py_assert1
    @py_assert4 = @py_assert3.read_text
    @py_assert6 = @py_assert4()
    @py_assert9 = '4'
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=537)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).read_text\n}()\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_move_file__enoent_reraised_if_not_due_to_missing_folder():
    with pytest.raises(IOError):
        move_file('', './dst')


def test_copy_file__simple_copy(tmp_path):
    file_1 = tmp_path / 'file_1'
    file_2 = tmp_path / 'file_2'
    file_1.write_text('1')
    @py_assert1 = os.listdir
    @py_assert4 = @py_assert1(tmp_path)
    @py_assert7 = [
     'file_1']
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=554)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
    copy_file(file_1, file_2)
    @py_assert2 = os.listdir
    @py_assert5 = @py_assert2(tmp_path)
    @py_assert7 = set(@py_assert5)
    @py_assert11 = [
     'file_1', 'file_2']
    @py_assert13 = set(@py_assert11)
    @py_assert9 = @py_assert7 == @py_assert13
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=556)
    if not @py_assert9:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py6)s\n{%(py6)s = %(py3)s\n{%(py3)s = %(py1)s.listdir\n}(%(py4)s)\n})\n} == %(py14)s\n{%(py14)s = %(py10)s(%(py12)s)\n}', ), (@py_assert7, @py_assert13)) % {'py0':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py1':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None
    @py_assert1 = file_1.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = '1'
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=557)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file_1) if 'file_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_1) else 'file_1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = file_2.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = '1'
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=558)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file_2) if 'file_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_2) else 'file_2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_copy_file__simple_copy_in_cwd(tmp_path):
    file_1 = tmp_path / 'file_1'
    file_2 = tmp_path / 'file_2'
    file_1.write_text('1')
    with SetWorkingDirectory(tmp_path):
        copy_file('file_1', 'file_2')
    @py_assert2 = os.listdir
    @py_assert5 = @py_assert2(tmp_path)
    @py_assert7 = set(@py_assert5)
    @py_assert11 = [
     'file_1', 'file_2']
    @py_assert13 = set(@py_assert11)
    @py_assert9 = @py_assert7 == @py_assert13
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=569)
    if not @py_assert9:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py6)s\n{%(py6)s = %(py3)s\n{%(py3)s = %(py1)s.listdir\n}(%(py4)s)\n})\n} == %(py14)s\n{%(py14)s = %(py10)s(%(py12)s)\n}', ), (@py_assert7, @py_assert13)) % {'py0':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py1':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None
    @py_assert1 = file_1.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = '1'
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=570)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file_1) if 'file_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_1) else 'file_1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = file_2.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = '1'
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=571)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file_2) if 'file_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_2) else 'file_2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_copy_file__copy_to_existing_folder(tmp_path):
    @py_assert2 = 'src'
    @py_assert4 = tmp_path / @py_assert2
    @py_assert5 = make_dirs(@py_assert4)
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=575)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py0)s((%(py1)s / %(py3)s))\n}' % {'py0':@pytest_ar._saferepr(make_dirs) if 'make_dirs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_dirs) else 'make_dirs',  'py1':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert2 = 'dst'
    @py_assert4 = tmp_path / @py_assert2
    @py_assert5 = make_dirs(@py_assert4)
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=576)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py0)s((%(py1)s / %(py3)s))\n}' % {'py0':@pytest_ar._saferepr(make_dirs) if 'make_dirs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_dirs) else 'make_dirs',  'py1':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    file_1 = tmp_path / 'src' / 'file_1'
    file_2 = tmp_path / 'dst' / 'file_2'
    file_1.write_text('2')
    copy_file(file_1, file_2)
    @py_assert1 = os.listdir
    @py_assert4 = file_1.parent
    @py_assert6 = @py_assert1(@py_assert4)
    @py_assert9 = [
     'file_1']
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=581)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py5)s\n{%(py5)s = %(py3)s.parent\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(file_1) if 'file_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_1) else 'file_1',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = os.listdir
    @py_assert4 = file_2.parent
    @py_assert6 = @py_assert1(@py_assert4)
    @py_assert9 = [
     'file_2']
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=582)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py5)s\n{%(py5)s = %(py3)s.parent\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(file_2) if 'file_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_2) else 'file_2',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = file_1.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = '2'
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=583)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file_1) if 'file_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_1) else 'file_1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = file_2.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = '2'
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=584)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file_2) if 'file_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_2) else 'file_2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_copy_file__copy_to_new_folder(tmp_path):
    @py_assert2 = 'src'
    @py_assert4 = tmp_path / @py_assert2
    @py_assert5 = make_dirs(@py_assert4)
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=588)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py0)s((%(py1)s / %(py3)s))\n}' % {'py0':@pytest_ar._saferepr(make_dirs) if 'make_dirs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(make_dirs) else 'make_dirs',  'py1':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    file_1 = tmp_path / 'src' / 'file_1'
    file_2 = tmp_path / 'dst' / 'file_2'
    file_1.write_text('2')
    copy_file(file_1, file_2)
    @py_assert1 = os.listdir
    @py_assert4 = file_1.parent
    @py_assert6 = @py_assert1(@py_assert4)
    @py_assert9 = [
     'file_1']
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=593)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py5)s\n{%(py5)s = %(py3)s.parent\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(file_1) if 'file_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_1) else 'file_1',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = os.listdir
    @py_assert4 = file_2.parent
    @py_assert6 = @py_assert1(@py_assert4)
    @py_assert9 = [
     'file_2']
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=594)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}(%(py5)s\n{%(py5)s = %(py3)s.parent\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(file_2) if 'file_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_2) else 'file_2',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = file_1.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = '2'
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=595)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file_1) if 'file_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_1) else 'file_1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = file_2.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = '2'
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=596)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file_2) if 'file_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_2) else 'file_2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_copy_file__copy_to_different_folder(tmp_path):
    (tmp_path / 'file_1').write_text('3')
    with SetWorkingDirectory(tmp_path):
        copy_file('file_1', 'dst/file_1')
    @py_assert2 = os.listdir
    @py_assert5 = @py_assert2(tmp_path)
    @py_assert7 = set(@py_assert5)
    @py_assert11 = [
     'file_1', 'dst']
    @py_assert13 = set(@py_assert11)
    @py_assert9 = @py_assert7 == @py_assert13
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=605)
    if not @py_assert9:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py6)s\n{%(py6)s = %(py3)s\n{%(py3)s = %(py1)s.listdir\n}(%(py4)s)\n})\n} == %(py14)s\n{%(py14)s = %(py10)s(%(py12)s)\n}', ), (@py_assert7, @py_assert13)) % {'py0':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py1':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None
    @py_assert1 = os.listdir
    @py_assert4 = 'dst'
    @py_assert6 = tmp_path / @py_assert4
    @py_assert7 = @py_assert1(@py_assert6)
    @py_assert10 = [
     'file_1']
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=606)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.listdir\n}((%(py3)s / %(py5)s))\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = 'file_1'
    @py_assert3 = tmp_path / @py_assert1
    @py_assert4 = @py_assert3.read_text
    @py_assert6 = @py_assert4()
    @py_assert9 = '3'
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=607)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = (%(py0)s / %(py2)s).read_text\n}()\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = 'dst'
    @py_assert3 = tmp_path / @py_assert1
    @py_assert4 = 'file_1'
    @py_assert6 = @py_assert3 / @py_assert4
    @py_assert7 = @py_assert6.read_text
    @py_assert9 = @py_assert7()
    @py_assert12 = '3'
    @py_assert11 = @py_assert9 == @py_assert12
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=608)
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = ((%(py0)s / %(py2)s) / %(py5)s).read_text\n}()\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None


def test_copy_file__overwrite(tmp_path):
    file_1 = tmp_path / 'file_1'
    file_1.write_text('4')
    file_2 = tmp_path / 'file_2'
    file_2.write_text('5')
    with SetWorkingDirectory(tmp_path):
        copy_file('file_1', 'file_2')
    @py_assert2 = os.listdir
    @py_assert5 = @py_assert2(tmp_path)
    @py_assert7 = set(@py_assert5)
    @py_assert11 = [
     'file_1', 'file_2']
    @py_assert13 = set(@py_assert11)
    @py_assert9 = @py_assert7 == @py_assert13
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=620)
    if not @py_assert9:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(%(py6)s\n{%(py6)s = %(py3)s\n{%(py3)s = %(py1)s.listdir\n}(%(py4)s)\n})\n} == %(py14)s\n{%(py14)s = %(py10)s(%(py12)s)\n}', ), (@py_assert7, @py_assert13)) % {'py0':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py1':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None
    @py_assert1 = file_1.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = '4'
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=621)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file_1) if 'file_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_1) else 'file_1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = file_2.read_text
    @py_assert3 = @py_assert1()
    @py_assert6 = '4'
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=622)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read_text\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file_2) if 'file_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_2) else 'file_2',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_copy_file__enoent_reraised_if_not_due_to_missing_folder():
    with pytest.raises(IOError):
        copy_file('', './dst')


def test_open_ro__uncompressed():
    with open_ro(test_file('fasta_file.fasta')) as (handle):
        @py_assert1 = handle.read
        @py_assert3 = @py_assert1()
        @py_assert6 = '>This_is_FASTA!\nACGTN\n>This_is_ALSO_FASTA!\nCGTNA\n'
        @py_assert5 = @py_assert3 == @py_assert6
        if @py_assert5 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=637)
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(handle) if 'handle' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(handle) else 'handle',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_open_ro__gz():
    with open_ro(test_file('fasta_file.fasta.gz')) as (handle):
        @py_assert1 = handle.read
        @py_assert3 = @py_assert1()
        @py_assert6 = '>This_is_GZipped_FASTA!\nACGTN\n>This_is_ALSO_GZipped_FASTA!\nCGTNA\n'
        @py_assert5 = @py_assert3 == @py_assert6
        if @py_assert5 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=642)
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(handle) if 'handle' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(handle) else 'handle',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_open_ro__bz2():
    with open_ro(test_file('fasta_file.fasta.bz2')) as (handle):
        @py_assert1 = handle.read
        @py_assert3 = @py_assert1()
        @py_assert6 = '>This_is_BZ_FASTA!\nCGTNA\n>This_is_ALSO_BZ_FASTA!\nACGTN\n'
        @py_assert5 = @py_assert3 == @py_assert6
        if @py_assert5 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=650)
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(handle) if 'handle' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(handle) else 'handle',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


class OddException(RuntimeError):
    pass


def test_open_ro__close_handle_on_error():
    mocks = Mock()
    mocks.file.read.side_effect = OddException('ARGH!')
    mocks.file.__enter__ = Mock(return_value=(mocks.file))
    mocks.file.__exit__ = Mock(return_value=None)
    mocks.open.return_value = mocks.file
    with patch('builtins.open', mocks.open):
        with pytest.raises(OddException):
            open_ro('/var/abc')
    mocks.assert_has_calls([
     call.open('/var/abc', 'rb'),
     call.file.__enter__(),
     call.file.read(2),
     call.file.__exit__(ANY, ANY, ANY)])


def test_try_remove(tmp_path):
    fpath = tmp_path / 'test.txt'
    fpath.write_text('1 2 3')
    @py_assert2 = try_remove(fpath)
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=689)
    if not @py_assert2:
        @py_format4 = 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}' % {'py0':@pytest_ar._saferepr(try_remove) if 'try_remove' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(try_remove) else 'try_remove',  'py1':@pytest_ar._saferepr(fpath) if 'fpath' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fpath) else 'fpath',  'py3':@pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None
    @py_assert1 = fpath.exists
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=690)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}' % {'py0':@pytest_ar._saferepr(fpath) if 'fpath' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fpath) else 'fpath',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_try_remove__missing(tmp_path):
    fpath = tmp_path / 'test.txt'
    @py_assert2 = try_remove(fpath)
    @py_assert4 = not @py_assert2
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=695)
    if not @py_assert4:
        @py_format5 = 'assert not %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}' % {'py0':@pytest_ar._saferepr(try_remove) if 'try_remove' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(try_remove) else 'try_remove',  'py1':@pytest_ar._saferepr(fpath) if 'fpath' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fpath) else 'fpath',  'py3':@pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert2 = @py_assert4 = None
    @py_assert1 = fpath.exists
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=696)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}' % {'py0':@pytest_ar._saferepr(fpath) if 'fpath' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fpath) else 'fpath',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_try_remove__non_file(tmp_path):
    with pytest.raises(OSError):
        try_remove(tmp_path)


def test_try_rmtree(tmp_path):
    fpath = tmp_path / 'testdir'
    os.mkdir(fpath)
    (fpath / 'file').write_text('1 2 3')
    @py_assert2 = try_rmtree(fpath)
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=713)
    if not @py_assert2:
        @py_format4 = 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}' % {'py0':@pytest_ar._saferepr(try_rmtree) if 'try_rmtree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(try_rmtree) else 'try_rmtree',  'py1':@pytest_ar._saferepr(fpath) if 'fpath' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fpath) else 'fpath',  'py3':@pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None
    @py_assert1 = fpath.exists
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=714)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}' % {'py0':@pytest_ar._saferepr(fpath) if 'fpath' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fpath) else 'fpath',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_try_treedir__missing(tmp_path):
    fpath = tmp_path / 'testdir'
    @py_assert2 = try_rmtree(fpath)
    @py_assert4 = not @py_assert2
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=719)
    if not @py_assert4:
        @py_format5 = 'assert not %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}' % {'py0':@pytest_ar._saferepr(try_rmtree) if 'try_rmtree' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(try_rmtree) else 'try_rmtree',  'py1':@pytest_ar._saferepr(fpath) if 'fpath' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fpath) else 'fpath',  'py3':@pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert2 = @py_assert4 = None
    @py_assert1 = fpath.exists
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=720)
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}' % {'py0':@pytest_ar._saferepr(fpath) if 'fpath' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fpath) else 'fpath',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_describe_files__no_files():
    @py_assert1 = ()
    @py_assert3 = describe_files(@py_assert1)
    @py_assert6 = 'No files'
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=729)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(describe_files) if 'describe_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(describe_files) else 'describe_files',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_describe_files__single_file():
    fpath = '/var/foo/bar'
    @py_assert1 = (fpath,)
    @py_assert3 = describe_files(@py_assert1)
    @py_assert8 = repr(fpath)
    @py_assert5 = @py_assert3 == @py_assert8
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=734)
    if not @py_assert5:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py9)s\n{%(py9)s = %(py6)s(%(py7)s)\n}', ), (@py_assert3, @py_assert8)) % {'py0':@pytest_ar._saferepr(describe_files) if 'describe_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(describe_files) else 'describe_files',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr',  'py7':@pytest_ar._saferepr(fpath) if 'fpath' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fpath) else 'fpath',  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = None


def test_describe_files__same_path_abs__3_differences():
    fpaths = ('/var/foo/bar', '/var/foo/foo')
    @py_assert2 = describe_files(fpaths)
    @py_assert5 = "2 files in '/var/foo'"
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=739)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(describe_files) if 'describe_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(describe_files) else 'describe_files',  'py1':@pytest_ar._saferepr(fpaths) if 'fpaths' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fpaths) else 'fpaths',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_describe_files__same_path_abs__2_differences():
    fpaths = ('/var/foo/faz', '/var/foo/foo')
    @py_assert2 = describe_files(fpaths)
    @py_assert5 = "'/var/foo/f??'"
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=744)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(describe_files) if 'describe_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(describe_files) else 'describe_files',  'py1':@pytest_ar._saferepr(fpaths) if 'fpaths' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fpaths) else 'fpaths',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_describe_files__same_path_abs__1_differences():
    fpaths = ('/var/foo/faz', '/var/foo/fao')
    @py_assert2 = describe_files(fpaths)
    @py_assert5 = "'/var/foo/fa?'"
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=749)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(describe_files) if 'describe_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(describe_files) else 'describe_files',  'py1':@pytest_ar._saferepr(fpaths) if 'fpaths' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fpaths) else 'fpaths',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_describe_files__different_paths_abs():
    fpaths = ('/var/foo/bar', '/var/bar/foo')
    @py_assert2 = describe_files(fpaths)
    @py_assert5 = '2 files'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=754)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(describe_files) if 'describe_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(describe_files) else 'describe_files',  'py1':@pytest_ar._saferepr(fpaths) if 'fpaths' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fpaths) else 'fpaths',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_describe_files__same_path_rel():
    fpaths = ('var/foo/bar', 'var/foo/foo')
    @py_assert2 = describe_files(fpaths)
    @py_assert5 = "2 files in 'var/foo'"
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=759)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(describe_files) if 'describe_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(describe_files) else 'describe_files',  'py1':@pytest_ar._saferepr(fpaths) if 'fpaths' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fpaths) else 'fpaths',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_describe_files__different_paths_rel():
    fpaths = ('var/foo/bar', 'var/bar/foo')
    @py_assert2 = describe_files(fpaths)
    @py_assert5 = '2 files'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=764)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(describe_files) if 'describe_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(describe_files) else 'describe_files',  'py1':@pytest_ar._saferepr(fpaths) if 'fpaths' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fpaths) else 'fpaths',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_describe_files__iterable():
    fpaths = iter(('/var/foo/bar', '/var/foo/foo'))
    @py_assert2 = describe_files(fpaths)
    @py_assert5 = "2 files in '/var/foo'"
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=769)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(describe_files) if 'describe_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(describe_files) else 'describe_files',  'py1':@pytest_ar._saferepr(fpaths) if 'fpaths' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fpaths) else 'fpaths',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_describe_files__none_files():
    with pytest.raises(ValueError):
        describe_files(None)


def test_describe_paired_files__single_file():
    fpath = '/var/foo/bar'
    @py_assert1 = (fpath,)
    @py_assert3 = ()
    @py_assert5 = describe_paired_files(@py_assert1, @py_assert3)
    @py_assert10 = repr(fpath)
    @py_assert7 = @py_assert5 == @py_assert10
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=784)
    if not @py_assert7:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py11)s\n{%(py11)s = %(py8)s(%(py9)s)\n}', ), (@py_assert5, @py_assert10)) % {'py0':@pytest_ar._saferepr(describe_paired_files) if 'describe_paired_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(describe_paired_files) else 'describe_paired_files',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr',  'py9':@pytest_ar._saferepr(fpath) if 'fpath' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fpath) else 'fpath',  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert10 = None


def test_describe_paired_files__identical_files():
    fpath = '/var/foo/bar'
    ftuple = (fpath,)
    @py_assert3 = describe_paired_files(ftuple, ftuple)
    @py_assert8 = repr(fpath)
    @py_assert5 = @py_assert3 == @py_assert8
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=790)
    if not @py_assert5:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py9)s\n{%(py9)s = %(py6)s(%(py7)s)\n}', ), (@py_assert3, @py_assert8)) % {'py0':@pytest_ar._saferepr(describe_paired_files) if 'describe_paired_files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(describe_paired_files) else 'describe_paired_files',  'py1':@pytest_ar._saferepr(ftuple) if 'ftuple' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ftuple) else 'ftuple',  'py2':@pytest_ar._saferepr(ftuple) if 'ftuple' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ftuple) else 'ftuple',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr',  'py7':@pytest_ar._saferepr(fpath) if 'fpath' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fpath) else 'fpath',  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert3 = @py_assert5 = @py_assert8 = None


def test_describe_paired_files__same_path__similar_files():
    files_1 = ('foo/1_abc', 'foo/1_def')
    files_2 = ('foo/1_ghi', 'foo/1_jkl')
    expected = "'foo/1_???'"
    result = describe_paired_files(files_1, files_2)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=798)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_describe_paired_files__same_path__similar_files__different_prefixes():
    files_1 = ('foo/1_abc', 'foo/1_def')
    files_2 = ('foo/2_ghi', 'foo/2_jkl')
    expected = "'foo/[12]_???'"
    result = describe_paired_files(files_1, files_2)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=806)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_describe_paired_files__same_path__similar_files__too_different():
    files_1 = ('foo/1a_abc', 'foo/1a_def')
    files_2 = ('foo/2b_ghi', 'foo/2b_jkl')
    expected = "2 pair(s) of files in 'foo'"
    result = describe_paired_files(files_1, files_2)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=814)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_describe_paired_files__same_path__different_files():
    files_1 = ('foo/1_abc', 'foo/2_def')
    files_2 = ('foo/3_ghi', 'foo/4_jkl')
    expected = "2 pair(s) of files in 'foo'"
    result = describe_paired_files(files_1, files_2)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=822)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_describe_paired_files__same_path__different_file_lens():
    files_1 = ('foo/1_a', 'foo/2_de')
    files_2 = ('foo/3_g', 'foo/4_jk')
    expected = "2 pair(s) of files in 'foo'"
    result = describe_paired_files(files_1, files_2)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=830)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_describe_paired_files__different_path_and_files():
    files_1 = ('foo/1_abc', 'bar/2_def')
    files_2 = ('zed/3_ghi', 'not/4_jkl')
    expected = '2 pair(s) of files'
    result = describe_paired_files(files_1, files_2)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/fileutils_test.py', lineno=838)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_describe_paired_files__files_1_longer():
    with pytest.raises(ValueError):
        describe_paired_files(('a', 'b'), ('c', ))


def test_describe_paired_files__files_2_longer():
    with pytest.raises(ValueError):
        describe_paired_files(('a', ), ('b', 'c'))


def test_describe_paired_files__none_files():
    with pytest.raises(ValueError):
        describe_paired_files(None, None)


def test_describe_paired_files__none_files_1():
    with pytest.raises(ValueError):
        describe_paired_files(None, ())


def test_describe_paired_files__none_files_2():
    with pytest.raises(ValueError):
        describe_paired_files((), None)