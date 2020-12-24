# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/mhclovac/argument_parser.py
# Compiled at: 2019-12-11 06:05:45
# Size of source mod 2**32: 999 bytes
import argparse
mhclovac_description = '\nmhclovac - MHC binding prediction based on modeled physicochemical \nproperties of peptides. Version: 1.0.1. Author: Stefan Stojanovic\n'

def parse_args(argv):
    parser = argparse.ArgumentParser(description=mhclovac_description)
    parser.add_argument('--sequence', type=str, help='Input sequence')
    parser.add_argument('--sequence_name', type=str, help='Sequence name')
    parser.add_argument('--fasta', type=str, help='FASTA file')
    parser.add_argument('--hla', type=str, help='HLA type', required=True)
    parser.add_argument('--peptide_length', type=int, help='Peptide length', required=True)
    parser.add_argument('--output', type=str, help='Output file. If not provided output will be written to stdout')
    parser.add_argument('--print_header', action='store_true', help='Print column names')
    return parser.parse_args(argv)