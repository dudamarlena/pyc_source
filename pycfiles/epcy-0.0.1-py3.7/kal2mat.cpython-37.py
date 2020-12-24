# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/epcy/tools/kal2mat.py
# Compiled at: 2020-03-19 17:47:34
# Size of source mod 2**32: 1570 bytes
import os, time, sys, h5py, numpy as np, pandas as pd
from ..utils import readers as ur
from ..utils import other as uo

def main_kal2mat(args, argparser):
    if args.KAL:
        if args.GENE:
            sys.stderr.write(time.strftime('%X') + ': Run EPCY on kallisto ' + 'output on gene\n')
        else:
            sys.stderr.write(time.strftime('%X') + ': Run EPCY on kallisto ' + 'output on transcript!!!\n')
            sys.stderr.write(time.strftime('%X') + ':\t add --gene to run ' + 'on gene level\n')
    df_anno = ur.read_anno(args)
    sys.stderr.write(time.strftime('%X') + ': Read design and matrix ' + 'features\n')
    design, data, list_ids = ur.read_design_matrix_rna(args, df_anno)
    df_data = pd.DataFrame(data=data, columns=(design['sample']))
    df_data.insert(loc=0, column='ID', value=list_ids)
    if not os.path.exists(args.PATH_OUT):
        os.makedirs(args.PATH_OUT)
    file_out = os.path.join(args.PATH_OUT, 'readcounts.xls')
    if args.CPM:
        if args.LOG:
            file_out = os.path.join(args.PATH_OUT, 'readcounts_cpm_log.xls')
        else:
            file_out = os.path.join(args.PATH_OUT, 'readcounts_cpm.xls')
    else:
        if args.TPM:
            if args.LOG:
                file_out = os.path.join(args.PATH_OUT, 'readcounts_tpm_log.xls')
            else:
                file_out = os.path.join(args.PATH_OUT, 'readcounts_tpm_.xls')
        df_data.to_csv(file_out, index=False, sep='\t')