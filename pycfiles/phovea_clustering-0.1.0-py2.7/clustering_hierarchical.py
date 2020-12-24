# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/phovea_clustering/clustering_hierarchical.py
# Compiled at: 2017-04-05 09:54:14
import phovea_server.config, numpy as np
from clustering_util import BinaryNode, BinaryTree
from clustering_util import similarity_measurement_matrix
from clustering_util import compute_cluster_intern_distances
from clustering_util import cut_json_tree_by_clusters
__author__ = 'Michael Kern'
__version__ = '0.0.3'
__email__ = 'kernm@in.tum.de'
config = phovea_server.config.view('caleydo-clustering')

class Hierarchical(object):
    """
  This is a implementation of hierarchical clustering on genomic data using the Lance-Williams dissimilarity update
  to compute different distance metrics (single linkage, complete linkage, ...).
  Lance-Williams explained in: http://arxiv.org/pdf/1105.0121.pdf
  """

    def __init__(self, obs, method='single', distance='euclidean'):
        """
    Initializes the algorithm
    :param obs: genomic data / matrix
    :param method: linkage method
    :return:
    """
        self.__obs = np.nan_to_num(obs)
        num_genes = np.shape(self.__obs)[0]
        self.__n = num_genes
        self.__distance = distance
        self.__d = []
        self.__compute_proximity_matrix()
        self.__id_map = {}
        self.__key_map = {}
        self.__cluster_map = {}
        for ii in range(self.__n):
            self.__id_map[str(ii)] = ii
            self.__key_map[ii] = str(ii)
            self.__cluster_map[str(ii)] = ii

        self.__method = method
        self.__tree = None
        return

    def __call__(self):
        """
    Caller function for server API
    :return:
    """
        return self.run()

    @property
    def tree(self):
        return self.__tree

    def __get_coefficients(self, cluster_i, cluster_j):
        """
    Compute the coefficients for the Lance-Williams algorithm
    :param cluster_i:
    :param cluster_j:
    :return:
    """
        if self.__method == 'single':
            return (0.5, 0.5, 0, -0.5)
        if self.__method == 'complete':
            return (0.5, 0.5, 0, 0.5)
        if self.__method == 'weighted':
            return (0.5, 0.5, 0, 0)
        if self.__method == 'median':
            return (0.5, 0.5, -0.25, 0)
        if self.__method == 'average':
            n_i = np.float(cluster_i.count(',') + 1)
            n_j = np.float(cluster_j.count(',') + 1)
            sum_n = n_i + n_j
            return (
             n_i / sum_n, n_j / sum_n, 0, 0)
        if self.__method == 'centroid':
            n_i = np.float(cluster_i.count(',') + 1)
            n_j = np.float(cluster_j.count(',') + 1)
            sum_n = n_i + n_j
            return (
             n_i / sum_n, n_j / sum_n, -(n_i * n_j / sum_n ** 2), 0)
        raise AttributeError

    def __compute_proximity_matrix(self):
        """
    Compute the proximity of each observation and store the results in a nxn matrix
    :return:
    """
        self.__d = np.zeros((self.__n, self.__n))
        self.__d = similarity_measurement_matrix(self.__obs, self.__distance)
        self.__max_value = self.__d.max() + 1
        np.fill_diagonal(self.__d, self.__max_value)

    def __get_matrix_minimum_indices(self):
        """
    Searches for the minimum distance in the distance matrix
    :return: indices of both clusters having the smallest distance
    """
        min_dist = self.__d.min()
        min_list = np.argwhere(self.__d == min_dist)
        min_i, min_j = (0, 0)
        for ii in range(len(min_list)):
            min_i, min_j = min_list[ii]
            if min_i < min_j:
                break

        if min_i == min_j:
            print 'ERROR'
        return (self.__key_map[min_i], self.__key_map[min_j], min_dist)

    def __delete_clusters(self, i, j):
        """
    Reorders and reduces the matrix to insert the new cluster formed of cluster i and j
    and its distance values, and removes the old clusters by cutting the last row.
    :param i: cluster index i
    :param j: cluster index j
    :return:
    """
        id_i = self.__id_map[str(i)]
        id_j = self.__id_map[str(j)]
        max_id = max(id_i, id_j)
        last_row = self.__d[(self.__n - 1)]
        self.__d[max_id] = last_row
        self.__d[:, max_id] = self.__d[:, self.__n - 1]
        key = self.__key_map[(self.__n - 1)]
        self.__id_map[key] = max_id
        self.__key_map[max_id] = key
        try:
            del self.__id_map[i]
            del self.__id_map[j]
            del self.__key_map[self.__n - 1]
        except KeyError:
            print ('\nERROR: Key {} not found in id_map').format(j)
            print ('ERROR: Previous key: {} in id_map').format(i)
            print 'Given keys: '
            for key in self.__id_map:
                print key

            return

        self.__n -= 1
        self.__d = self.__d[:-1, :-1]

    def __merge_clusters(self, i, j):
        """
    Merges cluster i and j, computes the new ID and distances of the newly formed cluster
    and stores required information
    :param i: cluster index i
    :param j: cluster index j
    :return:
    """
        id_i = self.__id_map[str(i)]
        id_j = self.__id_map[str(j)]
        min_id = min(id_i, id_j)
        max_id = max(id_i, id_j)
        dki = self.__d[:, min_id]
        dkj = self.__d[:, max_id]
        dij = self.__d[(min_id, max_id)]
        dist_ij = np.abs(dki - dkj)
        ai, aj, b, y = self.__get_coefficients(i, j)
        new_entries = ai * dki + aj * dkj + b * dij + y * dist_ij
        new_entries[min_id] = self.__max_value
        new_entries[max_id] = self.__max_value
        self.__d[min_id] = new_entries
        self.__d[:, min_id] = new_entries
        id_ij = min_id
        new_key = i + ',' + j
        self.__id_map[new_key] = id_ij
        self.__key_map[id_ij] = new_key
        self.__cluster_map[new_key] = len(self.__cluster_map)
        self.__delete_clusters(i, j)
        return new_key.count(',') + 1

    def run(self):
        """
    Conducts the algorithm until there's only one cluster.
    :return:
    """
        m = 0
        runs = self.__n - 1
        z = np.array([ [ 0 for _ in range(4) ] for _ in range(runs) ], dtype=np.float)
        while m < runs:
            m += 1
            i, j, dist_ij = self.__get_matrix_minimum_indices()
            num_ij = self.__merge_clusters(i, j)
            cluster_i, cluster_j = self.__cluster_map[i], self.__cluster_map[j]
            z[m - 1] = [int(min(cluster_i, cluster_j)), int(max(cluster_i, cluster_j)), np.float(dist_ij), int(num_ij)]

        self.__n = np.shape(self.__obs)[0]
        self.__tree = self.generate_tree(z)
        return z.tolist()

    def generate_tree(self, linkage_matrix):
        """
    Computes the dendrogram tree for a given linkage matrix.
    :param linkage_matrix:
    :return:
    """
        self.__tree = None
        tree_map = {}
        num_trees = len(linkage_matrix)
        for ii in range(num_trees):
            entry = linkage_matrix[ii]
            current_id = self.__n + ii
            left_index, right_index, value = (int(entry[1]), int(entry[0]), entry[2], int(entry[3]))
            left = right = None
            if left_index < self.__n:
                left = BinaryNode(self.__obs[left_index].tolist(), left_index, 1, None, None)
            else:
                left = tree_map[left_index]
            if right_index < self.__n:
                right = BinaryNode(self.__obs[right_index].tolist(), right_index, 1, None, None)
            else:
                right = tree_map[right_index]
            if isinstance(left, BinaryNode) and isinstance(right, BinaryNode):
                tree_map[current_id] = BinaryTree(left, right, current_id, value)
            elif isinstance(left, BinaryNode):
                tree_map[current_id] = right.add_node(left, current_id, value)
                del tree_map[right_index]
            elif isinstance(right, BinaryNode):
                tree_map[current_id] = left.add_node(right, current_id, value)
                del tree_map[left_index]
            else:
                tree_map[current_id] = left.merge(right, current_id, value)
                del tree_map[right_index]
                del tree_map[left_index]

        self.__tree = tree_map[(num_trees + self.__n - 1)]
        return self.__tree


def get_clusters(k, obs, dendrogram, sorted=True):
    """
  First implementation to cut dendrogram tree automatically by choosing nodes having the greatest node values
  or rather distance to the other node / potential cluster
  :param k: number of desired clusters
  :param obs: set of observations
  :param dendrogram: dendrogram tree
  :return: centroids, sorted cluster labels and normal label list
  """
    obs = np.nan_to_num(obs)
    n = obs.shape[0]
    if isinstance(dendrogram, BinaryTree):
        cluster_labels = dendrogram.cut_tree_by_clusters(k)
    else:
        cluster_labels = cut_json_tree_by_clusters(dendrogram, k)
    cluster_centroids = []
    labels = np.zeros(n, dtype=np.int)
    cluster_id = 0
    for ii in range(len(cluster_labels)):
        cluster = cluster_labels[ii]
        sub_obs = obs[cluster]
        cluster_centroids.append(np.mean(sub_obs, axis=0).tolist())
        for id in cluster:
            labels[id] = cluster_id

        if sorted:
            cluster_labels[ii], _ = compute_cluster_intern_distances(obs, cluster)
        cluster_id += 1

    return (cluster_centroids, cluster_labels, labels.tolist())


def _plugin_initialize():
    """
  optional initialization method of this module, will be called once
  :return:
  """
    pass


def create(data, method, distance):
    """
  by convention contain a factory called create returning the extension implementation
  :return:
  """
    return Hierarchical(data, method, distance)


def _main():
    from timeit import default_timer as timer
    np.random.seed(200)
    data = np.array([1, 1.1, 5, 8, 5.2, 8.3])
    time_mine = 0
    time_theirs = 0
    n = 10
    for i in range(n):
        s1 = timer()
        hier = Hierarchical(data, 'complete')
        linkage_matrix = hier.run()
        e1 = timer()
        print linkage_matrix
        tree = hier.generate_tree(linkage_matrix)
        import json
        json_tree = json.loads(tree.jsonify())
        get_clusters(3, data, json_tree)
        s2 = timer()
        e2 = timer()
        time_mine += e1 - s1
        time_theirs += e2 - s2

    print ('mine: {}').format(time_mine / n)
    print ('theirs: {}').format(time_theirs / n)


if __name__ == '__main__':
    _main()