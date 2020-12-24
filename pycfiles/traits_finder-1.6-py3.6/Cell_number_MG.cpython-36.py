# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/traits_finder/scripts/Cell_number_MG.py
# Compiled at: 2020-01-08 00:55:15
# Size of source mod 2**32: 4537 bytes
import os
from Bio import SeqIO
import argparse, glob
parser = argparse.ArgumentParser(formatter_class=(argparse.RawDescriptionHelpFormatter))
parser.add_argument('-m', help='file name of your cell number mapping file',
  type=str,
  default='all_KO30_name.list',
  metavar='all_KO30_name.list')
parser.add_argument('-fa', help='input format of metagenomes sequence',
  type=str,
  default='.fasta',
  metavar='.fasta or .fastq')
parser.add_argument('-r16', help='output directory or folder of your 16S sequences',
  type=str,
  default='Result_16S',
  metavar='Result_16S')
parser.add_argument('-r', help='output directory or folder of your results',
  type=str,
  default='Result_traits',
  metavar='Result_traits')
args = parser.parse_args()
try:
    os.mkdir(os.path.join(args.r, 'summary'))
except OSError:
    pass

def cell_calculate(inputfile, mapping_list):
    output = dict()
    for lines in open(inputfile):
        gene = lines.split('\t')[1]
        maplength = float(lines.split('\t')[3])
        if gene not in mapping_list:
            print(gene, ' not in mapping list!')
        else:
            geneID = mapping_list[gene][0]
            genelength = mapping_list[gene][1]
            if geneID not in output:
                output.setdefault(geneID, maplength / genelength)
            else:
                output[geneID] += maplength / genelength

    average_output = 0
    for geneID in output:
        average_output += output[geneID]

    return average_output / float(len(output))


def check_16S(inputfile):
    try:
        coverage = 0
        for lines in open(os.path.join(args.r16, inputfile.replace('.uscmg.blastx.txt', '.16S.txt'))):
            coverage += float(lines.split('\t')[3]) / 1500.0

        return coverage
    except IOError:
        return 0


Cell_out = 0
try:
    ftry = open(os.path.join(os.path.join(args.r, 'summary'), 'cell.copynum.all.txt'), 'r')
    Cell_out = 1
except IOError:
    pass

Cell16S_out = 0
try:
    ftry = open(os.path.join(os.path.join(args.r, 'summary'), '16S.copynum.all.txt'), 'r')
    Cell16S_out = 1
except IOError:
    pass

if Cell_out == 0 or Cell16S_out == 0:
    inputfiles = glob.glob(os.path.join(args.r16, '*.uscmg.blastx.txt'))
    Mapping = dict()
    for lines in open(args.m, 'r'):
        Mapping.setdefault(lines.split('\t')[0], [
         lines.split('\t')[1], float(lines.split('\t')[2].split('\r')[0].split('\n')[0])])

    Cellnum = dict()
    Cell16S = dict()
    for filenames in inputfiles:
        filename = os.path.split(filenames)[(-1)].split(args.fa)[0].split('.uscmg.blastx.txt')[0].split('_1')[0].split('_2')[0]
        if Cell_out == 0:
            if filename not in Cellnum:
                Cellnum.setdefault(filename, [])
            Cellnum[filename].append(cell_calculate(filenames, Mapping))
        if Cell16S_out == 0 and filename not in Cell16S:
            Cell16S.setdefault(filename, [])
            Cell16S[filename].append(check_16S(filenames))

    if Cell_out == 0:
        f1 = open(os.path.join(os.path.join(args.r, 'summary'), 'cell.copynum.all.txt'), 'w')
        for filename in Cellnum:
            f1.write(filename)
            for number in Cellnum[filename]:
                f1.write('\t' + str(number))

            f1.write('\n')

        f1.close()
    if Cell16S_out == 0:
        f1 = open(os.path.join(os.path.join(args.r, 'summary'), '16S.copynum.all.txt'), 'w')
        for filename in Cell16S:
            f1.write(filename)
            for number in Cell16S[filename]:
                f1.write('\t' + str(number))

            f1.write('\n')

        f1.close()