# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/epcy/tools/qc.py
# Compiled at: 2020-03-17 15:20:16
# Size of source mod 2**32: 5675 bytes
import pandas as pd, numpy as np, math
from ..utils import plot as up

def set_color_legend():
    df_pred['abs_l2fc'] = np.abs(df_pred['l2fc'])
    quantiles = [math.trunc(np.quantile(df_pred['abs_l2fc'], x) * 10000) / 10000 for x in (0.01,
                                                                                           0.05,
                                                                                           0.25,
                                                                                           0.5,
                                                                                           0.75,
                                                                                           0.95,
                                                                                           0.99)]
    legend_quantile = [
     'abs(l2fc) <' + str(quantiles[0]),
     str(quantiles[0]) + '<= abs(l2fc) <=' + str(quantiles[1]),
     str(quantiles[1]) + '<= abs(l2fc) <' + str(quantiles[2]),
     str(quantiles[2]) + '<= abs(l2fc) <' + str(quantiles[3]),
     str(quantiles[3]) + '<= abs(l2fc) <' + str(quantiles[4]),
     str(quantiles[4]) + '<= abs(l2fc) <' + str(quantiles[5]),
     str(quantiles[6]) + '<= abs(l2fc)']
    df_pred = df_pred.sort_values(['abs_l2fc'], ascending=True)
    df_pred['color_legend'] = legend_quantile[0]
    df_pred.loc[((df_pred['abs_l2fc'] >= quantiles[0]) & (df_pred['abs_l2fc'] < quantiles[1]), 'color_legend')] = legend_quantile[1]
    df_pred.loc[((df_pred['abs_l2fc'] >= quantiles[1]) & (df_pred['abs_l2fc'] < quantiles[2]), 'color_legend')] = legend_quantile[2]
    df_pred.loc[((df_pred['abs_l2fc'] >= quantiles[2]) & (df_pred['abs_l2fc'] < quantiles[3]), 'color_legend')] = legend_quantile[3]
    df_pred.loc[((df_pred['abs_l2fc'] >= quantiles[3]) & (df_pred['abs_l2fc'] < quantiles[4]), 'color_legend')] = legend_quantile[4]
    df_pred.loc[((df_pred['abs_l2fc'] >= quantiles[4]) & (df_pred['abs_l2fc'] < quantiles[5]), 'color_legend')] = legend_quantile[5]
    df_pred.loc[(df_pred['abs_l2fc'] >= quantiles[5], 'color_legend')] = legend_quantile[6]


def main_qc(args, argparser):
    df_pred = pd.read_csv((args.PRED), sep='\t')
    df_pred = df_pred.dropna()
    min_mcc = df_pred['kernel_mcc'].min()
    start_bin = math.trunc((round(min_mcc, 1) - 0.05) * 100)
    mcc_bins = [x / 100 for x in range(start_bin, 105, 5)]
    if args.L2FC:
        df_pred['abs_l2fc'] = np.abs(df_pred['l2fc'])
        quantiles = [math.trunc(np.quantile(df_pred['abs_l2fc'], x) * 10000) / 10000 for x in (0.01,
                                                                                               0.05,
                                                                                               0.25,
                                                                                               0.5,
                                                                                               0.75,
                                                                                               0.95,
                                                                                               0.99)]
        legend_quantile = [
         'abs(l2fc) <' + str(quantiles[0]),
         str(quantiles[0]) + '<= abs(l2fc) <' + str(quantiles[1]),
         str(quantiles[1]) + '<= abs(l2fc) <' + str(quantiles[2]),
         str(quantiles[2]) + '<= abs(l2fc) <' + str(quantiles[3]),
         str(quantiles[3]) + '<= abs(l2fc) <' + str(quantiles[4]),
         str(quantiles[4]) + '<= abs(l2fc) <' + str(quantiles[5]),
         str(quantiles[6]) + '<= abs(l2fc)']
        df_pred = df_pred.sort_values(['abs_l2fc'], ascending=True)
        df_pred['color_legend'] = legend_quantile[0]
        df_pred.loc[((df_pred['abs_l2fc'] >= quantiles[0]) & (df_pred['abs_l2fc'] < quantiles[1]), 'color_legend')] = legend_quantile[1]
        df_pred.loc[((df_pred['abs_l2fc'] >= quantiles[1]) & (df_pred['abs_l2fc'] < quantiles[2]), 'color_legend')] = legend_quantile[2]
        df_pred.loc[((df_pred['abs_l2fc'] >= quantiles[2]) & (df_pred['abs_l2fc'] < quantiles[3]), 'color_legend')] = legend_quantile[3]
        df_pred.loc[((df_pred['abs_l2fc'] >= quantiles[3]) & (df_pred['abs_l2fc'] < quantiles[4]), 'color_legend')] = legend_quantile[4]
        df_pred.loc[((df_pred['abs_l2fc'] >= quantiles[4]) & (df_pred['abs_l2fc'] < quantiles[5]), 'color_legend')] = legend_quantile[5]
        df_pred.loc[(df_pred['abs_l2fc'] >= quantiles[5], 'color_legend')] = legend_quantile[6]
    else:
        df_pred['max(query, ref)'] = df_pred[[
         'mean_query', 'mean_ref']].max(axis=1)
        quantiles = [math.trunc(np.quantile(df_pred['max(query, ref)'], x) * 10000) / 10000 for x in (0.01,
                                                                                                      0.05,
                                                                                                      0.25,
                                                                                                      0.5,
                                                                                                      0.75,
                                                                                                      0.95,
                                                                                                      0.99)]
        legend_quantile = [
         'max(query, ref) <' + str(quantiles[0]),
         str(quantiles[0]) + '<= max(query, ref) <' + str(quantiles[1]),
         str(quantiles[1]) + '<= max(query, ref) <' + str(quantiles[2]),
         str(quantiles[2]) + '<= max(query, ref) <' + str(quantiles[3]),
         str(quantiles[3]) + '<= max(query, ref) <' + str(quantiles[4]),
         str(quantiles[4]) + '<= max(query, ref) <' + str(quantiles[5]),
         str(quantiles[6]) + '<= max(query, ref)']
        df_pred = df_pred.sort_values(['max(query, ref)'], ascending=True)
        df_pred['color_legend'] = legend_quantile[0]
        df_pred.loc[((df_pred['max(query, ref)'] >= quantiles[0]) & (df_pred['max(query, ref)'] < quantiles[1]), 'color_legend')] = legend_quantile[1]
        df_pred.loc[((df_pred['max(query, ref)'] >= quantiles[1]) & (df_pred['max(query, ref)'] < quantiles[2]), 'color_legend')] = legend_quantile[2]
        df_pred.loc[((df_pred['max(query, ref)'] >= quantiles[2]) & (df_pred['max(query, ref)'] < quantiles[3]), 'color_legend')] = legend_quantile[3]
        df_pred.loc[((df_pred['max(query, ref)'] >= quantiles[3]) & (df_pred['max(query, ref)'] < quantiles[4]), 'color_legend')] = legend_quantile[4]
        df_pred.loc[((df_pred['max(query, ref)'] >= quantiles[4]) & (df_pred['max(query, ref)'] < quantiles[5]), 'color_legend')] = legend_quantile[5]
        df_pred.loc[(df_pred['max(query, ref)'] >= quantiles[5], 'color_legend')] = legend_quantile[6]
    up.plot_qc_histo(df_pred, quantiles, legend_quantile, mcc_bins, args)