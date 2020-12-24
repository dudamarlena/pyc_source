# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/bayesdb/diagnostics_utils.py
# Compiled at: 2015-02-12 15:25:14
import numpy as np
multi_state_diagnostics = []
single_state_diagnostics = [
 'num_views',
 'column_crp_alpha',
 'min_clusters_view',
 'max_clusters_view',
 'mean_clusters_view',
 'std_clusters_view']

def get_num_views(X_L, X_D):
    """Returns the number of views in X_L
    """
    return len(X_L['column_partition']['counts'])


def get_column_crp_alpha(X_L, X_D):
    """Retruns column crp alpha parameter
    """
    return X_L['column_partition']['hypers']['alpha']


def get_min_clusters_view(X_L, X_D):
    """ Returns the minimum number of clusters in a view
    """
    Z = np.array(X_D, dtype=int)
    num_clusters_view = np.max(Z, axis=1) + 1
    return np.min(num_clusters_view)


def get_max_clusters_view(X_L, X_D):
    """ Returns the maximum number of clusters in a view
    """
    Z = np.array(X_D, dtype=int)
    num_clusters_view = np.max(Z, axis=1) + 1
    return np.max(num_clusters_view)


def get_mean_clusters_view(X_L, X_D):
    """ Returns the mean number of clusters in views
    """
    Z = np.array(X_D, dtype=int)
    num_clusters_view = np.max(Z, axis=1) + 1
    return np.mean(num_clusters_view)


def get_std_clusters_view(X_L, X_D):
    """ Returns the standard deviation of numbers of clusters in views
    """
    Z = np.array(X_D, dtype=int)
    num_clusters_view = np.max(Z, axis=1) + 1
    return np.std(num_clusters_view)