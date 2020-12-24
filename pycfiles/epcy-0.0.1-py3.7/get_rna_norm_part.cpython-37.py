# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/epcy/argparser/get_rna_norm_part.py
# Compiled at: 2020-03-20 10:15:01
# Size of source mod 2**32: 601 bytes


def get_argparser_rna_norm_part(parser):
    parser.add_argument('--cpm', dest='CPM',
      help='To apply a Count Par Million (CPM) normalization to the matrix given in input (-m)',
      action='store_true')
    parser.add_argument('--tpm', dest='TPM',
      help='Compute TPM from readcounts. (Need --anno)',
      action='store_true')
    parser.set_defaults(TPM=False)
    parser.set_defaults(CPM=False)