# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/phovea_clustering/clustering_service.py
# Compiled at: 2017-04-05 09:54:14
import numpy as np
from clustering_hierarchical import get_clusters
__author__ = 'Michael Kern'
__version__ = '0.0.1'
__email__ = 'kernm@in.tum.de'

def load_data(dataset_id):
    """
  Loads the genomic data with given identifier dataset_id.
  :param dataset_id: identifier
  :return: array of the genomic data
  """
    import phovea_server.dataset as dt
    dataset = dt.get(dataset_id)
    try:
        arr = np.array(list(dataset.asnumpy()))
    except:
        raise Exception

    return arr


def load_plugin(plugin_id, *args, **kwargs):
    """
  Loads the clustering plugin with given arguments.
  :param plugin_id: identifier of plugin
  :param *args: additional caller function arguments
  :param **kwargs: additional arguments
  :return: plugin
  """
    import phovea_server.plugin
    plugins = phovea_server.plugin.list('clustering')
    for plugin in plugins:
        if plugin.id == plugin_id:
            return plugin.load().factory(*args, **kwargs)

    raise NotImplementedError


def run_kmeans(data, k, init_method, distance):
    """
  Runs the k-Means clustering algorithm given the loaded data set, the number of clusters k and the initialization
  method.
  :param data: observation matrix
  :param k: number of clusters
  :param init_method: number of clusters
  :return: result of k-means
  """
    kmeans = load_plugin('caleydo-clustering-kmeans', data, k, init_method, distance)
    centroids, labels, cluster_labels = kmeans()
    return {'centroids': centroids, 'clusterLabels': cluster_labels}


def run_hierarchical(data, k, method, distance):
    """
  Runs the hierarchical clustering algorithm given the loaded data set and type of linkage method.
  :param data: observation matrix
  :param method: linkage method
  :return: linkage matrix / dendrogram of the algorithm
  """
    hierarchical = load_plugin('caleydo-clustering-hierarchical', data, method, distance)
    hierarchical()
    centroids, cluster_labels, labels = get_clusters(k, data, hierarchical.tree, False)
    return {'centroids': centroids, 'clusterLabels': cluster_labels, 'dendrogram': hierarchical.tree.json()}


def run_affinity_propagation(data, damping, factor, preference, distance):
    """
  Runs the affinity propagation algorithm given the loaded dataset, a damping value, a certain factor and
  a preference method.
  :param data:
  :param damping:
  :param factor:
  :param preference:
  :return:
  """
    affinity = load_plugin('caleydo-clustering-affinity', data, damping, factor, preference, distance)
    centroids, labels, cluster_labels = affinity()
    return {'centroids': centroids, 'clusterLabels': cluster_labels}


def run_fuzzy(data, num_clusters, m, threshold, distance):
    fuzzy = load_plugin('caleydo-clustering-fuzzy', data, num_clusters, m, threshold, distance)
    centroids, cluster_labels, partition_matrix, max_prob = fuzzy()
    return {'centroids': centroids, 'clusterLabels': cluster_labels, 'partitionMatrix': partition_matrix, 'maxProbability': max_prob}


def get_cluster_distances(data, labels, metric, extern_labels=None, sorted=True):
    """
  Compute the cluster distances in a given data among certain rows (labels)
  :param data: genomic data
  :param labels: indices of rows
  :param metric: distance metric
  :param extern_labels:
  :return: labels and distances values sorted in ascending order
  """
    from clustering_util import compute_cluster_intern_distances, compute_cluster_extern_distances
    dist_labels, dist_values = compute_cluster_intern_distances(data, labels, sorted, metric)
    if extern_labels is not None:
        extern_dists = compute_cluster_extern_distances(data, dist_labels, extern_labels, metric)
        return {'labels': dist_labels, 'distances': dist_values, 'externDistances': extern_dists}
    else:
        return {'labels': dist_labels, 'distances': dist_values}
        return


def get_clusters_from_dendrogram(data, dendrogram, num_clusters):
    """

  :param data:
  :param dendrogram:
  :param num_clusters:
  :return:
  """
    centroids, cluster_labels, _ = get_clusters(num_clusters, data, dendrogram)
    return {'centroids': centroids, 'clusterLabels': cluster_labels}