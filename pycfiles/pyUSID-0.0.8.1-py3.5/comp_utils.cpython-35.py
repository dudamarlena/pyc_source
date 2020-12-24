# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pyUSID/processing/comp_utils.py
# Compiled at: 2019-12-17 08:47:36
# Size of source mod 2**32: 10807 bytes
"""
Utilities that assist in computation

Created on Tue Nov  3 21:14:25 2015

@author: Suhas Somnath, Chris Smith
"""
from __future__ import print_function, division, unicode_literals, absolute_import
import joblib, numpy as np
from multiprocessing import cpu_count
from psutil import virtual_memory as vm

def get_MPI():
    """
    Returns the mpi4py.MPI object if mpi4py is available and size > 1. Returns None otherwise

    Returns
    -------
    MPI : :class:`mpi4py.MPI` object or None
    """
    try:
        from mpi4py import MPI
        if MPI.COMM_WORLD.Get_size() == 1:
            MPI = None
    except ImportError:
        MPI = None

    return MPI


def group_ranks_by_socket(verbose=False):
    """
    Groups MPI ranks in COMM_WORLD by socket. Another way to think about this is that it assigns a master rank for each
    rank such that there is a single master rank per socket (CPU). The results from this function can be used to split
    MPI communicators based on the socket for intra-node communication.

    This is necessary when wanting to carve up the memory for all ranks within a socket.
    This is also relevant when trying to bring down the number of ranks that are writing to the HDF5 file.
    This is all based on the premise that data analysis involves a fair amount of file writing and writing with
    3 ranks is a lot better than writing with 100 ranks. An assumption is made that the communication between the
    ranks within each socket would be faster than communicating across nodes / scokets. No assumption is made about the
    names of each socket

    Parameters
    ----------
    verbose : bool, optional
        Whether or not to print debugging statements

    Returns
    -------
    master_ranks : 1D unsigned integer :class:`numpy.ndarray`
        Array with values that signify which rank a given rank should consider its master.
    """
    MPI = get_MPI()
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    sendbuf = MPI.Get_processor_name()
    if verbose:
        print('Rank: ', rank, ', sendbuf: ', sendbuf)
    recvbuf = comm.allgather(sendbuf)
    if verbose and rank == 0:
        print('Rank: ', rank, ', recvbuf received: ', recvbuf)
    recvbuf = np.array(recvbuf)
    unique_sockets = np.unique(recvbuf)
    if verbose and rank == 0:
        print('Unique sockets: {}'.format(unique_sockets))
    master_ranks = np.zeros(size, dtype=np.uint16)
    for item in unique_sockets:
        temp = np.where(recvbuf == item)[0]
        master_ranks[temp] = temp[0]

    if verbose and rank == 0:
        print('Parent rank for all ranks: {}'.format(master_ranks))
    return master_ranks


def parallel_compute(data, func, cores=None, lengthy_computation=False, func_args=None, func_kwargs=None, verbose=False, joblib_backend='multiprocessing'):
    """
    Computes the provided function using multiple cores using the joblib library

    Parameters
    ----------
    data : numpy.ndarray
        Data to map function to. Function will be mapped to the first axis of data
    func : callable
        Function to map to data
    cores : uint, optional
        Number of logical cores to use to compute
        Default - All cores - 1 (total cores <= 4) or - 2 (cores > 4) depending on number of cores. 
        Ignored in the MPI context - each rank will execute serially
    lengthy_computation : bool, optional
        Whether or not each computation is expected to take substantial time.
        Sometimes the time for adding more cores can outweigh the time per core
        Default - False
    func_args : list, optional
        arguments to be passed to the function
    func_kwargs : dict, optional
        keyword arguments to be passed onto function
    joblib_backend : str, optional
        Backend to use for parallel computation with Joblib.
        The older paradigm - "multiprocessing" is the default in pyUSID.
        Set to None to use the joblib default - "loky"
    verbose : bool, optional. default = False
        Whether or not to print statements that aid in debugging

    Returns
    -------
    results : list
        List of computational results
    """
    if not callable(func):
        raise TypeError('Function argument is not callable')
    if not isinstance(data, np.ndarray):
        raise TypeError('data must be a numpy array')
    if func_args is None:
        func_args = list()
    elif isinstance(func_args, tuple):
        func_args = list(func_args)
    if not isinstance(func_args, list):
        raise TypeError('Arguments to the mapped function should be specified as a list')
    if func_kwargs is None:
        func_kwargs = dict()
    else:
        if not isinstance(func_kwargs, dict):
            raise TypeError('Keyword arguments to the mapped function should be specified via a dictionary')
        req_cores = cores
        MPI = get_MPI()
        if MPI is not None:
            rank = MPI.COMM_WORLD.Get_rank()
            cores = 1
        else:
            rank = 0
            cores = recommend_cpu_cores(data.shape[0], requested_cores=cores, lengthy_computation=lengthy_computation, verbose=verbose)
    if verbose:
        print('Rank {} starting computing on {} cores (requested {} cores)'.format(rank, cores, req_cores))
    if cores > 1:
        values = [joblib.delayed(func)(x, *func_args, **func_kwargs) for x in data]
        results = joblib.Parallel(n_jobs=cores, backend=joblib_backend)(values)
        print('Rank {} finished parallel computation'.format(rank))
    else:
        if verbose:
            print('Rank {} computing serially ...'.format(rank))
        results = [func(vector, *func_args, **func_kwargs) for vector in data]
    return results


def get_available_memory():
    """
    Returns the available memory

    Chris Smith -- csmith55@utk.edu

    Parameters
    ----------

    Returns
    -------
    mem : unsigned int
        Memory in bytes
    """
    import sys
    mem = vm().available
    if sys.maxsize <= 4294967296:
        mem = min([mem, sys.maxsize])
    return mem


def recommend_cpu_cores(num_jobs, requested_cores=None, min_free_cores=None, lengthy_computation=False, verbose=False):
    """
    Decides the number of cores to use for parallel computing

    Parameters
    ----------
    num_jobs : unsigned int
        Number of times a parallel operation needs to be performed
    requested_cores : unsigned int (Optional. Default = None)
        Number of logical cores to use for computation
    lengthy_computation : Boolean (Optional. Default = False)
        Whether or not each computation takes a long time. If each computation is quick, it may not make sense to take
        a hit in terms of starting and using a larger number of cores, so use fewer cores instead.
        Eg- BE SHO fitting is fast (<1 sec) so set this value to False,
        Eg- Bayesian Inference is very slow (~ 10-20 sec)so set this to True
    min_free_cores : uint (Optional, default = 1 if number of logical cores < 5 and 2 otherwise)
        Number of CPU cores that should not be used)
    verbose : Boolean (Optional.  Default = False)
        Whether or not to print statements that aid in debugging

    Returns
    -------
    requested_cores : unsigned int
        Number of logical cores to use for computation
    """
    logical_cores = cpu_count()
    if min_free_cores is not None:
        if not isinstance(min_free_cores, int):
            raise TypeError('min_free_cores should be an unsigned integer')
        if min_free_cores < 0 or min_free_cores >= logical_cores:
            raise ValueError('min_free_cores should be an unsigned integer less than the number of logical cores')
        if verbose:
            print('Number of requested free CPU cores: {} was accepted'.format(min_free_cores))
    else:
        if logical_cores > 4:
            min_free_cores = 2
        else:
            min_free_cores = 1
        if verbose:
            print('Number of CPU free cores set to: {} given that the CPU has {} logical cores.'.format(min_free_cores, logical_cores))
        max_cores = max(1, logical_cores - min_free_cores)
        if requested_cores is None:
            if verbose:
                print('No requested_cores given.  Using estimate of {}.'.format(max_cores))
            requested_cores = max_cores
        elif not isinstance(requested_cores, int):
            raise TypeError('requested_cores should be an unsigned integer')
    if verbose:
        print('{} cores requested.'.format(requested_cores))
    if requested_cores < 0 or requested_cores > logical_cores:
        requested_cores = max(min(int(abs(requested_cores)), logical_cores), 1)
        if verbose:
            print('Clipped explicit request for CPU cores to: {}'.format(requested_cores))
    if not isinstance(num_jobs, int):
        raise TypeError('num_jobs should be an unsigned integer')
    if num_jobs < 1:
        raise ValueError('num_jobs should be greater than 0')
    jobs_per_core = max(int(num_jobs / requested_cores), 1)
    min_jobs_per_core = 20
    if verbose:
        print('computational jobs per core = {}. For short computations, each core must have at least {} jobs to warrant parallel computation.'.format(jobs_per_core, min_jobs_per_core))
    if not lengthy_computation:
        if verbose:
            print('Computations are not lengthy.')
        if requested_cores > 1 and jobs_per_core < min_jobs_per_core:
            jobs_per_core = 2 * min_jobs_per_core
            requested_cores = max(1, min(requested_cores, int(num_jobs / jobs_per_core)))
            if verbose:
                print('Not enough jobs per core. Reducing cores to {}'.format(requested_cores))
    return int(requested_cores)