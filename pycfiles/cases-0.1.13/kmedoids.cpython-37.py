# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/caserec/clustering/kmedoids.py
# Compiled at: 2019-08-20 09:47:28
# Size of source mod 2**32: 4127 bytes
__doc__ = '"\n    K-medoids Clustering Algorithm\n    [Co-Clustering Algorithm]\n\n    Literature:\n        H.S. Park , C.H. Jun:\n        A simple and fast algorithm for K-medoids clustering\n        Expert Systems with Applications, 36, (2) (2009), 3336–3341.\n\n'
import numpy as np
__author__ = 'Arthur Fortes <fortes.arthur@gmail.com>'

def kmedoids(distance_matrix, k, max_interactions=10000, random_seed=None):
    """
    k-medoids

    Usage::

        >> sm, c = kmedoids(distance_matrix, k=3)

    The k-medoids algorithm is a clustering algorithm related to the k-means algorithm and the medoidshift algorithm.
    Both the k-means and k-medoids algorithms are partitional (breaking the dataset up into groups) and both attempt to
    minimize the distance between points labeled to be in a cluster and a point designated as the center of that
    cluster. In contrast to the k-means algorithm, k-medoids chooses datapoints as centers (medoids or exemplars)
    and works with a generalization of the Manhattan Norm to define distance between datapoints instead of.
    This method was proposed in 1987[1] for the work with norm and other distances.

    k-medoid is a classical partitioning technique of clustering that clusters the data set of n objects into k
    clusters known a priori. A useful tool for determining k is the silhouette. It is more robust to noise and outliers
    as compared to k-means because it minimizes a sum of pairwise dissimilarities instead of a sum of squared
    Euclidean distances.

    A medoid can be defined as the object of a cluster whose average dissimilarity to all the objects in the cluster
    is minimal. i.e. it is a most centrally located point in the cluster.

    :param distance_matrix: Matrix with distances between the instances
    :type distance_matrix: matrix

    :param k: Number of groups to be generated
    :type k: int

    :param max_interactions: Number max of interaction to converge
    :type max_interactions: int, default 10000

    :param random_seed: Seed of random
    :type random_seed: int, default None

    :return: Support vector and List of labels (len = number of instances)

    """
    if random_seed is not None:
        np.random.seed(random_seed)
    row, col = distance_matrix.shape
    if k > col:
        raise Exception('Error:: Too many medoids')
    support_matrix = np.arange(col)
    np.random.shuffle(support_matrix)
    support_matrix = np.sort(support_matrix[:k])
    new_support_matrix = np.copy(support_matrix)
    clusters = {}
    for _ in range(max_interactions):
        j_vector = np.argmin((distance_matrix[:, support_matrix]), axis=1)
        for label in range(k):
            clusters[label] = np.where(j_vector == label)[0]

        for label in range(k):
            j_vector = np.mean((distance_matrix[np.ix_(clusters[label], clusters[label])]),
              axis=1)
            try:
                j = np.argmin(j_vector)
                new_support_matrix[label] = clusters[label][j]
            except ValueError:
                pass

        np.sort(new_support_matrix)
        if np.array_equal(support_matrix, new_support_matrix):
            break
        support_matrix = np.copy(new_support_matrix)
    else:
        j_vector = np.argmin((distance_matrix[:, support_matrix]), axis=1)
        for label in range(k):
            clusters[label] = np.where(j_vector == label)[0]

    remove_keys = set()
    for key in clusters:
        if len(clusters[key]) == 0:
            remove_keys.add(key)

    if remove_keys:
        for key in remove_keys:
            clusters.pop(key, None)

    return (
     support_matrix, clusters)