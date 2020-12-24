# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/io/readers.py
# Compiled at: 2019-09-04 14:12:25
# Size of source mod 2**32: 1123 bytes
from .bedfile import BedFile

def read_bed(filepath_or_buffer, column_names=[
 'chrom', 'chromStart', 'chromEnd', 'name', 'score',
 'strand', 'thickStart', 'thickEnd', 'itemRGB', 'blockCount',
 'blockSizes', 'blockStarts'], skiprows=None):
    return BedFile.read(filepath_or_buffer, column_names, skiprows)