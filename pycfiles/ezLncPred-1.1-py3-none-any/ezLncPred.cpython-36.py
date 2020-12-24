# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/ezLncPred/ezLncPred/ezLncPred.py
# Compiled at: 2020-01-12 08:44:53
# Size of source mod 2**32: 8769 bytes
from pyfiglet import Figlet
from colorama import init
init(autoreset=True)
from colorama import Fore, Back, Style
import ezLncPred.models.CPC2.bin.CPC2 as CPC2, ezLncPred.models.CPAT.bin.cpat as CPAT, ezLncPred.models.PredLnc_GFStack.src.PredLnc_GFStack as GFStack, ezLncPred.models.longdist.bin.longdist as longdist, ezLncPred.models.CPPred.bin.CPPred as CPPred, ezLncPred.models.CNCI.CNCI as CNCI, ezLncPred.models.PLEK.PLEK as PLEK, ezLncPred.models.lgc.lgc as lgc, ezLncPred.models.LncADeep.LncADeep as LncADeep, argparse, os

def parse_args():
    parser = argparse.ArgumentParser(prog='ezLncPred', description=(Fore.CYAN + 'ezLncPred: an integrated Python package and web server to identify lncRNA sequence conveniently. This                                             Lncrna Prediction Package contains 9 prediction methods collected by Zhao et al. (2020)' + '\x1b[39m'))
    parser.add_argument('-i', '--input', dest='fasta', help='input file', type=str)
    parser.add_argument('-o', '--output', dest='outfile', help='output file name', type=str)
    parser.add_argument('-m', '--manual', action='store_true', help='show manuals')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    subparsers = parser.add_subparsers(help='After model [-h] for additional help', dest='subparser_name')
    CNCI_parser = subparsers.add_parser('CNCI', usage='ezLncPred [-i FASTA] [-o OUTFILE] CNCI [-h] [--parallel] [-d DIRECTORY] [-p SPECIES]')
    CNCI_parser.add_argument('--parallel', action='store_true', default=True, help='assign the running CPU numbers')
    CNCI_parser.add_argument('-p', '--species', default='ve', choices=('ve', 'pl'), help='assign the classification models ("ve" for vertebrate species, "pl" for plat species)')
    CPC2_parser = subparsers.add_parser('CPC2', usage='ezLncPred [-i FASTA] [-o OUTFILE] CPC2 [-h] [-r]')
    CPC2_parser.add_argument('-r', '--reverse', help='also check the reverse strand')
    CPAT_parser = subparsers.add_parser('CPAT', usage='ezLncPred [-i FASTA] [-o OUTFILE] CPAT [-h] [-p SPECIES] [-s START_CODONS] [-t STOP_CODONS]')
    CPAT_parser.add_argument('-p', '--species', dest='species', default='Human', choices=('Human',
                                                                                          'Mouse',
                                                                                          'Fly',
                                                                                          'Zebrafish'), help='specify the species of the LncRNAs choose from `Human` `Mouse` `Fly` `Zebrafish` (note that the first character is upper case).')
    CPAT_parser.add_argument('-s', '--start', action='store', dest='start_codons', default='ATG', help="Start codon (DNA sequence, so use 'T' instead of 'U') used to define open reading frame (ORF). default=%%default")
    CPAT_parser.add_argument('-t', '--stop', action='store', dest='stop_codons', default='TAG,TAA,TGA', help="Stop codon (DNA sequence, so use 'T' instead of 'U') used to define open reading frame (ORF).                         Multiple stop codons should be separated by ','. default=%%default")
    lgc_parser = subparsers.add_parser('lgc', usage='ezLncPred [-i FASTA] [-o OUTFILE] lgc [-h]')
    CPPred_parser = subparsers.add_parser('CPPred', usage='ezLncPred [-i FASTA] [-o OUTFILE] CPPred [-h] [-p SPECIES]')
    CPPred_parser.add_argument('-p', '--species', dest='species', default='Human', choices=('Human',
                                                                                            'Integrated'), help='the model of the species to choose (Human,Integrated).')
    GFStack_parser = subparsers.add_parser('GFStack', usage='ezLncPred [-i FASTA] [-o OUTFILE] GFStack [-h] [-p SPECIES]')
    GFStack_parser.add_argument('-p', '--species', dest='species', default='human', choices=('human',
                                                                                             'mouse'), help='the model of the species to choose (human,mouse).')
    longdist_parser = subparsers.add_parser('longdist', usage='ezLncPred [-i FASTA] [-o OUTFILE] longdist [-h] [-z SIZE] [-p SPECIES]')
    longdist_parser.add_argument('-z', '--size', nargs=1, metavar='<200>', default=[200], type=int, dest='size', help='Minimun sequence size to consider. Default is 200.')
    longdist_parser.add_argument('-p', '--species', dest='species', default='Human', choices=('Human',
                                                                                              'Mouse'), help='the model of the species to choose (human,mouse).')
    PLEK_parser = subparsers.add_parser('PLEK', usage='ezLncPred [-i FASTA] [-o OUTFILE] longdist [-h] [-t THREAD] [--isoutmsg] [--isrmtempfile]')
    PLEK_parser.add_argument('-t', '--thread', dest='thread', default=1, help='The number of threads for running the PLEK program.')
    PLEK_parser.add_argument('--isoutmsg', action='store', help='output message to stdout or not,0 means that PLEK be run quietly.')
    PLEK_parser.add_argument('--isrmtempfile', action='store', help='remove temporary file or not,0 means that PLEK be run quietly.')
    LncADeep_parser = subparsers.add_parser('LncADeep', usage='ezLncPred [-i FASTA] [-o OUTFILE] longdist [-h] [-mt MODELTYPE] [-HMM HMMTHREAD] [-p SPECIES] [-t THREAD]')
    LncADeep_parser.add_argument('-mt', '--modeltype', action='store', dest='modeltype', choices=['full', 'partial'], type=str, default='partial', help='(Optional for lncRNA identification) The model used for lncRNA identification, default is "partial"')
    LncADeep_parser.add_argument('-HMM', '--HMMthread', action='store', dest='HMMthread', default=8, type=int, help='(Optional for lncRNA identification) The thread number of using HMMER, default is 8')
    LncADeep_parser.add_argument('-p', '--species', dest='species', default='human', choices=('human',
                                                                                              'mouse'), help='the model of the species to choose (human,mouse).')
    LncADeep_parser.add_argument('-t', '--thread', dest='thread', default=1, help='The number of threads for running the LncADeep program.')
    return parser


def mode_selection(args):
    model = args.subparser_name
    resultFile = 'results/' + model
    print(Fore.CYAN + Style.BRIGHT + 'Now ' + model + ' is ready to run ...\n')
    eval(model).main(args)
    print(Fore.CYAN + Style.BRIGHT + 'Now the lncRNA prediction task has been accomplished by ' + model + '. The results have been saved at ./' + args.outfile + '*\n')
    print(Fore.CYAN + Style.BRIGHT + 'Thanks for using ezLncPred!\n')


def mkdir_or_touch(args):
    if args.subparser_name == 'CNCI' or args.subparser_name == 'LncADeep':
        os.system('mkdir -p ' + args.outfile)
    else:
        os.system('touch ' + args.outfile)


def print_version():
    f = Figlet(font='slant')
    print(Fore.MAGENTA + Style.BRIGHT + f.renderText('ezLncPred'))
    print(Fore.GREEN + Style.BRIGHT + 'ezLncPred v1.0 (Based on Python). The website is http://bbdm.hzau.edu.cn/ezLncPred')
    print('=' * 85 + '\n')


def main():
    script_dir = os.path.split(os.path.realpath(__file__))[0]
    parser = parse_args()
    args = parser.parse_args()
    if args.fasta:
        if not os.path.exists(args.fasta):
            print(Fore.RED + Style.BRIGHT + args.fasta + ' is not a file ! Please check your input file')
            parser.print_usage()
    if args.outfile:
        if os.path.exists(args.outfile):
            print(Fore.RED + Style.BRIGHT + args.outfile + ' has existed ! Please check your output file name ')
            parser.print_usage()
    if args.manual and not args.subparser_name:
        print_version()
        os.system('more ' + script_dir + '/README.md')
    elif args.manual and args.subparser_name:
        os.system('more ' + script_dir + '/docs/README_%s' % args.subparser_name)
    else:
        if args.outfile and not os.path.exists(args.outfile) and args.subparser_name:
            mkdir_or_touch(args)
            print_version()
            mode_selection(args)
        elif args.fasta:
            if args.outfile:
                if args.subparser_name:
                    print_version()
                    mode_selection(args)
        else:
            print_version()
            parser.print_usage()