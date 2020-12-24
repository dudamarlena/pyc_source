# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/scicast/correlation.py
# Compiled at: 2017-01-19 15:15:02
import numpy as np, pandas as pd, os, matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator
import seaborn as sns
from operator import itemgetter
import matplotlib.ticker as ticker, math, matplotlib.patches as patches

def run_corr(args, df_by_gene, title, path_filename, method_name='pearson', sig_threshold=0.5, min_period=3, save_corrs=False):
    try:
        from .dim_reduction import return_top_pca_gene
    except (SystemError, ValueError, ImportError):
        from dim_reduction import return_top_pca_gene

    if len(df_by_gene.columns.tolist()) > 5000:
        df_by_gene, top_pca_list = return_top_pca_gene(args, df_by_gene.transpose(), user_num_genes=5000)
    if method_name != 'kendall':
        corr_by_gene = df_by_gene.corr(method=method_name, min_periods=min_period)
    else:
        corr_by_gene = df_by_gene.corr(method=method_name)
    cor = corr_by_gene
    cor.loc[:, :] = np.tril(cor.values, k=-1)
    cor = cor.stack()
    corr_by_gene_pos = cor[(cor >= sig_threshold)]
    corr_by_gene_neg = cor[(cor <= sig_threshold * -1)]
    cor_pos_df = pd.DataFrame(corr_by_gene_pos)
    cor_neg_df = pd.DataFrame(corr_by_gene_neg)
    sig_corr = cor_pos_df.append(cor_neg_df)
    sig_corrs = pd.DataFrame(sig_corr[0], columns=['corr'])
    sig_corrs.to_csv(os.path.join(path_filename, title + '_counts_corr_sig_' + method_name + '.txt'), sep='\t')
    return sig_corrs


def find_top_corrs(terms_to_search, sig_corrs, num_to_return, gene_corr_list=[]):
    all_corrs_list = []
    best_corrs_list = []
    for term_to_search in terms_to_search:
        corr_tup = [
         (
          term_to_search, 1)]
        for index, row in sig_corrs.iterrows():
            if term_to_search in index:
                if index[0] == term_to_search:
                    corr_tup.append((index[1], row['corr']))
                else:
                    corr_tup.append((index[0], row['corr']))

        all_corrs_list.append(corr_tup)

    all_corrs_list.sort(key=len, reverse=True)
    good_count = 0
    len_count = 0
    corr_genes_seen = []
    while good_count <= num_to_return and len_count <= len(all_corrs_list):
        for i, corrs in enumerate(all_corrs_list):
            len_count += 1
            if corrs[0][0] not in corr_genes_seen:
                best_corrs_list.append(corrs)
                good_count += 1
            for g, c in corrs:
                if g not in corr_genes_seen and '-' not in str(c):
                    corr_genes_seen.append(g)

    if gene_corr_list != []:
        search_corrs = []
        for term in gene_corr_list:
            corr_tup = [
             (
              term, 1)]
            for index, row in sig_corrs.iterrows():
                if term in index:
                    if index[0] == term:
                        corr_tup.append((index[1], row['corr']))
                    else:
                        corr_tup.append((index[0], row['corr']))

            search_corrs.append(corr_tup)

        best_corrs_list = search_corrs + best_corrs_list
        return best_corrs_list[0:num_to_return + len(gene_corr_list) + 1]
    else:
        return best_corrs_list[0:num_to_return]


def corr_plot(terms_to_search, df_by_gene_corr, args, matrix_data, title='', sort=True, sig_threshold=0.5):
    path_filename = matrix_data.new_filepath
    if args.genes_corr != '':
        gene_corr_list = args.genes_corr.split(',')
    else:
        gene_corr_list = []
    size_cells = len(df_by_gene_corr.index.tolist())
    figlen = int(size_cells / 11)
    if figlen < 15:
        figlen = 15
    ncol = int(figlen / 3.2)
    if size_cells < 100:
        sig_threshold = -0.137 * math.log(size_cells) + 1.1322
    sig_corrs = run_corr(args, df_by_gene_corr, title, path_filename, sig_threshold=sig_threshold)
    corr_list = find_top_corrs(terms_to_search, sig_corrs, num_to_return=3, gene_corr_list=gene_corr_list)
    for corr_tup in corr_list:
        term_to_search = corr_tup[0][0]
        corr_tup.sort(key=itemgetter(1), reverse=True)
        corr_df = pd.DataFrame(corr_tup, columns=['GeneID', 'Correlation'])
        corr_df.to_csv(os.path.join(matrix_data.new_filepath, title + '_Corr_w_' + term_to_search + '_list.txt'), sep='\t', index=False)
        to_plot = [ x[0] for x in corr_tup ]
        sns.set_palette(sns.cubehelix_palette(len(to_plot), start=1, rot=-0.9, reverse=True))
        sns.set_context('notebook', font_scale=0.9, rc={'lines.linewidth': 1})
        try:
            sorted_df = df_by_gene_corr.sort_values(by=[term_to_search])
            ylabel = 'Counts (log2)'
            if sort:
                ax = sorted_df[to_plot].plot(figsize=(figlen, 10))
                xlabels = sorted_df[to_plot].index.values
            else:
                ax = df_by_gene_corr[to_plot].plot(figsize=(figlen, 10))
                xlabels = df_by_gene_corr[to_plot].index.values
            ax.set_xlabel('Cell Label')
            ax.set_ylabel(ylabel)
            ax.set_title('Correlates with ' + term_to_search, loc='right')
            ax.xaxis.set_minor_locator(LinearLocator(numticks=len(xlabels)))
            if matrix_data.cell_label_map:
                ax.set_xticklabels(xlabels, minor=True, rotation='vertical', fontsize=3)
                Xcolors = [ matrix_data.cell_label_map[cell][0][0] for cell in xlabels ]
                group_labels = [ matrix_data.cell_label_map[cell][0][2] for cell in xlabels ]
                group_seen = []
                leg_handles = []
                for xtick, xcolor, group_name in zip(ax.get_xticklabels(which='minor'), Xcolors, group_labels):
                    xtick.set_color(xcolor)
                    xtick.set_rotation(90)
                    if group_name not in group_seen:
                        leg_handles.append(patches.Patch(color=xcolor, label=group_name))
                        group_seen.append(group_name)

            else:
                ax.set_xticklabels(xlabels, minor=True, rotation='vertical', fontsize=3)
            ax.set_ylim([0, df_by_gene_corr[to_plot].values.max()])
            ax.xaxis.set_major_formatter(ticker.NullFormatter())
            ax.tick_params(axis='x', which='minor', labelsize=9)
            if len(corr_tup) > 1:
                bbox_height = float(1e-13) * pow(len(corr_tup), 6) - float(7e-11) * pow(len(corr_tup), 5) + float(1e-08) * pow(len(corr_tup), 4) - float(8e-07) * pow(len(corr_tup), 3) - float(3e-05) * pow(len(corr_tup), 2) + 0.0086 * len(corr_tup) + 1.0042
            else:
                bbox_height = 1.05
            l_labels = [ str(x[0]) + ' ' + '%.2f' % x[1] for x in corr_tup ]
            if matrix_data.cell_label_map:
                first_legend = ax.legend(l_labels, loc='upper left', bbox_to_anchor=(0.01, bbox_height + 0.1), ncol=ncol, prop={'size': 10})
                ax = plt.gca().add_artist(first_legend)
                plt.legend(handles=leg_handles, loc='upper right', bbox_to_anchor=(0.9, bbox_height + 0.1))
            else:
                ax.legend(l_labels, loc='upper left', bbox_to_anchor=(0.01, bbox_height), ncol=ncol, prop={'size': 10})
            fig = plt.gcf()
            fig.subplots_adjust(bottom=0.08, top=0.95, right=0.98, left=0.03)
            plt.savefig(os.path.join(path_filename, title + '_corr_with_' + term_to_search + '.' + args.image_format), bbox_inches='tight')
            plt.close('all')
        except KeyError:
            if args.verbose:
                print term_to_search + ' not in this matrix.'