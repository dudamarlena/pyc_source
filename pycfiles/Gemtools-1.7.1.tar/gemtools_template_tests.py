# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/devel/thasso/git/github/gemtools/python/test/gemtools_template_tests.py
# Compiled at: 2013-04-17 04:25:02
import gem.gemtools as gt
from testfiles import testfiles
test_mapping = testfiles['test.map']
test_zipped_mapping = testfiles['test.map.gz']
test_fastq = testfiles['test.fastq']

def test_template_attribute_reading_first_mapping():
    infile = gt.InputFile(testfiles['test.map'])
    for tmpl in infile:
        print 'Template'
        assert tmpl.tag == 'HWI-ST661:153:D0FTJACXX:2:1102:13924:124292', tmpl.tag
        assert tmpl.blocks == 1, tmpl.blocks
        assert tmpl.counters == 3, tmpl.counters
        assert tmpl.mcs == 2, tmpl.mcs
        assert tmpl.level() == -1, tmpl.level()
        break


def test_template_uniqness_level():
    infile = gt.InputFile(testfiles['test.map'])
    levels = [ t.level() for t in infile ]
    assert levels == [-1, 37, 0, -1, 0, 0, 0, 0, 0, 0], levels


def test_template_interleave():
    infile1 = gt.InputFile(testfiles['test.map'])
    infile2 = gt.InputFile(testfiles['test.map'])
    interleave = gt.interleave([infile1, infile2])
    levels = [ t.level() for t in interleave ]
    assert levels == [-1, -1, 37, 37, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], levels


def test_template_unmapped_filter_length():
    infile = gt.InputFile(testfiles['test.map.gz'])
    assert 1 == len([ x for x in gt.unmapped(infile, 1) ]), len([ x for x in gt.unmapped(infile, 1) ])
    assert 5 == len([ x for x in gt.unmapped(infile, 0) ]), len([ x for x in gt.unmapped(infile, 0) ])
    assert 1 == len([ x for x in gt.unmapped(infile, 2) ]), len([ x for x in gt.unmapped(infile, 2) ])
    assert 0 == len([ x for x in gt.unmapped(infile, 3) ]), len([ x for x in gt.unmapped(infile, 3) ])
    assert 0 == len([ x for x in gt.unmapped(infile, 4) ]), len([ x for x in gt.unmapped(infile, 4) ])


def test_template_unique_filter_level():
    infile = gt.InputFile(testfiles['test.map.gz'])
    assert 1 == len([ x for x in gt.unique(infile, 20) ]), 'Should be length 1 buyt is: ' + str([ x.level() for x in gt.unique(infile, 20) ])


def test_template_map_parsing():
    template = gt.Template()
    template.parse('A/1\tAAA\t###\t0\t-\n')
    assert template.tag == 'A'


def test_template_length():
    template = gt.Template()
    template.parse('A/1\tAAA\t###\t0\t-\n')
    assert template.length == 3


def test_template_read():
    template = gt.Template()
    template.parse('A/1\tAAA\t###\t0\t-\n')
    assert template.read == 'AAA'


def test_template_qualities():
    template = gt.Template()
    template.parse('A/1\tAAA\t###\t0\t-\n')
    assert template.qualities == '###'


def test_template_no_qualities():
    template = gt.Template()
    template.parse('A/1\tAAA\t\t0\t-\n')
    assert template.qualities == ''


def test_template_to_map():
    template = gt.Template()
    template.parse('A/1\tAAA\t\t0\t-\n')
    assert template.to_map() == 'A/1\tAAA\t\t0\t-', "Not '%s'" % template.to_map()


def test_template_to_fasta():
    template = gt.Template()
    template.parse('A/1\tAAA\t\t0\t-\n')
    assert template.to_fasta() == '>A/1\nAAA', "Not '%s'" % template.to_fasta()


def test_template_to_fastq():
    template = gt.Template()
    template.parse('A/1\tAAA\t###\t0\t-\n')
    assert template.to_fastq() == '@A/1\nAAA\n+\n###', "Not '%s'" % template.to_fastq()


def test_template_to_sequence():
    template = gt.Template()
    template.parse('A/1\tAAA\t###\t0\t-\n')
    assert template.to_sequence() == '@A/1\nAAA\n+\n###', "Not '%s'" % template.to_sequence()
    template.parse('A/1\tAAA\t\t0\t-\n')
    assert template.to_fasta() == '>A/1\nAAA', "Not '%s'" % template.to_sequence()


def test_template_merge():
    template_1 = gt.Template()
    template_1.parse('A/1\tAAA\t###\t0\t-\n')
    template_2 = gt.Template()
    template_2.parse('A/1\tAAA\t###\t1\tchr1:+:50:3')
    template_1.merge(template_2)
    assert template_1.to_map() == 'A/1\tAAA\t###\t1\tchr1:+:50:3', "Not '%s'" % template_1.to_map()