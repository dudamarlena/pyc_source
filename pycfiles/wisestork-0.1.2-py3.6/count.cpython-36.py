# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wisestork/count.py
# Compiled at: 2019-06-13 09:35:55
# Size of source mod 2**32: 2860 bytes
"""
wisestork.count
~~~~~~~~~~~~~~
:copyright: (c) 2016-2019 Sander Bollen
:license: GPL-3.0
"""
import pysam
from .utils import get_bins, BedReader, BedLine

def reads_per_bin(bam_reader, chromosome, bin):
    """
    Number of reads per bin
    :param bam_reader: an instance of pysam.AlignmentFile
    :param chromosome: chromosome name
    :param bin: Bin namedtuple
    :return: integer
    """
    try:
        reads = bam_reader.count(chromosome, bin.start, bin.end)
    except ValueError:
        reads = 0

    return reads


def get_chromosomes_from_header(header):
    """
    Get list of chromosome names from bam headers
    :param header: bam header
    :return: list of tuples of (chromosome names, chromosome_length)
    """
    return [(x['SN'], x['LN']) for x in header['SQ']]


def get_chromosomes_from_fasta(fa):
    """
    Get chromosome names from fasta file
    :param fa: instance of pyfaidx.Fasta
    :return: list of tuples of (chromosome names, chromosome_lenght)
    """
    return [(x, len(fa[x])) for x in fa.keys()]


def count(input, output, binsize, reference, binfile=None):
    """
    Main function for counting reads per bin
    :param input: Path to input BAM
    :param output: path to output BED
    :param binsize: binsize
    :param reference: path to reference fasta
    """
    samfile = pysam.AlignmentFile(input, 'rb')
    chromosomes = get_chromosomes_from_header(samfile.header)
    with open(output, 'wb') as (ohandle):
        if binfile:
            bin_reader = BedReader(binfile)
            for bin in bin_reader:
                val = reads_per_bin(samfile, bin.chromosome, bin)
                bed = BedLine(bin.chromosome, bin.start, bin.end, val)
                ohandle.write(bytes(bed) + b'\n')

        else:
            for ch, ln in chromosomes:
                for bin in get_bins(ln, binsize):
                    val = reads_per_bin(samfile, ch, bin)
                    bed = BedLine(ch, bin.start, bin.end, val)
                    ohandle.write(bytes(bed) + b'\n')