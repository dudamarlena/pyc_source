# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johngiorgi/Documents/Masters/Class/natural_language_computing/project/saber/saber/tests/test_generic_utils.py
# Compiled at: 2018-11-03 12:42:23
# Size of source mod 2**32: 5392 bytes
"""Any and all unit tests for the generic_utils (saber/utils/generic_utils.py).
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, pytest
from ..config import Config
from ..utils import generic_utils
from .resources.dummy_constants import *

@pytest.fixture(scope='session')
def dummy_dir(tmpdir_factory):
    """Returns the path to a temporary directory.
    """
    dummy_dir = tmpdir_factory.mktemp('dummy_dir')
    return dummy_dir.strpath


@pytest.fixture
def dummy_config():
    """Returns an instance of a Config object."""
    dummy_config = Config(PATH_TO_DUMMY_CONFIG)
    return dummy_config


def test_is_consecutive_empty():
    """Asserts that `generic_utils.is_consecutive()` returns the expected value when passed an
    empty list.
    """
    test = []
    expected = True
    actual = generic_utils.is_consecutive(test)
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_is_consecutive_simple_sorted_list_no_duplicates():
    """Asserts that `generic_utils.is_consecutive()` returns the expected value when passed a
    simple sorted list with no duplicates.
    """
    test_true = [
     0, 1, 2, 3, 4, 5]
    test_false = [1, 2, 3, 4, 5, 6]
    expected_true = True
    expected_false = False
    actual_true = generic_utils.is_consecutive(test_true)
    actual_false = generic_utils.is_consecutive(test_false)
    @py_assert1 = actual_true == expected_true
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual_true, expected_true)) % {'py0':@pytest_ar._saferepr(actual_true) if 'actual_true' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_true) else 'actual_true',  'py2':@pytest_ar._saferepr(expected_true) if 'expected_true' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_true) else 'expected_true'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = actual_false == expected_false
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual_false, expected_false)) % {'py0':@pytest_ar._saferepr(actual_false) if 'actual_false' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_false) else 'actual_false',  'py2':@pytest_ar._saferepr(expected_false) if 'expected_false' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_false) else 'expected_false'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_is_consecutive_simple_unsorted_list_no_duplicates():
    """Asserts that `generic_utils.is_consecutive()` returns the expected value when passed a
    simple unsorted list with no duplicates.
    """
    test_true = [
     0, 1, 3, 2, 4, 5]
    test_false = [1, 2, 4, 3, 5, 6]
    expected_true = True
    expected_false = False
    actual_true = generic_utils.is_consecutive(test_true)
    actual_false = generic_utils.is_consecutive(test_false)
    @py_assert1 = actual_true == expected_true
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual_true, expected_true)) % {'py0':@pytest_ar._saferepr(actual_true) if 'actual_true' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_true) else 'actual_true',  'py2':@pytest_ar._saferepr(expected_true) if 'expected_true' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_true) else 'expected_true'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = actual_false == expected_false
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual_false, expected_false)) % {'py0':@pytest_ar._saferepr(actual_false) if 'actual_false' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_false) else 'actual_false',  'py2':@pytest_ar._saferepr(expected_false) if 'expected_false' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_false) else 'expected_false'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_is_consecutive_simple_sorted_list_duplicates():
    """Asserts that `generic_utils.is_consecutive()` returns the expected value when passed a
    simple sorted list with duplicates.
    """
    test = [
     0, 1, 2, 3, 3, 4, 5]
    expected = False
    actual = generic_utils.is_consecutive(test)
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_is_consecutive_simple_unsorted_list_duplicates():
    """Asserts that `generic_utils.is_consecutive()` returns the expected value when passed a
    simple unsorted list with duplicates.
    """
    test = [
     0, 1, 4, 3, 3, 2, 5]
    expected = False
    actual = generic_utils.is_consecutive(test)
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_is_consecutive_simple_dict_no_duplicates():
    """Asserts that `generic_utils.is_consecutive()` returns the expected value when passed a
    dictionaries values no duplicates.
    """
    test_true = {'a':0, 
     'b':1,  'c':2,  'd':3,  'e':4,  'f':5}
    test_false = {'a':1,  'b':2,  'c':3,  'd':4,  'e':5,  'f':6}
    expected_true = True
    expected_false = False
    actual_true = generic_utils.is_consecutive(test_true.values())
    actual_false = generic_utils.is_consecutive(test_false.values())
    @py_assert1 = actual_true == expected_true
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual_true, expected_true)) % {'py0':@pytest_ar._saferepr(actual_true) if 'actual_true' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_true) else 'actual_true',  'py2':@pytest_ar._saferepr(expected_true) if 'expected_true' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_true) else 'expected_true'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = actual_false == expected_false
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual_false, expected_false)) % {'py0':@pytest_ar._saferepr(actual_false) if 'actual_false' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_false) else 'actual_false',  'py2':@pytest_ar._saferepr(expected_false) if 'expected_false' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_false) else 'expected_false'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_is_consecutive_simple_dict_duplicates():
    """Asserts that `generic_utils.is_consecutive()` returns the expected value when passed a
    dictionaries values with duplicates.
    """
    test = {'a':0, 
     'b':1,  'c':2,  'd':3,  'e':3,  'f':4,  'g':5}
    expected = False
    actual = generic_utils.is_consecutive(test)
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_reverse_dict_empty():
    """Asserts that `generic_utils.reverse_dictionary()` returns the expected value when given an
    empty dictionary.
    """
    test = {}
    expected = {}
    actual = generic_utils.reverse_dict(test)
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_reverse_mapping_simple():
    """Asserts that `generic_utils.reverse_dictionary()` returns the expected value when given a
    simply dictionary.
    """
    test = {'a':1, 
     'b':2,  'c':3}
    expected = {1:'a', 
     2:'b',  3:'c'}
    actual = generic_utils.reverse_dict(test)
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_make_dir_new(tmpdir):
    """Assert that `generic_utils.make_dir()` creates a directory as expected when it does not
    already exist.
    """
    dummy_dirpath = os.path.join(tmpdir.strpath, 'dummy_dir')
    generic_utils.make_dir(dummy_dirpath)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.isdir
    @py_assert6 = @py_assert3(dummy_dirpath)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.isdir\n}(%(py5)s)\n}' % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(dummy_dirpath) if 'dummy_dirpath' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_dirpath) else 'dummy_dirpath',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None


def test_make_dir_exists(dummy_dir):
    """Assert that `generic_utils.make_dir()` fails silently when trying to create a directory that
    already exists.
    """
    generic_utils.make_dir(dummy_dir)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.isdir
    @py_assert6 = @py_assert3(dummy_dir)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.isdir\n}(%(py5)s)\n}' % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(dummy_dir) if 'dummy_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_dir) else 'dummy_dir',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None


def test_clean_path():
    """Asserts that filepath returned by `generic_utils.clean_path()` is as expected.
    """
    test = ' this/is//a/test/     '
    expected = os.path.abspath('this/is/a/test')
    @py_assert1 = generic_utils.clean_path
    @py_assert4 = @py_assert1(test)
    @py_assert6 = @py_assert4 == expected
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.clean_path\n}(%(py3)s)\n} == %(py7)s', ), (@py_assert4, expected)) % {'py0':@pytest_ar._saferepr(generic_utils) if 'generic_utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(generic_utils) else 'generic_utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(test) if 'test' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test) else 'test',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert6 = None


def test_decompress_model():
    """Asserts that `generic_utils.decompress_model()` decompresses a given directory.
    """
    pass


def test_compress_model():
    """Asserts that `generic_utils.compress_model()` compresses a given directory.
    """
    pass