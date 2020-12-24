# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/scicast/R_qgraph.py
# Compiled at: 2016-12-05 19:38:56
import os, pandas as pd
from collections import defaultdict
import warnings

def run_qgraph(args, matrix_data, gene_or_cell, minimum=0.25, cut=0.4, vsize=1.5, legend=True, borders=False):
    if not args.verbose:
        warnings.filterwarnings('ignore', category=RuntimeWarning)
    path_filename = matrix_data.new_filepath
    label_map = matrix_data.cell_label_map
    gene_map = matrix_data.gene_label_map
    if isinstance(matrix_data.log2_df_cell_gene_restricted, pd.DataFrame):
        cell_list = matrix_data.cell_list
        data = matrix_data.log2_df_cell_gene_restricted
        cell_list_all = cell_list
    else:
        data = matrix_data.log2_df_cell
        cell_list_all = data.columns.tolist()
    from rpy2.robjects import pandas2ri
    pandas2ri.activate()
    import rpy2.robjects as robjects
    from rpy2.robjects.packages import importr
    robjects.r.setwd(os.path.dirname(path_filename))
    qgraph = importr('qgraph')
    psych = importr('psych')
    if gene_or_cell == 'cell':
        r_dataframe = pandas2ri.py2ri(data)
        d = defaultdict(list)
        for i, cell in enumerate(cell_list_all):
            group = label_map[cell][0][2]
            d[group].append(i + 1)

        label_list = robjects.vectors.StrVector(cell_list_all)
    else:
        if gene_or_cell == 'gene':
            r_dataframe = pandas2ri.py2ri(data.transpose())
            d = defaultdict(list)
            d_color = []
            gene_list_all = data.transpose().columns.tolist()
            for i, gene in enumerate(gene_list_all):
                group = gene_map[gene][2]
                color = gene_map[gene][0]
                d[group].append(i + 1)

            label_list = robjects.vectors.StrVector(gene_list_all)
        group_num = len(d)
        from rpy2.robjects.vectors import FloatVector
        for colname in d:
            d[colname] = FloatVector(d[colname])

    from rpy2.robjects.vectors import ListVector
    group_data = ListVector(d)
    pca = psych.principal(robjects.r.cor(r_dataframe), group_num, rotate='promax')
    robjects.r.setwd(path_filename)
    qpca = qgraph.qgraph(pca, groups=group_data, layout='circle', rotation='promax', minimum=0.2, cut=0.4, vsize=FloatVector([1.5, 15]), labels=label_list, borders=False, vTrans=200, filename='graph_pca_' + gene_or_cell, filetype='pdf', height=15, width=15)
    if gene_or_cell == 'gene':
        Q = qgraph.qgraph(robjects.r.cor(r_dataframe), minimum=0.25, cut=0.4, vsize=1.5, groups=group_data, legend=True, borders=False, labels=label_list, filename='graph_' + gene_or_cell, filetype='pdf', height=15, width=15)
    elif gene_or_cell == 'cell':
        Q = qgraph.qgraph(robjects.r.cor(r_dataframe), minimum=0.25, cut=0.4, vsize=1.5, groups=group_data, legend=True, borders=False, labels=label_list, filename='graph_' + gene_or_cell, filetype='pdf', height=15, width=15)
    Q = qgraph.qgraph(Q, layout='spring', overlay=True)
    robjects.r.setwd(os.path.dirname(path_filename))