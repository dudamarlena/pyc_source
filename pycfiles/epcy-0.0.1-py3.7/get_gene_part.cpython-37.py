# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/epcy/argparser/get_gene_part.py
# Compiled at: 2020-03-19 17:51:02
# Size of source mod 2**32: 745 bytes
from .common import *

def get_argparser_gene_part(parser):
    parser.add_argument('--gene', dest='GENE',
      help='If the quantification is compute on transcripts, this option allow to calculate predictive capability on genes, using annotation file (--anno).',
      action='store_true')
    parser.add_argument('--anno', dest='ANNO',
      help='(Optional) gff3 file of the feautres annotation.',
      type=(lambda x: is_valid_file(parser, x)))
    parser.set_defaults(GENE=False)