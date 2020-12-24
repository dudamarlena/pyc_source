# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/bayesdb/pairwise.py
# Compiled at: 2015-02-12 15:25:14
import numpy, os, re, inspect, ast, pylab, matplotlib.cm, time, data_utils as du, select_utils, functions, utils, parser

def parse_pairwise_function(function_name, column=True, M_c=None, column_lists={}):
    if column:
        if function_name == 'mutual information':
            return functions._mutual_information
        if function_name == 'dependence probability':
            return functions._dependence_probability
        if function_name == 'correlation':
            return functions._correlation
        raise utils.BayesDBParseError('Invalid column function: %s' % function_name)
    else:
        p = parser.Parser()
        _, target_columns = p.get_args_similarity(function_name, M_c, None, M_c, None, column_lists)
        if target_columns is None:
            return (functions._similarity, None)
        if type(target_columns) == list:
            return (functions._similarity, target_columns)
        raise utils.BayesDBParseError('Invalid row function: %s' % function_name)
    return


def get_columns(column_names, M_c):
    if column_names is not None:
        column_indices = [ M_c['name_to_idx'][name] for name in column_names ]
    else:
        num_cols = len(M_c['name_to_idx'].keys())
        column_names = [ M_c['idx_to_name'][str(idx)] for idx in range(num_cols) ]
        column_indices = range(num_cols)
    column_names = numpy.array(column_names)
    return (column_names, column_indices)


def compute_raw_column_pairwise_matrix(function, X_L_list, X_D_list, M_c, T, engine, column_indices=None, numsamples=None):
    num_cols = len(column_indices)
    matrix = numpy.zeros((num_cols, num_cols))
    for i, orig_i in enumerate(column_indices):
        for j in range(i, num_cols):
            orig_j = column_indices[j]
            func_val = function((orig_i, orig_j), None, None, M_c, X_L_list, X_D_list, T, engine, numsamples)
            matrix[i][j] = func_val
            matrix[j][i] = func_val

    return matrix


def compute_raw_row_pairwise_matrix(function, arg, X_L_list, X_D_list, M_c, T, engine, row_indices=None, numsamples=None):
    if row_indices is None:
        row_indices = range(len(T))
    num_rows = len(row_indices)
    matrix = numpy.zeros((num_rows, num_rows))
    for i, orig_i in enumerate(row_indices):
        for j in range(i, num_rows):
            orig_j = row_indices[j]
            func_val = function((orig_i, arg), orig_j, None, M_c, X_L_list, X_D_list, T, engine, numsamples)
            matrix[i][j] = func_val
            matrix[j][i] = func_val

    return matrix


def reorder_indices_by_cluster(matrix):
    from scipy.spatial.distance import pdist
    from scipy.cluster.hierarchy import linkage, dendrogram
    Y = pdist(matrix)
    Z = linkage(Y)
    pylab.figure()
    dendrogram(Z)
    intify = lambda x: int(x.get_text())
    reorder_indices = map(intify, pylab.gca().get_xticklabels())
    pylab.clf()
    matrix_reordered = matrix[:, reorder_indices][reorder_indices, :]
    return (matrix_reordered, reorder_indices)


def get_connected_clusters(matrix, cluster_threshold):
    from collections import defaultdict
    clusters = []
    neighbors_dict = defaultdict(list)
    for i in range(matrix.shape[0]):
        for j in range(i + 1, matrix.shape[0]):
            if matrix[i][j] > cluster_threshold:
                neighbors_dict[i].append(j)
                neighbors_dict[j].append(i)

    unvisited = set(range(matrix.shape[0]))
    while len(unvisited) > 0:
        cluster = []
        stack = [
         unvisited.pop()]
        while len(stack) > 0:
            cur = stack.pop()
            cluster.append(cur)
            neighbors = neighbors_dict[cur]
            for n in neighbors:
                if n in unvisited:
                    stack.append(n)
                    unvisited.remove(n)

        if len(cluster) > 1:
            clusters.append(cluster)

    return clusters


def generate_pairwise_column_matrix(function_name, X_L_list, X_D_list, M_c, T, tablename='', limit=None, engine=None, column_names=None, cluster_threshold=None, numsamples=None):
    """
    Compute a matrix. In using a function that requires engine (currently only
    mutual information), engine must not be None.
    """
    function = parse_pairwise_function(function_name, column=True, M_c=M_c)
    column_names, column_indices = get_columns(column_names, M_c)
    matrix = compute_raw_column_pairwise_matrix(function, X_L_list, X_D_list, M_c, T, engine, column_indices, numsamples)
    if cluster_threshold is not None:
        clusters = get_connected_clusters(matrix, cluster_threshold)
        new_comps = []
        for comp in clusters:
            new_comps.append([ column_indices[c] for c in comp ])

        clusters = new_comps
    else:
        clusters = None
    matrix, reorder_indices = reorder_indices_by_cluster(matrix)
    column_names_reordered = column_names[reorder_indices]
    return (
     matrix, column_names_reordered, clusters)


def generate_pairwise_row_matrix(function_name, X_L_list, X_D_list, M_c, T, tablename='', engine=None, row_indices=None, cluster_threshold=None, column_lists={}, numsamples=None):
    """
    Compute a matrix. In using a function that requires engine (currently only
    mutual information), engine must not be None.
    """
    function, arg = parse_pairwise_function(function_name, column=False, M_c=M_c, column_lists=column_lists)
    if row_indices is None:
        row_indices = numpy.array(range(len(T)))
    else:
        row_indices = numpy.array(row_indices)
    matrix = compute_raw_row_pairwise_matrix(function, arg, X_L_list, X_D_list, M_c, T, engine, row_indices, numsamples)
    if cluster_threshold is not None:
        clusters = get_connected_clusters(matrix, cluster_threshold)
        new_comps = []
        for comp in clusters:
            new_comps.append([ row_indices[c] for c in comp ])

        clusters = new_comps
    else:
        clusters = None
    matrix, reorder_indices = reorder_indices_by_cluster(matrix)
    row_indices_reordered = row_indices[reorder_indices]
    return (
     matrix, row_indices_reordered, clusters)