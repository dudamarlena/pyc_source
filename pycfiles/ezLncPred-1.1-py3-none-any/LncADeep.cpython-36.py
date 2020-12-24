# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/ezLncPred/ezLncPred/models/LncADeep/LncADeep.py
# Compiled at: 2019-12-09 22:10:09
# Size of source mod 2**32: 8246 bytes
import argparse, sys, os, ezLncPred.models.LncADeep.LncADeep_lncRNA.LncADeep_partial.bin.lncRNA_Predict as lncRNA_Predict_partial, ezLncPred.models.LncADeep.LncADeep_lncRNA.LncADeep_full.bin.lncRNA_Predict as lncRNA_Predict_full
from colorama import init
init(autoreset=True)
from colorama import Fore, Back, Style

def main(args):
    script_dir = os.path.split(os.path.realpath(__file__))[0]
    saveDir_lncRNA = script_dir + '/LncADeep_lncRNA/src/'
    saveDir_hmmer = script_dir + '/LncADeep_lncRNA/LncADeep_partial/bin/'
    if getDatabase('Pfam-A.hmm', saveDir_lncRNA):
        if args.modeltype == 'partial':
            if gethmmer('hmmer-3.2.1', saveDir_hmmer):
                if args.fasta:
                    if args.outfile:
                        lncRNA_Predict_partial.predict(filename=(args.fasta), output_prefix=(args.outfile), species=(args.species), thread=(args.thread), HMMthread=(args.HMMthread))
                parser.parse_args(['-h'])
        else:
            if args.modeltype == 'full':
                if args.fasta:
                    if args.outfile:
                        lncRNA_Predict_full.predict(filename=(args.fasta), output_prefix=(args.outfile), species=(args.species), thread=(args.thread), HMMthread=(args.HMMthread))
                parser.parse_args(['-h'])
            else:
                parser.parse_args(['-h'])


def getDatabase(database, saveDir):
    print(Fore.CYAN + Style.BRIGHT + '------------------------------Start Loading %s database----------------------------\n' % database)
    modelAbsPath = saveDir + database
    if os.path.exists(modelAbsPath):
        print(Fore.CYAN + Style.BRIGHT + '----------------------------------Loading Completed-------------------------\n')
        return True
    else:
        choice = input(Fore.GREEN + Style.BRIGHT + 'Loading Failed! Do you want to download ' + database + ' database from remote repository (243M) ? [y/n]' + '\x1b[39m')
        if choice == 'y':
            downURL = 'http://120.27.208.220/lncRNAPredModels/Pfam-A.hmm.tgz'
            downComm = 'wget -nv --show-progress -O ' + modelAbsPath + '.tgz ' + downURL
            os.system(downComm)
            print(Fore.CYAN + Style.BRIGHT + '\n-------------------------------Download Succeed!Now Decompressing---------------------------\n')
            extractComm = 'tar -xzf ' + modelAbsPath + '.tgz' + ' -C ' + saveDir
            os.system(extractComm)
            rmComm = 'rm ' + modelAbsPath + '.tgz'
            os.system(rmComm)
            if os.path.exists(modelAbsPath):
                print(Fore.CYAN + Style.BRIGHT + '-----------------------------------------Loading Succeed----------------------------------------\n')
                return True
        else:
            print(Fore.RED + Style.BRIGHT + '-----------------------------------------Loading Failed----------------------------------------\n')
        return False


def gethmmer(hmmer, saveDir):
    print(Fore.CYAN + Style.BRIGHT + '------------------------------Start Loading hmmer ----------------------------\n')
    modelAbsPath = saveDir + hmmer
    if os.path.exists(modelAbsPath):
        print(Fore.CYAN + Style.BRIGHT + '----------------------------------Loading Completed-------------------------\n')
        return True
    else:
        choice = input(Fore.GREEN + Style.BRIGHT + 'Loading Failed! Do you want to download ' + hmmer + ' from remote repository (75M) ? [y/n]' + '\x1b[39m')
        if choice == 'y':
            downURL = 'http://120.27.208.220/lncRNAPredModels/hmmer-3.2.1.tgz'
            downComm = 'wget -nv --show-progress -O ' + modelAbsPath + '.tgz ' + downURL
            os.system(downComm)
            print(Fore.CYAN + Style.BRIGHT + '\n-------------------------------Download Succeed!Now Decompressing---------------------------\n')
            extractComm = 'tar -xzf ' + modelAbsPath + '.tgz' + ' -C ' + saveDir
            os.system(extractComm)
            rmComm = 'rm ' + modelAbsPath + '.tgz'
            os.system(rmComm)
            if os.path.exists(modelAbsPath):
                print(Fore.CYAN + Style.BRIGHT + '-----------------------------------------Loading Succeed----------------------------------------\n')
                return True
        else:
            print(Fore.RED + Style.BRIGHT + '-----------------------------------------Loading Failed----------------------------------------\n')
        return False


if __name__ == '__main__':
    main()