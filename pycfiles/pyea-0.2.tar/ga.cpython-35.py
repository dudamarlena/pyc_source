# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/al/DriveAl/Studies/PhD/Project/simufraud/pyea/pyea/models/ga.py
# Compiled at: 2016-01-29 09:54:26
# Size of source mod 2**32: 10392 bytes
"""
This module include the Genetic Algorithms method. 
"""
import numpy as np
from numpy.core.defchararray import add
import pandas as pd
from scipy.stats import norm
from sklearn.externals.joblib import Parallel, delayed, cpu_count
import itertools

def _partition_estimators(n_estimators, n_jobs):
    """Private function used to partition estimators between jobs."""
    if n_jobs == -1:
        n_jobs = min(cpu_count(), n_estimators)
    else:
        n_jobs = min(n_jobs, n_estimators)
    n_estimators_per_job = n_estimators // n_jobs * np.ones(n_jobs, dtype=np.int)
    n_estimators_per_job[:n_estimators % n_jobs] += 1
    starts = np.cumsum(n_estimators_per_job)
    return (
     n_jobs, n_estimators_per_job.tolist(), [0] + starts.tolist())


def _fitness_function_parallel(pop, fitness_function, fargs):
    return fitness_function(pop, *fargs).tolist()


class GeneticAlgorithmOptimizer:
    __doc__ = 'Genetic Algorithms method. \n       Works with either binary or continuous functions\n\n    Parameters\n    ----------\n    fitness_function : object\n        The function to measure the performance of each chromosome.\n        Must accept a vector of chromosomes and return a vector of cost.\n        By default it is assumed that it is a minimization problem.\n        \n    n_parameters : int\n        Number of parameters to estimate.\n    \n    iters : int, optional (default=10)\n        Number of iterations\n        \n    type : string, optional (default="cont")\n        Type of problem, either continuous or binary ("cont" or "binary")\n\n    n_chromosomes : int, optional (default=10)\n        Number of chromosomes.\n        \n    per_mutations : float, optional (default=0.2)\n        Percentage of mutations.\n            \n    n_elite : int, optional (default=2)\n        Number of elite chromosomes.\n\n    fargs : tuple, optional (default=())\n        Additional parameters to be send to the fitness_function\n\n    range_ : tuple of floats, optional (default = (-1, 1))\n        Only for continuous problems. The range of the search space.\n\n    n_jobs : integer, optional (default=1)\n        The number of jobs to run in parallel for \'fit`.\n        If -1, then the number of jobs is set to the number of cores.\n\n    verbose : int, optional (default=0)\n        Controls the verbosity of the GA process.\n\n\n    Attributes\n    ----------\n    `hist_` : pandas.DataFrame of shape = [n_chromosomes * iters, columns=[\'iter\', \'x0\', \'x1\', .., \'xk\', \'cost\', \'orig\']]\n        History of the optimization process\n\n    References\n    ----------\n    .. [1] R. Haupt, S. Haupt, A.Correa, "Practical genetic algorithms (Second Edi.)",\n           New Jersey: John Wiley & Sons, Inc. (2004).\n\n    .. [2] S. Marslan, "Machine Learning: An Algorithmic Perspective",\n           New Jersey, USA: CRC Press. (2009).\n\n    Examples\n    --------\n    >>> import numpy as np\n    >>> from pyea.models import GeneticAlgorithmOptimizer\n    >>> from pyea.functions import func_rosenbrock, func_rosenbrock_bin\n    >>> f1 = GeneticAlgorithmOptimizer(func_rosenbrock, n_parameters=2, iters=10, type_=\'cont\', range_=(-31, 31))\n    >>> f2 = GeneticAlgorithmOptimizer(func_rosenbrock_bin, n_parameters=40, iters=10, type_=\'binary\')\n    >>> f1.fit()\n    >>> f2.fit()\n    >>> # Best per iter\n    >>> print(f1.hist_[[\'iter\', \'cost\']].groupby(\'iter\').aggregate(np.min))\n    >>> print(f2.hist_[[\'iter\', \'cost\']].groupby(\'iter\').aggregate(np.min))\n    '

    def __init__(self, fitness_function, n_parameters, iters=10, type_='cont', n_chromosomes=10, per_mutations=0.2, n_elite=2, fargs=(), range_=(-1, 1), n_jobs=1, verbose=0):
        self.n_parameters = n_parameters
        self.n_chromosomes = n_chromosomes
        self.per_mutations = per_mutations
        self.iters = iters
        self.fitness_function = fitness_function
        self.fargs = fargs
        self.n_elite = n_elite
        self.type_ = type_
        self.range_ = range_
        self.n_jobs = n_jobs
        self.verbose = verbose

    def _random(self, n):
        if self.type_ == 'binary':
            temp_ = np.random.binomial(1, 0.5, size=(n, self.n_parameters)).astype(np.int)
        else:
            temp_ = (self.range_[1] - self.range_[0]) * np.random.rand(n, self.n_parameters) + self.range_[0]
        return temp_

    def _fitness_function(self):
        n_jobs, _, starts = _partition_estimators(self.n_chromosomes, self.n_jobs)
        all_results = Parallel(n_jobs=n_jobs, verbose=self.verbose, backend='multiprocessing')(delayed(_fitness_function_parallel)(self.pop_[starts[i]:starts[(i + 1)]], self.fitness_function, self.fargs) for i in range(n_jobs))
        return np.array(list(itertools.chain.from_iterable(t for t in all_results)))

    def fit(self):
        _cols_x = ['x%d' % i for i in range(self.n_parameters)]
        self.hist_ = pd.DataFrame(index=range((self.iters + 1) * self.n_chromosomes), columns=[
         'iter'] + _cols_x + ['cost', 'orig'])
        self.hist_[['orig']] = '-1'
        self.pop_ = self._random(self.n_chromosomes)
        self.cost_ = self._fitness_function()
        filter_iter = range(0, self.n_chromosomes)
        self.hist_.loc[(filter_iter, 'iter')] = 0
        self.hist_.loc[(filter_iter, 'cost')] = self.cost_
        self.hist_.loc[(filter_iter, _cols_x)] = self.pop_
        for i in range(self.iters):
            if self.verbose > 0:
                print('Iteration ' + str(i) + ' of ' + str(self.iters))
            orig = np.empty(self.n_chromosomes, dtype='S10')
            cost_sort = np.argsort(self.cost_)
            new_pop = np.empty_like(self.pop_)
            new_pop[0:self.n_elite] = self.pop_[cost_sort[0:self.n_elite]]
            orig[0:self.n_elite] = (cost_sort[0:self.n_elite] + i * self.n_chromosomes).astype(np.str)
            zcost = (self.cost_ - np.average(self.cost_)) / np.std(self.cost_)
            pzcost = 1 - norm.cdf(zcost)
            pcost = np.cumsum(pzcost / sum(pzcost))
            numparents = self.n_chromosomes - self.n_elite
            rand_parents = np.random.rand(numparents, 2)
            parents = np.zeros(rand_parents.shape, dtype=np.int)
            for parent1 in range(numparents):
                for parent2 in range(2):
                    parents[(parent1, parent2)] = np.searchsorted(pcost, rand_parents[(parent1, parent2)])

                if self.type_ == 'binary':
                    rand_match = int(np.random.rand() * self.n_parameters)
                    child = self.pop_[parents[(parent1, 0)]]
                    child[rand_match:] = self.pop_[parents[(parent1, 1)], rand_match:]
                else:
                    rand_match = np.random.rand(self.n_parameters)
                    child = self.pop_[parents[(parent1, 0)]] * rand_match
                    child += (1 - rand_match) * self.pop_[parents[(parent1, 1)]]
                new_pop[self.n_elite + parent1] = child

            orig[self.n_elite:] = [','.join(row.astype(np.str)) for row in parents + i * self.n_chromosomes]
            m_rand = np.random.rand(self.n_chromosomes, self.n_parameters)
            m_rand[0:self.n_elite] = 1.0
            mutations = m_rand <= self.per_mutations
            num_mutations = np.count_nonzero(mutations)
            if self.type_ == 'binary':
                new_pop[mutations] = (new_pop[mutations] == 0).astype(np.int)
            else:
                new_pop[mutations] = self._random(num_mutations)[:, 0]
            rows_mutations = np.any(mutations, axis=1)
            orig[rows_mutations] = add(orig[rows_mutations], np.array(['_M'] * np.count_nonzero(rows_mutations), dtype='S10'))
            temp_unique = np.ascontiguousarray(new_pop).view(np.dtype((np.void,
             new_pop.dtype.itemsize * new_pop.shape[1])))
            _, temp_unique_idx = np.unique(temp_unique, return_index=True)
            n_replace = self.n_chromosomes - temp_unique_idx.shape[0]
            if n_replace > 0:
                temp_unique_replace = np.ones(self.n_chromosomes, dtype=np.bool)
                temp_unique_replace[:] = True
                temp_unique_replace[temp_unique_idx] = False
                new_pop[temp_unique_replace] = self._random(n_replace)
                orig[temp_unique_replace] = '-1'
            self.pop_ = new_pop
            self.cost_ = self._fitness_function()
            filter_iter = range((i + 1) * self.n_chromosomes, (i + 2) * self.n_chromosomes)
            self.hist_.loc[(filter_iter, 'iter')] = i + 1
            self.hist_.loc[(filter_iter, 'cost')] = self.cost_
            self.hist_.loc[(filter_iter, _cols_x)] = self.pop_
            self.hist_.loc[(filter_iter, 'orig')] = orig

        best = np.argmin(self.cost_)
        self.x = self.pop_[best]
        self.x_cost = self.cost_[best]


if __name__ == '__main__':
    import numpy as np
    from pyea.models import GeneticAlgorithmOptimizer
    from pyea.functions import func_rosenbrock, func_rosenbrock_bin
    f1 = GeneticAlgorithmOptimizer(func_rosenbrock, n_parameters=2, iters=10, type_='cont', range_=(-31,
                                                                                                    31))
    f2 = GeneticAlgorithmOptimizer(func_rosenbrock_bin, n_parameters=40, iters=10, type_='binary')
    f1.fit()
    f2.fit()
    print(f1.hist_[['iter', 'cost']].groupby('iter').aggregate(np.min))
    print(f2.hist_[['iter', 'cost']].groupby('iter').aggregate(np.min))