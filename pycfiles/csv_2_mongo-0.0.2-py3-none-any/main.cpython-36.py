# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/src/main.py
# Compiled at: 2018-02-08 21:26:38
# Size of source mod 2**32: 675 bytes
import argparse
from .csv2json import Csv2Json

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