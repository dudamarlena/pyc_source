# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dreegdl/smote.py
# Compiled at: 2020-03-04 18:08:43
# Size of source mod 2**32: 2485 bytes
from sklearn.neighbors import NearestNeighbors
import random as rd

class Smote:
    __doc__ = '\n  Implement SMOTE, synthetic minority oversampling technique.\n  Parameters\n  -----------\n  sample      2D (numpy)array\n              minority class samples\n  N           Integer\n              amount of SMOTE N%\n  k           Integer\n              number of nearest neighbors k\n              k <= number of minority class samples\n  Attributes\n  ----------\n  newIndex    Integer\n              keep a count of number of synthetic samples\n              initialize as 0\n  synthetic   2D array\n              array for synthetic samples\n  neighbors   K-Nearest Neighbors model\n  '

    def __init__(self, sample, N, k):
        self.sample = sample
        self.k = k
        self.T = len(self.sample)
        self.N = N
        self.newIndex = 0
        self.synthetic = []
        self.neighbors = NearestNeighbors(n_neighbors=(self.k)).fit(self.sample)

    def over_sampling(self):
        if self.N < 100:
            self.T = self.N / 100 * self.T
            self.N = 100
        self.N = int(self.N / 100)
        for i in range(0, self.T):
            nn_array = self.compute_k_nearest(i)
            self.populate(self.N, i, nn_array)

    def compute_k_nearest(self, i):
        nn_array = self.neighbors.kneighbors([self.sample[i]], (self.k), return_distance=False)
        if len(nn_array) is 1:
            return nn_array[0]
        return []

    def populate(self, N, i, nn_array):
        while N is not 0:
            nn = rd.randint(1, self.k - 1)
            self.synthetic.append([])
            for attr in range(0, len(self.sample[i])):
                dif = self.sample[nn_array[nn]][attr] - self.sample[i][attr]
                gap = rd.random()
                while gap == 0:
                    gap = rd.random()

                self.synthetic[self.newIndex].append(self.sample[i][attr] + gap * dif)

            self.newIndex += 1
            N -= 1