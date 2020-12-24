# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/test_test_utils.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 535 bytes
"""Tests for the test utils module."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from .utils import RegexCompare

def test_use_of_regex_compare():
    regex_compare = RegexCompare('test')
    @py_assert2 = 'test'
    @py_assert1 = regex_compare == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (regex_compare, @py_assert2)) % {'py0':@pytest_ar._saferepr(regex_compare) if 'regex_compare' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(regex_compare) else 'regex_compare',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert0 = 'test'
    @py_assert2 = @py_assert0 == regex_compare
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, regex_compare)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(regex_compare) if 'regex_compare' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(regex_compare) else 'regex_compare'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'ttest'
    @py_assert2 = @py_assert0 == regex_compare
    @py_assert6 = not @py_assert2
    if not @py_assert6:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, regex_compare)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(regex_compare) if 'regex_compare' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(regex_compare) else 'regex_compare'}
        @py_format7 = 'assert not %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert6 = None


def test_more_complicated_regex_comparisons():
    regex_compare = RegexCompare('\\[Compiling\\] .+test\\.template"')
    @py_assert2 = '[Compiling] something "/a/b/c/test.template"'
    @py_assert1 = regex_compare == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (regex_compare, @py_assert2)) % {'py0':@pytest_ar._saferepr(regex_compare) if 'regex_compare' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(regex_compare) else 'regex_compare',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = '[Compiling] something "/a/b/c/test.templates"'
    @py_assert1 = regex_compare == @py_assert2
    @py_assert6 = not @py_assert1
    if not @py_assert6:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (regex_compare, @py_assert2)) % {'py0':@pytest_ar._saferepr(regex_compare) if 'regex_compare' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(regex_compare) else 'regex_compare',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format7 = 'assert not %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert2 = @py_assert6 = None