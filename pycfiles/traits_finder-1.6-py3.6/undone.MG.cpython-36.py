# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/traits_finder/scripts/undone.MG.py
# Compiled at: 2018-12-03 13:55:18
# Size of source mod 2**32: 1542 bytes
import argparse, os
from Bio import SeqIO
parser = argparse.ArgumentParser(formatter_class=(argparse.RawDescriptionHelpFormatter))
parser.add_argument('-i', help='file name of your genome',
  type=str,
  default='.fa',
  metavar='.fa')
args = parser.parse_args()

def check_genome(filename):
    for record in SeqIO.parse(open(filename, 'r'), 'fasta'):
        if 'GCA_' in record.id:
            try:
                str(record.id).split('_')[2]
                return 0
            except IndexError:
                return 1

        else:
            return 0


def formate_genome(filename, Necessary):
    if Necessary == 1:
        os.system('mv ' + filename + ' ' + filename + '.unformat')
        f1 = open(filename, 'w')
        for record in SeqIO.parse(open(filename + '.unformat', 'r'), 'fasta'):
            newid = str(record.id) + '_' + str(record.description).split(' ')[0]
            f1.write('>' + str(newid) + '\n' + str(record.seq) + '\n')

        f1.close()


formate_genome(args.i, check_genome(args.i))