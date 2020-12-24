# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/arg_ranker/__main__.py
# Compiled at: 2019-09-26 09:39:42
# Size of source mod 2**32: 9068 bytes
import argparse, os, arg_ranker, sys, pandas as pd
print("------------------------------------------------------------------------\nSample_ranking.py evaluates and assigns the risk and priority levels to environmental samples\nbased on their profile of antibiotic resistant genes (ARGs).\nRequirement: python packages (pandas, argparse)\nRequirement: a mothertable of the ARG abundance in all your samples \nannotated by ARGs-OAP v1.0 (see example/All_sample_cellnumber.txt).\nOptimal: a table of the metadata of your samples (see example/All_sample_metadata.txt).\nRecommend unit of ARG abundance is copy per cell.\n\nThe mother table can be obtained by ARGs-OAP v1.0.\n'perl dir_to_ARGs_OAP/database/DB/gene_subtype_type_ppm_16s_cellnumber_differentversion.pl dir_to_your_result/extracted.fa.blast6out.txt dir_to_your_result/meta_data_online.txt 25 1e-7 80 output_mothertable_name dir_to_ARGs_OAP/database/DB/other/structure_20160422.list dir_to_ARGs_OAP/database/DB/other/SARG-20160422.mod.fasta'\nThe mother table to input is output_mothertable_name.normalize_cellnumber.gene.tab\n\nCopyright:An-Ni Zhang, Prof. Tong Zhang, University of Hong Kong\nCitation:\n1. This study\n2. Yang Y, Jiang X, Chai B, Ma L, Li B, Zhang A, Cole JR, Tiedje JM, Zhang T: ARGs-OAP: online analysispipeline for antibiotic resistance genes detection from metagenomic data using an integrated structured ARG-database. Bioinformatics 2016. (optional: antibiotic resistance database)\nContact caozhichongchong@gmail.com\n------------------------------------------------------------------------\n")

def main():
    usage = 'usage: arg_ranker -i ARG_in_metagenomes -m metadata_metagenomes '
    version_string = 'arg_ranker {v}, on Python {pyv[0]}.{pyv[1]}.{pyv[2]}'.format(v=(arg_ranker.__version__),
      pyv=(sys.version_info))
    parser = argparse.ArgumentParser(formatter_class=(argparse.RawDescriptionHelpFormatter))
    parser.add_argument('-i', default='test',
      action='store',
      type=str,
      metavar='ARGprofile.txt',
      help='input directory or folder of the mother table containing the ARGs abundance of your samples\nrecommend unit of ARG abundance is copy per cell')
    parser.add_argument('-m', default='None',
      action='store',
      type=str,
      metavar='metadata.txt',
      help="input directory or folder of the table containing the metadata of your samples\n'None' for no metadata input")
    parser.add_argument('-o', default='ranking',
      action='store',
      type=str,
      metavar='ranking',
      help='output directory to store the ranking result')
    args = parser.parse_args()
    Metadata = args.m
    Mothertable = args.i
    if Mothertable == 'test':
        Mothertable = os.getcwd() + '/example/ARGprofile_example_1.txt'
        Metadata = os.getcwd() + '/example/metadata.txt'
    else:
        ARGranks = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'ARG_rank.txt')
        try:
            os.mkdir(args.o)
        except OSError:
            pass

        infolder, infile = os.path.split(Mothertable)
        fout = open(os.path.join(args.o, infile + '_sample_ranking_results.txt'), 'w')
        MD = dict()
        i = 0
        if Metadata != 'None':
            for lines in open(Metadata, 'r'):
                lines = str(lines).split('\r')[0].split('\n')[0]
                if i == 0:
                    fout.write('Sample\tRank_I\tRank_II\tRank_III\tRank_IV\tARGs_unassessed\tTotal_abu\tRank_code\tRank_I_risk\tRank_II_risk\tRank_III_risk\tRank_IV_risk' + '\tARGs_unassessed_risk\t%s\n' % '\t'.join(str(lines).split('\t')[1:]))
                else:
                    try:
                        MD.setdefault(str(lines).split('\t')[0], '\t'.join(str(lines).split('\t')[1:]))
                    except KeyError:
                        pass

                i += 1

        else:
            fout.write('Sample\tRank_I\tRank_II\tRank_III\tRank_IV\tARGs_unassessed\tTotal_abu\tRank_code\tRank_I_risk\tRank_II_risk\tRank_III_risk\tRank_IV_risk\tARGs_unassessed_risk\n')
    RK = dict()
    RK_profile = {'I':0,  'II':1,  'III':2,  'IV':3,  'Unassessed':4}
    RKN = [0.0, 0.0, 0.0, 0.0, 0.0]
    for lines in open(ARGranks, 'r'):
        lines = str(lines).split('\r')[0].split('\n')[0]
        RK.setdefault(lines.split('\t')[0], lines.split('\t')[(-1)])
        Rank_num(lines.split('\t')[(-1)], RKN, RK_profile)

    df = pd.read_csv(Mothertable, index_col=None, header=None, skipinitialspace=True, sep='\t')
    df.dropna(axis=0, thresh=2, subset=None, inplace=True)
    df = df.T
    df.to_csv((str(Mothertable) + '.t'), header=None, index=None, sep='\t', mode='a')
    i = 0
    for row in df.itertuples(index=True, name='Pandas'):
        if i == 0:
            ARGlist = row[2:]
        else:
            Level_ranking(row[1:], ARGlist, RK, RKN, fout, RK_profile, MD, Mothertable)
        i += 1

    fout.close()
    print('Finished ranking ARGs\nPlease check your results in ' + str(os.path.join(args.o, infile + '_sample_ranking_results.txt')))


def Rank_num(rank, RKN, RK_profile):
    try:
        RKN[RK_profile[rank]] += 1.0
    except (KeyError, IndexError, TypeError, ValueError):
        pass


def Level_ranking(row, ARGlist, RK, RKN, fout, RK_profile, MD, inputfile):
    Abu = [
     0.0, 0.0, 0.0, 0.0, 0.0]
    ARGposition = 1
    for ARG in ARGlist:
        rank = RK.get(ARG, 'None')
        if rank == 'None':
            print('ARGs in mothertable do not match with the ARGs in ARG_rank.txt.\nPlease check ' + ARG + ' in ' + inputfile + '!\n')
        else:
            try:
                Abu[RK_profile[rank]] += float(row[ARGposition])
            except (KeyError, IndexError, TypeError, ValueError):
                pass

        ARGposition += 1

    total_abu_all = sum(Abu)
    total_abu_I_IV = sum(Abu[0:4])
    if total_abu_all > 0:
        Abu1 = []
        Abu2 = []
        for abu in range(0, 5):
            Abu1.append(float(Abu[abu]) / total_abu_all)

        Num_all = sum(RKN[0:5])
        if total_abu_I_IV > 0:
            for abu in range(0, 5):
                Abu2.append(Abu[abu] / RKN[abu] / (total_abu_all / Num_all))

            if Abu2[0] >= 4.5:
                Level = 1
            else:
                if Abu2[0] >= 2.5:
                    Level = 2
                else:
                    if Abu2[0] > 0.3:
                        Level = 3
                    else:
                        if Abu2[0] > 0.0 or Abu2[1] >= 2.1:
                            Level = 4
                        else:
                            Level = 5
        else:
            Level = 6
            Abu2 = [0.0, 0.0, 0.0, 0.0, 0.0]
        samplename = row[0]
        if MD != {}:
            metadata_sample = MD.get(samplename, 'None')
            fout.write(str(samplename) + '\t' + '\t'.join(str('%.1E' % abu) for abu in Abu1) + '\t' + str('%.1E' % total_abu_all) + '\t' + str('-'.join(str('%.1f' % abu) for abu in Abu2)) + '\t' + '\t'.join(str('%.1f' % abu) for abu in Abu2) + '\t' + str(metadata_sample) + '\n')
        else:
            fout.write(str(samplename) + '\t' + '\t'.join(str('%.1E' % abu) for abu in Abu1) + '\t' + str('%.1E' % total_abu_all) + '\t' + str('-'.join(str('%.1f' % abu) for abu in Abu2)) + '\t' + '\t'.join(str('%.1f' % abu) for abu in Abu2) + '\n')


if __name__ == '__main__':
    main()