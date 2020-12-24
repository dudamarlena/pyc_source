# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/LncrnaPackage/models/LncADeep/LncADeep.py
# Compiled at: 2019-10-31 07:25:52
import argparse, sys, os, LncADeep_lncRNA.LncADeep_partial.bin.lncRNA_Predict as lncRNA_Predict_partial, LncADeep_lncRNA.LncADeep_full.bin.lncRNA_Predict as lncRNA_Predict_full
from LncADeep_anno.bin.lncRNA_func_model_release import Predict as lncRNA_func_Predict
from LncADeep_anno.bin.lncRNA_func_model_release import Annotate as lncRNA_func_Annotate

def main(args):
    if args.modeltype == 'partial':
        if args.fasta and args.outfile:
            lncRNA_Predict_partial.predict(filename=args.fasta, output_prefix=args.outfile, species=args.species, thread=args.thread, HMMthread=args.HMMthread)
        else:
            parser.parse_args(['-h'])
    elif args.modeltype == 'full':
        if args.fasta and args.outfile:
            lncRNA_Predict_full.predict(filename=args.fasta, output_prefix=args.outfile, species=args.species, thread=args.thread, HMMthread=args.HMMthread)
        else:
            parser.parse_args(['-h'])
    else:
        parser.parse_args(['-h'])


if __name__ == '__main__':
    main()