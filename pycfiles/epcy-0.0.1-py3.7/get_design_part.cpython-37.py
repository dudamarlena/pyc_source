# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/epcy/argparser/get_design_part.py
# Compiled at: 2020-03-19 17:49:49
# Size of source mod 2**32: 867 bytes
from .common import *

def get_argparser_design_part(parser):
    parser.add_argument('-d', dest='DESIGN',
      help='Tabulated file who discribe your design.',
      type=(lambda x: is_valid_file(parser, x)))
    parser.add_argument('--query', dest='QUERY',
      help='Query value specify in the subgroup column for samples queried (Default: Query).',
      type=str,
      default='Query')
    parser.add_argument('--subgroup', dest='SUBGROUP',
      help='Header name of the subgroup column in your design file (Default: subgroup).',
      type=str,
      default='subgroup')