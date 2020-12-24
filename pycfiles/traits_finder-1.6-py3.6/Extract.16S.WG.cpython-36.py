# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/traits_finder/scripts/Extract.16S.WG.py
# Compiled at: 2020-01-23 22:42:03
# Size of source mod 2**32: 4336 bytes
import argparse
from Bio import SeqIO
import os
parser = argparse.ArgumentParser(formatter_class=(argparse.RawDescriptionHelpFormatter))
parser.add_argument('-i', help='input dir',
  type=str,
  default='.',
  metavar='current dir (.)')
parser.add_argument('-f', help='input filename',
  type=str,
  default='input.faa',
  metavar='input.faa')
parser.add_argument('-n', help='prefix name for usearch result',
  type=str,
  default='.usearch.txt',
  metavar='.usearch.txt')
parser.add_argument('-r', help='output dir',
  type=str,
  default='.',
  metavar='current dir (.)')
args = parser.parse_args()

def checkfile(filename, i):
    try:
        f1 = open(filename, 'r')
        if os.path.getsize(filename) > 0:
            for lines in f1:
                try:
                    lines.split('\t', maxsplit=(i + 1))[i]
                    return 'not empty'
                except IndexError:
                    return 'wrong content by spliting %s \\t' % str(i)

                break

        else:
            return 'empty'
    except IOError:
        return 'non-existed'


def Extract16S(root, searchfile, seqfile, resultdir):
    Seq_16S = dict()
    try:
        input_file = os.path.join(resultdir, searchfile)
        Checkoutput = checkfile(input_file, 7)
        if Checkoutput == 'not empty':
            f1 = open(os.path.join(resultdir, searchfile + '.fasta'), 'w')
            for line in open(input_file, 'r'):
                Seq = str(line).split('\t')[0].split(' ')[0]
                if Seq not in Seq_16S:
                    Seq_16S.setdefault(Seq, [[int(str(line).split('\t')[6]) - 1, int(str(line).split('\t')[7]) - 1]])
                else:
                    for locus in Seq_16S[Seq]:
                        if max(int(str(line).split('\t')[7]) - 1, locus[1]) - min(int(str(line).split('\t')[6]) - 1, locus[0]) <= 2000:
                            locus[0] = min(int(str(line).split('\t')[6]) - 1, locus[0])
                            locus[1] = max(int(str(line).split('\t')[7]) - 1, locus[1])
                        else:
                            Seq_16S[Seq].append([int(str(line).split('\t')[6]) - 1, int(str(line).split('\t')[7]) - 1])

            Genome = []
            Maxlen = 0
            for Seq in Seq_16S:
                for locus in Seq_16S[Seq]:
                    if locus[1] - locus[0] > Maxlen:
                        Genome = [
                         Seq, locus[0], locus[1]]
                        Maxlen = locus[1] - locus[0]

            for record in SeqIO.parse(open(os.path.join(root, seqfile), 'r'), 'fasta'):
                if str(record.id) == Genome[0]:
                    if Genome[2] - Genome[1] >= 1000:
                        if Genome[2] - Genome[1] <= 2000:
                            f1.write('>' + seqfile.split('.')[0] + '\t' + str(record.id) + '\n' + str(str(record.seq)[Genome[1]:Genome[2]]) + '\n')
                            flog.write(seqfile + '\toutput\n')
                        else:
                            flog.write(seqfile + '\ttoo_long\n')
                    else:
                        flog.write(seqfile + '\ttoo_short\n')

            f1.close()
    except IOError:
        flog.write(seqfile + '\tfile_missing\n')


flog = open(os.path.join(args.r, '16S_output.log'), 'a')
Extract16S(args.i, args.f + args.n, args.f, args.r)
flog.close()