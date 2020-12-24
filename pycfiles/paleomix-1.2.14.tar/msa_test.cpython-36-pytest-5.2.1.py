# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py
# Compiled at: 2019-10-16 12:05:38
# Size of source mod 2**32: 15177 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, copy, io, os
from unittest.mock import patch
import pytest
from paleomix.common.formats.fasta import FASTA
from paleomix.common.formats.msa import MSA, FASTAError, MSAError

def test_dir():
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def test_file(*args):
    return (os.path.join)(test_dir(), 'data', *args)


def test_msa_constructor__calls_validate():
    with patch('paleomix.common.formats.msa.MSA.validate', wrap=(MSA.validate)) as (mock):
        MSA([FASTA('NA', None, 'ACGT')])
    mock.assert_called_once()


def test_msa_constructor__duplicate_names():
    records = [
     FASTA('Foo', None, 'ACGT'), FASTA('Foo', None, 'GTCA')]
    with pytest.raises(MSAError):
        MSA(records)


def test_msa_constructor__empty_msa():
    with pytest.raises(MSAError):
        MSA([])


def test_msa__len__corresponds_to_sequence_number_of_records():
    msa = MSA((
     FASTA('seq1', None, 'ACGCGTATGCATGCCGA'),
     FASTA('seq2', None, 'TGAACACACAGTAGGAT')))
    @py_assert2 = len(msa)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=77)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(msa) if 'msa' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msa) else 'msa',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_msa__seqlen__corresponds_to_sequence_lengths():
    msa = MSA((
     FASTA('seq1', None, 'ACGCGTATGCATGCCGA'),
     FASTA('seq2', None, 'TGAACACACAGTAGGAT')))
    @py_assert1 = msa.seqlen
    @py_assert3 = @py_assert1()
    @py_assert6 = 17
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=87)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.seqlen\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(msa) if 'msa' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msa) else 'msa',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_msa_exclude__remove_one():
    fa_1 = FASTA('A', None, 'ACGT')
    fa_2 = FASTA('B', None, 'GCTA')
    initial = MSA([fa_1, fa_2])
    expected = MSA([fa_1])
    result = initial.exclude(['B'])
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=101)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_msa_exclude__missing_keys():
    msa = MSA([FASTA('Foo', None, 'ACGT')])
    with pytest.raises(KeyError):
        msa.exclude(['Bar'])


def test_msa_exclude__no_keys():
    msa = MSA([FASTA('Foo', None, 'ACGT')])
    with pytest.raises(ValueError):
        msa.exclude([])


def test_msa_select__remove_one():
    fa_1 = FASTA('A', None, 'ACGT')
    fa_2 = FASTA('B', None, 'GCTA')
    initial = MSA([fa_1, fa_2])
    expected = MSA([fa_1])
    result = initial.select(['A'])
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=127)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_msa_select__missing_keys():
    msa = MSA([FASTA('Foo', None, 'ACGT')])
    with pytest.raises(KeyError):
        msa.select(['Bar'])


def test_msa_select__no_keys():
    msa = MSA([FASTA('Foo', None, 'ACGT')])
    with pytest.raises(ValueError):
        msa.select([])


def test_msa_reduce__no_empty_columns__no_columns_are_removed():
    fa_1 = FASTA('Name_A', 'Meta_A', 'ACnT')
    fa_2 = FASTA('Name_B', 'Meta_B', 'C-TN')
    initial = MSA([fa_1, fa_2])
    expected = MSA([fa_1, fa_2])
    @py_assert1 = initial.reduce
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == expected
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=152)
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.reduce\n}()\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(initial) if 'initial' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(initial) else 'initial',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_msa_reduce__one_empty_column__column_are_removed():
    fa_1 = FASTA('Name_A', 'Meta_A', 'AnT')
    fa_2 = FASTA('Name_B', 'Meta_B', 'C-N')
    initial = MSA([fa_1, fa_2])
    fa_reduced_1 = FASTA('Name_A', 'Meta_A', 'AT')
    fa_reduced_2 = FASTA('Name_B', 'Meta_B', 'CN')
    expected = MSA([fa_reduced_1, fa_reduced_2])
    @py_assert1 = initial.reduce
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == expected
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=162)
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.reduce\n}()\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(initial) if 'initial' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(initial) else 'initial',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_msa_reduce__multiple_empty_column__all_empty_column_are_removed():
    fa_1 = FASTA('Name_A', 'Meta_A', '-AnTN')
    fa_2 = FASTA('Name_B', 'Meta_B', 'NC-NN')
    initial = MSA([fa_1, fa_2])
    fa_reduced_1 = FASTA('Name_A', 'Meta_A', 'AT')
    fa_reduced_2 = FASTA('Name_B', 'Meta_B', 'CN')
    expected = MSA([fa_reduced_1, fa_reduced_2])
    @py_assert1 = initial.reduce
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == expected
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=172)
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.reduce\n}()\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(initial) if 'initial' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(initial) else 'initial',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_msa_reduce__only_empty_column__none_is_returned():
    fa_1 = FASTA('Name_A', 'Meta_A', '---Nn')
    fa_2 = FASTA('Name_B', 'Meta_B', 'Nn--N')
    initial = MSA([fa_1, fa_2])
    @py_assert1 = initial.reduce
    @py_assert3 = @py_assert1()
    @py_assert6 = None
    @py_assert5 = @py_assert3 is @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=179)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.reduce\n}()\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(initial) if 'initial' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(initial) else 'initial',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


_FILTER_MSA_1 = MSA((
 FASTA('Seq1', 'Meta1', 'ACGNTYCSTG'),
 FASTA('Seq2', 'Meta2', 'ACTA-WCCTG'),
 FASTA('Seq3', 'Meta3', 'NCGGTYCGTC')))

def test_msa_filter_singletons__filter_by_second():
    expected = MSA((
     FASTA('Seq1', 'Meta1', 'ACnNntCcTG'),
     FASTA('Seq2', 'Meta2', 'ACTA-WCCTG'),
     FASTA('Seq3', 'Meta3', 'NCGGTYCGTC')))
    result = _FILTER_MSA_1.filter_singletons('Seq1', ['Seq2'])
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=204)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_msa_filter_singletons__filter_by_third():
    expected = MSA((
     FASTA('Seq1', 'Meta1', 'nCGNTYCgTn'),
     FASTA('Seq2', 'Meta2', 'ACTA-WCCTG'),
     FASTA('Seq3', 'Meta3', 'NCGGTYCGTC')))
    result = _FILTER_MSA_1.filter_singletons('Seq1', ['Seq3'])
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=216)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_msa_filter_singletons__filter_by_both():
    result = _FILTER_MSA_1.filter_singletons('Seq1', ['Seq2', 'Seq3'])
    @py_assert1 = result == _FILTER_MSA_1
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=221)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, _FILTER_MSA_1)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(_FILTER_MSA_1) if '_FILTER_MSA_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_FILTER_MSA_1) else '_FILTER_MSA_1'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_msa_filter_singletons__filter_by_itself():
    with pytest.raises(MSAError):
        _FILTER_MSA_1.filter_singletons('Seq1', ['Seq1', 'Seq2'])


def test_msa_filter_singletons__filter_by_nothing():
    with pytest.raises(ValueError):
        _FILTER_MSA_1.filter_singletons('Seq1', [])


_JOIN_MSA_1 = MSA((
 FASTA('nc', None, 'ACG'), FASTA('nm', None, 'TGA'), FASTA('miRNA', None, 'UCA')))
_JOIN_MSA_2 = MSA((
 FASTA('nc', None, 'TGA'), FASTA('nm', None, 'CTT'), FASTA('miRNA', None, 'GAC')))
_JOIN_MSA_3 = MSA((
 FASTA('nc', None, 'AAG'), FASTA('nm', None, 'GAG'), FASTA('miRNA', None, 'CAU')))

def test_msa_join__single_msa():
    result = MSA.join(_JOIN_MSA_1)
    @py_assert1 = result == _JOIN_MSA_1
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=251)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, _JOIN_MSA_1)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(_JOIN_MSA_1) if '_JOIN_MSA_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_JOIN_MSA_1) else '_JOIN_MSA_1'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_msa_join__two_msa():
    expected = MSA((
     FASTA('nc', None, 'ACGTGA'),
     FASTA('nm', None, 'TGACTT'),
     FASTA('miRNA', None, 'UCAGAC')))
    result = MSA.join(_JOIN_MSA_1, _JOIN_MSA_2)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=263)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_msa_join__three_msa():
    expected = MSA((
     FASTA('nc', None, 'ACGTGAAAG'),
     FASTA('nm', None, 'TGACTTGAG'),
     FASTA('miRNA', None, 'UCAGACCAU')))
    result = MSA.join(_JOIN_MSA_1, _JOIN_MSA_2, _JOIN_MSA_3)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=275)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_msa_join__missing_arguments():
    with pytest.raises(TypeError):
        MSA.join()


def test_msa_from_lines__single_entry():
    lines = [
     '>seq1', 'ACG']
    result = MSA([FASTA('seq1', None, 'ACG')])
    @py_assert1 = MSA.from_lines
    @py_assert4 = @py_assert1(lines)
    @py_assert6 = @py_assert4 == result
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=291)
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.from_lines\n}(%(py3)s)\n} == %(py7)s', ), (@py_assert4, result)) % {'py0':@pytest_ar._saferepr(MSA) if 'MSA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(MSA) else 'MSA',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(lines) if 'lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lines) else 'lines',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert6 = None


def test_msa_from_lines__single_entry_with_meta():
    lines = [
     '>seq1 Meta info', 'ACG']
    expected = MSA([FASTA('seq1', 'Meta info', 'ACG')])
    result = MSA.from_lines(lines)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=298)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_msa_from_lines__two_entries():
    lines = [
     '>seq1', 'ACG', '>seq2', 'TGA']
    expected = MSA([FASTA('seq1', None, 'ACG'), FASTA('seq2', None, 'TGA')])
    result = MSA.from_lines(lines)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=305)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_msa_from_lines__two_entries_with_meta():
    lines = [
     '>seq1', 'ACG', '>seq2 Second meta', 'TGA']
    expected = MSA([FASTA('seq1', None, 'ACG'), FASTA('seq2', 'Second meta', 'TGA')])
    result = MSA.from_lines(lines)
    @py_assert1 = result == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=312)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_msa_from_lines__duplicate_names():
    with pytest.raises(MSAError):
        MSA.from_lines(['>seq1', 'ACG', '>seq1', 'TGA'])


def test_msa_from_lines__mismatched_lengths():
    with pytest.raises(MSAError):
        MSA.from_lines(['>seq1', 'ACG', '>seq2', 'TGAN'])


def test_msa_from_lines__empty_name():
    with pytest.raises(FASTAError):
        MSA.from_lines(['>', 'ACG', '>seq1', 'TGAN'])


def test_msa_from_file__uncompressed():
    expected = MSA([
     FASTA('This_is_FASTA!', None, 'ACGTN'),
     FASTA('This_is_ALSO_FASTA!', None, 'CGTNA')])
    results = MSA.from_file(test_file('fasta_file.fasta'))
    @py_assert1 = results == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=343)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_msa_from_file__compressed_gz():
    expected = MSA([
     FASTA('This_is_GZipped_FASTA!', None, 'ACGTN'),
     FASTA('This_is_ALSO_GZipped_FASTA!', None, 'CGTNA')])
    results = MSA.from_file(test_file('fasta_file.fasta.gz'))
    @py_assert1 = results == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=354)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_msa_from_file__compressed_bz2():
    expected = MSA([
     FASTA('This_is_BZ_FASTA!', None, 'CGTNA'),
     FASTA('This_is_ALSO_BZ_FASTA!', None, 'ACGTN')])
    results = MSA.from_file(test_file('fasta_file.fasta.bz2'))
    @py_assert1 = results == expected
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=365)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_msa_split_msa__single_group():
    msa = MSA([FASTA('seq1', None, 'ACGCAT'), FASTA('seq2', None, 'GAGTGA')])
    expected = {'1': copy.copy(msa)}
    @py_assert1 = msa.split
    @py_assert3 = '111'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == expected
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=376)
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.split\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, expected)) % {'py0':@pytest_ar._saferepr(msa) if 'msa' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msa) else 'msa',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_msa_split_msa__two_groups():
    msa = MSA([FASTA('seq1', None, 'ACGCAT'), FASTA('seq2', None, 'GAGTGA')])
    expected = {'1':MSA([FASTA('seq1', None, 'ACCA'), FASTA('seq2', None, 'GATG')]), 
     '2':MSA([FASTA('seq1', None, 'GT'), FASTA('seq2', None, 'GA')])}
    @py_assert1 = msa.split
    @py_assert3 = '112'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == expected
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=385)
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.split\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, expected)) % {'py0':@pytest_ar._saferepr(msa) if 'msa' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msa) else 'msa',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_msa_split__three_groups():
    msa = MSA([FASTA('seq1', None, 'ACGCAT'), FASTA('seq2', None, 'GAGTGA')])
    expected = {'1':MSA([FASTA('seq1', None, 'AC'), FASTA('seq2', None, 'GT')]), 
     '2':MSA([FASTA('seq1', None, 'CA'), FASTA('seq2', None, 'AG')]), 
     '3':MSA([FASTA('seq1', None, 'GT'), FASTA('seq2', None, 'GA')])}
    @py_assert1 = msa.split
    @py_assert3 = '123'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == expected
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=395)
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.split\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, expected)) % {'py0':@pytest_ar._saferepr(msa) if 'msa' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msa) else 'msa',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_msa_split__empty_group():
    msa = MSA([FASTA('seq1', None, 'AC'), FASTA('seq2', None, 'GA')])
    expected = {'1':MSA([FASTA('seq1', None, 'A'), FASTA('seq2', None, 'G')]), 
     '2':MSA([FASTA('seq1', None, 'C'), FASTA('seq2', None, 'A')]), 
     '3':MSA([FASTA('seq1', None, ''), FASTA('seq2', None, '')])}
    @py_assert1 = msa.split
    @py_assert3 = '123'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == expected
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=405)
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.split\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, expected)) % {'py0':@pytest_ar._saferepr(msa) if 'msa' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msa) else 'msa',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_msa_split__partial_group():
    msa = MSA([FASTA('seq1', None, 'ACGCA'), FASTA('seq2', None, 'GAGTG')])
    expected = {'1':MSA([FASTA('seq1', None, 'AC'), FASTA('seq2', None, 'GT')]), 
     '2':MSA([FASTA('seq1', None, 'CA'), FASTA('seq2', None, 'AG')]), 
     '3':MSA([FASTA('seq1', None, 'G'), FASTA('seq2', None, 'G')])}
    @py_assert1 = msa.split
    @py_assert3 = '123'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == expected
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=415)
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.split\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, expected)) % {'py0':@pytest_ar._saferepr(msa) if 'msa' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msa) else 'msa',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_msa_split_msa__no_split_by():
    msa = MSA([FASTA('seq1', None, 'ACG'), FASTA('seq2', None, 'GAT')])
    with pytest.raises(TypeError):
        msa.split(split_by='')


def test_msa_to_file__complete_line_test():
    msa = MSA([
     FASTA('barfoo', None, 'ACGATA' * 10 + 'CGATAG' * 5),
     FASTA('foobar', None, 'CGAATG' * 10 + 'TGTCAT' * 5)])
    expected = '>barfoo\n%s\n%s\n' % ('ACGATA' * 10, 'CGATAG' * 5)
    expected += '>foobar\n%s\n%s\n' % ('CGAATG' * 10, 'TGTCAT' * 5)
    stringf = io.StringIO()
    MSA.to_file(msa, stringf)
    @py_assert1 = stringf.getvalue
    @py_assert3 = @py_assert1()
    @py_assert5 = @py_assert3 == expected
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=440)
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.getvalue\n}()\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(stringf) if 'stringf' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stringf) else 'stringf',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_msa_validate__missing_names_first():
    msa_1 = MSA(list(_JOIN_MSA_1)[:-1])
    msa_2 = copy.copy(_JOIN_MSA_2)
    with pytest.raises(MSAError):
        MSA.validate(msa_1, msa_2)


def test_msa_validate__missing_names_second():
    msa_1 = copy.copy(_JOIN_MSA_1)
    msa_2 = MSA(list(_JOIN_MSA_2)[:-1])
    with pytest.raises(MSAError):
        MSA.validate(msa_1, msa_2)


def test_msa_names():
    @py_assert1 = _JOIN_MSA_1.names
    @py_assert3 = @py_assert1()
    @py_assert7 = ('nc', 'nm', 'miRNA')
    @py_assert9 = set(@py_assert7)
    @py_assert5 = @py_assert3 == @py_assert9
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=468)
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.names\n}()\n} == %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(_JOIN_MSA_1) if '_JOIN_MSA_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_JOIN_MSA_1) else '_JOIN_MSA_1',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_msa_repr():
    msa = MSA((
     FASTA('nc', None, 'ACGTA'),
     FASTA('nm', 'META', 'TGAGT'),
     FASTA('miRNA', None, 'UCAGA')))
    @py_assert2 = str(msa)
    @py_assert5 = "MSA(FASTA('miRNA', '', 'UCAGA'), FASTA('nc', '', 'ACGTA'), FASTA('nm', 'META', 'TGAGT'))"
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=485)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(msa) if 'msa' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msa) else 'msa',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_msa_repr__same_as_str():
    @py_assert2 = str(_JOIN_MSA_1)
    @py_assert7 = repr(_JOIN_MSA_1)
    @py_assert4 = @py_assert2 == @py_assert7
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/msa_test.py', lineno=493)
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}', ), (@py_assert2, @py_assert7)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(_JOIN_MSA_1) if '_JOIN_MSA_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_JOIN_MSA_1) else '_JOIN_MSA_1',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr',  'py6':@pytest_ar._saferepr(_JOIN_MSA_1) if '_JOIN_MSA_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_JOIN_MSA_1) else '_JOIN_MSA_1',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None