# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johngiorgi/Documents/Masters/Class/natural_language_computing/project/saber/saber/tests/test_data_utils.py
# Compiled at: 2018-11-03 12:42:23
# Size of source mod 2**32: 7826 bytes
"""Any and all unit tests for the data_utils (saber/utils/data_utils.py).
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, numpy as np, pytest
from ..config import Config
from ..dataset import Dataset
from ..utils import data_utils
from .resources.dummy_constants import *

@pytest.fixture
def dummy_config():
    """Returns an instance of a Config object."""
    dummy_config = Config(PATH_TO_DUMMY_CONFIG)
    return dummy_config


@pytest.fixture
def dummy_dataset_1():
    """Returns a single dummy Dataset instance after calling Dataset.load().
    """
    dataset = Dataset(directory=PATH_TO_DUMMY_DATASET_1, replace_rare_tokens=False)
    dataset.load()
    return dataset


@pytest.fixture
def dummy_dataset_2():
    """Returns a single dummy Dataset instance after calling `Dataset.load()`.
    """
    dataset = Dataset(directory=PATH_TO_DUMMY_DATASET_2, replace_rare_tokens=False)
    dataset.load()
    return dataset


@pytest.fixture
def dummy_compound_dataset(dummy_config):
    """
    """
    dummy_config.dataset_folder = [
     PATH_TO_DUMMY_DATASET_1, PATH_TO_DUMMY_DATASET_2]
    dummy_config.replace_rare_tokens = False
    dataset = data_utils.load_compound_dataset(dummy_config)
    return dataset


@pytest.fixture(scope='session')
def dummy_dataset_paths_all(tmpdir_factory):
    """Creates and returns the path to a temporary dataset folder, and train, valid, test files.
    """
    dummy_dir = tmpdir_factory.mktemp('dummy_dataset')
    train_file = dummy_dir.join('train.tsv')
    train_file.write('arbitrary')
    valid_file = dummy_dir.join('valid.tsv')
    valid_file.write('arbitrary')
    test_file = dummy_dir.join('test.tsv')
    test_file.write('arbitrary')
    return (
     dummy_dir.strpath, train_file.strpath, valid_file.strpath, test_file.strpath)


@pytest.fixture(scope='session')
def dummy_dataset_paths_no_valid(tmpdir_factory):
    """Creates and returns the path to a temporary dataset folder, and train, and test files.
    """
    dummy_dir = tmpdir_factory.mktemp('dummy_dataset')
    train_file = dummy_dir.join('train.tsv')
    train_file.write('arbitrary')
    test_file = dummy_dir.join('test.tsv')
    test_file.write('arbitrary')
    return (
     dummy_dir.strpath, train_file.strpath, test_file.strpath)


def test_get_filepaths_value_error(tmpdir):
    """Asserts that a ValueError is raised when `data_utils.get_filepaths(tmpdir)` is called and
    no file '<tmpdir>/train.*' exists.
    """
    with pytest.raises(ValueError):
        data_utils.get_filepaths(tmpdir.strpath)


def test_get_filepaths_all(dummy_dataset_paths_all):
    """Asserts that `data_utils.get_filepaths()` returns the expected filepaths when all partitions
    (train/test/valid) are provided.
    """
    dummy_dataset_directory, train_filepath, valid_filepath, test_filepath = dummy_dataset_paths_all
    expected = {'train':train_filepath,  'valid':valid_filepath, 
     'test':test_filepath}
    actual = data_utils.get_filepaths(dummy_dataset_directory)
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_get_filepaths_no_valid(dummy_dataset_paths_no_valid):
    """Asserts that `data_utils.get_filepaths()` returns the expected filepaths when train and
    test partitions are provided.
    """
    dummy_dataset_directory, train_filepath, test_filepath = dummy_dataset_paths_no_valid
    expected = {'train':train_filepath,  'valid':None, 
     'test':test_filepath}
    actual = data_utils.get_filepaths(dummy_dataset_directory)
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_load_single_dataset(dummy_config, dummy_dataset_1):
    """Asserts that `data_utils.load_single_dataset()` returns the expected value.
    """
    actual = data_utils.load_single_dataset(dummy_config)
    expected = [dummy_dataset_1]
    @py_assert3 = isinstance(actual, list)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py2':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert2 = len(actual)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert1 = actual[0]
    @py_assert4 = isinstance(@py_assert1, Dataset)
    if not @py_assert4:
        @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(Dataset) if 'Dataset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Dataset) else 'Dataset',  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    @py_assert1 = actual[0]
    @py_assert3 = @py_assert1.__dict__
    @py_assert5 = dir(@py_assert3)
    @py_assert9 = expected[0]
    @py_assert11 = @py_assert9.__dict__
    @py_assert13 = dir(@py_assert11)
    @py_assert7 = @py_assert5 == @py_assert13
    if not @py_assert7:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py2)s.__dict__\n})\n} == %(py14)s\n{%(py14)s = %(py8)s(%(py12)s\n{%(py12)s = %(py10)s.__dict__\n})\n}', ), (@py_assert5, @py_assert13)) % {'py0':@pytest_ar._saferepr(dir) if 'dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dir) else 'dir',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(dir) if 'dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dir) else 'dir',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None


def test_load_compound_dataset_unchanged_attributes(dummy_dataset_1, dummy_dataset_2, dummy_compound_dataset):
    """Asserts that attributes of `Dataset` objects which are expected to remain unchanged
    are unchanged after call to `data_utils.load_compound_dataset()`.
    """
    actual = dummy_compound_dataset
    expected = [dummy_dataset_1, dummy_dataset_2]
    @py_assert3 = isinstance(actual, list)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py2':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert2 = len(actual)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert1 = [isinstance(ds, Dataset) for ds in actual]
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = actual[0]
    @py_assert2 = @py_assert0.directory
    @py_assert5 = expected[0]
    @py_assert7 = @py_assert5.directory
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.directory\n} == %(py8)s\n{%(py8)s = %(py6)s.directory\n}', ), (@py_assert2, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = None
    @py_assert0 = actual[0]
    @py_assert2 = @py_assert0.replace_rare_tokens
    @py_assert5 = expected[0]
    @py_assert7 = @py_assert5.replace_rare_tokens
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.replace_rare_tokens\n} == %(py8)s\n{%(py8)s = %(py6)s.replace_rare_tokens\n}', ), (@py_assert2, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = None
    @py_assert0 = actual[0]
    @py_assert2 = @py_assert0.type_seq
    @py_assert5 = expected[0]
    @py_assert7 = @py_assert5.type_seq
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.type_seq\n} == %(py8)s\n{%(py8)s = %(py6)s.type_seq\n}', ), (@py_assert2, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = None
    @py_assert0 = actual[0].type_to_idx['tag']
    @py_assert3 = expected[0].type_to_idx['tag']
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = actual[0]
    @py_assert2 = @py_assert0.idx_to_tag
    @py_assert5 = expected[0]
    @py_assert7 = @py_assert5.idx_to_tag
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.idx_to_tag\n} == %(py8)s\n{%(py8)s = %(py6)s.idx_to_tag\n}', ), (@py_assert2, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = None
    @py_assert0 = actual[(-1)]
    @py_assert2 = @py_assert0.directory
    @py_assert5 = expected[(-1)]
    @py_assert7 = @py_assert5.directory
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.directory\n} == %(py8)s\n{%(py8)s = %(py6)s.directory\n}', ), (@py_assert2, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = None
    @py_assert0 = actual[(-1)]
    @py_assert2 = @py_assert0.replace_rare_tokens
    @py_assert5 = expected[(-1)]
    @py_assert7 = @py_assert5.replace_rare_tokens
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.replace_rare_tokens\n} == %(py8)s\n{%(py8)s = %(py6)s.replace_rare_tokens\n}', ), (@py_assert2, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = None
    @py_assert0 = actual[(-1)]
    @py_assert2 = @py_assert0.type_seq
    @py_assert5 = expected[(-1)]
    @py_assert7 = @py_assert5.type_seq
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.type_seq\n} == %(py8)s\n{%(py8)s = %(py6)s.type_seq\n}', ), (@py_assert2, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = None
    @py_assert0 = actual[(-1)].type_to_idx['tag']
    @py_assert3 = expected[(-1)].type_to_idx['tag']
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = actual[(-1)]
    @py_assert2 = @py_assert0.idx_to_tag
    @py_assert5 = expected[(-1)]
    @py_assert7 = @py_assert5.idx_to_tag
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.idx_to_tag\n} == %(py8)s\n{%(py8)s = %(py6)s.idx_to_tag\n}', ), (@py_assert2, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = None


def test_load_compound_dataset_changed_attributes(dummy_dataset_1, dummy_dataset_2, dummy_compound_dataset):
    """Asserts that attributes of `Dataset` objects which are expected to be changed are changed
    after call to `data_utils.load_compound_dataset()`.
    """
    actual = dummy_compound_dataset
    expected = [dummy_dataset_1, dummy_dataset_2]
    @py_assert3 = isinstance(actual, list)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py2':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert2 = len(actual)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert1 = [isinstance(ds, Dataset) for ds in actual]
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = actual[0].type_to_idx['word']
    @py_assert3 = actual[(-1)].type_to_idx['word']
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = actual[0].type_to_idx['char']
    @py_assert3 = actual[(-1)].type_to_idx['char']
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_setup_dataset_for_transfer(dummy_dataset_1, dummy_dataset_2):
    """Asserts that the `type_to_idx` attribute of a "source" dataset and a "target" dataset are
    as expected after call to `data_utils.setup_dataset_for_transfer()`.
    """
    source_type_to_idx = dummy_dataset_1.type_to_idx
    data_utils.setup_dataset_for_transfer(dummy_dataset_2, source_type_to_idx)
    @py_assert1 = (dummy_dataset_2.type_to_idx[type_] == source_type_to_idx[type_] for type_ in ('word',
                                                                                                 'char'))
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None