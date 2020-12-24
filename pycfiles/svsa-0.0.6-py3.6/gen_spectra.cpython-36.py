# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/svsa/gen_spectra.py
# Compiled at: 2019-06-10 16:14:05
# Size of source mod 2**32: 1033 bytes
import itertools, numpy as np, pandas as pd, pickle
from .crbs6 import crbs6
from .crbs7 import crbs7

def gen_spectra(y_seq, ri_seq, ef_seq, ci_seq, ct_seq, x_seq, scatter_type='sptsig', model='s6', file=None):
    all_combs = itertools.product(y_seq, ri_seq, ef_seq, ci_seq, ct_seq)
    if model is 's6':
        all_signals = [crbs6(p[0], p[1], p[2], p[3], p[4], x_seq) for p in all_combs]
    if model is 's7':
        all_signals = [crbs7(p[0], p[1], p[2], p[3], p[4], x_seq) for p in all_combs]
    lineshapes = [out[scatter_type] for out in all_signals]
    lineshape_df = pd.DataFrame(np.array(lineshapes))
    params = [(out['y'], out['rlx_int'], out['eukenf'], out['c_int'], out['c_tr']) for out in all_signals]
    param_df = pd.DataFrame(np.array(params))
    param_df.columns = ['y', 'rlx_int', 'eukenf', 'c_int', 'c_tr']
    if file is not None:
        filehandler = open(file, 'wb')
        obj = (lineshape_df, param_df, x_seq)
        pickle.dump(obj, filehandler)
    return (lineshape_df, param_df, x_seq)