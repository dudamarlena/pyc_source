# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/buty_phyl/scripts/treeformat.py
# Compiled at: 2019-04-08 19:00:23
# Size of source mod 2**32: 2733 bytes
import argparse
from Bio import AlignIO
import os
from Bio import SeqIO
parser = argparse.ArgumentParser(formatter_class=(argparse.RawDescriptionHelpFormatter))
parser.add_argument('-s', help='file name of your otu_seq',
  type=str,
  default='a.otu.fasta',
  metavar='a.otu.fasta')
parser.add_argument('-r', help='results_dir',
  type=str,
  default='ButyPhyl',
  metavar='ButyPhyl')
parser.add_argument('-rd', help='the reference data of gene traits',
  type=str,
  default='Data.txt',
  metavar='Data.txt')
parser.add_argument('-a', help='file name of alignment',
  type=str,
  default='None',
  metavar='a.align.16S')
args = parser.parse_args()

def Alignname_format(filename):
    Alignroot, Alignfile = os.path.split(filename)
    f1 = open(os.path.join(Alignroot, Alignfile + '.format'), 'w')
    f2 = open(os.path.join(Alignroot, Alignfile + '.format.name'), 'w')
    for record in SeqIO.parse(open(filename, 'r'), 'fasta'):
        f1.write('>' + str(record.id).replace('_R_', '') + '\n' + str(record.seq) + '\n')
        f2.write(str(record.id).replace('_R_', '') + '\t' + str(record.id).replace('_R_', '') + '\n')

    f1.close()
    f2.close()


if args.a == 'None':
    rootofus, otuseq = os.path.split(args.s)
    f1 = open(os.path.join(args.r, otuseq + '.format'), 'w')
    f2 = open(os.path.join(args.r, otuseq + '.taxa.translate'), 'w')
    os.system('cp ' + args.rd + ' ' + os.path.join(args.r, otuseq + '.data'))
    Refdata = []
    for lines in open(os.path.join(args.r, otuseq + '.data'), 'r'):
        Refdata.append(lines.split('\t')[0])

    f3 = open(os.path.join(args.r, otuseq + '.data'), 'ab')
    f2.write('#NEXUS\nBegin trees;\n\ttranslate')
    i = 1
    for record in SeqIO.parse(open(os.path.join(args.r, args.s), 'r'), 'fasta'):
        f1.write('>' + str(i) + '\n' + str(record.seq) + '\n')
        if i == 1:
            f2.write('\n')
        else:
            f2.write(',\n')
        f2.write('\t\t' + str(i) + '\t' + str(record.id))
        if str(record.id) not in Refdata:
            f3.write(str(record.id) + '\t?\n')
        i += 1

    f2.write(';\n\t\ttree tree.taxa = ')
    f1.close()
    f2.close()
    f3.close()
else:
    Alignname_format(args.a)