# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/complexconstructor/argparser.py
# Compiled at: 2020-04-02 08:26:01
# Size of source mod 2**32: 2328 bytes
import sys, os, argparse, gzip
from os.path import isfile, join

def readArgs():
    """ Read and organize the command line arguments and return the namespace"""
    parser = argparse.ArgumentParser(description='Build a protein complex from a set of pdb files containing the paired structures of its elements.')
    parser.add_argument('-fa', '--fasta', dest='infasta', action='store', default=None, help='FASTA file with the sequences of the proteins\n                               or DNA that will conform the complex.')
    parser.add_argument('-pdb', '--pdbDir', dest='inpdb', action='store', default=None, help='Diretory containing the PDB files with the \n                               structure of the pairs that will conform the complex.')
    parser.add_argument('-o', '--output', dest='outfile', action='store', default=None, help='Directory name where the complex results will be stored. \n                                ')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Show the detailed progression of the building process \n                                in a file called ComplexConstructor.log.')
    parser.add_argument('-st', '--stoichiometry', dest='stoich', action='store', default=None, help="File containing a determined stoichiometry to the complex. \n                               The information of the stoichiometry must be: the ID of the \n                               sequence chain (concordant with the FASTA file ID) followed by \n                               the number of times it has to be present in the complex after ':'\n                               ID_as_FASTA_file : stoichiometry (one per line) in format .txt. ")
    parser.add_argument('-gui', '--graphicInterface', dest='gui', action='store_true', default=False, help="To use ComplexConstructor with the graphical interface just use \n                              '-gui' argument in commandline.")
    return parser.parse_args()