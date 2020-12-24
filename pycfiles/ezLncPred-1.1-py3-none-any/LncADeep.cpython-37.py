# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/LncrnaPackage/models/LncADeep/LncADeep.py
# Compiled at: 2019-10-31 08:54:18
# Size of source mod 2**32: 4894 bytes
import argparse, sys, os
import models.LncADeep.LncADeep_lncRNA.LncADeep_partial.bin.lncRNA_Predict as lncRNA_PredictPartial
import models.LncADeep.LncADeep_lncRNA.LncADeep_full.bin.lncRNA_Predict as lncRNA_Predict_full
import models.LncADeep.LncADeep_anno.bin.lncRNA_func_model_release as lncRNA_func_Predict
import models.LncADeep.LncADeep_anno.bin.lncRNA_func_model_release as lncRNA_func_Annotate

def main(args):
    if args.modeltype == 'partial':
        if args.fasta and args.outfile:
            lncRNA_Predict_partial.predict(filename=(args.fasta), output_prefix=(args.outfile), species=(args.species), thread=(args.thread), HMMthread=(args.HMMthread))
        else:
            parser.parse_args(['-h'])
    elif args.modeltype == 'full':
        if args.fasta and args.outfile:
            lncRNA_Predict_full.predict(filename=(args.fasta), output_prefix=(args.outfile), species=(args.species), thread=(args.thread), HMMthread=(args.HMMthread))
        else:
            parser.parse_args(['-h'])
    else:
        parser.parse_args(['-h'])


if __name__ == '__main__':
    main()