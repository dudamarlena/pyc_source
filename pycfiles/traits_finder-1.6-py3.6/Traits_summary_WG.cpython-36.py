# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/traits_finder/scripts/Traits_summary_WG.py
# Compiled at: 2020-01-24 13:03:32
# Size of source mod 2**32: 13712 bytes
import os
from Bio import SeqIO
import argparse, glob
parser = argparse.ArgumentParser(formatter_class=(argparse.RawDescriptionHelpFormatter))
parser.add_argument('-t', help='trait name',
  type=str,
  default='ARG',
  metavar='trait name')
parser.add_argument('-db', help='file name of your input database',
  type=str,
  default='Butyrate.pro.aa',
  metavar='database.aa')
parser.add_argument('-i', help='input dir of genomes',
  type=str,
  default='.',
  metavar='.')
parser.add_argument('-m', help='mapping file of traits to function',
  type=str,
  default='Butyrate.pro.mapping.txt',
  metavar='Butyrate.pro.mapping.txt')
parser.add_argument('-dbf', help="sequence format of your input database                        (1: nucleotide; 2: protein),                         (default '1' for nucleotide)",
  metavar='1 or 2',
  choices=[
 1, 2],
  action='store',
  default=1,
  type=int)
parser.add_argument('--mge', help="whether your input sequences are genomes or mobile genetic elements (MGEs)                        (1: genomes; 2: mge),                         (default '1' for genomes)",
  metavar='1 or 2',
  choices=[
 1, 2],
  action='store',
  default=1,
  type=int)
parser.add_argument('--fa', help='input format of genome sequence',
  type=str,
  default='.fna.add',
  metavar='.fasta, .fna or .fa')
parser.add_argument('--orf', help='input format of genome orfs',
  type=str,
  default='.genes.faa',
  metavar='.faa')
parser.add_argument('--r', help='input directory or folder of your previous results by Traits_WGD.py',
  type=str,
  default='Result',
  metavar='Result')
parser.add_argument('--r16', help='input directory or folder of your previous 16S sequences extracted by Traits_WGD.py',
  type=str,
  default='Result',
  metavar='Result')
parser.add_argument('--s', help='output directory or folder of your results of traits summary',
  type=str,
  default='summary',
  metavar='summary')
parser.add_argument('-c', help='cutoff for traits',
  type=float,
  default=60.0,
  metavar='60.0')
args = parser.parse_args()
fasta_format = args.fa
orfs_format = args.orf
if '.add' not in orfs_format:
    orfs_format = orfs_format + '.add'
else:
    try:
        os.mkdir(args.s)
    except OSError:
        pass

    try:
        os.mkdir(os.path.join(args.s, 'sub_sequences/'))
    except OSError:
        pass

    def check_file(listoffiles):
        for files in listoffiles:
            try:
                f1 = open(files, 'r')
                return files
            except FileNotFoundError:
                pass


    def check_16S(inputfile):
        try:
            file16S = check_file(glob.glob(os.path.join(args.r16 + '/*', inputfile.replace(orfs_format, fasta_format) + '.16S.txt.fasta')))
            Has16S = 0
            if file16S != None:
                for lines in open(file16S, 'r'):
                    if str(lines) != '':
                        Has16S = 1
                    break

            if Has16S == 1:
                for record in SeqIO.parse(file16S, 'fasta'):
                    f16s.write('>' + str(record.id).split('_final')[0] + '\n' + str(record.seq) + '\n')

        except FileNotFoundError:
            pass


    def check_traits(inputfile, outputfile_aa, outputfile_aa_500, outputfile_blast, outputfile_summary, outputfile_summary_fun, file_subfix, i):
        blastout = check_file(glob.glob(args.r + '/search_output/*/' + inputfile + '.blast.txt.filter'))
        Hastraits = 0
        short_filename = inputfile.split(file_subfix)[0]
        if blastout != None:
            for lines in open(blastout, 'r'):
                if str(lines) != '':
                    Hastraits = 1
                break

        else:
            if Hastraits == 1:
                Functionset = dict()
                totaltraits = []
                temp = []
                while i > 0:
                    totaltraits.append(0)
                    i = i - 1

                for functions in allfunction:
                    allfunction[functions] = 0

                for lines in open(blastout, 'r'):
                    if short_filename not in lines:
                        lines = short_filename + '_' + lines
                    if args.mge == 2:
                        lines = 'mge_' + lines
                    lines_set = str(lines).split('\t')
                    traits_gene = lines_set[1]
                    if Function != dict():
                        loci1 = min(int(lines_set[6]), int(lines_set[7].split('\r')[0].split('\n')[0]))
                        loci2 = max(int(lines_set[6]), int(lines_set[7].split('\r')[0].split('\n')[0]))
                        if outputfile_aa_500 == 'None':
                            Functionset.setdefault(lines_set[0], Function.get(traits_gene, 'None'))
                            outputfile_blast.write('%s\t%s' % (Function.get(traits_gene, 'None'), lines))
                        else:
                            Functionset.setdefault('%s_%s_%s' % (lines_set[0],
                             str(loci1 - 1), str(loci2)), Function.get(traits_gene, 'None'))
                            outputfile_blast.write('%s\t%s_%s_%s\t%s' % (Function.get(traits_gene, 'None'), lines_set[0],
                             str(loci1 - 1), str(loci2),
                             '\t'.join(lines_set[1:])))
                    else:
                        if outputfile_aa_500 == 'None':
                            outputfile_blast.write(lines)
                        else:
                            outputfile_blast.write('%s_%s_%s\t%s' % (lines_set[0],
                             str(loci1 - 1), str(loci2),
                             '\t'.join(lines_set[1:])))
                        if float(lines.split('\t')[2]) >= args.c:
                            try:
                                totaltraits[Functionlist[traits_gene]] += 1
                                allfunction[Function.get(traits_gene, 'None')] += 1
                            except KeyError:
                                pass

                for copy_number in totaltraits:
                    temp.append(str(copy_number))

                outputfile_summary.write(short_filename + '\t' + '\t'.join(temp) + '\n')
                outputfile_summary_fun.write(short_filename)
                for functions in allfunction:
                    outputfile_summary_fun.write('\t' + str(allfunction[functions]))

                outputfile_summary_fun.write('\n')
                aaout = blastout + '.aa'
                aaout500 = blastout + '.extra*.aa'
                for record in SeqIO.parse(aaout, 'fasta'):
                    if short_filename not in str(record.id):
                        record.id = short_filename + '_' + str(record.id)
                    else:
                        if args.mge == 2:
                            record.id = 'mge_' + record.id
                        if str(record.id) in Functionset:
                            outputfile_aa_file = open(outputfile_aa.replace('fasta', Functionset[str(record.id)] + '.fasta'), 'a')
                            outputfile_aa_file.write('>%s\n%s\n' % (
                             str(record.id),
                             str(record.seq)))
                            outputfile_aa_file.close()
                        else:
                            print('%s not found in blast output' % str(record.id))

                if outputfile_aa_500 != 'None':
                    for record in SeqIO.parse(glob.glob(aaout500)[0], 'fasta'):
                        if short_filename not in str(record.id):
                            record.id = short_filename + '_' + str(record.id)
                        if args.mge == 2:
                            record.id = 'mge_' + record.id
                        outputfile_aa_500.write('>' + str(record.id) + '\n' + str(record.seq) + '\n')

            else:
                outputfile_summary.write(short_filename + '\tNo_hit\n')
                outputfile_summary_fun.write(short_filename + '\tNo_hit\n')


    in_dir = args.i
    Targetroot = dict()
    for root, dirs, files in os.walk(in_dir):
        list_fasta1 = glob.glob(os.path.join(root, '*' + orfs_format))
        if list_fasta1 != []:
            for files in list_fasta1:
                Targetroot.setdefault(files, orfs_format)

    f16s = open(os.path.join(args.s, args.t + '.all.16S.fasta'), 'w')
    ftraits = open(os.path.join(args.s, args.t + '.all.traits.aa.txt'), 'w')
    ftraits_dna = open(os.path.join(args.s, args.t + '.all.traits.dna.txt'), 'w')
    fsum_aa = open(os.path.join(args.s, args.t + '.all.traits.aa.summarize.gene.' + str(args.c) + '.txt'), 'w')
    fsum_aa_fun = open(os.path.join(args.s, args.t + '.all.traits.aa.summarize.function.' + str(args.c) + '.txt'), 'w')
    fsum_dna = open(os.path.join(args.s, args.t + '.all.traits.dna.summarize.gene.' + str(args.c) + '.txt'), 'w')
    fsum_dna_fun = open(os.path.join(args.s, args.t + '.all.traits.dna.summarize.function.' + str(args.c) + '.txt'), 'w')
    faa = os.path.join(args.s, 'sub_sequences/' + args.t + '.all.traits.aa.fasta')
    fdna = os.path.join(args.s, 'sub_sequences/' + args.t + '.all.traits.dna.fasta')
    fdna_500 = open(os.path.join(args.s, args.t + '.all.traits.dna.extra500.fasta'), 'w')
    outputfile_aa_file = open(faa, 'w')
    outputfile_aa_file.close()
    outputfile_aa_file = open(fdna, 'w')
    outputfile_aa_file.close()
    Function = dict()
    Functionlist = dict()
    genenum = 0
    allfunction = dict()
    for lines in open(args.m, 'r'):
        lines_set = str(lines).split('\t')
        gene = lines_set[0]
        gene_fun = lines_set[1].split('\r')[0].split('\n')[0]
        Function.setdefault(gene, gene_fun)
        if gene_fun not in allfunction:
            allfunction.setdefault(gene_fun, 0)
        outputfile_aa_file = open(faa.replace('fasta', gene_fun + '.fasta'), 'w')
        outputfile_aa_file.close()
        outputfile_aa_file = open(fdna.replace('fasta', gene_fun + '.fasta'), 'w')
        outputfile_aa_file.close()
        if gene not in Functionlist:
            Functionlist.setdefault(gene, genenum)
            genenum += 1

    if args.dbf == 2:
        for record in SeqIO.parse(args.db, 'fasta'):
            if str(record.id) in Function:
                outputfile_aa_file = open(faa.replace('fasta', Function[str(record.id)] + '.fasta'), 'a')
                outputfile_aa_file.write('>reference_' + str(record.id) + '\n' + str(record.seq) + '\n')
                outputfile_aa_file.close()

    else:
        for record in SeqIO.parse(args.db, 'fasta'):
            if str(record.id) in Function:
                outputfile_aa_file = open(fdna.replace('fasta', Function[str(record.id)] + '.fasta'), 'a')
                outputfile_aa_file.write('>reference_' + str(record.id) + '\n' + str(record.seq) + '\n')
                outputfile_aa_file.close()

fsum_aa.write('SampleID')
for functions in Functionlist:
    fsum_aa.write('\t' + str(functions))

fsum_aa.write('\n')
fsum_aa_fun.write('SampleID')
for functions in allfunction:
    fsum_aa_fun.write('\t' + str(functions))

fsum_aa_fun.write('\n')
fsum_dna.write('SampleID')
for functions in Functionlist:
    fsum_dna.write('\t' + str(functions))

fsum_dna.write('\n')
fsum_dna_fun.write('SampleID')
for functions in allfunction:
    fsum_dna_fun.write('\t' + str(functions))

fsum_dna_fun.write('\n')
for filenames in Targetroot:
    filedir, filename = os.path.split(filenames)
    check_16S(filename)
    check_traits(filename, faa, 'None', ftraits, fsum_aa, fsum_aa_fun, orfs_format, genenum)
    check_traits(filename.replace(orfs_format, fasta_format), fdna, fdna_500, ftraits_dna, fsum_dna, fsum_dna_fun, fasta_format, genenum)

os.system('cat %s > %s' % (faa.replace('fasta', '*.fasta'),
 os.path.join(args.s, os.path.split(faa)[(-1)])))
os.system('cat %s > %s' % (fdna.replace('fasta', '*.fasta'),
 os.path.join(args.s, os.path.split(fdna)[(-1)])))
f16s.close()
ftraits.close()
fdna_500.close()
ftraits_dna.close()
fsum_aa.close()
fsum_dna.close()
fsum_aa_fun.close()
fsum_dna_fun.close()