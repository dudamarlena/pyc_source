# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/epcy/argparser/get_bandwidth_part.py
# Compiled at: 2020-03-20 10:33:07
# Size of source mod 2**32: 483 bytes


def get_argparser_bandwidth_part(parser):
    parser.add_argument('--min_bw', dest='MIN_BW',
      help='To compute KDE MCC a bandwidth need to be estimate from data using bw_nrd. To avoid very small bw you can use this parameter to set a minimum (Default:0.1).',
      type=float,
      default=0.1)