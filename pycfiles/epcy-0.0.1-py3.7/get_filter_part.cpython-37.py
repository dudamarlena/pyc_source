# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/epcy/argparser/get_filter_part.py
# Compiled at: 2020-03-19 17:50:07
# Size of source mod 2**32: 522 bytes


def get_argparser_filter_part(parser):
    parser.add_argument('-e', dest='EXP',
      help='filter features with sum(values(features)) < (Default:0).',
      type=float,
      default=0)
    parser.add_argument('-l', dest='L2FC',
      help='filter trans/genes with log2FC < (Default:0.3).',
      type=float,
      default=0.3)