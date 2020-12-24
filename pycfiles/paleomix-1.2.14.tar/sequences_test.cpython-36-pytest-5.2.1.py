# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/common_tests/sequences_test.py
# Compiled at: 2019-10-16 12:05:38
# Size of source mod 2**32: 4181 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, itertools, pytest
from paleomix.common.sequences import complement, reverse_complement, encode_genotype, split
_REF_SRC = 'ACGTMRWSYKVHDBNX'
_REF_DST = 'TGCAKYWSRMBDHVNX'

@pytest.mark.parametrize('src, dst', zip(_REF_SRC, _REF_DST))
def test_complement__single_nt(src, dst):
    @py_assert2 = complement(src)
    @py_assert4 = @py_assert2 == dst
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/sequences_test.py', lineno=45)
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, dst)) % {'py0':@pytest_ar._saferepr(complement) if 'complement' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(complement) else 'complement',  'py1':@pytest_ar._saferepr(src) if 'src' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(src) else 'src',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(dst) if 'dst' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dst) else 'dst'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None
    @py_assert2 = src.lower
    @py_assert4 = @py_assert2()
    @py_assert6 = complement(@py_assert4)
    @py_assert10 = dst.lower
    @py_assert12 = @py_assert10()
    @py_assert8 = @py_assert6 == @py_assert12
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/sequences_test.py', lineno=46)
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.lower\n}()\n})\n} == %(py13)s\n{%(py13)s = %(py11)s\n{%(py11)s = %(py9)s.lower\n}()\n}', ), (@py_assert6, @py_assert12)) % {'py0':@pytest_ar._saferepr(complement) if 'complement' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(complement) else 'complement',  'py1':@pytest_ar._saferepr(src) if 'src' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(src) else 'src',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(dst) if 'dst' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dst) else 'dst',  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None


def test_complement__multiple_nts_upper():
    @py_assert2 = complement(_REF_SRC)
    @py_assert4 = @py_assert2 == _REF_DST
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/sequences_test.py', lineno=50)
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, _REF_DST)) % {'py0':@pytest_ar._saferepr(complement) if 'complement' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(complement) else 'complement',  'py1':@pytest_ar._saferepr(_REF_SRC) if '_REF_SRC' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_REF_SRC) else '_REF_SRC',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(_REF_DST) if '_REF_DST' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_REF_DST) else '_REF_DST'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None


def test_complement__multiple_nts_lower():
    @py_assert2 = _REF_SRC.lower
    @py_assert4 = @py_assert2()
    @py_assert6 = complement(@py_assert4)
    @py_assert10 = _REF_DST.lower
    @py_assert12 = @py_assert10()
    @py_assert8 = @py_assert6 == @py_assert12
    if @py_assert8 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/sequences_test.py', lineno=54)
    if not @py_assert8:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.lower\n}()\n})\n} == %(py13)s\n{%(py13)s = %(py11)s\n{%(py11)s = %(py9)s.lower\n}()\n}', ), (@py_assert6, @py_assert12)) % {'py0':@pytest_ar._saferepr(complement) if 'complement' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(complement) else 'complement',  'py1':@pytest_ar._saferepr(_REF_SRC) if '_REF_SRC' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_REF_SRC) else '_REF_SRC',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(_REF_DST) if '_REF_DST' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_REF_DST) else '_REF_DST',  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = None


def test_complement__multiple_nts_mixed_case():
    @py_assert1 = 'aGtCn'
    @py_assert3 = complement(@py_assert1)
    @py_assert6 = 'tCaGn'
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/sequences_test.py', lineno=58)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(complement) if 'complement' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(complement) else 'complement',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_reverse_complement():
    @py_assert2 = reverse_complement(_REF_SRC)
    @py_assert5 = _REF_DST[::-1]
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/sequences_test.py', lineno=67)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(reverse_complement) if 'reverse_complement' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reverse_complement) else 'reverse_complement',  'py1':@pytest_ar._saferepr(_REF_SRC) if '_REF_SRC' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_REF_SRC) else '_REF_SRC',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


_IUB_SRC = ('A', 'C', 'G', 'T', 'AC', 'AG', 'AT', 'CG', 'CT', 'GT', 'ACG', 'ACT', 'AGT',
            'CGT', 'ACGT')
_IUB_DST = 'ACGTMRWSYKVHDB'

@pytest.mark.parametrize('src, dst', zip(_IUB_SRC, _IUB_DST))
def test_genotype__permutations(src, dst):
    for seq in itertools.permutations(src):
        @py_assert1 = ''
        @py_assert3 = @py_assert1.join
        @py_assert6 = @py_assert3(src)
        @py_assert8 = encode_genotype(@py_assert6)
        @py_assert10 = @py_assert8 == dst
        if @py_assert10 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/sequences_test.py', lineno=97)
        if not @py_assert10:
            @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py0)s(%(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s.join\n}(%(py5)s)\n})\n} == %(py11)s', ), (@py_assert8, dst)) % {'py0':@pytest_ar._saferepr(encode_genotype) if 'encode_genotype' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(encode_genotype) else 'encode_genotype',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(src) if 'src' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(src) else 'src',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(dst) if 'dst' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dst) else 'dst'}
            @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
            raise AssertionError(@pytest_ar._format_explanation(@py_format14))
        @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = None


@pytest.mark.parametrize('value', ('a', 'At', 'Z', '+'))
def test_genotype__bad_input(value):
    with pytest.raises(ValueError):
        encode_genotype(value)


@pytest.mark.parametrize('sequence', ('CT', 'C,T', ',C,T', 'C,T,', ',C,T,'))
def test_comma_or_not(sequence):
    @py_assert2 = encode_genotype(sequence)
    @py_assert5 = 'Y'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/sequences_test.py', lineno=108)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(encode_genotype) if 'encode_genotype' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(encode_genotype) else 'encode_genotype',  'py1':@pytest_ar._saferepr(sequence) if 'sequence' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sequence) else 'sequence',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_split__empty_sequence():
    @py_assert1 = ''
    @py_assert3 = split(@py_assert1)
    @py_assert6 = {'1':'', 
     '2':'',  '3':''}
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/sequences_test.py', lineno=117)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(split) if 'split' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(split) else 'split',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_split__no_split_by():
    with pytest.raises(ValueError, match='No split_by specified'):
        split('', split_by='')


def test_split__single_group():
    @py_assert1 = 'ACGCAT'
    @py_assert3 = '111'
    @py_assert5 = split(@py_assert1, @py_assert3)
    @py_assert8 = {'1': 'ACGCAT'}
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/sequences_test.py', lineno=126)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(split) if 'split' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(split) else 'split',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_split__two_groups():
    @py_assert1 = 'ACGCAT'
    @py_assert3 = '112'
    @py_assert5 = split(@py_assert1, @py_assert3)
    @py_assert8 = {'1':'ACCA', 
     '2':'GT'}
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/sequences_test.py', lineno=130)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(split) if 'split' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(split) else 'split',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_split__three_groups():
    expected = {'1':'AC', 
     '2':'CA',  '3':'GT'}
    @py_assert1 = 'ACGCAT'
    @py_assert3 = '123'
    @py_assert5 = split(@py_assert1, @py_assert3)
    @py_assert7 = @py_assert5 == expected
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/sequences_test.py', lineno=135)
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py8)s', ), (@py_assert5, expected)) % {'py0':@pytest_ar._saferepr(split) if 'split' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(split) else 'split',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = 'ACGCAT'
    @py_assert3 = split(@py_assert1)
    @py_assert5 = @py_assert3 == expected
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/sequences_test.py', lineno=136)
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(split) if 'split' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(split) else 'split',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_split__empty_group():
    expected = {'1':'A', 
     '2':'C',  '3':''}
    @py_assert1 = 'AC'
    @py_assert3 = split(@py_assert1)
    @py_assert5 = @py_assert3 == expected
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/sequences_test.py', lineno=141)
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(split) if 'split' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(split) else 'split',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_split__partial_group():
    expected = {'1':'AA', 
     '2':'CA',  '3':'G'}
    @py_assert1 = 'ACGAA'
    @py_assert3 = split(@py_assert1)
    @py_assert5 = @py_assert3 == expected
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/sequences_test.py', lineno=146)
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(split) if 'split' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(split) else 'split',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None