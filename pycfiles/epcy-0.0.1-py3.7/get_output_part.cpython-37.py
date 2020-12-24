# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/epcy/argparser/get_output_part.py
# Compiled at: 2020-03-17 11:26:44
# Size of source mod 2**32: 246 bytes


def get_argparser_output_part(parser):
    parser.add_argument('-o', dest='PATH_OUT',
      help='Path to the directory output.',
      type=str,
      default=None)