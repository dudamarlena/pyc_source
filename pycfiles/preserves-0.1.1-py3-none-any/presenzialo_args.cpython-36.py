# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/presenzialo/presenzialo_args.py
# Compiled at: 2020-01-24 06:11:30
# Size of source mod 2**32: 553 bytes
import argparse
from .presenzialo_config import version

def add_parser_debug(parser):
    parser.add_argument('--version',
      action='version',
      version=('%(prog)s ' + version),
      help='print version information')
    parser.add_argument('-v',
      '--verbose', action='count', default=0, help='increase verbosity')
    parser.add_argument('--debug',
      '--dry-run', dest='dry_run', action='store_true', help='dry-run mode')
    parser.add_argument('--raw', action='store_true', help='raw data')