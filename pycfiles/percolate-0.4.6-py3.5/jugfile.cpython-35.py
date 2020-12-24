# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/percolate/share/jugfile.py
# Compiled at: 2015-12-12 17:04:41
# Size of source mod 2**32: 7532 bytes
"""
A sample jugfile to use with Jug

jug execute jugfile
"""
from __future__ import unicode_literals
from builtins import map, zip
from future.utils import iteritems
from functools import reduce
import itertools, numpy as np, scipy.stats
from jug import Task, TaskGenerator, barrier
from jug.utils import CustomHash
import jug.mapreduce, percolate, percolate.hpc
SYSTEM_DIMENSIONS = [
 8, 16, 32]
RUNS_PER_TASK = 100
NUMBER_OF_TASKS = 100
NUMBER_OF_RUNS = NUMBER_OF_TASKS * RUNS_PER_TASK
PS = np.linspace(0.4, 0.6, num=40)
SPANNING_CLUSTER = True
UINT32_MAX = 4294967296
SEED = 201508061904 % UINT32_MAX
ALPHA = 2 * scipy.stats.norm.cdf(-1.0)

@TaskGenerator
def prepare_percolation_graph(dimension):
    graph = percolate.spanning_2d_grid(length=dimension)
    return percolate.percolate.percolation_graph(graph=graph, spanning_cluster=SPANNING_CLUSTER)


@TaskGenerator
def compute_convolution_factors_for_single_p(perc_graph_result, p):
    return percolate.percolate._binomial_pmf(n=perc_graph_result['num_edges'], p=p)


def bond_run(perc_graph_result, seed, ps, convolution_factors_tasks):
    """
    Perform a single run (realization) over all microstates and return the
    canonical cluster statistics
    """
    microcanonical_statistics = percolate.hpc.bond_microcanonical_statistics(seed=seed, **perc_graph_result)
    canonical_statistics = np.empty(ps.size, dtype=percolate.hpc.canonical_statistics_dtype(spanning_cluster=SPANNING_CLUSTER))
    for row, convolution_factors_task in zip(np.nditer(canonical_statistics, op_flags=['writeonly']), convolution_factors_tasks):
        assert not convolution_factors_task.is_loaded()
        convolution_factors_task.load()
        my_convolution_factors = convolution_factors_task.result
        row[...] = percolate.hpc.bond_canonical_statistics(microcanonical_statistics=microcanonical_statistics, convolution_factors=my_convolution_factors, spanning_cluster=SPANNING_CLUSTER)
        convolution_factors_task.unload()

    ret = percolate.hpc.bond_initialize_canonical_averages(canonical_statistics=canonical_statistics, spanning_cluster=SPANNING_CLUSTER)
    return ret


@TaskGenerator
def bond_task(perc_graph_result, seeds, ps, convolution_factors_tasks_iterator):
    """
    Perform a number of runs

    The number of runs is the number of seeds

    convolution_factors_tasks_iterator needs to be an iterator

    We shield the convolution factors tasks from jug value/result mechanism
    by supplying an iterator to the list of tasks for lazy evaluation
    http://github.com/luispedro/jug/blob/43f0d80a78f418fd3aa2b8705eaf7c4a5175fff7/jug/task.py#L100
    http://github.com/luispedro/jug/blob/43f0d80a78f418fd3aa2b8705eaf7c4a5175fff7/jug/task.py#L455
    """
    convolution_factors_tasks = list(convolution_factors_tasks_iterator)
    return reduce(percolate.hpc.bond_reduce, map(bond_run, itertools.repeat(perc_graph_result), seeds, itertools.repeat(ps), itertools.repeat(convolution_factors_tasks)))


@TaskGenerator
def write_to_disk(dimension, canonical_averages):
    import h5py
    f = h5py.File('percolate_hpc.hdf5', mode='a')
    key = '{}'.format(dimension)
    if key in f:
        raise RuntimeError
    f.create_dataset(name=key, data=canonical_averages)
    f.close()


def dummy_hash(x):
    """
    Supplies a constant dummy hash
    """
    return 'dummy_hash'.encode('utf-8')


convolution_factors = {}
perc_graph_results = {}
reduced_canonical_averages = {}
final_canonical_averages = {}
rng = np.random.RandomState(seed=SEED)
for dimension in SYSTEM_DIMENSIONS:
    perc_graph_results[dimension] = prepare_percolation_graph(dimension)
    convolution_factors[dimension] = [compute_convolution_factors_for_single_p(perc_graph_result=perc_graph_results[dimension], p=p) for p in PS]
    barrier()
    seeds = rng.randint(UINT32_MAX, size=NUMBER_OF_RUNS)
    bond_tasks = list()
    for my_seeds in np.split(seeds, NUMBER_OF_TASKS):
        convolution_iterator = iter(convolution_factors[dimension])
        convolution_iterator_hashed = CustomHash(convolution_iterator, dummy_hash)
        bond_tasks.append(bond_task(perc_graph_result=perc_graph_results[dimension], seeds=my_seeds, ps=PS, convolution_factors_tasks_iterator=convolution_iterator_hashed))

    reduced_canonical_averages[dimension] = jug.mapreduce.reduce(reducer=percolate.hpc.bond_reduce, inputs=bond_tasks, reduce_step=100)
    final_canonical_averages[dimension] = Task(percolate.hpc.finalize_canonical_averages, number_of_nodes=perc_graph_results[dimension]['num_nodes'], ps=PS, canonical_averages=reduced_canonical_averages[dimension], alpha=ALPHA)
    write_to_disk(dimension=dimension, canonical_averages=final_canonical_averages[dimension])