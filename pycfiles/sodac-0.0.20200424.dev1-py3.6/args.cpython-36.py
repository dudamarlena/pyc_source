# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soda/optimization/args.py
# Compiled at: 2020-04-24 19:37:56
# Size of source mod 2**32: 915 bytes
import argparse
from typing import Dict

def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('--inline', type=str,
      metavar='(yes|no)',
      dest='inline',
      nargs='?',
      const='yes',
      default='no')
    parser.add_argument('--temporal-cse',
      type=str,
      metavar='(yes|no|greedy|optimal|glore|built-in|built-in:greedy|built-in:optimal)',
      dest='temporal_cse',
      nargs='?',
      const='yes',
      default='no',
      help='enable temporal common subexpression elimination or not')


def get_kwargs(args: argparse.Namespace) -> Dict[(str, str)]:
    optimizations = {}
    if args.temporal_cse != 'no':
        optimizations['tcse'] = args.temporal_cse
    if args.inline != 'no':
        optimizations['inline'] = args.inline
    return optimizations