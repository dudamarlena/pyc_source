# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pycovjson/cli/viewer.py
# Compiled at: 2016-11-10 06:15:19
# Size of source mod 2**32: 839 bytes
__doc__ = '\nPycovjson - Command line viewer\nAuthor: rileywilliams\nVersion: 0.1.0\nTODO - Add support for other formats and more customisation\n'
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