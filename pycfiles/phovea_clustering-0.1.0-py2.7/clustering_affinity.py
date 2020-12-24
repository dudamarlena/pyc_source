# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/phovea_clustering/clustering_affinity.py
# Compiled at: 2017-04-05 09:54:14
import phovea_server.config, numpy as np
from clustering_util import similarity_measurementmatrix
from timeit import default_timer as timer
config = phovea_server.config.view('caleydo-clustering')
__author__ = 'Michael Kern'
__version__ = '0.0.1'
__email__ = 'kernm@in.tum.de'

class AffinityPropagation:
    """
  This is an implementation of the affinity propagation algorithm to cluster genomic data / matrices.
  Implementation details: <http://www.psi.toronto.edu/index.php?q=affinity%20propagation>.
  Matlab implementation: <http://www.psi.toronto.edu/affinitypropagation/software/apcluster.m>
  Returns the centroids and labels / stratification of each row belonging to one cluster.
  """

    def __init__(self, obs, damping=0.5, factor=1.0, pref_method='minimum', distance='euclidean'):
        """
    Initializes the algorithm.
    :param obs: genomic data / matrix
    :param damping: controls update process to dampen oscillations
    :param factor: controls the preference value (influences number of clusters)
    :param pref_method: all points are chosen equally with a given preference (median or minimum of similarity matrix)
    :return:
    """
        self.__n = np.shape(obs)[0]
        self.__obs = np.nan_to_num(obs)
        self.__damping = damping
        self.__factor = factor
        self.__prev_method = pref_method
        self.__S = np.zeros((self.__n, self.__n))
        self.__A = np.zeros((self.__n, self.__n))
        self.__R = np.zeros((self.__n, self.__n))
        self.min_value = np.finfo(np.float).min
        self.__idx = np.zeros(self.__n)
        self.__distance = distance
        self.__compute_similarity()

    def __call__(self):
        """
    Caller function for server API.
    """
        return self.run()

    def __compute_similarity(self):
        """
    Compute the similarity matrix from the original observation matrix and set preference of each element.
    :return: _similarity matrix
    """
        self.__S = -similarity_measurementmatrix(self.__obs, self.__distance)
        pref = 0
        if self.__prev_method == 'median':
            pref = float(np.median(self.__S)) * self.__factor
        elif self.__prev_method == 'minimum':
            pref = np.min(self.__S) * self.__factor
        else:
            raise AttributeError
        np.fill_diagonal(self.__S, pref)

    def run(self):
        """
    Runs the algorithm of affinity propagation. Conducts at least 100 iterations and checks if the outcome of
    current exemplars/clusters has converged. If not, the algorithm will continue until convergence is found
    or the maximum number of iterations (200) is reached.
    :return:
    """
        max_iter = 200
        max_conv_iter = 100
        decision_sum = np.zeros(self.__n)
        decision_iter = np.zeros((max_conv_iter, self.__n))
        decision_counter = max_conv_iter
        is_converged = False
        centroids = []
        it = 0
        cluster_i = []
        index_diag = np.arange(self.__n)
        indices_diag = np.diag_indices_from(self.__R)
        new_a = np.zeros((self.__n, self.__n))
        new_r = np.zeros((self.__n, self.__n))
        for it in range(1, max_iter + 1):
            m_as = self.__A + self.__S
            max_y = np.max(m_as, axis=1)
            index_y = np.argmax(m_as, axis=1)
            m_as[(index_diag, index_y)] = self.min_value
            max_y2 = np.max(m_as, axis=1)
            for ii in range(self.__n):
                new_r[ii] = self.__S[ii] - max_y[ii]

            new_r[(index_diag, index_y)] = self.__S[(index_diag, index_y)] - max_y2[index_diag]
            self.__R *= self.__damping
            self.__R += (1 - self.__damping) * new_r
            rp = np.maximum(self.__R, 0)
            rp[indices_diag] = self.__R[indices_diag]
            sum_cols = np.sum(rp, axis=0)
            new_a[:,] = sum_cols
            new_a -= rp
            diag_a = np.diag(new_a)
            new_a[new_a > 0] = 0
            new_a[indices_diag] = diag_a[index_diag]
            self.__A *= self.__damping
            self.__A += (1 - self.__damping) * new_a
            diag_e = np.diag(self.__R) + np.diag(self.__A)
            cluster_i = np.argwhere(diag_e > 0).flatten()
            num_clusters = len(cluster_i)
            decision_counter += 1
            if decision_counter >= max_conv_iter:
                decision_counter = 0
            decision_sum -= decision_iter[decision_counter]
            decision_iter[decision_counter].fill(0)
            decision_iter[decision_counter][cluster_i] = 1
            decision_sum += decision_iter[decision_counter]
            if it >= max_conv_iter or it >= max_iter:
                is_converged = True
                for ii in range(self.__n):
                    if decision_sum[ii] != 0 and decision_sum[ii] != max_conv_iter:
                        is_converged = False
                        break

                if is_converged and num_clusters > 0:
                    break

        centroids = self.__obs[cluster_i]
        self.__A.fill(self.min_value)
        self.__A[:, cluster_i] = 0.0
        np.fill_diagonal(self.__S, 0.0)
        m_as = self.__A + self.__S
        self.__idx = np.argmax(m_as, axis=1)
        cluster_i = cluster_i.tolist()
        cluster_labels = [ [] for _ in range(num_clusters) ]
        for ii in range(self.__n):
            index = cluster_i.index(self.__idx[ii])
            self.__idx[ii] = index
            cluster_labels[index].append(ii)

        return (
         centroids.tolist(), self.__idx.tolist(), cluster_labels)


def _plugin_initialize():
    """
  optional initialization method of this module, will be called once
  :return:
  """
    pass


def create(data, damping, factor, preference, distance):
    """
  by convention contain a factory called create returning the extension implementation
  :return:
  """
    return AffinityPropagation(data, damping, factor, preference, distance)


if __name__ == '__main__':
    np.random.seed(200)
    data = np.array([1, 1.1, 5, 8, 5.2, 8.3])
    s = timer()
    aff = AffinityPropagation(data, 0.9, 1.0, 'median', 'euclidean')
    result = aff.run()
    e = timer()
    print result
    print ('time elapsed: {}').format(e - s)