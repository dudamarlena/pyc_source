# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cuteSV/cuteSV_Description.py
# Compiled at: 2020-04-29 04:13:06
# Size of source mod 2**32: 10274 bytes
__doc__ = ' \n * All rights Reserved, Designed By HIT-Bioinformatics   \n * @Title:  cuteSV_Description.py\n * @author: tjiang\n * @date: Apr 26th 2020\n * @version V1.0.6   \n'
import argparse
VERSION = '1.0.6'

class cuteSVdp(object):
    """cuteSVdp"""
    USAGE = '\tLong read based fast and accurate SV detection with cuteSV.\n\t\n\tCurrent version: v%s\n\tAuthor: Tao Jiang\n\tContact: tjiang@hit.edu.cn\n\n\n\tSuggestions:\n\n\tFor PacBio CLR/ONT data:\n\t\t--max_cluster_bias_INS\t\t100\n\t\t--diff_ratio_merging_INS\t0.2\n\t\t--diff_ratio_filtering_INS\t0.6\n\t\t--diff_ratio_filtering_DEL\t0.7\n\tFor PacBio CCS(HIFI) data:\n\t\t--max_cluster_bias_INS\t\t200\n\t\t--diff_ratio_merging_INS\t0.65\n\t\t--diff_ratio_filtering_INS\t0.65\n\t\t--diff_ratio_filtering_DEL\t0.35\n\n\n\t' % VERSION


def parseArgs(argv):
    parser = argparse.ArgumentParser(prog='cuteSV', description=(cuteSVdp.USAGE),
      formatter_class=(argparse.RawDescriptionHelpFormatter))
    parser.add_argument('--version', '-v', action='version',
      version='%(prog)s {version}'.format(version=VERSION))
    parser.add_argument('input', metavar='[BAM]',
      type=str,
      help='Sorted .bam file form NGMLR or Minimap2.')
    parser.add_argument('output', type=str,
      help='Output VCF format file.')
    parser.add_argument('work_dir', type=str,
      help='Work-directory for distributed jobs')
    parser.add_argument('-t', '--threads', help='Number of threads to use.[%(default)s]',
      default=16,
      type=int)
    parser.add_argument('-b', '--batches', help='Batch of genome segmentation interval.[%(default)s]',
      default=10000000,
      type=int)
    parser.add_argument('-S', '--sample', help='Sample name/id',
      default='NULL',
      type=str)
    parser.add_argument('--retain_work_dir', help='Enable to retain temporary folder and files.',
      action='store_true')
    GroupSignaturesCollect = parser.add_argument_group('Collection of SV signatures')
    GroupSignaturesCollect.add_argument('-p', '--max_split_parts', help='Maximum number of split segments a read may be aligned before it is ignored.[%(default)s]',
      default=7,
      type=int)
    GroupSignaturesCollect.add_argument('-q', '--min_mapq', help='Minimum mapping quality value of alignment to be taken into account.[%(default)s]',
      default=20,
      type=int)
    GroupSignaturesCollect.add_argument('-r', '--min_read_len', help='Ignores reads that only report alignments with not longer than bp.[%(default)s]',
      default=500,
      type=int)
    GroupSignaturesCollect.add_argument('-md', '--merge_del_threshold', help='Maximum distance of deletion signals to be merged.[%(default)s]',
      default=0,
      type=int)
    GroupSignaturesCollect.add_argument('-mi', '--merge_ins_threshold', help='Maximum distance of insertion signals to be merged.[%(default)s]',
      default=100,
      type=int)
    GroupSVCluster = parser.add_argument_group('Generation of SV clusters')
    GroupSVCluster.add_argument('-s', '--min_support', help='Minimum number of reads that support a SV to be reported.[%(default)s]',
      default=10,
      type=int)
    GroupSVCluster.add_argument('-l', '--min_size', help='Minimum size of SV to be reported.[%(default)s]',
      default=30,
      type=int)
    GroupSVCluster.add_argument('-L', '--max_size', help='Maximum size of SV to be reported.[%(default)s]',
      default=100000,
      type=int)
    GroupSVCluster.add_argument('-sl', '--min_siglength', help='Minimum length of SV signal to be extracted.[%(default)s]',
      default=10,
      type=int)
    GroupGenotype = parser.add_argument_group('Computing genotypes')
    GroupGenotype.add_argument('--genotype', help='Enable to generate genotypes.',
      action='store_true')
    GroupGenotype.add_argument('--gt_round', help='Maximum round of iteration for alignments searching if perform genotyping.[%(default)s]',
      default=500,
      type=int)
    GroupAdvanced = parser.add_argument_group('Advanced')
    GroupAdvanced.add_argument('--max_cluster_bias_INS', help='Maximum distance to cluster read together for insertion.[%(default)s]',
      default=100,
      type=int)
    GroupAdvanced.add_argument('--diff_ratio_merging_INS', help='Do not merge breakpoints with basepair identity more than [%(default)s] for insertion.',
      default=0.2,
      type=float)
    GroupAdvanced.add_argument('--diff_ratio_filtering_INS', help='Filter breakpoints with basepair identity less than [%(default)s] for insertion.',
      default=0.6,
      type=float)
    GroupAdvanced.add_argument('--max_cluster_bias_DEL', help='Maximum distance to cluster read together for deletion.[%(default)s]',
      default=200,
      type=int)
    GroupAdvanced.add_argument('--diff_ratio_merging_DEL', help='Do not merge breakpoints with basepair identity more than [%(default)s] for deletion.',
      default=0.3,
      type=float)
    GroupAdvanced.add_argument('--diff_ratio_filtering_DEL', help='Filter breakpoints with basepair identity less than [%(default)s] for deletion.',
      default=0.7,
      type=float)
    GroupAdvanced.add_argument('--max_cluster_bias_INV', help='Maximum distance to cluster read together for inversion.[%(default)s]',
      default=500,
      type=int)
    GroupAdvanced.add_argument('--max_cluster_bias_DUP', help='Maximum distance to cluster read together for duplication.[%(default)s]',
      default=500,
      type=int)
    GroupAdvanced.add_argument('--max_cluster_bias_TRA', help='Maximum distance to cluster read together for translocation.[%(default)s]',
      default=50,
      type=int)
    GroupAdvanced.add_argument('--diff_ratio_filtering_TRA', help='Filter breakpoints with basepair identity less than [%(default)s] for translocation.',
      default=0.6,
      type=float)
    args = parser.parse_args(argv)
    return args


def Generation_VCF_header(file, contiginfo, sample, argv):
    file.write('##fileformat=VCFv4.2\n')
    file.write('##source=cuteSV-%s\n' % VERSION)
    import time
    file.write('##fileDate=%s\n' % time.strftime('%Y-%m-%d %H:%M:%S %w-%Z', time.localtime()))
    for i in contiginfo:
        file.write('##contig=<ID=%s,length=%d>\n' % (i[0], i[1]))

    file.write('##ALT=<ID=INS,Description="Insertion of novel sequence relative to the reference">\n')
    file.write('##ALT=<ID=DEL,Description="Deletion relative to the reference">\n')
    file.write('##ALT=<ID=DUP,Description="Region of elevated copy number relative to the reference">\n')
    file.write('##ALT=<ID=INV,Description="Inversion of reference sequence">\n')
    file.write('##ALT=<ID=BND,Description="Breakend of translocation">\n')
    file.write('##INFO=<ID=PRECISE,Number=0,Type=Flag,Description="Precise structural variant">\n')
    file.write('##INFO=<ID=IMPRECISE,Number=0,Type=Flag,Description="Imprecise structural variant">\n')
    file.write('##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">\n')
    file.write('##INFO=<ID=SVLEN,Number=1,Type=Integer,Description="Difference in length between REF and ALT alleles">\n')
    file.write('##INFO=<ID=CHR2,Number=1,Type=String,Description="Chromosome for END coordinate in case of a translocation">\n')
    file.write('##INFO=<ID=END,Number=1,Type=Integer,Description="End position of the variant described in this record">\n')
    file.write('##INFO=<ID=CIPOS,Number=2,Type=Integer,Description="Confidence interval around POS for imprecise variants">\n')
    file.write('##INFO=<ID=CILEN,Number=2,Type=Integer,Description="Confidence interval around inserted/deleted material between breakends">\n')
    file.write('##INFO=<ID=RE,Number=1,Type=Integer,Description="Number of read support this record">\n')
    file.write('##INFO=<ID=STRANDS,Number=1,Type=String,Description="Strand orientation of the adjacency in BEDPE format (DEL:+-, DUP:-+, INV:++/--)">>\n')
    file.write('##FILTER=<ID=q5,Description="Quality below 5">\n')
    file.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
    file.write('##FORMAT=<ID=DR,Number=1,Type=Integer,Description="# High-quality reference reads">\n')
    file.write('##FORMAT=<ID=DV,Number=1,Type=Integer,Description="# High-quality variant reads">\n')
    file.write('##FORMAT=<ID=PL,Number=1,Type=Integer,Description="# Phred-scaled genotype likelihoods rounded to the closest integer">\n')
    file.write('##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="# Genotype quality">\n')
    file.write('##CommandLine="cuteSV %s"\n' % ' '.join(argv))
    file.write('#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t%s\n' % sample)