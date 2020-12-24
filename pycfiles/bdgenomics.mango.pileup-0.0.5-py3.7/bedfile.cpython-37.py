# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/io/bedfile.py
# Compiled at: 2019-09-04 14:12:25
# Size of source mod 2**32: 2029 bytes
from .genomicfile import GenomicFile

class BedFile(GenomicFile):

    @classmethod
    def _read(cls, filepath_or_buffer, column_names, skiprows):
        return cls.dataframe_lib.read_table(filepath_or_buffer, names=column_names, skiprows=skiprows)

    @classmethod
    def _parse(cls, df):
        chromosomes = list(df['chrom'])
        chrom_starts = list(df['chromStart'])
        chrom_ends = list(df['chromEnd'])
        return (chrom_starts, chrom_ends, chromosomes)

    @classmethod
    def _to_json(cls, df):
        chrom_starts, chrom_ends, chromosomes = cls._parse(df)
        json_ga4gh = '{"features":['
        for i in range(len(chromosomes) + 1):
            if i < len(chromosomes):
                bed_content = '"referenceName":{}, "start":{}, "end":{}'.format('"' + str(chromosomes[i]) + '"', '"' + str(chrom_starts[i]) + '"', '"' + str(chrom_ends[i]) + '"')
                json_ga4gh = json_ga4gh + '{' + bed_content + '},'
            else:
                json_ga4gh = json_ga4gh[:len(json_ga4gh) - 1]

        json_ga4gh = json_ga4gh + ']}'
        return json_ga4gh

    @classmethod
    def _visualization(cls, df):
        return 'featureJson'