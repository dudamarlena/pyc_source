# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tareen/Desktop/Desktop_Tests/MPathic3/mpathic/src/EstimateMutualInfoforMImax.py
# Compiled at: 2018-06-21 15:30:08
# Size of source mod 2**32: 8118 bytes
from __future__ import division
import numpy as np, argparse, sys
from subprocess import Popen, PIPE
from sklearn.model_selection import GridSearchCV
if __name__ == '__main__':
    import sortseq.utils
from collections import Counter
from io import StringIO
import pandas as pd, scipy as sp, scipy.ndimage
from mpathic.src import utils
import pdb
from mpathic.src import info

def alt2(df):
    """This is our standard mutual information calculator which is called when
        lm=mi. It is the fastest currently, but requires building a large matrix
        and so takes a lot of memory and can't run the mpra data set on my computer."""
    n_bins = 1000
    n_seqs = len(df.index)
    binheaders = utils.get_column_headers(df)
    ct_vec = np.array((df['ct']), dtype=int)
    n_batches = len(binheaders)
    f = np.repeat((np.array(df[binheaders])), ct_vec, axis=0)
    zlen = f.shape[0]
    f_binned = f.cumsum(axis=0)
    bins = np.linspace((zlen / 1000 - 1), (zlen - 1), 1000, dtype=int)
    f_binned = f_binned[bins, :]
    f_binned[1:, :] = np.subtract(f_binned[1:, :], f_binned[:-1, :])
    f_reg = scipy.ndimage.gaussian_filter1d(f_binned, (0.04 * n_bins), axis=0)
    f_reg = f_reg / f_reg.sum()
    p_b = sp.sum(f_reg, axis=1)
    p_s = sp.sum(f_reg, axis=0)
    MI = 0
    for j in range(n_batches):
        for i in range(n_bins):
            if f_reg[(i, j)] != 0:
                MI = MI + f_reg[(i, j)] * sp.log2(f_reg[(i, j)] / (p_b[i] * p_s[j]))

    return MI


def integrand_1(x):
    index = np.searchsorted(cum_vec, x, side='left')
    return np.array(df.loc[(index, batch_name)])


def integrand_2(y):
    index = np.searchsorted(cum_vec, y, side='left')
    ans = quadgl(integrand_1, [0, n_seqs])
    return ans * mp.log(ans / pb2 / pj[index])


def integrator_solve(df):
    cum_vec = np.array(np.cumsum(df['ct']))
    binheaders = utils.get_column_headers(df)
    n_bins = 1000
    n_batches = len(binheaders)
    f_binned = sp.zeros((n_batches, n_bins))
    bins = np.linspace((cum_vec[(-1)] / 1000 - 1), (cum_vec[(-1)] - 1), 1000, dtype=int)
    for i in range(n_bins):
        for j in range(n_batches):
            batch_name = binheaders[j]
            f_binned[(j, i)] = scipy.integrate.quad(integrand_1, bins[i], bins[(i + 1)])[0]

    f_reg = scipy.ndimage.gaussian_filter1d(f_binned, (0.04 * n_bins), axis=0)
    f_reg = f_reg / f_reg.sum()
    p_b = sp.sum(f_reg, axis=1)
    p_s = sp.sum(f_reg, axis=0)
    MI = 0
    for j in range(n_batches):
        for i in range(n_bins):
            if f_reg[(i, j)] != 0:
                MI = MI + f_reg[(i, j)] * sp.log2(f_reg[(i, j)] / (p_b[i] * p_s[j]))

    return MI


def alt4(df, coarse_graining_level=0.01, return_freg=False):
    """
    MI ESTIMATOR EDITED BY JBK 
    Used when lm=memsaver 
    REQUIRES TESTING AND PROFILING.
    """
    n_groups = 500
    n_seqs = len(df.index)
    binheaders = utils.get_column_headers(df)
    n_batches = len(binheaders)
    cts_grouped = sp.zeros([n_groups, n_batches])
    group_num = 0
    frac_empty = 1.0
    tmp_df = df.copy(binheaders + ['val'])
    if coarse_graining_level:
        if not type(coarse_graining_level) == float:
            raise AssertionError
        elif not coarse_graining_level > 0:
            raise AssertionError
        vals = tmp_df['val'].values
        scale = np.std(vals)
        coarse_vals = np.floor(vals / scale / coarse_graining_level)
        tmp_df['val'] = coarse_vals
        grouped = tmp_df.groupby('val')
        grouped_tmp_df = grouped.aggregate(np.sum)
        grouped_tmp_df.sort_index(inplace=True)
    else:
        grouped_tmp_df = tmp_df
        grouped_tmp_df.sort_values(by='val', inplace=True)
    ct_df = grouped_tmp_df[binheaders].astype(float)
    cts_per_group = ct_df.sum(axis=0).sum() / n_groups
    group_vec = np.zeros(n_batches)
    for i, row in ct_df.iterrows():
        row_ct_tot = row.sum()
        row_ct_vec = row.values
        row_frac_vec = row_ct_vec / row_ct_tot
        while row_ct_tot >= cts_per_group * frac_empty:
            group_vec = group_vec + row_frac_vec * (cts_per_group * frac_empty)
            row_ct_tot -= cts_per_group * frac_empty
            cts_grouped[group_num, :] = group_vec.copy()
            group_num += 1
            frac_empty = 1.0
            group_vec[:] = 0.0

        group_vec += row_frac_vec * row_ct_tot
        frac_empty -= row_ct_tot / cts_per_group

    if group_num == n_groups - 1:
        cts_grouped[group_num, :] = group_vec.copy()
    else:
        if group_num == n_groups:
            pass
        else:
            raise TypeError('group_num=%d does not match n_groups=%s' % (group_num, n_groups))
    f_reg = scipy.ndimage.gaussian_filter1d(cts_grouped, (0.08 * n_groups), axis=0)
    if return_freg:
        return (info.mutualinfo(f_reg), f_reg)
    else:
        return info.mutualinfo(f_reg)


def main():
    parser = argparse.ArgumentParser(description='Estimate mutual information between two variables')
    parser.add_argument('-q1',
      '--q1type', choices=['Continuous', 'Discrete'], default='Discrete', help='Data type for first quantity.')
    parser.add_argument('-q2',
      '--q2type', choices=['Continuous', 'Discrete'], default='Discrete', help='Data type for first quantity.')
    parser.add_argument('-k',
      '--kneig', default='6', help='If you are estimating Continuous\n        vs Continuous, you can overwrite default arguments for the Kraskov \n        estimator here. This argument is number of nearest neighbors \n        to use, with 6 as the default.')
    parser.add_argument('-td',
      '--timedelay', default='1', help='Kraskov Time Delay, default=1')
    parser.add_argument('-cv',
      '--crossvalidate', default=False, choices=[True, False], help='Cross validate Kernel Density Estimate. Default=False')
    parser.add_argument('-o',
      '--out', default=False, help='Output location/type, by \n        default it writes to standard output, if a file name is supplied \n        it will write to a text file')
    args = parser.parse_args()
    MI, V = EstimateMI(quant1,
      quant2, (args.q1type), (args.q2type), timedelay=(args.timedelay), embedding=(args.embedding),
      kneig=(args.kneig),
      cv=(args.crossvalidate))
    if args.out:
        outloc = open(args.out, 'w')
    else:
        outloc = sys.stdout
    outloc.write('Mutual Info \n')
    outloc.write('%.5s' % MI)
    if args.q1type == args.q2type:
        if args.q1type == 'Discrete':
            outloc.write(' +/- %.5s' % np.sqrt(V))
    outloc.write('\n')


if __name__ == '__main__':
    main()