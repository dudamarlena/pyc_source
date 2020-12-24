# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clareau/dat/Research/BuenrostroResearch/lareau_dev/bap/bap/cli_reanno.py
# Compiled at: 2018-10-29 20:09:49
# Size of source mod 2**32: 1310 bytes
import click, os, os.path, sys, shutil, yaml, random, string, itertools, time, pysam, csv, re
from itertools import groupby
from .bapHelp import *
from pkg_resources import get_distribution

@click.command()
@click.version_option()
@click.option('--input', '-i', help='Input bam file.')
@click.option('--output', '-o', help='Output bam file.')
@click.option('--sep', '-s', default='_', help='Separator for reannotation. Assume: {barcode}_{readname} (default delim = "_")')
@click.option('--tag', '-t', default='XB', help='Sam tag for barcode; by default, assume XB.\n\n')
def main(input, output, sep, tag):
    """
        bap-reanno: Reannotate samples that were de-barcoded and aligned 

        Caleb Lareau, clareau <at> broadinstitute <dot> org 
        
        """
    __version__ = get_distribution('bap').version
    script_dir = os.path.dirname(os.path.realpath(__file__))
    click.echo(gettime() + 'Starting re-barcoding from bap pipeline v%s' % __version__)
    bam = pysam.AlignmentFile(input, 'rb')
    out = pysam.AlignmentFile(output, 'wb', template=bam)
    for read in bam:
        name = read.query_name
        ss = name.split(sep)
        read.query_name = ss[1]
        read.tags = read.tags + [(tag, ss[0])]
        out.write(read)