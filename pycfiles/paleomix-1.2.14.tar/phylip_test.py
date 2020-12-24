# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/common_tests/formats_tests/phylip_test.py
# Compiled at: 2019-10-27 09:55:00
from flexmock import flexmock
from nose.tools import assert_equal
from paleomix.common.formats.phylip import sequential_phy, interleaved_phy
from paleomix.common.formats.msa import MSA
from paleomix.common.formats.fasta import FASTA
_MSA_SHORT_SEQUENCES = MSA([FASTA('seq1', None, 'ACGTTGATAACCAGG'),
 FASTA('seq2', None, 'TGCAGAGTACGACGT')])
_MSA_MEDIUM_SEQUENCES = MSA([FASTA('seq1', None, 'ACGTTGATAACCAGGAGGGATTCGCGATTGGTGGTAACGTAGCC'),
 FASTA('seq2', None, 'TGCAGAGTACGACGTCTCCTAGATCCTGGACAATTTAAACCGAA')])
_MSA_LONG_SEQUENCES = MSA([FASTA('seq1', None, 'CGGATCTGCTCCTCCACTGGCCACGTTTACTGTCCCCCAACCGTTCGTCCCGACCTAGTTATACTTCTTAGCAAGGTGTAAAACCAGAGATTGAGGTTATAACGTTCCTAATCAGTTATTAAATTACCGCGCCCCGACAG'),
 FASTA('seq2', None, 'AGTTGAAGAGGCGGAACGTTTGTAAACCGCGCTAACGTAGTTCTACAACCAGCCACCCGGTTCGAAGGAACAACTGGTCGCCATAATTAGGCGAAACGATAGTGCACTAAGGTCAGGTGCGCCCCTGTAAATAATTAGAT')])
_MSA_MEDIUM_NAMES = MSA([FASTA('A_really_long_sequence', None, 'ACGTTGATAACCAGG'),
 FASTA('Another_real_long_one!', None, 'TGCAGAGTACGACGT')])
_MSA_LONG_NAMES = MSA([FASTA('A_really_long_sequence_name_that_is_in_fact_too_long', None, 'ACGTTGATAACCAGG'),
 FASTA('Another_really_long_sequence_name_that_is_too_long', None, 'TGCAGAGTACGACGT')])

def test_sequential_phy__short_sequences():
    expected = '2 44\n\nseq1\nACGTTGATAA  CCAGGAGGGA  TTCGCGATTG  GTGGTAACGT  AGCC\nseq2\nTGCAGAGTAC  GACGTCTCCT  AGATCCTGGA  CAATTTAAAC  CGAA'
    assert_equal(sequential_phy(_MSA_MEDIUM_SEQUENCES), expected)


def test_sequential_phy__multi_line_sequences():
    expected = '2 140\n\nseq1\nCGGATCTGCT  CCTCCACTGG  CCACGTTTAC  TGTCCCCCAA  CCGTTCGTCC  CGACCTAGTT\nATACTTCTTA  GCAAGGTGTA  AAACCAGAGA  TTGAGGTTAT  AACGTTCCTA  ATCAGTTATT\nAAATTACCGC  GCCCCGACAG\nseq2\nAGTTGAAGAG  GCGGAACGTT  TGTAAACCGC  GCTAACGTAG  TTCTACAACC  AGCCACCCGG\nTTCGAAGGAA  CAACTGGTCG  CCATAATTAG  GCGAAACGAT  AGTGCACTAA  GGTCAGGTGC\nGCCCCTGTAA  ATAATTAGAT'
    assert_equal(sequential_phy(_MSA_LONG_SEQUENCES), expected)


def test_sequential_phy__with_flag():
    expected = '2 15 S\n\nseq1\nACGTTGATAA  CCAGG\nseq2\nTGCAGAGTAC  GACGT'
    assert_equal(sequential_phy(_MSA_SHORT_SEQUENCES, add_flag=True), expected)


def test_sequentual_phy__long_names():
    expected = '2 15\n\nA_really_long_sequence_name_th\nACGTTGATAA  CCAGG\nAnother_really_long_sequence_n\nTGCAGAGTAC  GACGT'
    assert_equal(sequential_phy(_MSA_LONG_NAMES), expected)


def test_sequential_phy__different_lengths():
    _mock = flexmock(MSA).should_receive('validate').at_least.once
    sequential_phy(_MSA_MEDIUM_NAMES)


def test_interleaved_phy__short_sequences():
    expected = '2 44\n\nseq1        ACGTTGATAA  CCAGGAGGGA  TTCGCGATTG  GTGGTAACGT  AGCC\nseq2        TGCAGAGTAC  GACGTCTCCT  AGATCCTGGA  CAATTTAAAC  CGAA'
    assert_equal(interleaved_phy(_MSA_MEDIUM_SEQUENCES), expected)


def test_interleaved_phy__multi_line_sequences():
    expected = '2 140\n\nseq1        CGGATCTGCT  CCTCCACTGG  CCACGTTTAC  TGTCCCCCAA  CCGTTCGTCC\nseq2        AGTTGAAGAG  GCGGAACGTT  TGTAAACCGC  GCTAACGTAG  TTCTACAACC\n\nCGACCTAGTT  ATACTTCTTA  GCAAGGTGTA  AAACCAGAGA  TTGAGGTTAT  AACGTTCCTA\nAGCCACCCGG  TTCGAAGGAA  CAACTGGTCG  CCATAATTAG  GCGAAACGAT  AGTGCACTAA\n\nATCAGTTATT  AAATTACCGC  GCCCCGACAG\nGGTCAGGTGC  GCCCCTGTAA  ATAATTAGAT'
    assert_equal(interleaved_phy(_MSA_LONG_SEQUENCES), expected)


def test_interleaved_phy__with_flag():
    expected = '2 15 I\n\nseq1        ACGTTGATAA  CCAGG\nseq2        TGCAGAGTAC  GACGT'
    assert_equal(interleaved_phy(_MSA_SHORT_SEQUENCES, add_flag=True), expected)


def test_interleaved_phy__medium_names():
    expected = '2 15\n\nA_really_long_sequence  ACGTTGATAA  CCAGG\nAnother_real_long_one!  TGCAGAGTAC  GACGT'
    assert_equal(interleaved_phy(_MSA_MEDIUM_NAMES), expected)


def test_interleaved_phy__long_names():
    expected = '2 15\n\nA_really_long_sequence_name_th      ACGTTGATAA  CCAGG\nAnother_really_long_sequence_n      TGCAGAGTAC  GACGT'
    assert_equal(interleaved_phy(_MSA_LONG_NAMES), expected)


def test_sequentual_phy__different_length_names_1():
    msa = MSA([FASTA('A_short_name', None, 'ACGTTGATAACCAGG'),
     FASTA('Another_really_long_sequence_name_that_is_too_long', None, 'TGCAGAGTACGACGT')])
    expected = '2 15\n\nA_short_name                        ACGTTGATAA  CCAGG\nAnother_really_long_sequence_n      TGCAGAGTAC  GACGT'
    print interleaved_phy(msa), expected
    assert_equal(interleaved_phy(msa), expected)
    return


def test_sequentual_phy__different_length_names_2():
    msa = MSA([FASTA('Burchelli_4', None, 'ACGTTGATAACCAGG'),
     FASTA('Donkey', None, 'TGCAGAGTACGACGT')])
    expected = '2 15\n\nBurchelli_4             ACGTTGATAA  CCAGG\nDonkey                  TGCAGAGTAC  GACGT'
    print interleaved_phy(msa), expected
    assert_equal(interleaved_phy(msa), expected)
    return


def test_interleaved_phy__different_lengths():
    _mock = flexmock(MSA).should_receive('validate').at_least.once
    interleaved_phy(_MSA_MEDIUM_NAMES)