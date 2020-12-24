# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/flint/src/flinter/linter.py
# Compiled at: 2020-05-07 09:30:40
# Size of source mod 2**32: 1266 bytes
"""Fortran linter"""
import os, argparse
from flinter.formatting import parse_format_line, init_format_rules
__all__ = [
 'fmt_analysis']

def fmt_analysis(filename):
    """Start the linter of file FILENAME."""
    file_stats = dict()
    all_errors = dict()
    file_stats['modifs'] = 0
    file_stats['errors'] = 0
    with open(filename, 'r') as (fin):
        lines = fin.readlines()
    file_stats['total_lines'] = len(lines)
    format_rules = init_format_rules()
    for i, line in enumerate(lines, 1):
        line_stats, line_errors = parse_format_line(filename, line, i, format_rules)
        file_stats['errors'] += line_stats['errors']
        file_stats['modifs'] += line_stats['modifs']
        for key in line_errors:
            if key in all_errors:
                all_errors[key] += line_errors[key]
            else:
                all_errors[key] = line_errors[key]

    rate = float(file_stats['errors']) / file_stats['total_lines'] * 10
    rate = 10.0 - rate
    print(50 * '-')
    print('Your code has been rated %2.2f/10' % rate)
    for key in all_errors:
        print(format_rules[key]['message'], len(all_errors[key]))

    return rate