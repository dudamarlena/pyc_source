# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/epcy/tools/pred_rna.py
# Compiled at: 2020-03-30 14:12:49
# Size of source mod 2**32: 1041 bytes
import os, time, sys, h5py, numpy as np, pandas as pd
from ..utils import readers as ur
from ..utils import other as uo

def main_pred_rna(args, argparser):
    if args.KAL:
        if args.GENE:
            sys.stderr.write(time.strftime('%X') + ': Run EPCY on kallisto ' + 'output on gene\n')
        else:
            sys.stderr.write(time.strftime('%X') + ': Run EPCY on kallisto ' + 'output on transcript!!!\n')
            sys.stderr.write(time.strftime('%X') + ':\t add --gene to run ' + 'on gene level\n')
    df_anno = ur.read_anno(args)
    sys.stderr.write(time.strftime('%X') + ': Read design and matrix ' + 'features\n')
    design, data, list_ids = ur.read_design_matrix_rna(args, df_anno)
    if design is None:
        exit()
    num_pred = data.shape[0]
    all_classifier = uo.compute_pred(args, num_pred, list_ids, data, design)
    uo.save_pred_res(args, all_classifier)