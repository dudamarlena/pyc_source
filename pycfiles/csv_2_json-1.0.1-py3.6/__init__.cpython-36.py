# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/__init__.py
# Compiled at: 2018-02-08 21:01:52
# Size of source mod 2**32: 675 bytes
import argparse
from csv2json import Csv2Json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv', help='CSV input file path', type=str)
    parser.add_argument('json', help='JSON otput path', type=str)
    parser.add_argument('--has_header',
      help='Does the CSV file have a header',
      action='store_true')
    parser.add_argument('--pretty_print',
      help='JSON should be pretty formated',
      action='store_true')
    args = parser.parse_args()
    Csv2Json().run(args.csv, args.json, args.has_header, args.pretty_print)