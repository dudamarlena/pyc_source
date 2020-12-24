# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synaw_tools/cli.py
# Compiled at: 2020-03-06 14:03:21
"""
CLI wrapper for SYNAW tools.
"""
import argparse

def main():
    parser = argparse.ArgumentParser(description='Python tooling for SYNAW.')
    subparsers = parser.add_subparsers(title='subcommands', description='available subcommands', help='additional help')
    ciphers_parser = subparsers.add_parser('ciphers')
    parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const', const=sum, default=max, help='sum the integers (default: find the max)')
    args = parser.parse_args()