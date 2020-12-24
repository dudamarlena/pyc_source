# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soda/optimization/args.py
# Compiled at: 2020-04-29 14:13:41
# Size of source mod 2**32: 924 bytes
import argparse
from typing import Dict

def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('--inline', type=str,
      metavar='(yes|no)',
      dest='inline',
      nargs='?',
      const='yes',
      default='no')
    parser.add_argument('--computation-reuse',
      type=str,
      metavar='(yes|no|greedy|optimal|glore|built-in|built-in:greedy|built-in:optimal)',
      dest='computation_reuse',
      nargs='?',
      const='yes',
      default='no',
      help='enable computation reuse or not')


def get_kwargs(args: argparse.Namespace) -> Dict[(str, str)]:
    optimizations = {}
    if args.computation_reuse != 'no':
        optimizations['computation-reuse'] = args.computation_reuse
    if args.inline != 'no':
        optimizations['inline'] = args.inline
    return optimizations