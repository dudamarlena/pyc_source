# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/epcy/tools/pred.py
# Compiled at: 2020-03-20 10:15:51
# Size of source mod 2**32: 486 bytes
import time, sys, numpy as np, pandas as pd
from ..utils import other as uo
from ..utils import readers as ur

def main_pred(args, argparser):
    sys.stderr.write(time.strftime('%X') + ': Read design and matrix ' + 'features\n')
    design, data, list_ids = ur.read_design_matrix(args)
    num_pred = data.shape[0]
    all_classifier = uo.compute_pred(args, num_pred, list_ids, data, design)
    uo.save_pred_res(args, all_classifier)