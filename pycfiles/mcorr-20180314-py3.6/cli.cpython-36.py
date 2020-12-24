# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mcorr/cli.py
# Compiled at: 2018-03-18 13:38:17
# Size of source mod 2**32: 879 bytes
from argparse import ArgumentParser
from . import fitp2

def main():
    """Run fitting using lmfit"""
    parser = ArgumentParser(description='Infer recombination rates                                         by fitting correlation profile of mutations.')
    parser.add_argument('corr_file', type=str)
    parser.add_argument('output_prefix', type=str)
    parser.add_argument('--xmin', nargs='?', const=3, type=int, default=3)
    parser.add_argument('--xmax', nargs='?', const=300, type=int, default=300)
    parser.add_argument('--fit_bootstraps', nargs='?', const='true', type=bool, default=True)
    opts = parser.parse_args()
    datafile = opts.corr_file
    prefix = opts.output_prefix
    xmin = opts.xmin
    xmax = opts.xmax
    fit_bootstraps = opts.fit_bootstraps
    fitp2(datafile, prefix, xmin, xmax, fit_bootstraps)


if __name__ == '__main__':
    main()