# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johngiorgi/Documents/Masters/Class/natural_language_computing/project/saber/saber/tests/test_preprocessor.py
# Compiled at: 2018-11-02 12:56:46
# Size of source mod 2**32: 4405 bytes
"""Contains any and all unit tests for the `Preprocessor` class (saber/preprocessor.py).
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, en_coref_md, pytest
from .. import constants
from ..preprocessor import Preprocessor

@pytest.fixture
def preprocessor():
    """Returns an instance of a Preprocessor object."""
    return Preprocessor()


@pytest.fixture
def nlp():
    """Returns Sacy NLP model."""
    return en_coref_md.load()


def test_process_text(preprocessor, nlp):
    """Asserts that call to Preprocessor._process_text() returns the expected
    results."""
    simple_text = nlp('Simple example. With two sentences!')
    simple_expected = (
     [['Simple', 'example', '.'],
      ['With', 'two',
       'sentences', '!']],
     [[(0, 6), (7, 14), (14, 15)],
      [(16, 20),
       (21, 24), (25, 34), (34, 35)]])
    blank_test = nlp('')
    blank_expected = ([], [])
    @py_assert1 = preprocessor._process_text
    @py_assert4 = @py_assert1(simple_text)
    @py_assert6 = @py_assert4 == simple_expected
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s._process_text\n}(%(py3)s)\n} == %(py7)s', ), (@py_assert4, simple_expected)) % {'py0':@pytest_ar._saferepr(preprocessor) if 'preprocessor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(preprocessor) else 'preprocessor',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(simple_text) if 'simple_text' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(simple_text) else 'simple_text',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(simple_expected) if 'simple_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(simple_expected) else 'simple_expected'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert6 = None
    @py_assert1 = preprocessor._process_text
    @py_assert4 = @py_assert1(blank_test)
    @py_assert6 = @py_assert4 == blank_expected
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s._process_text\n}(%(py3)s)\n} == %(py7)s', ), (@py_assert4, blank_expected)) % {'py0':@pytest_ar._saferepr(preprocessor) if 'preprocessor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(preprocessor) else 'preprocessor',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(blank_test) if 'blank_test' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(blank_test) else 'blank_test',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(blank_expected) if 'blank_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(blank_expected) else 'blank_expected'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert6 = None


def test_type_to_idx_value_error():
    """
    """
    with pytest.raises(ValueError):
        invalid_input = {'a':0, 
         'b':2,  'c':3}
        Preprocessor.type_to_idx([], initial_mapping=invalid_input)


def test_type_to_idx_empty_input():
    """Asserts that call to Preprocessor.test_type_to_idx() returns the expected results when
    an empty list is passed as input."""
    expected = {}
    actual = Preprocessor.type_to_idx([])
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_type_to_idx_simple_input():
    """Asserts that call to Preprocessor.test_type_to_idx() returns the expected results when
    a simple list of strings is passed as input."""
    test = [
     'This', 'is', 'a', 'test', '.']
    expected = {'This':0,  'is':1,  'a':2,  'test':3,  '.':4}
    actual = Preprocessor.type_to_idx(test)
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_type_to_idx_intial_mapping():
    """Asserts that call to Preprocessor.test_type_to_idx() returns the expected results when
    a simple list of strings is passed as input and a supplied `intitial_mapping` argument"""
    test = [
     'This', 'is', 'a', 'test', '.']
    initial_mapping = {'This':0,  'is':1}
    expected = {'This':0, 
     'is':1,  'a':2,  'test':3,  '.':4}
    actual = Preprocessor.type_to_idx(test, initial_mapping=initial_mapping)
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_get_type_to_idx_sequence():
    """"""
    simple_seq = [
     'This', 'is', 'a', 'test', '.', constants.UNK]
    simple_type_to_idx = Preprocessor.type_to_idx(simple_seq)
    simple_expected = [0, 1, 2, 3, 4]
    simple_actual = Preprocessor.get_type_idx_sequence(simple_seq, type_to_idx=simple_type_to_idx)


def test_chunk_entities():
    """Asserts that call to Preprocessor.chunk_entities() returns the
    expected results."""
    simple_seq = [
     'B-PRGE', 'I-PRGE', 'O', 'B-PRGE']
    simple_expected = [('PRGE', 0, 2), ('PRGE', 3, 4)]
    two_type_seq = [
     'B-LIVB', 'I-LIVB', 'O', 'B-PRGE']
    two_type_expected = [('LIVB', 0, 2), ('PRGE', 3, 4)]
    invalid_seq = [
     'O', 'I-CHED', 'I-CHED', 'O']
    invalid_expected = []
    blank_seq = []
    blank_expected = []
    @py_assert1 = Preprocessor.chunk_entities
    @py_assert4 = @py_assert1(simple_seq)
    @py_assert6 = @py_assert4 == simple_expected
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.chunk_entities\n}(%(py3)s)\n} == %(py7)s', ), (@py_assert4, simple_expected)) % {'py0':@pytest_ar._saferepr(Preprocessor) if 'Preprocessor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Preprocessor) else 'Preprocessor',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(simple_seq) if 'simple_seq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(simple_seq) else 'simple_seq',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(simple_expected) if 'simple_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(simple_expected) else 'simple_expected'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert6 = None
    @py_assert1 = Preprocessor.chunk_entities
    @py_assert4 = @py_assert1(two_type_seq)
    @py_assert6 = @py_assert4 == two_type_expected
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.chunk_entities\n}(%(py3)s)\n} == %(py7)s', ), (@py_assert4, two_type_expected)) % {'py0':@pytest_ar._saferepr(Preprocessor) if 'Preprocessor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Preprocessor) else 'Preprocessor',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(two_type_seq) if 'two_type_seq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(two_type_seq) else 'two_type_seq',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(two_type_expected) if 'two_type_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(two_type_expected) else 'two_type_expected'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert6 = None
    @py_assert1 = Preprocessor.chunk_entities
    @py_assert4 = @py_assert1(invalid_seq)
    @py_assert6 = @py_assert4 == invalid_expected
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.chunk_entities\n}(%(py3)s)\n} == %(py7)s', ), (@py_assert4, invalid_expected)) % {'py0':@pytest_ar._saferepr(Preprocessor) if 'Preprocessor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Preprocessor) else 'Preprocessor',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(invalid_seq) if 'invalid_seq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(invalid_seq) else 'invalid_seq',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(invalid_expected) if 'invalid_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(invalid_expected) else 'invalid_expected'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert6 = None
    @py_assert1 = Preprocessor.chunk_entities
    @py_assert4 = @py_assert1(blank_seq)
    @py_assert6 = @py_assert4 == blank_expected
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.chunk_entities\n}(%(py3)s)\n} == %(py7)s', ), (@py_assert4, blank_expected)) % {'py0':@pytest_ar._saferepr(Preprocessor) if 'Preprocessor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Preprocessor) else 'Preprocessor',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(blank_seq) if 'blank_seq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(blank_seq) else 'blank_seq',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(blank_expected) if 'blank_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(blank_expected) else 'blank_expected'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert6 = None


def test_sterilize():
    """Asserts that call to Preprocessor.sterilize() returns the
    expected results."""
    simple_text = ' This is an easy test. '
    simple_expected = 'This is an easy test.'
    multiple_spaces_text = 'This  is a test   with improper  spacing. '
    multiple_spaces_expected = 'This is a test with improper spacing.'
    blank_text = ''
    blank_expected = ''
    @py_assert1 = Preprocessor.sterilize
    @py_assert4 = @py_assert1(simple_text)
    @py_assert6 = @py_assert4 == simple_expected
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.sterilize\n}(%(py3)s)\n} == %(py7)s', ), (@py_assert4, simple_expected)) % {'py0':@pytest_ar._saferepr(Preprocessor) if 'Preprocessor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Preprocessor) else 'Preprocessor',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(simple_text) if 'simple_text' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(simple_text) else 'simple_text',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(simple_expected) if 'simple_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(simple_expected) else 'simple_expected'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert6 = None
    @py_assert1 = Preprocessor.sterilize
    @py_assert4 = @py_assert1(multiple_spaces_text)
    @py_assert6 = @py_assert4 == multiple_spaces_expected
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.sterilize\n}(%(py3)s)\n} == %(py7)s', ), (@py_assert4, multiple_spaces_expected)) % {'py0':@pytest_ar._saferepr(Preprocessor) if 'Preprocessor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Preprocessor) else 'Preprocessor',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(multiple_spaces_text) if 'multiple_spaces_text' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(multiple_spaces_text) else 'multiple_spaces_text',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(multiple_spaces_expected) if 'multiple_spaces_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(multiple_spaces_expected) else 'multiple_spaces_expected'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert6 = None
    @py_assert1 = Preprocessor.sterilize
    @py_assert4 = @py_assert1(blank_text)
    @py_assert6 = @py_assert4 == blank_expected
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.sterilize\n}(%(py3)s)\n} == %(py7)s', ), (@py_assert4, blank_expected)) % {'py0':@pytest_ar._saferepr(Preprocessor) if 'Preprocessor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Preprocessor) else 'Preprocessor',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(blank_text) if 'blank_text' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(blank_text) else 'blank_text',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(blank_expected) if 'blank_expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(blank_expected) else 'blank_expected'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert6 = None