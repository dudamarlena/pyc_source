# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/epcy/argparser/get_bootstrap_part.py
# Compiled at: 2020-03-19 17:49:11
# Size of source mod 2**32: 405 bytes


def get_argparser_bootstrap_part(parser):
    parser.add_argument('--bs', dest='BS',
      help='Number of bootstrap (BS) used for each sample (Default: No BS). Use -1 to let EPCY find the number of BS in kallisto output.',
      type=int,
      default=0)