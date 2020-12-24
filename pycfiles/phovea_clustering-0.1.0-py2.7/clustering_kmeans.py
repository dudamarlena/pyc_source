# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/phovea_clustering/clustering_kmeans.py
# Compiled at: 2017-04-05 09:54:14
import phovea_server.config, numpy as np, random
from clustering_util import weighted_choice, similarity_measurement
__author__ = 'Michael Kern'
__version__ = '0.0.2'
__email__ = 'kernm@in.tum.de'
config = phovea_server.config.view('caleydo-clustering')

class KMeans():
    """
  This is an implementation of the k-means algorithm to cluster genomic data / matrices.
  Returns the centroids, the labels / stratification of each row belonging to one cluster,
  distance matrix for cluster-cluster distance and distance arrays for row-cluster_centroid distance.
  Implementation detail: <https://en.wikipedia.org/wiki/K-means_clustering>
  """

    def __init__(self, obs, k, init_mode='kmeans++', distance='sqeuclidean', iters=1000):
        """
    Initializes the algorithm with observation, number of k clusters, the initial method and
    the maximum number of iterations.
    Initialization method of random cluster choice can be: forgy, uniform, random, plusplus
    :param obs: genomic data / matrix
    :param k: number of clusters
    :param init_mode: initialization method
    :param distance: distance measurement
    :param iters: number of maximum iterations
    :return:
    """
        self.__k = k
        self.__obs = np.nan_to_num(obs)
        self.__n = np.shape(obs)[0]
        self.__label_map = np.zeros(self.__n, dtype=np.int)
        self.__cluster_means = np.array([ obs[0] for _ in range(k) ], dtype=np.float)
        self.__cluster_nums = np.array([ 0 for _ in range(k) ], dtype=np.int)
        self.__changed = True
        self.__iters = iters
        self.__init_mode = init_mode
        self.__distance = distance

    def __call__(self):
        """
    Caller function for server API.
    """
        return self.run()

    def __init(self):
        """
    Initialize clustering with random clusters using a user-specified method
    :return:
    """
        if self.__init_mode == 'forgy':
            self.__forgy_method()
        elif self.__init_mode == 'uniform':
            self.__uniform_method()
        elif self.__init_mode == 'random':
            self.__random_method()
        elif self.__init_mode == 'kmeans++':
            self.__plusplus_method()
        else:
            raise AttributeError

    def __forgy_method(self):
        """
    Initialization method:
    Randomly choose k observations from the data using a uniform random distribution.
    :return:
    """
        for ii in range(self.__k):
            self.__cluster_means[ii] = self.__obs[random.randint(0, self.__n - 1)]

    def __uniform_method(self):
        """
    Initialization method:
    Randomly assign each observation to one of the k clusters using uniform random distribution
    and compute the centroids of each cluster.
    :return:
    """
        for i in range(self.__n):
            self.__label_map[i] = random.randint(0, self.__k - 1)

        self.__update()

    def __random_method(self):
        """
    Initialization method:
    Randomly choose k observations from the data by estimating the mean and standard deviation of the data and
    using the gaussian random distribution.
    :return:
    """
        mean = np.mean(self.__obs, axis=0)
        std = np.std(self.__obs, axis=0)
        for ii in range(self.__k):
            self.__cluster_means[ii] = np.random.normal(mean, std)

    def __plusplus_method(self):
        """
    Initialization method:
    Chooses k observations by computing probabilities for each observation and using a weighted random distribution.
    Algorithm: <https://en.wikipedia.org/wiki/K-means%2B%2B>. This method should accelerate the algorithm by finding
    the appropriate clusters right at the beginning and hence should make it more robust.
    :return:
    """
        self.__cluster_means[0] = random.choice(self.__obs)
        max_value = np.max(self.__obs) + 1
        probs = np.array([ max_value for _ in range(self.__n) ])
        for i in range(1, self.__k):
            probs.fill(max_value)
            for j in range(0, i):
                dists = similarity_measurement(self.__obs, self.__cluster_means[j], self.__distance)
                probs = np.minimum(probs, dists)

            sum_probs = np.float(np.sum(probs))
            if sum_probs != 0:
                probs /= sum_probs
                self.__cluster_means[i] = self.__obs[weighted_choice(probs)]
            else:
                print 'ERROR: cannot find enough cluster centroids for given k = ' + str(self.__k)

    def get_cluster_mean(self, num):
        """
    Returns the centroid of the cluster with index num.
    :param num:
    :return:
    """
        if num >= self.__k:
            return
        else:
            return self.__cluster_means[num]
            return

    def get_cluster_of_element(self, index):
        """
    :param index: number of element in observation array
    :return: cluster id of observation with given index.
    """
        if index >= self.__n:
            return
        else:
            return self.__label_map[index]
            return

    def print_clusters(self):
        """
    Print the cluster centroids and the labels.
    :return:
    """
        print 'Centroids: ' + str(self.__centroids) + ' | _labels: ' + str(self.__labels)

    def __assignment(self):
        """
    Assignment step:
    Compute distance of current observation to each cluster centroid and move gene to the nearest cluster.
    :return:
    """
        for i in range(self.__n):
            value = self.__obs[i]
            dists = similarity_measurement(self.__cluster_means, value, self.__distance)
            nearest_i_d = np.argmin(dists)
            if self.__label_map[i] != nearest_i_d:
                self.__changed = True
                self.__label_map[i] = nearest_i_d

    def __update(self):
        """
    Update step:
    Compute the new centroids of each cluster after the assignment.
    :return:
    """
        self.__cluster_means.fill(0)
        self.__cluster_nums.fill(0)
        self.__cluster_labels = [ [] for _ in range(self.__k) ]
        for ii in range(self.__n):
            cluster_i_d = self.__label_map[ii]
            self.__cluster_labels[cluster_i_d].append(ii)
            self.__cluster_nums[cluster_i_d] += 1

        for ii in range(self.__k):
            self.__cluster_means[ii] = np.mean(self.__obs[self.__cluster_labels[ii]], axis=0)

    def __end(self):
        """
    Writes the results to the corresponding member variables.
    :return:
    """
        self.__centroids = np.array([ self.__obs[0] for _ in range(self.__k) ], dtype=np.float)
        self.__labels = np.array([ 0 for _ in range(self.__n) ], dtype=np.int)
        for index in range(self.__n):
            cluster_i_d = self.__label_map[index]
            self.__labels[index] = cluster_i_d

        for ii in range(self.__k):
            self.__centroids[ii] = self.__cluster_means[ii]

    def run(self):
        """
    Runs the algorithm of k-means, using the initialization method and the assignment/update step.
    Conducts at most iters iterations and terminates if this number is exceeded or no observations
    was moved to another cluster.
    :return:
    """
        self.__init()
        max_iters = self.__iters
        counter = 0
        while self.__changed and counter < max_iters:
            self.__changed = False
            self.__assignment()
            self.__update()
            counter += 1

        self.num_iters = counter
        self.__end()
        return (self.__centroids.tolist(), self.__labels.tolist(), self.__cluster_labels)


def _plugin_initialize():
    """
  optional initialization method of this module, will be called once
  :return:
  """
    pass


def create(data, k, init_method, distance):
    """
  by convention contain a factory called create returning the extension implementation
  :return:
  """
    return KMeans(data, k, init_method, distance)


def _main():
    from timeit import default_timer as timer
    from scipy.cluster.vq import kmeans2
    data = np.array([1, 1.1, 5, 8, 5.2, 8.3])
    k = 3
    time_mine = 0
    time_theirs = 0
    n = 10
    for i in range(10):
        s1 = timer()
        k_means_plus = KMeans(data, k, 'kmeans++', 'sqeuclidean', 10)
        result1 = k_means_plus.run()
        e1 = timer()
        s2 = timer()
        result2 = kmeans2(data, k)
        e2 = timer()
        time_mine += e1 - s1
        time_theirs += e2 - s2

    print result1
    print result2
    print ('mine: {}').format(time_mine / n)
    print ('theirs: {}').format(time_theirs / n)


if __name__ == '__main__':
    _main()