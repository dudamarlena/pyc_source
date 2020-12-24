# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/MFEprimer/chilli/FastaRemoveRedundant.py
# Compiled at: 2017-07-16 05:34:29
from __future__ import division
Author = 'Wubin Qu  <quwubin@gmail.com>'
Date = 'Sep-02-2011 19:15:07'
import sys, os, argparse
from itertools import groupby

def get_opt():
    """Get options"""
    global args
    parser = argparse.ArgumentParser(description='Remove the same sequences in the FASTA files')
    parser.add_argument('-i', '--infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='Input file to be processed', required=True)
    parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='Output file name for storing the results')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()


def fasta_remove_redundant(infile, outfile):
    """ Remove the same sequences in the FASTA files"""
    ishead = lambda x: x.startswith('>')
    all_seqs = set()
    head = None
    for h, lines in groupby(infile, ishead):
        if h:
            pre_head = lines.next()
            head = pre_head.split()[0].strip()[1:]
            try:
                acc = head.split('|')[3]
            except:
                acc = head

        else:
            seq = ('').join(lines)
            if acc not in all_seqs:
                all_seqs.add(acc)
                outfile.write('%s%s' % (pre_head, seq))

    return


def main():
    """Main"""
    get_opt()
    fasta_remove_redundant(args.infile, args.outfile)


if __name__ == '__main__':
    main()