# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/common_tests/formats_tests/phylip_test.py
# Compiled at: 2019-10-16 14:47:34
# Size of source mod 2**32: 5237 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from paleomix.common.formats.fasta import FASTA
from paleomix.common.formats.msa import MSA
from paleomix.common.formats.phylip import interleaved_phy
_MSA_SHORT_SEQUENCES = MSA([
 FASTA('seq1', None, 'ACGTTGATAACCAGG'), FASTA('seq2', None, 'TGCAGAGTACGACGT')])
_MSA_MEDIUM_SEQUENCES = MSA([
 FASTA('seq1', None, 'ACGTTGATAACCAGGAGGGATTCGCGATTGGTGGTAACGTAGCC'),
 FASTA('seq2', None, 'TGCAGAGTACGACGTCTCCTAGATCCTGGACAATTTAAACCGAA')])
_MSA_LONG_SEQUENCES = MSA([
 FASTA('seq1', None, 'CGGATCTGCTCCTCCACTGGCCACGTTTACTGTCCCCCAACCGTTCGTCCCGACCTAGTTATACTTCTTAGCAAGGTGTAAAACCAGAGATTGAGGTTATAACGTTCCTAATCAGTTATTAAATTACCGCGCCCCGACAG'),
 FASTA('seq2', None, 'AGTTGAAGAGGCGGAACGTTTGTAAACCGCGCTAACGTAGTTCTACAACCAGCCACCCGGTTCGAAGGAACAACTGGTCGCCATAATTAGGCGAAACGATAGTGCACTAAGGTCAGGTGCGCCCCTGTAAATAATTAGAT')])
_MSA_MEDIUM_NAMES = MSA([
 FASTA('A_really_long_sequence', None, 'ACGTTGATAACCAGG'),
 FASTA('Another_real_long_one!', None, 'TGCAGAGTACGACGT')])
_MSA_LONG_NAMES = MSA([
 FASTA('A_really_long_sequence_name_that_is_in_fact_too_long', None, 'ACGTTGATAACCAGG'),
 FASTA('Another_really_long_sequence_name_that_is_too_long', None, 'TGCAGAGTACGACGT')])

def test_interleaved_phy__short_sequences():
    expected = ' 2 44\nseq1  ACGTTGATAA CCAGGAGGGA TTCGCGATTG GTGGTAACGT AGCC\nseq2  TGCAGAGTAC GACGTCTCCT AGATCCTGGA CAATTTAAAC CGAA\n'
    @py_assert2 = interleaved_phy(_MSA_MEDIUM_SEQUENCES)
    @py_assert4 = @py_assert2 == expected
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/phylip_test.py', lineno=92)
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, expected)) % {'py0':@pytest_ar._saferepr(interleaved_phy) if 'interleaved_phy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(interleaved_phy) else 'interleaved_phy',  'py1':@pytest_ar._saferepr(_MSA_MEDIUM_SEQUENCES) if '_MSA_MEDIUM_SEQUENCES' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_MSA_MEDIUM_SEQUENCES) else '_MSA_MEDIUM_SEQUENCES',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None


def test_interleaved_phy__multi_line_sequences():
    expected = ' 2 140\nseq1  CGGATCTGCT CCTCCACTGG CCACGTTTAC TGTCCCCCAA CCGTTCGTCC\nseq2  AGTTGAAGAG GCGGAACGTT TGTAAACCGC GCTAACGTAG TTCTACAACC\n\n      CGACCTAGTT ATACTTCTTA GCAAGGTGTA AAACCAGAGA TTGAGGTTAT\n      AGCCACCCGG TTCGAAGGAA CAACTGGTCG CCATAATTAG GCGAAACGAT\n\n      AACGTTCCTA ATCAGTTATT AAATTACCGC GCCCCGACAG \n      AGTGCACTAA GGTCAGGTGC GCCCCTGTAA ATAATTAGAT \n'
    @py_assert2 = interleaved_phy(_MSA_LONG_SEQUENCES)
    @py_assert4 = @py_assert2 == expected
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/phylip_test.py', lineno=106)
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, expected)) % {'py0':@pytest_ar._saferepr(interleaved_phy) if 'interleaved_phy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(interleaved_phy) else 'interleaved_phy',  'py1':@pytest_ar._saferepr(_MSA_LONG_SEQUENCES) if '_MSA_LONG_SEQUENCES' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_MSA_LONG_SEQUENCES) else '_MSA_LONG_SEQUENCES',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None


def test_interleaved_phy__medium_names():
    expected = ' 2 15\nA_really_long_sequence  ACGTTGATAA CCAGG\nAnother_real_long_one!  TGCAGAGTAC GACGT\n'
    @py_assert2 = interleaved_phy(_MSA_MEDIUM_NAMES)
    @py_assert4 = @py_assert2 == expected
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/phylip_test.py', lineno=114)
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, expected)) % {'py0':@pytest_ar._saferepr(interleaved_phy) if 'interleaved_phy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(interleaved_phy) else 'interleaved_phy',  'py1':@pytest_ar._saferepr(_MSA_MEDIUM_NAMES) if '_MSA_MEDIUM_NAMES' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_MSA_MEDIUM_NAMES) else '_MSA_MEDIUM_NAMES',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None


def test_interleaved_phy__long_names():
    expected = ' 2 15\nA_really_long_sequence_name_that_is_in_fact_too_long  ACGTTGATAA CCAGG\nAnother_really_long_sequence_name_that_is_too_long    TGCAGAGTAC GACGT\n'
    @py_assert2 = interleaved_phy(_MSA_LONG_NAMES)
    @py_assert4 = @py_assert2 == expected
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/phylip_test.py', lineno=122)
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, expected)) % {'py0':@pytest_ar._saferepr(interleaved_phy) if 'interleaved_phy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(interleaved_phy) else 'interleaved_phy',  'py1':@pytest_ar._saferepr(_MSA_LONG_NAMES) if '_MSA_LONG_NAMES' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_MSA_LONG_NAMES) else '_MSA_LONG_NAMES',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None


def test_sequentual_phy__different_length_names_1():
    msa = MSA([
     FASTA('A_short_name', None, 'ACGTTGATAACCAGG'),
     FASTA('Another_really_long_sequence_name_that_is_too_long', None, 'TGCAGAGTACGACGT')])
    expected = ' 2 15\nA_short_name                                        ACGTTGATAA CCAGG\nAnother_really_long_sequence_name_that_is_too_long  TGCAGAGTAC GACGT\n'
    @py_assert2 = interleaved_phy(msa)
    @py_assert4 = @py_assert2 == expected
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/phylip_test.py', lineno=140)
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, expected)) % {'py0':@pytest_ar._saferepr(interleaved_phy) if 'interleaved_phy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(interleaved_phy) else 'interleaved_phy',  'py1':@pytest_ar._saferepr(msa) if 'msa' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msa) else 'msa',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None


def test_sequentual_phy__different_length_names_2():
    msa = MSA([
     FASTA('Burchelli_4', None, 'ACGTTGATAACCAGG'),
     FASTA('Donkey', None, 'TGCAGAGTACGACGT')])
    expected = ' 2 15\nBurchelli_4  ACGTTGATAA CCAGG\nDonkey       TGCAGAGTAC GACGT\n'
    @py_assert2 = interleaved_phy(msa)
    @py_assert4 = @py_assert2 == expected
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/formats_tests/phylip_test.py', lineno=154)
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, expected)) % {'py0':@pytest_ar._saferepr(interleaved_phy) if 'interleaved_phy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(interleaved_phy) else 'interleaved_phy',  'py1':@pytest_ar._saferepr(msa) if 'msa' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msa) else 'msa',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None


def test_interleaved_phy__different_lengths():
    with pytest.raises(ValueError, match='Sequences must all be the same length'):
        interleaved_phy([
         FASTA('seq1', None, 'ACGTTGATAACCAGG'),
         FASTA('seq2', None, 'TGCAGAGTACGACGTA')])