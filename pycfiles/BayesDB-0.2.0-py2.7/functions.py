# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/bayesdb/functions.py
# Compiled at: 2015-02-12 15:25:14
import re, utils, numpy, os, pylab, matplotlib.cm, inspect, operator, ast, math
from scipy.stats import pearsonr, chi2_contingency, f_oneway
import utils, select_utils, data_utils as du

def _column(column_args, row_id, data_values, M_c, X_L_list, X_D_list, T, engine, numsamples):
    col_idx = column_args[0]
    confidence = column_args[1]
    if confidence is None or not numpy.isnan(T[row_id][col_idx]):
        return du.convert_code_to_value(M_c, col_idx, T[row_id][col_idx])
    else:
        Y = [ (row_id, cidx, T[row_id][cidx]) for cidx in M_c['name_to_idx'].values() if not numpy.isnan(T[row_id][cidx]) ]
        code = utils.infer(M_c, X_L_list, X_D_list, Y, row_id, col_idx, numsamples, confidence, engine)
        if code is not None:
            value = du.convert_code_to_value(M_c, col_idx, code)
            return value
        return du.convert_code_to_value(M_c, col_idx, T[row_id][col_idx])
        return


def _column_ignore(col_idx, row_id, data_values, M_c_full, T_full, engine):
    """
    This function handles selecting data from ignore columns. It's split into a different
    function because it needs to be passed M_c_full and T_full instead of M_c and T, as in _column.
    Since selecting ignore columns is probably a rare event, we can avoid passing M_c_full and T_full
    to _column as "just in case" arguments.
    """
    return du.convert_code_to_value(M_c_full, col_idx, T_full[row_id][col_idx])


def _row_id(args, row_id, data_values, M_c, X_L_list, X_D_list, T, engine, numsamples):
    return row_id


def _similarity(similarity_args, row_id, data_values, M_c, X_L_list, X_D_list, T, engine, numsamples):
    target_row_id, target_columns = similarity_args
    return engine.call_backend('similarity', dict(M_c=M_c, X_L_list=X_L_list, X_D_list=X_D_list, given_row_id=row_id, target_row_id=target_row_id, target_columns=target_columns))


def _row_typicality(row_typicality_args, row_id, data_values, M_c, X_L_list, X_D_list, T, engine, numsamples):
    return engine.call_backend('row_structural_typicality', dict(X_L_list=X_L_list, X_D_list=X_D_list, row_id=row_id))


def _predictive_probability(predictive_probability_args, row_id, data_values, M_c, X_L_list, X_D_list, T, engine, numsamples):
    c_idx = predictive_probability_args
    assert type(c_idx) == int
    Q = [(row_id, c_idx, T[row_id][c_idx])]
    Y = []
    p = math.exp(engine.call_backend('simple_predictive_probability_multistate', dict(M_c=M_c, X_L_list=X_L_list, X_D_list=X_D_list, Y=Y, Q=Q)))
    return p


def _col_typicality(col_typicality_args, row_id, data_values, M_c, X_L_list, X_D_list, T, engine, numsamples):
    c_idx = col_typicality_args
    assert type(c_idx) == int
    return engine.call_backend('column_structural_typicality', dict(X_L_list=X_L_list, col_id=c_idx))


def _probability(probability_args, row_id, data_values, M_c, X_L_list, X_D_list, T, engine, numsamples):
    c_idx, value = probability_args
    assert type(c_idx) == int
    try:
        observed = du.convert_value_to_code(M_c, c_idx, value)
    except KeyError:
        return 0

    row_id = len(X_D_list[0][0]) + 1
    Q = [(row_id, c_idx, observed)]
    Y = []
    p = math.exp(engine.call_backend('simple_predictive_probability_multistate', dict(M_c=M_c, X_L_list=X_L_list, X_D_list=X_D_list, Y=Y, Q=Q)))
    return p


def _dependence_probability(dependence_probability_args, row_id, data_values, M_c, X_L_list, X_D_list, T, engine, numsamples):
    """
    TODO: THIS NEEDS TO BE A FUNCTION ON CROSSCAT ENGINE! MOVE IT THERE!
    """
    col1, col2 = dependence_probability_args
    prob_dep = 0
    for X_L, X_D in zip(X_L_list, X_D_list):
        assignments = X_L['column_partition']['assignments']
        if assignments[col1] == assignments[col2]:
            if len(numpy.unique(X_D[assignments[col1]])) > 1 or col1 == col2:
                prob_dep += 1

    prob_dep /= float(len(X_L_list))
    return prob_dep


def _old_dependence_probability(dependence_probability_args, row_id, data_values, M_c, X_L_list, X_D_list, T, engine, numsamples):
    col1, col2 = dependence_probability_args
    prob_dep = 0
    for X_L, X_D in zip(X_L_list, X_D_list):
        assignments = X_L['column_partition']['assignments']
        if assignments[col1] == assignments[col2]:
            prob_dep += 1

    prob_dep /= float(len(X_L_list))
    return prob_dep


def _mutual_information(mutual_information_args, row_id, data_values, M_c, X_L_list, X_D_list, T, engine, numsamples):
    col1, col2 = mutual_information_args
    Q = [(col1, col2)]
    if numsamples is None:
        numsamples = 100
    n_samples = int(math.ceil(float(numsamples) / len(X_L_list)))
    results_by_model = engine.call_backend('mutual_information', dict(M_c=M_c, X_L_list=X_L_list, X_D_list=X_D_list, Q=Q, n_samples=n_samples))[0][0]
    mi = float(sum(results_by_model)) / len(results_by_model)
    return mi


def _correlation(correlation_args, row_id, data_values, M_c, X_L_list, X_D_list, T, engine, numsamples):
    col1, col2 = correlation_args
    cctype_map = dict(normal_inverse_gamma='numerical', symmetric_dirichlet_discrete='categorical', vonmises='numerical')
    cctype1 = cctype_map[M_c['column_metadata'][col1]['modeltype']]
    cctype2 = cctype_map[M_c['column_metadata'][col2]['modeltype']]
    correlation = numpy.nan
    t_array = numpy.array(T, dtype=float)
    nan_index = numpy.logical_or(numpy.isnan(t_array[:, col1]), numpy.isnan(t_array[:, col2]))
    t_array = t_array[numpy.logical_not(nan_index), :]
    n = t_array.shape[0]
    if cctype1 == 'numerical' and cctype2 == 'numerical':
        correlation, p_value = pearsonr(t_array[:, col1], t_array[:, col2])
        correlation = correlation ** 2
    elif cctype1 == 'categorical' and cctype2 == 'categorical':
        data_i = numpy.array(t_array[:, col1], dtype='int32')
        data_j = numpy.array(t_array[:, col2], dtype='int32')
        unique_i = numpy.unique(data_i)
        unique_j = numpy.unique(data_j)
        min_levels = min(len(unique_i), len(unique_j))
        if min_levels >= 2:
            contingency_table = numpy.zeros((len(unique_i), len(unique_j)), dtype='int')
            for i in unique_i:
                for j in unique_j:
                    contingency_table[i][j] = numpy.logical_and(data_i == i, data_j == j).sum()

            chisq, p, dof, expected = chi2_contingency(contingency_table, correction=False)
            correlation = (chisq / (n * (min_levels - 1))) ** 0.5
    else:
        if cctype1 == 'categorical':
            data_group = t_array[:, col1]
            data_y = t_array[:, col2]
        else:
            data_group = t_array[:, col2]
            data_y = t_array[:, col1]
        group_values = numpy.unique(data_group)
        n_groups = float(len(group_values))
        if n > n_groups:
            F, p = f_oneway(*[ data_y[(data_group == j)] for j in group_values ])
            correlation = 1 - (1 + F * ((n_groups - 1) / (n - n_groups))) ** (-1)
    return correlation