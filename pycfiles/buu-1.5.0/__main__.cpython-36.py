# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/buty_phyl/__main__.py
# Compiled at: 2020-01-24 19:09:57
# Size of source mod 2**32: 10761 bytes
import os
from Bio import SeqIO
import argparse, glob, buty_phyl, sys
print('------------------------------------------------------------------------\nbuty_phyl infers traits by 16S\ninput: otu table (-t) and otu sequences (-s)\nrequirement: mafft and fasttree\n\nCopyright:An Ni Zhang, Prof. Eric Alm, MIT\n\nCitation:\nContact anniz44@mit.edu\n------------------------------------------------------------------------\n')

def main():
    usage = 'usage: buty_phyl -t your.otu.table -s your.otu.seqs'
    version_string = 'buty_phyl {v}, on Python {pyv[0]}.{pyv[1]}.{pyv[2]}'.format(v=(buty_phyl.__version__),
      pyv=(sys.version_info))
    parser = argparse.ArgumentParser(formatter_class=(argparse.RawDescriptionHelpFormatter))
    parser.add_argument('-t', help='file name of your otu_table',
      type=str,
      default='example/example.otu_table',
      metavar='your.otu.table')
    parser.add_argument('-s', help='file name of your otu_seq',
      type=str,
      default='your.otu.fasta',
      metavar='your.otu.fasta')
    parser.add_argument('-r', help='results_dir',
      type=str,
      default='ButyPhyl',
      metavar='ButyPhyl')
    parser.add_argument('-top', help='number of top OTUs',
      type=int,
      default=1000,
      metavar=1000)
    parser.add_argument('--m', help='the path of mafft',
      type=str,
      default='/usr/local/bin/mafft',
      metavar='mafft')
    parser.add_argument('--ft', help='the path of fasttree',
      type=str,
      default='/usr/local/bin/FastTree',
      metavar='your FastTree')
    parser.add_argument('--rs', help='the reference 16S or your own reference 16s sequences',
      type=str,
      default='genome',
      metavar='genome (for full 16S), meta or metagenome (for V4-V5 16S)')
    parser.add_argument('--rt', help='the reference data of gene traits',
      type=str,
      default='b',
      metavar='b (for butyrate), or n (for nitrate), or s (for sulfate), AHR_1 (for AHR pathway 1), AHR_2 (for AHR pks path), AHR_all (for 2 AHR pathways)')
    parser.add_argument('--th', help='number of threads',
      type=int,
      default=1,
      metavar=1)
    parser.add_argument('--test', help='test the buty_phyl',
      action='store_true')
    parser.add_argument('--p', help='further seperate the pathogens and commensals',
      type=str,
      default='TRUE',
      metavar='FALSE or TRUE or your own reference pathogen list')
    parser.add_argument('--sp', help='further infer the species',
      type=str,
      default='FALSE',
      metavar='FALSE or TRUE or your own reference species list')
    args = parser.parse_args()
    workingdir = os.path.abspath(os.path.dirname(__file__))
    ref_pathogen = 'FALSE'
    ref_sp = 'FALSE'
    if args.rs == 'genome':
        ref_tree = os.path.join(workingdir, 'data/GMC_CG_16S.fasta')
        if args.rt == 'b':
            ref_traits = os.path.join(workingdir, 'data/GMC_CG_buk_ptbORbut.txt')
        else:
            if args.rt == 'n':
                ref_traits = os.path.join(workingdir, 'data/GMC_CG_napORnar_nir.txt')
            else:
                if args.rt == 's':
                    ref_traits = os.path.join(workingdir, 'data/GMC_CG_sat_apr_dsr.txt')
                else:
                    if args.rt == 'AHR_1':
                        ref_traits = os.path.join(workingdir, 'data/GMC_CG_AHR_gene_3ofpath.txt')
                    else:
                        if args.rt == 'AHR_2':
                            ref_traits = os.path.join(workingdir, 'data/GMC_CG_AHR_gene_3ofpks.txt')
                        else:
                            if args.rt == 'AHR_all':
                                ref_traits = os.path.join(workingdir, 'data/GMC_CG_AHR_2path.txt')
                            else:
                                ref_traits = args.rt
            if args.sp == 'TRUE':
                ref_sp = os.path.join(workingdir, 'data/GMC_CG_species.txt')
            else:
                ref_sp = args.sp
        if args.p == 'TRUE':
            ref_pathogen = os.path.join(workingdir, 'data/GMC_CG_pathogen.txt')
            ef_sp = os.path.join(workingdir, 'data/GMC_CG_species.txt')
        else:
            ref_pathogen = args.p
    else:
        if args.rs == 'meta' or args.rs == 'metagenome':
            ref_tree = os.path.join(workingdir, 'data/GMC_CG_16S.fasta.all.V4_V5.fasta')
            if args.rt == 'b':
                ref_traits = os.path.join(workingdir, 'data/GMC_CG_buk_ptbORbut.V4_V5.txt')
            else:
                ref_traits = args.rt
            if args.sp == 'TRUE':
                ref_sp = os.path.join(workingdir, 'data/GMC_CG_species.V4_V5.txt')
            else:
                ref_sp = args.sp
            if args.p == 'TRUE':
                ref_pathogen = os.path.join(workingdir, 'data/GMC_CG_pathogen.V4_V5.txt')
                ref_sp = os.path.join(workingdir, 'data/GMC_CG_species.V4_V5.txt')
            else:
                ref_pathogen = args.p
        else:
            ref_tree = args.rs
            ref_traits = args.rt
            ref_sp = args.sp
            ref_pathogen = args.p
            ref_sp = args.sp
        if args.test:
            input_table = os.path.join(workingdir, 'example/example.otu_table')
            input_seq = os.path.join(workingdir, 'example/example.otu_seqs')
        else:
            if args.t == 'example/example.otu_table':
                print('testing buty_phyl')
                input_table = os.path.join(workingdir, 'example/example.otu_table')
                input_seq = os.path.join(workingdir, 'example/example.otu_seqs')
            else:
                input_table = args.t
                input_seq = args.s
            result_dir = args.r
            try:
                os.mkdir(result_dir)
            except OSError:
                pass

            try:
                os.mkdir(result_dir + '/Bayers_model')
            except OSError:
                pass

            rootofus, otuseq = os.path.split(input_seq)
            rootofutb, otutable = os.path.split(input_table)
            f1 = open(os.path.join(result_dir, otutable + 'BayersTraits.log'), 'w')
            print('filter the OTU sequences of top ' + str(args.top) + ' max abudance')
            try:
                ftry = open(str(result_dir) + '/Filtered_OTU/' + str(otuseq) + '.filter', 'r')
            except IOError:
                cmd = 'python ' + workingdir + '/scripts/OTU.filter.py -t ' + str(input_table) + ' -s ' + str(input_seq) + ' -top ' + str(args.top) + ' -r ' + str(result_dir) + '/Filtered_OTU \n'
                os.system(cmd)
                f1.write(cmd)

            print('align the otus sequences with reference 16S sequences\nit takes quite a while...')
            try:
                ftry = open(str(result_dir) + '/Filtered_OTU/' + str(otuseq) + '.filter.align.16S', 'r')
            except IOError:
                cmd = 'cat ' + str(result_dir) + '/Filtered_OTU/' + str(otuseq) + '.filter ' + str(ref_tree) + ' > ' + str(result_dir) + '/Filtered_OTU/' + str(otuseq) + '.filter.16S \n'
                os.system(cmd)
                f1.write(cmd)
                cmd = args.m + ' --nuc --adjustdirection --quiet --maxiterate 0 --retree 2 --nofft --thread ' + str(args.th) + ' ' + str(result_dir) + '/Filtered_OTU/' + str(otuseq) + '.filter.16S > ' + str(result_dir) + '/Filtered_OTU/' + str(otuseq) + '.filter.align.16S \n'
                os.system(cmd)
                f1.write(cmd)

            print('alignment finished!\nnow we are building the tree\nit also takes quite a while...')
            try:
                ftry = open(str(result_dir) + '/Filtered_OTU/' + str(otuseq) + '.filter.align.16S.nwk', 'r')
            except IOError:
                cmd = 'python ' + workingdir + '/scripts/treeformat.py -a ' + str(result_dir) + '/Filtered_OTU/' + str(otuseq) + '.filter.align.16S \n'
                os.system(cmd)
                f1.write(cmd)
                cmd = args.ft + ' -quiet -fastest -nt -nosupport ' + str(result_dir) + '/Filtered_OTU/' + str(otuseq) + '.filter.align.16S.format > ' + str(result_dir) + '/Filtered_OTU/' + str(otuseq) + '.filter.align.16S.nwk \n'
                os.system(cmd)
                f1.write(cmd)

            print('infer the traits based on 16s\nwe are almost there!')
            try:
                ftry = open(str(result_dir) + '/Bayers_model/' + str(otuseq) + '.filter.align.16S.nwk.infertraits.txt', 'r')
            except IOError:
                if ref_sp == 'FALSE':
                    cmd = 'python ' + workingdir + '/scripts/Bayers.model.py -t ' + str(result_dir) + '/Filtered_OTU/' + str(otuseq) + '.filter.align.16S.nwk -n ' + str(result_dir) + '/Filtered_OTU/' + str(otuseq) + '.filter.align.16S.format.name -rd ' + str(ref_traits) + ' -a ' + str(result_dir) + '/Filtered_OTU/' + str(otutable) + '.abu.table -r ' + str(result_dir) + '/Bayers_model -b ' + str(workingdir + '/scripts/inferTraits.py') + ' --p ' + str(ref_pathogen) + ' \n'
                else:
                    cmd = 'python ' + workingdir + '/scripts/Bayers.model.species.py -t ' + str(args.r) + '/Filtered_OTU/' + str(otuseq) + '.filter.align.16S.nwk -n ' + str(args.r) + '/Filtered_OTU/' + str(otuseq) + '.filter.align.16S.format.name -rd ' + str(ref_traits) + ' -a ' + str(args.r) + '/Filtered_OTU/' + str(otutable) + '.abu.table -r ' + str(args.r) + '/Bayers_model -b ' + str(workingdir + '/scripts/inferTraits.py') + ' --p ' + str(ref_pathogen) + ' --sp ' + str(ref_sp) + ' \n'
                os.system(cmd)
                f1.write(cmd)

        f1.close()


if __name__ == '__main__':
    main()