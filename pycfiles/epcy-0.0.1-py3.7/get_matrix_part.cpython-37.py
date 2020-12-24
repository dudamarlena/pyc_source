# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/epcy/argparser/get_matrix_part.py
# Compiled at: 2020-03-20 10:15:12
# Size of source mod 2**32: 897 bytes
from .common import *

def get_argparser_matrix(parser):
    parser.add_argument('-m', dest='MATRIX',
      help='tsv file of features matrix quantification.',
      type=(lambda x: is_valid_file(parser, x)))
    parser.add_argument('--replacena', dest='REPLACE_NA',
      help='To specify a value to replace missing value. Without (and if missing value is present) predictive capabilty will be compute without samples with missing value into the feature. In that case, the number of samples used for each group will be reported for each features.',
      type=float,
      default=None)