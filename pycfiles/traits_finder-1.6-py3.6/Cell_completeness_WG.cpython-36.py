# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/traits_finder/scripts/Cell_completeness_WG.py
# Compiled at: 2019-05-18 23:59:15
# Size of source mod 2**32: 3169 bytes
import os
from Bio import SeqIO
import argparse, glob
parser = argparse.ArgumentParser(formatter_class=(argparse.RawDescriptionHelpFormatter))
parser.add_argument('-m', help='file name of your cell number mapping file',
  type=str,
  default='/scratch/users/anniz44/scripts/argoap/DB/all_KO30_name.list',
  metavar='all_KO30_name.list')
parser.add_argument('-i', help='input dir of cell number search result',
  type=str,
  default='/scratch/users/anniz44/Metagenomes/cellnumber',
  metavar='.')
parser.add_argument('-f', help='input format of search result',
  type=str,
  default='.uscmg.blastx.txt',
  metavar='.uscmg.blastx.txt')
parser.add_argument('--r', help='output directory or folder of your results',
  type=str,
  default='/scratch/users/anniz44/Metagenomes/summary',
  metavar='Result')
args = parser.parse_args()
try:
    os.mkdir(args.r)
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

    geneID_count = 0
    for geneID in output:
        geneID_count += 1

    return geneID_count / 40.0


inputfiles = glob.glob(os.path.join(args.i, '*' + args.f))
Mapping = dict()
for lines in open(args.m, 'r'):
    Mapping.setdefault(lines.split('\t')[0], [
     lines.split('\t')[1], float(lines.split('\t')[2].split('\r')[0].split('\n')[0])])

Cellnum = dict()
for filenames in inputfiles:
    filename = os.path.split(filenames)[(-1)].split(args.f)[0].split('_1')[0].split('_2')[0]
    if filename not in Cellnum:
        Cellnum.setdefault(filename, [])
    Cellnum[filename].append(cell_calculate(filenames, Mapping))

f1 = open(os.path.join(args.r, 'cell.num.all.txt'), 'w')
for filename in Cellnum:
    f1.write(filename)
    for number in Cellnum[filename]:
        f1.write('\t' + str(number))

    f1.write('\n')

f1.close()