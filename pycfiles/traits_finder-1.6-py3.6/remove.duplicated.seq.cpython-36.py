# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/traits_finder/scripts/remove.duplicated.seq.py
# Compiled at: 2019-12-18 02:34:18
# Size of source mod 2**32: 1157 bytes
from Bio import SeqIO
import argparse, os
parser = argparse.ArgumentParser(formatter_class=(argparse.RawDescriptionHelpFormatter))
parser.add_argument('-i', help='input sequence name',
  type=str,
  default='input.fasta',
  metavar='input.fasta')
args = parser.parse_args()
input_fasta = args.i
if 'dereplicated' not in input_fasta:
    f1 = open(input_fasta + '.dereplicated.id.fasta', 'w')
    input_id = []
    for record in SeqIO.parse(open(input_fasta, 'r'), 'fasta'):
        if str(record.id) not in input_id:
            input_id.append(str(record.id))
            f1.write('>%s\n%s\n' % (str(record.id), str(record.seq)))

    f1.close()