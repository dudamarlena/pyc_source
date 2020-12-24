# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/MFEprimer/chilli/PenultimateTable.py
# Compiled at: 2017-07-16 05:34:29
"""ARMS primer additional mismatch selection table

by Wubin Qu <quwubin@gmail.com>,
Copyright @ 2010, All Rights Reserved.
"""
Author = 'Wubin Qu  <quwubin@gmail.com>, China'
Date = 'Nov-13-2010 23:25:42'
Version = '1.0'
import sys, os
from optparse import OptionParser
pt = {'AA': {'A': 'A', 'G': 'G', 'C': 'A', 'T': 'G'}, 'AG': {'A': 'C', 'G': 'T', 'C': 'A', 'T': 'G'}, 'AC': {'A': 'G', 'G': 'A', 'C': 'C', 'T': 'T'}, 'TT': {'A': 'C', 'G': 'T', 'C': 'A', 'T': 'G'}, 'TG': {'A': 'G', 'G': 'A', 'C': 'T', 'T': 'C'}, 'TC': {'A': 'C', 'G': 'T', 'C': 'A', 'T': 'G'}, 'CC': {'A': 'C', 'G': 'T', 'C': 'A', 'T': 'G'}, 'GG': {'A': 'A', 'G': 'G', 'C': 'A', 'T': 'G'}, 'GA': {'A': 'C', 'G': 'T', 'C': 'A', 'T': 'G'}, 'CA': {'A': 'G', 'G': 'A', 'C': 'C', 'T': 'T'}, 'GT': {'A': 'G', 'G': 'A', 'C': 'T', 'T': 'C'}, 'CT': {'A': 'C', 'G': 'T', 'C': 'A', 'T': 'G'}}

def get_opt():
    """Handle options"""
    usage = 'Usage: %prog [options]'
    version = '%prog Version: ' + '%s [%s]' % (Version, Date)
    parser = OptionParser(usage=usage, version=version)
    parser.add_option('-i', '--infile', dest='infile', help='Input file name. [String]')
    parser.add_option('-o', '--outfile', dest='outfile', help='Output file name. [String]')
    options, args = parser.parse_args()
    if len(args) > 1:
        parser.error('Incorrect argument, add" "-h" for help.')
    if not options.infile:
        pass
    return options


def main():
    """Main"""
    print pt


if __name__ == '__main__':
    main()