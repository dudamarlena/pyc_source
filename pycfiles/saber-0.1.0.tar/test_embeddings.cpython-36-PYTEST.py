# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johngiorgi/Documents/Masters/Class/natural_language_computing/project/saber/saber/tests/test_embeddings.py
# Compiled at: 2019-01-14 18:15:15
# Size of source mod 2**32: 9111 bytes
"""Any and all unit tests for the Embeddings class (saber/embeddings.py).
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, numpy as np, pytest
from ..embeddings import Embeddings
from .resources import helpers
from .resources.dummy_constants import *

@pytest.fixture
def dummy_embedding_idx():
    """Returns embedding index from call to `Embeddings._prepare_embedding_index()`.
    """
    embeddings = Embeddings(filepath=PATH_TO_DUMMY_EMBEDDINGS, token_map=DUMMY_TOKEN_MAP)
    embedding_idx = embeddings._prepare_embedding_index(binary=False)
    return embedding_idx


@pytest.fixture
def dummy_embedding_matrix_and_type_to_idx():
    """Returns the `embedding_matrix` and `type_to_index` objects from call to
    `Embeddings._prepare_embedding_matrix(load_all=False)`.
    """
    embeddings = Embeddings(filepath=PATH_TO_DUMMY_EMBEDDINGS, token_map=DUMMY_TOKEN_MAP)
    embedding_idx = embeddings._prepare_embedding_index(binary=False)
    embeddings.num_found = len(embedding_idx)
    embeddings.dimension = len(list(embedding_idx.values())[0])
    embedding_matrix, type_to_idx = embeddings._prepare_embedding_matrix(embedding_idx, load_all=False)
    embeddings.num_embed = embedding_matrix.shape[0]
    return (
     embedding_matrix, type_to_idx)


@pytest.fixture
def dummy_embedding_matrix_and_type_to_idx_load_all():
    """Returns the embedding matrix and type to index objects from call to
    `Embeddings._prepare_embedding_matrix(load_all=True)`.
    """
    test = {'This':0, 
     'is':1,  'a':2,  'test':3}
    embeddings = Embeddings(filepath=PATH_TO_DUMMY_EMBEDDINGS, token_map=test)
    embedding_idx = embeddings._prepare_embedding_index(binary=False)
    embeddings.num_found = len(embedding_idx)
    embeddings.dimension = len(list(embedding_idx.values())[0])
    embedding_matrix, type_to_idx = embeddings._prepare_embedding_matrix(embedding_idx, load_all=True)
    embeddings.num_embed = embedding_matrix.shape[0]
    return (
     embedding_matrix, type_to_idx)


@pytest.fixture
def dummy_embeddings_before_load():
    """Returns an instance of an Embeddings() object BEFORE the `Embeddings.load()` method is
    called.
    """
    return Embeddings(filepath=PATH_TO_DUMMY_EMBEDDINGS, token_map=DUMMY_TOKEN_MAP,
      totally_arbitrary='arbitrary')


@pytest.fixture
def dummy_embeddings_after_load():
    """Returns an instance of an Embeddings() object AFTER `Embeddings.load(load_all=False)` is
    called.
    """
    embeddings = Embeddings(filepath=PATH_TO_DUMMY_EMBEDDINGS, token_map=DUMMY_TOKEN_MAP)
    embeddings.load(binary=False, load_all=False)
    return embeddings


@pytest.fixture
def dummy_embeddings_after_load_with_load_all():
    """Returns an instance of an Embeddings() object AFTER `Embeddings.load(load_all=True)` is
    called.
    """
    test = {'This':0, 
     'is':1,  'a':2,  'test':3}
    embeddings = Embeddings(filepath=PATH_TO_DUMMY_EMBEDDINGS, token_map=test)
    embeddings.load(binary=False, load_all=True)
    return embeddings


def test_initialization(dummy_embeddings_before_load):
    """Asserts that Embeddings object contains the expected attribute values after initialization.
    """
    @py_assert1 = dummy_embeddings_before_load.filepath
    @py_assert3 = @py_assert1 == PATH_TO_DUMMY_EMBEDDINGS
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.filepath\n} == %(py4)s', ), (@py_assert1, PATH_TO_DUMMY_EMBEDDINGS)) % {'py0':@pytest_ar._saferepr(dummy_embeddings_before_load) if 'dummy_embeddings_before_load' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_embeddings_before_load) else 'dummy_embeddings_before_load',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(PATH_TO_DUMMY_EMBEDDINGS) if 'PATH_TO_DUMMY_EMBEDDINGS' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(PATH_TO_DUMMY_EMBEDDINGS) else 'PATH_TO_DUMMY_EMBEDDINGS'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = dummy_embeddings_before_load.token_map
    @py_assert3 = @py_assert1 == DUMMY_TOKEN_MAP
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.token_map\n} == %(py4)s', ), (@py_assert1, DUMMY_TOKEN_MAP)) % {'py0':@pytest_ar._saferepr(dummy_embeddings_before_load) if 'dummy_embeddings_before_load' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_embeddings_before_load) else 'dummy_embeddings_before_load',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(DUMMY_TOKEN_MAP) if 'DUMMY_TOKEN_MAP' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DUMMY_TOKEN_MAP) else 'DUMMY_TOKEN_MAP'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = dummy_embeddings_before_load.matrix
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.matrix\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(dummy_embeddings_before_load) if 'dummy_embeddings_before_load' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_embeddings_before_load) else 'dummy_embeddings_before_load',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = dummy_embeddings_before_load.num_found
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.num_found\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(dummy_embeddings_before_load) if 'dummy_embeddings_before_load' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_embeddings_before_load) else 'dummy_embeddings_before_load',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = dummy_embeddings_before_load.num_embed
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.num_embed\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(dummy_embeddings_before_load) if 'dummy_embeddings_before_load' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_embeddings_before_load) else 'dummy_embeddings_before_load',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = dummy_embeddings_before_load.dimension
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.dimension\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(dummy_embeddings_before_load) if 'dummy_embeddings_before_load' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_embeddings_before_load) else 'dummy_embeddings_before_load',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = dummy_embeddings_before_load.totally_arbitrary
    @py_assert4 = 'arbitrary'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.totally_arbitrary\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(dummy_embeddings_before_load) if 'dummy_embeddings_before_load' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_embeddings_before_load) else 'dummy_embeddings_before_load',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_prepare_embedding_index(dummy_embedding_idx):
    """Asserts that we get the expected value back after call to
    `Embeddings._prepare_embedding_index()`.
    """
    @py_assert1 = dummy_embedding_idx.keys
    @py_assert3 = @py_assert1()
    @py_assert7 = DUMMY_EMBEDDINGS_INDEX.keys
    @py_assert9 = @py_assert7()
    @py_assert5 = @py_assert3 == @py_assert9
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.keys\n}()\n} == %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s.keys\n}()\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(dummy_embedding_idx) if 'dummy_embedding_idx' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_embedding_idx) else 'dummy_embedding_idx',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(DUMMY_EMBEDDINGS_INDEX) if 'DUMMY_EMBEDDINGS_INDEX' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DUMMY_EMBEDDINGS_INDEX) else 'DUMMY_EMBEDDINGS_INDEX',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = (np.allclose(actual, expected) for actual, expected in zip(dummy_embedding_idx.values(), DUMMY_EMBEDDINGS_INDEX.values()))
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_prepare_embedding_matrix(dummy_embedding_matrix_and_type_to_idx):
    """Asserts that we get the expected value back after successive calls to
    `Embeddings._prepare_embedding_index()` and
    `Embeddings._prepare_embedding_matrix(load_all=False)`.
    """
    embedding_matrix_expected, type_to_idx_expected = DUMMY_EMBEDDINGS_MATRIX, None
    embedding_matrix_actual, type_to_idx_actual = dummy_embedding_matrix_and_type_to_idx
    @py_assert1 = np.allclose
    @py_assert5 = @py_assert1(embedding_matrix_actual, embedding_matrix_expected)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.allclose\n}(%(py3)s, %(py4)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(embedding_matrix_actual) if 'embedding_matrix_actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(embedding_matrix_actual) else 'embedding_matrix_actual',  'py4':@pytest_ar._saferepr(embedding_matrix_expected) if 'embedding_matrix_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(embedding_matrix_expected) else 'embedding_matrix_expected',  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert5 = None
    @py_assert1 = type_to_idx_actual is type_to_idx_expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (type_to_idx_actual, type_to_idx_expected)) % {'py0':@pytest_ar._saferepr(type_to_idx_actual) if 'type_to_idx_actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type_to_idx_actual) else 'type_to_idx_actual',  'py2':@pytest_ar._saferepr(type_to_idx_expected) if 'type_to_idx_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type_to_idx_expected) else 'type_to_idx_expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_prepare_embedding_matrix_load_all(dummy_embedding_matrix_and_type_to_idx_load_all):
    """Asserts that we get the expected value back after successive calls to
    `Embeddings._prepare_embedding_index()` and
    `Embeddings._prepare_embedding_matrix(load_all=True)`.
    """
    embedding_matrix_expected = DUMMY_EMBEDDINGS_MATRIX
    type_to_idx_expected = {'word':DUMMY_TOKEN_MAP,  'char':DUMMY_CHAR_MAP}
    embedding_matrix_actual, type_to_idx_actual = dummy_embedding_matrix_and_type_to_idx_load_all
    @py_assert1 = np.allclose
    @py_assert5 = @py_assert1(embedding_matrix_actual, embedding_matrix_expected)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.allclose\n}(%(py3)s, %(py4)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(embedding_matrix_actual) if 'embedding_matrix_actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(embedding_matrix_actual) else 'embedding_matrix_actual',  'py4':@pytest_ar._saferepr(embedding_matrix_expected) if 'embedding_matrix_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(embedding_matrix_expected) else 'embedding_matrix_expected',  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert5 = None
    helpers.assert_type_to_idx_as_expected(actual=type_to_idx_actual, expected=type_to_idx_expected)


def test_matrix_after_load(dummy_embeddings_after_load):
    """Asserts that pre-trained token embeddings are loaded correctly when
    `Embeddings.load(load_all=False)` is called."""
    @py_assert1 = np.allclose
    @py_assert4 = dummy_embeddings_after_load.matrix
    @py_assert7 = @py_assert1(@py_assert4, DUMMY_EMBEDDINGS_MATRIX)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.allclose\n}(%(py5)s\n{%(py5)s = %(py3)s.matrix\n}, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(dummy_embeddings_after_load) if 'dummy_embeddings_after_load' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_embeddings_after_load) else 'dummy_embeddings_after_load',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(DUMMY_EMBEDDINGS_MATRIX) if 'DUMMY_EMBEDDINGS_MATRIX' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DUMMY_EMBEDDINGS_MATRIX) else 'DUMMY_EMBEDDINGS_MATRIX',  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert4 = @py_assert7 = None


def test_matrix_after_load_with_load_all(dummy_embeddings_after_load):
    """Asserts that pre-trained token embeddings are loaded correctly when
    `Embeddings.load(load_all=True)` is called."""
    @py_assert1 = np.allclose
    @py_assert4 = dummy_embeddings_after_load.matrix
    @py_assert7 = @py_assert1(@py_assert4, DUMMY_EMBEDDINGS_MATRIX)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.allclose\n}(%(py5)s\n{%(py5)s = %(py3)s.matrix\n}, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(dummy_embeddings_after_load) if 'dummy_embeddings_after_load' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_embeddings_after_load) else 'dummy_embeddings_after_load',  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(DUMMY_EMBEDDINGS_MATRIX) if 'DUMMY_EMBEDDINGS_MATRIX' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DUMMY_EMBEDDINGS_MATRIX) else 'DUMMY_EMBEDDINGS_MATRIX',  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert4 = @py_assert7 = None


def test_attributes_after_load(dummy_embedding_idx, dummy_embeddings_after_load):
    """Asserts that attributes of Embeddings object are updated as expected after
    `Embeddings.load(load_all=False)` is called.
    """
    num_found_expected = len(dummy_embedding_idx)
    dimension_expected = len(list(dummy_embedding_idx.values())[0])
    num_embed_expected = dummy_embeddings_after_load.matrix.shape[0]
    num_found_actual = dummy_embeddings_after_load.num_found
    dimension_actual = dummy_embeddings_after_load.dimension
    num_embed_actual = dummy_embeddings_after_load.num_embed
    @py_assert1 = num_found_expected == num_found_actual
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (num_found_expected, num_found_actual)) % {'py0':@pytest_ar._saferepr(num_found_expected) if 'num_found_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(num_found_expected) else 'num_found_expected',  'py2':@pytest_ar._saferepr(num_found_actual) if 'num_found_actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(num_found_actual) else 'num_found_actual'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = dimension_expected == dimension_actual
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (dimension_expected, dimension_actual)) % {'py0':@pytest_ar._saferepr(dimension_expected) if 'dimension_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dimension_expected) else 'dimension_expected',  'py2':@pytest_ar._saferepr(dimension_actual) if 'dimension_actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dimension_actual) else 'dimension_actual'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = num_embed_expected == num_embed_actual
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (num_embed_expected, num_embed_actual)) % {'py0':@pytest_ar._saferepr(num_embed_expected) if 'num_embed_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(num_embed_expected) else 'num_embed_expected',  'py2':@pytest_ar._saferepr(num_embed_actual) if 'num_embed_actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(num_embed_actual) else 'num_embed_actual'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_attributes_after_load_with_load_all(dummy_embedding_idx, dummy_embeddings_after_load_with_load_all):
    """Asserts that attributes of Embeddings object are updated as expected after
    `Embeddings.load(load_all=True)` is called.
    """
    num_found_expected = len(dummy_embedding_idx)
    dimension_expected = len(list(dummy_embedding_idx.values())[0])
    num_embed_expected = dummy_embeddings_after_load_with_load_all.matrix.shape[0]
    num_found_actual = dummy_embeddings_after_load_with_load_all.num_found
    dimension_actual = dummy_embeddings_after_load_with_load_all.dimension
    num_embed_actual = dummy_embeddings_after_load_with_load_all.num_embed
    @py_assert1 = num_found_expected == num_found_actual
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (num_found_expected, num_found_actual)) % {'py0':@pytest_ar._saferepr(num_found_expected) if 'num_found_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(num_found_expected) else 'num_found_expected',  'py2':@pytest_ar._saferepr(num_found_actual) if 'num_found_actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(num_found_actual) else 'num_found_actual'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = dimension_expected == dimension_actual
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (dimension_expected, dimension_actual)) % {'py0':@pytest_ar._saferepr(dimension_expected) if 'dimension_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dimension_expected) else 'dimension_expected',  'py2':@pytest_ar._saferepr(dimension_actual) if 'dimension_actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dimension_actual) else 'dimension_actual'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = num_embed_expected == num_embed_actual
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (num_embed_expected, num_embed_actual)) % {'py0':@pytest_ar._saferepr(num_embed_expected) if 'num_embed_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(num_embed_expected) else 'num_embed_expected',  'py2':@pytest_ar._saferepr(num_embed_actual) if 'num_embed_actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(num_embed_actual) else 'num_embed_actual'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_generate_type_to_idx(dummy_embeddings_before_load):
    """Asserts that the dictionary returned from 'Embeddings._generate_type_to_idx()' is as
    expected.
    """
    test = {'This':0, 
     'is':1,  'a':2,  'test':3}
    expected = {'word':list(test.keys()), 
     'char':[]}
    for word in expected['word']:
        expected['char'].extend(list(word))

    expected['char'] = list(set(expected['char']))
    actual = dummy_embeddings_before_load._generate_type_to_idx(test)
    helpers.assert_type_to_idx_as_expected(actual=actual, expected=expected)