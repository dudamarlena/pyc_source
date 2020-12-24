# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johngiorgi/Documents/Masters/Class/natural_language_computing/project/saber/saber/tests/test_dataset.py
# Compiled at: 2018-12-17 16:56:04
# Size of source mod 2**32: 9923 bytes
"""Contains any and all unit tests for the `Dataset` class (saber/dataset.py).
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, numpy as np
from nltk.corpus.reader.conll import ConllCorpusReader
import pytest
from .. import constants
from ..dataset import Dataset
from ..utils import generic_utils
from .resources.dummy_constants import *

@pytest.fixture
def empty_dummy_dataset():
    """Returns an empty single dummy Dataset instance.
    """
    return Dataset(directory=PATH_TO_DUMMY_DATASET_1, replace_rare_tokens=False, totally_arbitrary='arbitrary')


@pytest.fixture
def loaded_dummy_dataset():
    """Returns a single dummy Dataset instance after calling Dataset.load().
    """
    dataset = Dataset(directory=PATH_TO_DUMMY_DATASET_1, replace_rare_tokens=False)
    dataset.load()
    return dataset


def test_attributes_after_initilization_of_dataset(empty_dummy_dataset):
    """Asserts instance attributes are initialized correctly when dataset is empty (i.e.,
    `Dataset.load()` has not been called).
    """
    for partition in empty_dummy_dataset.directory:
        expected = os.path.join(PATH_TO_DUMMY_DATASET_1, '{}.tsv'.format(partition))
        @py_assert0 = empty_dummy_dataset.directory[partition]
        @py_assert2 = @py_assert0 == expected
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, expected)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None

    @py_assert1 = empty_dummy_dataset.replace_rare_tokens
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = 'assert not %(py2)s\n{%(py2)s = %(py0)s.replace_rare_tokens\n}' % {'py0':@pytest_ar._saferepr(empty_dummy_dataset) if 'empty_dummy_dataset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(empty_dummy_dataset) else 'empty_dummy_dataset',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = empty_dummy_dataset.conll_parser
    @py_assert3 = @py_assert1.root
    @py_assert5 = @py_assert3 == PATH_TO_DUMMY_DATASET_1
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.conll_parser\n}.root\n} == %(py6)s', ), (@py_assert3, PATH_TO_DUMMY_DATASET_1)) % {'py0':@pytest_ar._saferepr(empty_dummy_dataset) if 'empty_dummy_dataset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(empty_dummy_dataset) else 'empty_dummy_dataset',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(PATH_TO_DUMMY_DATASET_1) if 'PATH_TO_DUMMY_DATASET_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(PATH_TO_DUMMY_DATASET_1) else 'PATH_TO_DUMMY_DATASET_1'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = empty_dummy_dataset.type_seq
    @py_assert4 = {'train':None, 
     'valid':None,  'test':None}
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.type_seq\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(empty_dummy_dataset) if 'empty_dummy_dataset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(empty_dummy_dataset) else 'empty_dummy_dataset',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = empty_dummy_dataset.type_to_idx
    @py_assert4 = {'word':None, 
     'char':None,  'tag':None}
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.type_to_idx\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(empty_dummy_dataset) if 'empty_dummy_dataset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(empty_dummy_dataset) else 'empty_dummy_dataset',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = empty_dummy_dataset.idx_to_tag
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.idx_to_tag\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(empty_dummy_dataset) if 'empty_dummy_dataset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(empty_dummy_dataset) else 'empty_dummy_dataset',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = empty_dummy_dataset.idx_seq
    @py_assert4 = {'train':None, 
     'valid':None,  'test':None}
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.idx_seq\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(empty_dummy_dataset) if 'empty_dummy_dataset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(empty_dummy_dataset) else 'empty_dummy_dataset',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = empty_dummy_dataset.totally_arbitrary
    @py_assert4 = 'arbitrary'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.totally_arbitrary\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(empty_dummy_dataset) if 'empty_dummy_dataset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(empty_dummy_dataset) else 'empty_dummy_dataset',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_value_error_load(empty_dummy_dataset):
    """Asserts that `Dataset.load()` raises a ValueError when `Dataset.directory` is None.
    """
    empty_dummy_dataset.directory = None
    with pytest.raises(ValueError):
        empty_dummy_dataset.load()


def test_get_types_single_dataset(empty_dummy_dataset):
    """Asserts that `Dataset._get_types()` returns the expected values.
    """
    actual = empty_dummy_dataset._get_types()
    expected = {'word':DUMMY_WORD_TYPES,  'char':DUMMY_CHAR_TYPES,  'tag':DUMMY_TAG_TYPES}
    @py_assert1 = (actual['word'].sort() == v.sort() for k, v in expected.items())
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_get_type_seq_single_dataset_before_load(empty_dummy_dataset):
    """Asserts that `Dataset.type_seq` is updated as expected after call to
    `Dataset._get_type_seq()`.
    """
    empty_dummy_dataset._get_type_seq()
    @py_assert1 = np.array_equal
    @py_assert3 = empty_dummy_dataset.type_seq['train']['word']
    @py_assert6 = @py_assert1(@py_assert3, DUMMY_WORD_SEQ)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.array_equal\n}(%(py4)s, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(DUMMY_WORD_SEQ) if 'DUMMY_WORD_SEQ' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DUMMY_WORD_SEQ) else 'DUMMY_WORD_SEQ',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    @py_assert1 = np.array_equal
    @py_assert3 = empty_dummy_dataset.type_seq['train']['char']
    @py_assert6 = @py_assert1(@py_assert3, DUMMY_CHAR_SEQ)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.array_equal\n}(%(py4)s, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(DUMMY_CHAR_SEQ) if 'DUMMY_CHAR_SEQ' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DUMMY_CHAR_SEQ) else 'DUMMY_CHAR_SEQ',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    @py_assert1 = np.array_equal
    @py_assert3 = empty_dummy_dataset.type_seq['train']['tag']
    @py_assert6 = @py_assert1(@py_assert3, DUMMY_TAG_SEQ)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.array_equal\n}(%(py4)s, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(DUMMY_TAG_SEQ) if 'DUMMY_TAG_SEQ' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DUMMY_TAG_SEQ) else 'DUMMY_TAG_SEQ',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None


def test_get_idx_maps_single_dataset_before_load(empty_dummy_dataset):
    """Asserts that `Dataset.type_to_idx` is updated as expected after successive calls to
    `Dataset._get_types()` and `Dataset._get_idx_maps()`.
    """
    types = empty_dummy_dataset._get_types()
    empty_dummy_dataset._get_idx_maps(types)
    @py_assert1 = generic_utils.is_consecutive
    @py_assert3 = empty_dummy_dataset.type_to_idx['word']
    @py_assert5 = @py_assert3.values
    @py_assert7 = @py_assert5()
    @py_assert9 = @py_assert1(@py_assert7)
    if not @py_assert9:
        @py_format11 = 'assert %(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.is_consecutive\n}(%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.values\n}()\n})\n}' % {'py0':@pytest_ar._saferepr(generic_utils) if 'generic_utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(generic_utils) else 'generic_utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = generic_utils.is_consecutive
    @py_assert3 = empty_dummy_dataset.type_to_idx['char']
    @py_assert5 = @py_assert3.values
    @py_assert7 = @py_assert5()
    @py_assert9 = @py_assert1(@py_assert7)
    if not @py_assert9:
        @py_format11 = 'assert %(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.is_consecutive\n}(%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.values\n}()\n})\n}' % {'py0':@pytest_ar._saferepr(generic_utils) if 'generic_utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(generic_utils) else 'generic_utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = generic_utils.is_consecutive
    @py_assert3 = empty_dummy_dataset.type_to_idx['tag']
    @py_assert5 = @py_assert3.values
    @py_assert7 = @py_assert5()
    @py_assert9 = @py_assert1(@py_assert7)
    if not @py_assert9:
        @py_format11 = 'assert %(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.is_consecutive\n}(%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.values\n}()\n})\n}' % {'py0':@pytest_ar._saferepr(generic_utils) if 'generic_utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(generic_utils) else 'generic_utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = (key in DUMMY_WORD_TYPES for key in empty_dummy_dataset.type_to_idx['word'])
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (key in DUMMY_CHAR_TYPES for key in empty_dummy_dataset.type_to_idx['char'])
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (key in DUMMY_TAG_TYPES for key in empty_dummy_dataset.type_to_idx['tag'])
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_get_idx_maps_single_dataset_before_load_special_tokens(empty_dummy_dataset):
    """Asserts that `Dataset.type_to_idx` contains the special tokens as keys with expected values
     after successive calls to `Dataset._get_types()` and `Dataset._get_idx_maps()`.
    """
    types = empty_dummy_dataset._get_types()
    empty_dummy_dataset._get_idx_maps(types)
    @py_assert1 = (empty_dummy_dataset.type_to_idx['word'][k] == v for k, v in constants.INITIAL_MAPPING['word'].items())
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (empty_dummy_dataset.type_to_idx['char'][k] == v for k, v in constants.INITIAL_MAPPING['word'].items())
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (empty_dummy_dataset.type_to_idx['tag'][k] == v for k, v in constants.INITIAL_MAPPING['tag'].items())
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_get_idx_seq_single_dataset_before_load(empty_dummy_dataset):
    """Asserts that `Dataset.idx_seq` is updated as expected after successive calls to
    `Dataset._get_type_seq()`, `Dataset._get_idx_maps()` and `Dataset.get_idx_seq()`.
    """
    types = empty_dummy_dataset._get_types()
    empty_dummy_dataset._get_type_seq()
    empty_dummy_dataset._get_idx_maps(types)
    empty_dummy_dataset.get_idx_seq()
    expected_word_idx_shape = (
     len(DUMMY_WORD_SEQ), constants.MAX_SENT_LEN)
    expected_char_idx_shape = (len(DUMMY_WORD_SEQ), constants.MAX_SENT_LEN, constants.MAX_CHAR_LEN)
    expected_tag_idx_shape = (len(DUMMY_WORD_SEQ), constants.MAX_SENT_LEN, len(DUMMY_TAG_TYPES))
    @py_assert1 = (empty_dummy_dataset.idx_seq[partition]['word'].shape == expected_word_idx_shape for partition in ('train',
                                                                                                                     'test',
                                                                                                                     'valid'))
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (empty_dummy_dataset.idx_seq[partition]['char'].shape == expected_char_idx_shape for partition in ('train',
                                                                                                                     'test',
                                                                                                                     'valid'))
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (empty_dummy_dataset.idx_seq[partition]['tag'].shape == expected_tag_idx_shape for partition in ('train',
                                                                                                                   'test',
                                                                                                                   'valid'))
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_get_type_seq_single_dataset_after_load(loaded_dummy_dataset):
    """Asserts that `Dataset.type_seq` is updated as expected after call to `Dataset.load()`.
    """
    @py_assert1 = np.array_equal
    @py_assert3 = loaded_dummy_dataset.type_seq['train']['word']
    @py_assert6 = @py_assert1(@py_assert3, DUMMY_WORD_SEQ)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.array_equal\n}(%(py4)s, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(DUMMY_WORD_SEQ) if 'DUMMY_WORD_SEQ' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DUMMY_WORD_SEQ) else 'DUMMY_WORD_SEQ',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    @py_assert1 = np.array_equal
    @py_assert3 = loaded_dummy_dataset.type_seq['train']['char']
    @py_assert6 = @py_assert1(@py_assert3, DUMMY_CHAR_SEQ)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.array_equal\n}(%(py4)s, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(DUMMY_CHAR_SEQ) if 'DUMMY_CHAR_SEQ' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DUMMY_CHAR_SEQ) else 'DUMMY_CHAR_SEQ',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    @py_assert1 = np.array_equal
    @py_assert3 = loaded_dummy_dataset.type_seq['train']['tag']
    @py_assert6 = @py_assert1(@py_assert3, DUMMY_TAG_SEQ)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.array_equal\n}(%(py4)s, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(DUMMY_TAG_SEQ) if 'DUMMY_TAG_SEQ' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DUMMY_TAG_SEQ) else 'DUMMY_TAG_SEQ',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None


def test_get_idx_maps_single_dataset_after_load(loaded_dummy_dataset):
    """Asserts that `Dataset.type_to_idx` is updated as expected after call to `Dataset.load()`.
    """
    @py_assert1 = generic_utils.is_consecutive
    @py_assert3 = loaded_dummy_dataset.type_to_idx['word']
    @py_assert5 = @py_assert3.values
    @py_assert7 = @py_assert5()
    @py_assert9 = @py_assert1(@py_assert7)
    if not @py_assert9:
        @py_format11 = 'assert %(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.is_consecutive\n}(%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.values\n}()\n})\n}' % {'py0':@pytest_ar._saferepr(generic_utils) if 'generic_utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(generic_utils) else 'generic_utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = generic_utils.is_consecutive
    @py_assert3 = loaded_dummy_dataset.type_to_idx['char']
    @py_assert5 = @py_assert3.values
    @py_assert7 = @py_assert5()
    @py_assert9 = @py_assert1(@py_assert7)
    if not @py_assert9:
        @py_format11 = 'assert %(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.is_consecutive\n}(%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.values\n}()\n})\n}' % {'py0':@pytest_ar._saferepr(generic_utils) if 'generic_utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(generic_utils) else 'generic_utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = generic_utils.is_consecutive
    @py_assert3 = loaded_dummy_dataset.type_to_idx['tag']
    @py_assert5 = @py_assert3.values
    @py_assert7 = @py_assert5()
    @py_assert9 = @py_assert1(@py_assert7)
    if not @py_assert9:
        @py_format11 = 'assert %(py10)s\n{%(py10)s = %(py2)s\n{%(py2)s = %(py0)s.is_consecutive\n}(%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.values\n}()\n})\n}' % {'py0':@pytest_ar._saferepr(generic_utils) if 'generic_utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(generic_utils) else 'generic_utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = (key in DUMMY_WORD_TYPES for key in loaded_dummy_dataset.type_to_idx['word'])
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (key in DUMMY_CHAR_TYPES for key in loaded_dummy_dataset.type_to_idx['char'])
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (key in DUMMY_TAG_TYPES for key in loaded_dummy_dataset.type_to_idx['tag'])
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_get_idx_maps_single_dataset_after_load_special_tokens(loaded_dummy_dataset):
    """Asserts that `Dataset.type_to_idx` contains the special tokens as keys with expected values
     after successive calls to `Dataset._get_types()` and `Dataset.get_idx_maps()`.
    """
    @py_assert1 = (loaded_dummy_dataset.type_to_idx['word'][k] == v for k, v in constants.INITIAL_MAPPING['word'].items())
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (loaded_dummy_dataset.type_to_idx['char'][k] == v for k, v in constants.INITIAL_MAPPING['word'].items())
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (loaded_dummy_dataset.type_to_idx['tag'][k] == v for k, v in constants.INITIAL_MAPPING['tag'].items())
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_get_idx_seq_after_load(loaded_dummy_dataset):
    """Asserts that `Dataset.idx_seq` is updated as expected after calls to `Dataset.load()`.
    """
    expected_word_idx_shape = (
     len(DUMMY_WORD_SEQ), constants.MAX_SENT_LEN)
    expected_char_idx_shape = (len(DUMMY_WORD_SEQ), constants.MAX_SENT_LEN, constants.MAX_CHAR_LEN)
    expected_tag_idx_shape = (len(DUMMY_WORD_SEQ), constants.MAX_SENT_LEN, len(DUMMY_TAG_TYPES))
    @py_assert1 = (loaded_dummy_dataset.idx_seq[partition]['word'].shape == expected_word_idx_shape for partition in ('train',
                                                                                                                      'test',
                                                                                                                      'valid'))
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (loaded_dummy_dataset.idx_seq[partition]['char'].shape == expected_char_idx_shape for partition in ('train',
                                                                                                                      'test',
                                                                                                                      'valid'))
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (loaded_dummy_dataset.idx_seq[partition]['tag'].shape == expected_tag_idx_shape for partition in ('train',
                                                                                                                    'test',
                                                                                                                    'valid'))
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None