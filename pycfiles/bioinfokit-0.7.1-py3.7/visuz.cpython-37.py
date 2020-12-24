# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/bioinfokit/visuz.py
# Compiled at: 2020-04-16 23:04:47
# Size of source mod 2**32: 24218 bytes
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.cm as cmc
import seaborn as sns
from matplotlib_venn import venn3, venn2
from random import sample
from functools import reduce
import sys

def volcano(d='dataframe', lfc=None, pv=None, lfc_thr=1, pv_thr=0.05, color=('green', 'red'), valpha=1, geneid=None, genenames=None, gfont=8, dim=(6, 4), r=300, ar=90, dotsize=8, markerdot='o', sign_line=False):
    general.depr_mes('bioinfokit.visuz.gene_exp.volcano')


def involcano(table='dataset_file', lfc='logFC', pv='p_values', lfc_thr=1, pv_thr=0.05, color=('green', 'red'), valpha=1, geneid=None, genenames=None, gfont=8):
    general.depr_mes('bioinfokit.visuz.gene_exp.involcano')


def ma(table='dataset_file', lfc='logFC', ct_count='value1', st_count='value2', lfc_thr=1):
    general.depr_mes('bioinfokit.visuz.gene_exp.ma')


def corr_mat(table='p_df', corm='pearson'):
    general.depr_mes('bioinfokit.visuz.stat.corr_mat')


def screeplot(obj='pcascree'):
    y = [x * 100 for x in obj[1]]
    plt.bar(obj[0], y)
    plt.xlabel('PCs', fontsize=12, fontname='sans-serif')
    plt.ylabel('Proportion of variance (%)', fontsize=12, fontname='sans-serif')
    plt.xticks(fontsize=7, rotation=70)
    plt.savefig('screeplot.png', format='png', bbox_inches='tight', dpi=300)
    plt.close()


def pcaplot(x='x', y='y', z='z', labels='d_cols', var1='var1', var2='var2', var3='var3'):
    for i, varnames in enumerate(labels):
        plt.scatter(x[i], y[i])
        plt.text((x[i]), (y[i]), varnames, fontsize=10)

    plt.xlabel(('PC1 ({}%)'.format(var1)), fontsize=12, fontname='sans-serif')
    plt.ylabel(('PC2 ({}%)'.format(var2)), fontsize=12, fontname='sans-serif')
    plt.tight_layout()
    plt.savefig('pcaplot_2d.png', format='png', bbox_inches='tight', dpi=300)
    plt.close()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i, varnames in enumerate(labels):
        ax.scatter(x[i], y[i], z[i])
        ax.text((x[i]), (y[i]), (z[i]), varnames, fontsize=10)

    ax.set_xlabel(('PC1 ({}%)'.format(var1)), fontsize=12, fontname='sans-serif')
    ax.set_ylabel(('PC2 ({}%)'.format(var2)), fontsize=12, fontname='sans-serif')
    ax.set_zlabel(('PC3 ({}%)'.format(var3)), fontsize=12, fontname='sans-serif')
    plt.tight_layout()
    plt.savefig('pcaplot_3d.png', format='png', bbox_inches='tight', dpi=300)
    plt.close()


def hmap(table='dataset_file', cmap='seismic', scale=True, dim=(4, 6), clus=True, zscore=None, xlabel=True, ylabel=True, tickfont=(10, 10)):
    general.depr_mes('bioinfokit.visuz.gene_exp.hmap')


def venn(vennset=(1, 1, 1, 1, 1, 1, 1), venncolor=('#00909e', '#f67280', '#ff971d'), vennalpha=0.5, vennlabel=('A', 'B', 'C')):
    fig = plt.figure()
    if len(vennset) == 7:
        venn3(subsets=vennset, set_labels=vennlabel, set_colors=venncolor, alpha=vennalpha)
        plt.savefig('venn3.png', format='png', bbox_inches='tight', dpi=300)
    else:
        if len(vennset) == 3:
            venn2(subsets=vennset, set_labels=vennlabel, set_colors=venncolor, alpha=vennalpha)
            plt.savefig('venn2.png', format='png', bbox_inches='tight', dpi=300)
        else:
            print('Error: check the set dataset')


class gene_exp:

    def __init__(self):
        pass

    def geneplot(d, geneid, lfc, lfc_thr, pv_thr, genenames, gfont, pv, gstyle):
        if genenames is not None and genenames == 'deg':
            for i in d[geneid].unique():
                if not d.loc[(d[geneid] == i, lfc)].iloc[0] >= lfc_thr or d.loc[(d[geneid] == i, pv)].iloc[0] < pv_thr or d.loc[(d[geneid] == i, lfc)].iloc[0] <= -lfc_thr and d.loc[(d[geneid] == i, pv)].iloc[0] < pv_thr:
                    if gstyle == 1:
                        plt.text((d.loc[(d[geneid] == i, lfc)].iloc[0]), (d.loc[(d[geneid] == i, 'logpv')].iloc[0]), i, fontsize=gfont)
                    elif gstyle == 2:
                        plt.annotate(i, xy=(d.loc[(d[geneid] == i, lfc)].iloc[0], d.loc[(d[geneid] == i, 'logpv')].iloc[0]), xycoords='data',
                          xytext=(5, -15),
                          textcoords='offset points',
                          size=6,
                          bbox=dict(boxstyle='round', alpha=0.1),
                          arrowprops=dict(arrowstyle='wedge,tail_width=0.5', alpha=0.1, relpos=(0,
                                                                                                0)))
                    else:
                        print('Error: invalid gstyle choice')
                        sys.exit(1)

        else:
            if genenames is not None and type(genenames) is tuple:
                for i in d[geneid].unique():
                    if i in genenames:
                        if gstyle == 1:
                            plt.text((d.loc[(d[geneid] == i, lfc)].iloc[0]), (d.loc[(d[geneid] == i, 'logpv')].iloc[0]), i, fontsize=gfont)
                        elif gstyle == 2:
                            plt.annotate(i, xy=(d.loc[(d[geneid] == i, lfc)].iloc[0], d.loc[(d[geneid] == i, 'logpv')].iloc[0]), xycoords='data',
                              xytext=(5, -15),
                              textcoords='offset points',
                              size=6,
                              bbox=dict(boxstyle='round', alpha=0.1),
                              arrowprops=dict(arrowstyle='wedge,tail_width=0.5', alpha=0.1, relpos=(0,
                                                                                                    0)))
                        else:
                            print('Error: invalid gstyle choice')
                            sys.exit(1)

            else:
                if genenames is not None:
                    if type(genenames) is dict:
                        for i in d[geneid].unique():
                            if i in genenames:
                                if gstyle == 1:
                                    plt.text((d.loc[(d[geneid] == i, lfc)].iloc[0]), (d.loc[(d[geneid] == i, 'logpv')].iloc[0]), (genenames[i]),
                                      fontsize=gfont)
                                elif gstyle == 2:
                                    plt.annotate((genenames[i]), xy=(d.loc[(d[geneid] == i, lfc)].iloc[0], d.loc[(d[geneid] == i, 'logpv')].iloc[0]), xycoords='data',
                                      xytext=(5, -15),
                                      textcoords='offset points',
                                      size=6,
                                      bbox=dict(boxstyle='round', alpha=0.1),
                                      arrowprops=dict(arrowstyle='wedge,tail_width=0.5', alpha=0.1, relpos=(0,
                                                                                                            0)))
                                else:
                                    print('Error: invalid gstyle choice')
                                    sys.exit(1)

    def volcano(d='dataframe', lfc=None, pv=None, lfc_thr=1, pv_thr=0.05, color=('green', 'red'), valpha=1, geneid=None, genenames=None, gfont=8, dim=(5, 5), r=300, ar=90, dotsize=8, markerdot='o', sign_line=False, gstyle=1, show=False, figtype='png', axtickfontsize=9, axtickfontname='Arial', axlabelfontsize=9, axlabelfontname='Arial', axxlabel=None, axylabel=None, xlm=None, ylm=None):
        _x = '$ log_{2}(Fold Change)$'
        _y = '$ -log_{10}(P-value)$'
        color = color
        d.loc[((d[lfc] >= lfc_thr) & (d[pv] < pv_thr), 'color')] = color[0]
        d.loc[((d[lfc] <= -lfc_thr) & (d[pv] < pv_thr), 'color')] = color[1]
        d['color'].fillna('grey', inplace=True)
        d['logpv'] = -np.log10(d[pv])
        plt.subplots(figsize=dim)
        plt.scatter((d[lfc]), (d['logpv']), c=(d['color']), alpha=valpha, s=dotsize, marker=markerdot)
        if sign_line:
            plt.axhline(y=(-np.log10(pv_thr)), linestyle='--', color='#7d7d7d', linewidth=1)
            plt.axvline(x=lfc_thr, linestyle='--', color='#7d7d7d', linewidth=1)
            plt.axvline(x=(-lfc_thr), linestyle='--', color='#7d7d7d', linewidth=1)
        gene_exp.geneplot(d, geneid, lfc, lfc_thr, pv_thr, genenames, gfont, pv, gstyle)
        if axxlabel:
            _x = axxlabel
        if axylabel:
            _y = axylabel
        general.axis_labels(_x, _y, axlabelfontsize, axlabelfontname)
        general.axis_ticks(xlm, ylm, axtickfontsize, axtickfontname, ar)
        general.get_figure(show, r, figtype, 'volcano')

    def involcano(d='dataframe', lfc='logFC', pv='p_values', lfc_thr=1, pv_thr=0.05, color=('green', 'red'), valpha=1, geneid=None, genenames=None, gfont=8, dim=(5, 5), r=300, ar=90, dotsize=8, markerdot='o', sign_line=False, gstyle=1, show=False, figtype='png', axtickfontsize=9, axtickfontname='Arial', axlabelfontsize=9, axlabelfontname='Arial', axxlabel=None, axylabel=None, xlm=None, ylm=None):
        _x = '$ log_{2}(Fold Change)$'
        _y = '$ -log_{10}(P-value)$'
        color = color
        d.loc[((d[lfc] >= lfc_thr) & (d[pv] < pv_thr), 'color')] = color[0]
        d.loc[((d[lfc] <= -lfc_thr) & (d[pv] < pv_thr), 'color')] = color[1]
        d['color'].fillna('grey', inplace=True)
        d['logpv'] = -np.log10(d[pv])
        plt.subplots(figsize=dim)
        plt.scatter((d[lfc]), (d['logpv']), c=(d['color']), alpha=valpha, s=dotsize, marker=markerdot)
        gene_exp.geneplot(d, geneid, lfc, lfc_thr, pv_thr, genenames, gfont, pv, gstyle)
        plt.gca().invert_yaxis()
        if axxlabel:
            _x = axxlabel
        if axylabel:
            _y = axylabel
        general.axis_labels(_x, _y, axlabelfontsize, axlabelfontname)
        if xlm:
            print('Error: xlm not compatible with involcano')
            sys.exit(1)
        if ylm:
            print('Error: ylm not compatible with involcano')
            sys.exit(1)
        general.axis_ticks(xlm, ylm, axtickfontsize, axtickfontname, ar)
        general.get_figure(show, r, figtype, 'involcano')

    def ma(df='dataframe', lfc='logFC', ct_count='value1', st_count='value2', lfc_thr=1, valpha=1, dotsize=8, markerdot='o', dim=(6, 5), r=300, show=False, color=('green', 'red'), ar=90, figtype='png', axtickfontsize=9, axtickfontname='Arial', axlabelfontsize=9, axlabelfontname='Arial', axxlabel=None, axylabel=None, xlm=None, ylm=None):
        _x, _y = ('A', 'M')
        df.loc[(df[lfc] >= lfc_thr, 'color')] = color[0]
        df.loc[(df[lfc] <= -lfc_thr, 'color')] = color[1]
        df['color'].fillna('grey', inplace=True)
        df['A'] = np.log2((df[ct_count] + df[st_count]) / 2)
        plt.subplots(figsize=dim)
        plt.scatter((df['A']), (df[lfc]), c=(df['color']), alpha=valpha, s=dotsize, marker=markerdot)
        plt.axhline(y=0, color='#7d7d7d', linestyle='--')
        if axxlabel:
            _x = axxlabel
        if axylabel:
            _y = axylabel
        general.axis_labels(_x, _y, axlabelfontsize, axlabelfontname)
        general.axis_ticks(xlm, ylm, axtickfontsize, axtickfontname, ar)
        general.get_figure(show, r, figtype, 'ma')

    def hmap(df='dataframe', cmap='seismic', scale=True, dim=(4, 6), clus=True, zscore=None, xlabel=True, ylabel=True, tickfont=(10, 10), r=300, show=False, figtype='png'):
        fig, hm = plt.subplots(figsize=dim)
        if clus:
            hm = sns.clustermap(df, cmap=cmap, cbar=scale, z_score=zscore, xticklabels=xlabel, yticklabels=ylabel, figsize=dim)
            hm.ax_heatmap.set_xticklabels((hm.ax_heatmap.get_xmajorticklabels()), fontsize=(tickfont[0]))
            hm.ax_heatmap.set_yticklabels((hm.ax_heatmap.get_ymajorticklabels()), fontsize=(tickfont[1]))
            general.get_figure(show, r, figtype, 'heatmap')
        else:
            hm = sns.heatmap(df, cmap=cmap, cbar=scale, xticklabels=xlabel, yticklabels=ylabel)
            plt.xticks(fontsize=(tickfont[0]))
            plt.yticks(fontsize=(tickfont[1]))
            general.get_figure(show, r, figtype, 'heatmap')


class general:

    def __init__(self):
        pass

    rand_colors = ('#a7414a', '#282726', '#6a8a82', '#a37c27', '#563838', '#0584f2',
                   '#f28a30', '#f05837', '#6465a5', '#00743f', '#be9063', '#de8cf0',
                   '#888c46', '#c0334d', '#270101', '#8d2f23', '#ee6c81', '#65734b',
                   '#14325c', '#704307', '#b5b3be', '#f67280', '#ffd082', '#ffd800',
                   '#ad62aa', '#21bf73', '#a0855b', '#5edfff', '#08ffc8', '#ca3e47',
                   '#c9753d', '#6c5ce7')

    def get_figure(show, r, figtype, fig_name):
        if show:
            plt.show()
        else:
            plt.savefig((fig_name + '.' + figtype), format=figtype, bbox_inches='tight', dpi=r)
        plt.close()

    def axis_labels(x, y, axlabelfontsize=None, axlabelfontname=None):
        plt.xlabel(x, fontsize=axlabelfontsize, fontname=axlabelfontname)
        plt.ylabel(y, fontsize=axlabelfontsize, fontname=axlabelfontname)

    def axis_ticks(xlm=None, ylm=None, axtickfontsize=None, axtickfontname=None, ar=None):
        if xlm:
            plt.xlim(left=(xlm[0]), right=(xlm[1]))
            plt.xticks((np.arange(xlm[0], xlm[1], xlm[2])), fontsize=axtickfontsize, rotation=ar, fontname=axtickfontname)
        else:
            plt.xticks(fontsize=axtickfontsize, rotation=ar, fontname=axtickfontname)
        if ylm:
            plt.ylim(bottom=(ylm[0]), top=(ylm[1]))
            plt.yticks((np.arange(ylm[0], ylm[1], ylm[2])), fontsize=axtickfontsize, rotation=ar, fontname=axtickfontname)
        else:
            plt.yticks(fontsize=axtickfontsize, rotation=ar, fontname=axtickfontname)

    def depr_mes(func_name):
        print('This function is deprecated. Please use', func_name)
        print('Read docs at https://reneshbedre.github.io/blog/howtoinstall.html')


class marker:

    def geneplot_mhat--- This code section failed: ---

 L. 272         0  LOAD_FAST                'markeridcol'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
              6_8  POP_JUMP_IF_FALSE   400  'to 400'

 L. 273        10  LOAD_FAST                'markernames'
               12  LOAD_CONST               None
               14  COMPARE_OP               is-not
               16  POP_JUMP_IF_FALSE   152  'to 152'
               18  LOAD_FAST                'markernames'
               20  LOAD_CONST               True
               22  COMPARE_OP               is
               24  POP_JUMP_IF_FALSE   152  'to 152'

 L. 274        26  SETUP_LOOP          150  'to 150'
               28  LOAD_FAST                'df'
               30  LOAD_FAST                'markeridcol'
               32  BINARY_SUBSCR    
               34  LOAD_METHOD              unique
               36  CALL_METHOD_0         0  '0 positional arguments'
               38  GET_ITER         
             40_0  COME_FROM            74  '74'
               40  FOR_ITER            148  'to 148'
               42  STORE_FAST               'i'

 L. 275        44  LOAD_FAST                'df'
               46  LOAD_ATTR                loc
               48  LOAD_FAST                'df'
               50  LOAD_FAST                'markeridcol'
               52  BINARY_SUBSCR    
               54  LOAD_FAST                'i'
               56  COMPARE_OP               ==
               58  LOAD_FAST                'pv'
               60  BUILD_TUPLE_2         2 
               62  BINARY_SUBSCR    
               64  LOAD_ATTR                iloc
               66  LOAD_CONST               0
               68  BINARY_SUBSCR    
               70  LOAD_FAST                'gwasp'
               72  COMPARE_OP               <=
               74  POP_JUMP_IF_FALSE    40  'to 40'

 L. 276        76  LOAD_GLOBAL              plt
               78  LOAD_ATTR                text
               80  LOAD_FAST                'df'
               82  LOAD_ATTR                loc
               84  LOAD_FAST                'df'
               86  LOAD_FAST                'markeridcol'
               88  BINARY_SUBSCR    
               90  LOAD_FAST                'i'
               92  COMPARE_OP               ==
               94  LOAD_STR                 'ind'
               96  BUILD_TUPLE_2         2 
               98  BINARY_SUBSCR    
              100  LOAD_ATTR                iloc
              102  LOAD_CONST               0
              104  BINARY_SUBSCR    
              106  LOAD_FAST                'df'
              108  LOAD_ATTR                loc
              110  LOAD_FAST                'df'
              112  LOAD_FAST                'markeridcol'
              114  BINARY_SUBSCR    
              116  LOAD_FAST                'i'
              118  COMPARE_OP               ==
              120  LOAD_STR                 'tpval'
              122  BUILD_TUPLE_2         2 
              124  BINARY_SUBSCR    
              126  LOAD_ATTR                iloc
              128  LOAD_CONST               0
              130  BINARY_SUBSCR    

 L. 277       132  LOAD_GLOBAL              str
              134  LOAD_FAST                'i'
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  LOAD_FAST                'gfont'
              140  LOAD_CONST               ('fontsize',)
              142  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              144  POP_TOP          
              146  JUMP_BACK            40  'to 40'
              148  POP_BLOCK        
            150_0  COME_FROM_LOOP       26  '26'
              150  JUMP_FORWARD        398  'to 398'
            152_0  COME_FROM            24  '24'
            152_1  COME_FROM            16  '16'

 L. 278       152  LOAD_FAST                'markernames'
              154  LOAD_CONST               None
              156  COMPARE_OP               is-not
          158_160  POP_JUMP_IF_FALSE   270  'to 270'
              162  LOAD_GLOBAL              type
              164  LOAD_FAST                'markernames'
              166  CALL_FUNCTION_1       1  '1 positional argument'
              168  LOAD_GLOBAL              tuple
              170  COMPARE_OP               is
          172_174  POP_JUMP_IF_FALSE   270  'to 270'

 L. 279       176  SETUP_LOOP          398  'to 398'
              178  LOAD_FAST                'df'
              180  LOAD_FAST                'markeridcol'
              182  BINARY_SUBSCR    
              184  LOAD_METHOD              unique
              186  CALL_METHOD_0         0  '0 positional arguments'
              188  GET_ITER         
              190  FOR_ITER            266  'to 266'
              192  STORE_FAST               'i'

 L. 280       194  LOAD_GLOBAL              plt
              196  LOAD_ATTR                text
              198  LOAD_FAST                'df'
              200  LOAD_ATTR                loc
              202  LOAD_FAST                'df'
              204  LOAD_FAST                'markeridcol'
              206  BINARY_SUBSCR    
              208  LOAD_FAST                'i'
              210  COMPARE_OP               ==
              212  LOAD_STR                 'ind'
              214  BUILD_TUPLE_2         2 
              216  BINARY_SUBSCR    
              218  LOAD_ATTR                iloc
              220  LOAD_CONST               0
              222  BINARY_SUBSCR    
              224  LOAD_FAST                'df'
              226  LOAD_ATTR                loc
              228  LOAD_FAST                'df'
              230  LOAD_FAST                'markeridcol'
              232  BINARY_SUBSCR    
              234  LOAD_FAST                'i'
              236  COMPARE_OP               ==
              238  LOAD_STR                 'tpval'
              240  BUILD_TUPLE_2         2 
              242  BINARY_SUBSCR    
              244  LOAD_ATTR                iloc
              246  LOAD_CONST               0
              248  BINARY_SUBSCR    

 L. 281       250  LOAD_GLOBAL              str
              252  LOAD_FAST                'i'
              254  CALL_FUNCTION_1       1  '1 positional argument'
              256  LOAD_FAST                'gfont'
              258  LOAD_CONST               ('fontsize',)
              260  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              262  POP_TOP          
              264  JUMP_BACK           190  'to 190'
              266  POP_BLOCK        
              268  JUMP_FORWARD        398  'to 398'
            270_0  COME_FROM           172  '172'
            270_1  COME_FROM           158  '158'

 L. 282       270  LOAD_FAST                'markernames'
              272  LOAD_CONST               None
              274  COMPARE_OP               is-not
          276_278  POP_JUMP_IF_FALSE   418  'to 418'
              280  LOAD_GLOBAL              type
              282  LOAD_FAST                'markernames'
              284  CALL_FUNCTION_1       1  '1 positional argument'
              286  LOAD_GLOBAL              dict
              288  COMPARE_OP               is
          290_292  POP_JUMP_IF_FALSE   418  'to 418'

 L. 283       294  SETUP_LOOP          418  'to 418'
              296  LOAD_FAST                'df'
              298  LOAD_FAST                'markeridcol'
              300  BINARY_SUBSCR    
              302  LOAD_METHOD              unique
              304  CALL_METHOD_0         0  '0 positional arguments'
              306  GET_ITER         
            308_0  COME_FROM           318  '318'
              308  FOR_ITER            396  'to 396'
              310  STORE_FAST               'i'

 L. 284       312  LOAD_FAST                'i'
              314  LOAD_FAST                'markernames'
              316  COMPARE_OP               in
          318_320  POP_JUMP_IF_FALSE   308  'to 308'

 L. 285       322  LOAD_GLOBAL              plt
              324  LOAD_ATTR                text
              326  LOAD_FAST                'df'
              328  LOAD_ATTR                loc
              330  LOAD_FAST                'df'
              332  LOAD_FAST                'markeridcol'
              334  BINARY_SUBSCR    
              336  LOAD_FAST                'i'
              338  COMPARE_OP               ==
              340  LOAD_STR                 'ind'
              342  BUILD_TUPLE_2         2 
              344  BINARY_SUBSCR    
              346  LOAD_ATTR                iloc
              348  LOAD_CONST               0
              350  BINARY_SUBSCR    
              352  LOAD_FAST                'df'
              354  LOAD_ATTR                loc
              356  LOAD_FAST                'df'
              358  LOAD_FAST                'markeridcol'
              360  BINARY_SUBSCR    
              362  LOAD_FAST                'i'
              364  COMPARE_OP               ==
              366  LOAD_STR                 'tpval'
              368  BUILD_TUPLE_2         2 
              370  BINARY_SUBSCR    
              372  LOAD_ATTR                iloc
              374  LOAD_CONST               0
              376  BINARY_SUBSCR    

 L. 286       378  LOAD_FAST                'markernames'
              380  LOAD_FAST                'i'
              382  BINARY_SUBSCR    
              384  LOAD_FAST                'gfont'
              386  LOAD_CONST               ('fontsize',)
              388  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              390  POP_TOP          
          392_394  JUMP_BACK           308  'to 308'
              396  POP_BLOCK        
            398_0  COME_FROM_LOOP      294  '294'
            398_1  COME_FROM           268  '268'
            398_2  COME_FROM_LOOP      176  '176'
            398_3  COME_FROM           150  '150'
              398  JUMP_FORWARD        418  'to 418'
            400_0  COME_FROM             6  '6'

 L. 288       400  LOAD_GLOBAL              print
              402  LOAD_STR                 "Error: provide 'markeridcol' parameter"
              404  CALL_FUNCTION_1       1  '1 positional argument'
              406  POP_TOP          

 L. 289       408  LOAD_GLOBAL              sys
              410  LOAD_METHOD              exit
              412  LOAD_CONST               1
              414  CALL_METHOD_1         1  '1 positional argument'
              416  POP_TOP          
            418_0  COME_FROM           398  '398'
            418_1  COME_FROM           290  '290'
            418_2  COME_FROM           276  '276'

Parse error at or near `JUMP_FORWARD' instruction at offset 398

    def mhat(df='dataframe', chr=None, pv=None, color=None, dim=(6, 4), r=300, ar=90, gwas_sign_line=False, gwasp=5e-08, dotsize=8, markeridcol=None, markernames=None, gfont=8, valpha=1, show=False, figtype='png', axxlabel=None, axylabel=None, axlabelfontsize=9, axlabelfontname='Arial', axtickfontsize=9, axtickfontname='Arial', ylm=None):
        _x, _y = ('Chromosomes', '$ -log_{10}(P)$')
        rand_colors = ('#a7414a', '#282726', '#6a8a82', '#a37c27', '#563838', '#0584f2',
                       '#f28a30', '#f05837', '#6465a5', '#00743f', '#be9063', '#de8cf0',
                       '#888c46', '#c0334d', '#270101', '#8d2f23', '#ee6c81', '#65734b',
                       '#14325c', '#704307', '#b5b3be', '#f67280', '#ffd082', '#ffd800',
                       '#ad62aa', '#21bf73', '#a0855b', '#5edfff', '#08ffc8', '#ca3e47',
                       '#c9753d', '#6c5ce7')
        df['tpval'] = -np.log10(df[pv])
        df = df.sort_values(chr)
        df['ind'] = range(len(df))
        df_group = df.groupby(chr)
        if color is not None:
            if len(color) == 2:
                color_1 = int(df[chr].nunique() / 2) * [color[0]]
                color_2 = int(df[chr].nunique() / 2) * [color[1]]
                if df[chr].nunique() % 2 == 0:
                    color_list = list(reduce(lambda x, y: x + y, zip(color_1, color_2)))
            elif df[chr].nunique() % 2 == 1:
                color_list = list(reduce(lambda x, y: x + y, zip(color_1, color_2)))
                color_list.append(color[0])
        else:
            if color is not None:
                if len(color) == df[chr].nunique():
                    color_list = color
                else:
                    if color is None:
                        color_list = sample(rand_colors, df[chr].nunique())
                    else:
                        print('Error: in color argument')
                        sys.exit(1)
            else:
                xlabels = []
                xticks = []
                fig, ax = plt.subplots(figsize=dim)
                i = 0
                for label, df1 in df.groupby(chr):
                    df1.plot(kind='scatter', x='ind', y='tpval', color=(color_list[i]), s=dotsize, alpha=valpha, ax=ax)
                    df1_max_ind = df1['ind'].iloc[(-1)]
                    df1_min_ind = df1['ind'].iloc[0]
                    xlabels.append(label)
                    xticks.append(df1_max_ind - (df1_max_ind - df1_min_ind) / 2)
                    i += 1

                if gwas_sign_line is True:
                    ax.axhline(y=(-np.log10(gwasp)), linestyle='--', color='#7d7d7d', linewidth=1)
                if markernames is not None:
                    marker.geneplot_mhat(df, markeridcol, chr, pv, gwasp, markernames, gfont, ax=ax)
                ax.margins(x=0)
                ax.margins(y=0)
                ax.set_xticks(xticks)
                ax.set_ylim([0, max(df['tpval'] + 1)])
                if ylm:
                    ylm = np.arange(ylm[0], ylm[1], ylm[2])
                else:
                    ylm = np.arange(0, max(df['tpval'] + 1), 1)
            ax.set_yticks(ylm)
            ax.set_xticklabels(xlabels, rotation=ar)
            if axxlabel:
                _x = axxlabel
            if axylabel:
                _y = axylabel
            ax.set_xlabel(_x, fontsize=axlabelfontsize, fontname=axlabelfontname)
            ax.set_ylabel(_y, fontsize=axlabelfontsize, fontname=axlabelfontname)
            general.get_figure(show, r, figtype, 'manhatten')


class stat:

    def __init__(self):
        pass

    def bardot(df='dataframe', dim=(6, 4), bw=0.4, colorbar='#f2aa4cff', colordot=['#101820ff'], hbsize=4, r=300, ar=0, dotsize=6, valphabar=1, valphadot=1, markerdot='o', errorbar=True, show=False, ylm=None, axtickfontsize=9, axtickfontname='Arial', axlabelfontsize=9, axlabelfontname='Arial', yerrlw=None, yerrcw=None, axxlabel=None, axylabel=None, figtype='png'):
        _x = None
        _y = None
        xbar = np.arange(len(df.columns.to_numpy()))
        color_list_bar = colorbar
        color_list_dot = colordot
        if len(color_list_dot) == 1:
            color_list_dot = colordot * len(df.columns.to_numpy())
        else:
            plt.subplots(figsize=dim)
            if errorbar:
                plt.bar(x=xbar, height=(df.describe().loc['mean']), yerr=(df.sem()), width=bw, color=color_list_bar, capsize=hbsize, zorder=0,
                  alpha=valphabar,
                  error_kw={'elinewidth':yerrlw,  'capthick':yerrcw})
            else:
                plt.bar(x=xbar, height=(df.describe().loc['mean']), width=bw, color=color_list_bar, capsize=hbsize,
                  zorder=0,
                  alpha=valphabar)
        plt.xticks(xbar, (df.columns.to_numpy()), fontsize=axtickfontsize, rotation=ar, fontname=axtickfontname)
        if axxlabel:
            _x = axxlabel
        if axylabel:
            _y = axylabel
        general.axis_labels(_x, _y, axlabelfontsize, axlabelfontname)
        if ylm:
            plt.ylim(bottom=(ylm[0]), top=(ylm[1]))
            plt.yticks((np.arange(ylm[0], ylm[1], ylm[2])), fontsize=axtickfontsize, fontname=axtickfontname)
        plt.yticks(fontsize=axtickfontsize, rotation=ar, fontname=axtickfontname)
        for cols in range(len(df.columns.to_numpy())):
            plt.scatter(x=(np.linspace(xbar[cols] - bw / 2, xbar[cols] + bw / 2, int(df.describe().loc['count'][cols]))), y=(df[df.columns[cols]]),
              s=dotsize,
              color=(color_list_dot[cols]),
              zorder=1,
              alpha=valphadot,
              marker=markerdot)

        general.get_figure(show, r, figtype, 'bardot')

    def regplot(df='dataframe', x=None, y=None, yhat=None, dim=(6, 4), colordot='#4a4e4d', colorline='#fe8a71', r=300, ar=0, dotsize=6, valphaline=1, valphadot=1, linewidth=1, markerdot='o', show=False, axtickfontsize=9, axtickfontname='Arial', axlabelfontsize=9, axlabelfontname='Arial', ylm=None, xlm=None, axxlabel=None, axylabel=None, figtype='png'):
        fig, ax = plt.subplots(figsize=dim)
        plt.scatter((df[x].to_numpy()), (df[y].to_numpy()), color=colordot, s=dotsize, alpha=valphadot, marker=markerdot, label='Observed data')
        plt.plot((df[x].to_numpy()), (df[yhat].to_numpy()), color=colorline, linewidth=linewidth, alpha=valphaline, label='Regression line')
        if axxlabel:
            x = axxlabel
        if axylabel:
            y = axylabel
        general.axis_labels(x, y, axlabelfontsize, axlabelfontname)
        general.axis_ticks(xlm, ylm, axtickfontsize, axtickfontname, ar)
        plt.legend(fontsize=9)
        general.get_figure(show, r, figtype, 'reg_plot')

    def reg_resid_plot(df='dataframe', yhat=None, resid=None, stdresid=None, dim=(6, 4), colordot='#4a4e4d', colorline='#2ab7ca', r=300, ar=0, dotsize=6, valphaline=1, valphadot=1, linewidth=1, markerdot='o', show=False, figtype='png'):
        fig, ax = plt.subplots(figsize=dim)
        if resid is not None:
            plt.scatter((df[yhat]), (df[resid]), color=colordot, s=dotsize, alpha=valphadot, marker=markerdot)
            plt.axhline(y=0, color=colorline, linestyle='--', linewidth=linewidth, alpha=valphaline)
            plt.xlabel('Fitted')
            plt.ylabel('Residuals')
            general.get_figure(show, r, figtype, 'resid_plot')
        else:
            print('Error: Provide residual data')
        if stdresid is not None:
            plt.scatter((df[yhat]), (df[stdresid]), color=colordot, s=dotsize, alpha=valphadot, marker=markerdot)
            plt.axhline(y=0, color=colorline, linestyle='--', linewidth=linewidth, alpha=valphaline)
            plt.xlabel('Fitted')
            plt.ylabel('Standardized Residuals')
            general.get_figure(show, r, figtype, 'std_resid_plot')
        else:
            print('Error: Provide standardized residual data')

    def corr_mat(df='dataframe', corm='pearson', cmap='seismic', r=300, show=False, dim=(6, 5), axtickfontname='Arial', axtickfontsize=7, ar=90, figtype='png'):
        d_corr = df.corr(method=corm)
        plt.subplots(figsize=dim)
        plt.matshow(d_corr, vmin=(-1), vmax=1, cmap=cmap)
        plt.colorbar()
        cols = list(df)
        ticks = list(range(0, len(list(df))))
        plt.xticks(ticks, cols, fontsize=axtickfontsize, fontname=axtickfontname, rotation=ar)
        plt.yticks(ticks, cols, fontsize=axtickfontsize, fontname=axtickfontname)
        general.get_figure(show, r, figtype, 'corr_mat')