# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pycovjson/cli/viewer.py
# Compiled at: 2016-11-10 06:15:19
# Size of source mod 2**32: 839 bytes
"""
Pycovjson - Command line viewer
Author: rileywilliams
Version: 0.1.0
TODO - Add support for other formats and more customisation
"""
import argparse
from pycovjson.read_netcdf import NetCDFReader as Reader

def main():
    parser = argparse.ArgumentParser(description='View Scientific Data files.')
    parser.add_argument('inputfile', action='store', help='Name of input file')
    parser.add_argument('-v', '--variables,', dest='variables', help='Display variables', action='store_true')
    args = parser.parse_args()
    inputfile = args.inputfile
    variables = args.variables
    reader = Reader(inputfile)
    ds = reader.get_xarray()
    print(ds)


if __name__ == '__main__':
    main()