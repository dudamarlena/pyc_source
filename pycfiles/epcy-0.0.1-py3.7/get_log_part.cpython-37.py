# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/epcy/argparser/get_log_part.py
# Compiled at: 2020-03-20 10:10:43
# Size of source mod 2**32: 585 bytes


def get_argparser_log_part(parser):
    parser.add_argument('--log', dest='LOG',
      help='To apply a log2 transformation log2(x + C) (see -c) ).',
      action='store_true')
    parser.add_argument('-c', dest='C',
      help='Constant value used during log transformation, log2(x+C) (Default: C=1).',
      type=float,
      default=1.0)
    parser.set_defaults(LOG=False)