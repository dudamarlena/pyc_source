# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/io/test/test_bed.py
# Compiled at: 2019-09-04 14:12:25
# Size of source mod 2**32: 3224 bytes
import unittest, json, pandas as pd
from bdgenomics.mango.io import *
import bdgenomics.mango.pileup as pileup
from bdgenomics.mango.pileup.track import *
from bdgenomics.mango.io.test import IOTestCase

class BedFileTest(IOTestCase):

    def test_required_columns(self):
        dataframe = read_bed(self.exampleFile('chr17.582500-594500.bed'))
        dataframe_columns = list(dataframe.columns)
        for name in ('chrom', 'chromStart', 'chromEnd'):
            assert name in dataframe_columns

    def test_column_type(self):
        dataframe = read_bed(self.exampleFile('chr17.582500-594500.bed'))
        chromosomes = list(dataframe['chrom'])
        chromStart = list(dataframe['chromStart'])
        chromEnd = list(dataframe['chromEnd'])
        d1, d2, d3 = dataframe._mango_parse
        for i in range(len(chromStart)):
            assert type(d1[i] == int)
            assert d1[i] == chromStart[i]

        for i in range(len(chromEnd)):
            assert type(d2[i] == int)
            assert d2[i] == chromEnd[i]

        for i in range(len(chromosomes)):
            assert type(d3[i] == int)
            assert d3[i] == chromosomes[i]

    def test_validate_num_rows(self):
        file = self.exampleFile('chr17.582500-594500.bed')
        dataframe = read_bed(file)
        with open(file, 'r') as (ins):
            lines = []
            for line in ins:
                lines.append(line)

            assert len(lines) == len(dataframe.index)

    def test_to_json(self):
        dataframe = read_bed(self.exampleFile('chr17.582500-594500.bed'))

        def is_valid_json(string):
            try:
                json_object = json.loads(string)
            except ValueError:
                return False
            else:
                return True

        assert type(dataframe._mango_to_json) == str
        assert is_valid_json(dataframe._mango_to_json) == True

    def test_visualization(self):
        dataframe = read_bed(self.exampleFile('chr17.582500-594500.bed'))
        assert dataframe._pileup_visualization == 'featureJson'
        tracks = [Track(viz='features', label='my features', source=(pileup.sources.DataFrameSource(dataframe)))]
        reads = pileup.PileupViewer(locus='chr22:10436-10564', reference='hg19', tracks=tracks)
        assert str(type(reads)) == "<class 'bdgenomics.mango.pileup.pileupViewer.PileupViewer'>"


if __name__ == '__main__':
    unittest.main()