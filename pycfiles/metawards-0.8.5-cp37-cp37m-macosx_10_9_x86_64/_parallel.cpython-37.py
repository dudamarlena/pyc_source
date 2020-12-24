# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/GitHub/MetaWards/build/lib.macosx-10.9-x86_64-3.7/metawards/utils/_parallel.py
# Compiled at: 2020-04-20 09:02:59
# Size of source mod 2**32: 4332 bytes
from array import array
__all__ = [
 'guess_num_threads_and_procs',
 'get_available_num_threads',
 'create_thread_generators']

def guess_num_threads_and_procs(njobs: int, nthreads: int=None, nprocs: int=None, ncores: int=None, parallel_scheme: str=None):
    """Guess the number of processes and threads per process
       to use to make most-efficient processing of
       'njobs' jobs.

       Parameters
       ----------
       njobs: int
         The number of jobs (model runs) that must be performed
       nthreads: int
         The number of threads requested - if None then this this will be
         guessed
       nprocs: int
         The number of processes requested - if None then this will be
         guessed
       ncores: int
         The number of available cores on each node (or this computer).
         This will be obtained from the OS if it is not supplied
       parallel_scheme: str
         The parallelisation scheme that is being used to parallelise
         over processes

       Returns
       -------
       (nthreads, nprocs): Tuple[int, int]
         Tuple of the best-guessed 'nthreads' and 'nprocs' values to use
    """
    if nthreads is None:
        nthreads = 0
    if nprocs is None:
        nprocs = 0
    if not njobs is None:
        if njobs < 0:
            return (1, 1)
        if parallel_scheme is None:
            parallel_scheme = 'multiprocessing'
        if nprocs < 1:
            if parallel_scheme != 'multiprocessing':
                from metawards.utils import get_number_of_processes
                nprocs = get_number_of_processes(parallel_scheme, nprocs)
        if ncores is None:
            ncores = get_available_num_threads()
        if nthreads < 1 and nprocs < 1:
            if njobs >= 0.8 * ncores:
                nthreads = 1
                nprocs = ncores
        else:
            import math
            nthreads = int(math.floor(ncores / njobs))
            if nthreads < 1:
                nthreads = 1
            nprocs = int(math.floor(ncores / nthreads))
            if nprocs < 1:
                nprocs = 1
    else:
        if nthreads < 1:
            import math
            nthreads = int(math.floor(ncores / nprocs))
            if nthreads < 1:
                nthreads = 1
        elif nprocs < 1:
            import math
            max_nprocs = int(math.floor(ncores / nthreads))
            if max_nprocs < njobs:
                nprocs = max_nprocs
            else:
                nprocs = max_nprocs
        return (
         nthreads, nprocs)


def get_available_num_threads():
    """Return the maximum number of threads that are recommended
       for this computer (the OMP_NUM_THREADS value)
    """
    import os
    omp_num_threads = os.getenv('OMP_NUM_THREADS', None)
    if omp_num_threads is not None:
        try:
            return int(omp_num_threads)
        except Exception:
            pass

    return os.cpu_count()


def create_thread_generators(rng, nthreads):
    """Return a set of random number generators, one for each
       thread - these are seeded using the next 'nthreads'
       random numbers drawn from the passed generator

       If 'nthreads' is 1, 0 or None, then then just
       returns the passed 'rng'
    """
    rngs = []
    if nthreads is None or nthreads <= 1:
        rngs.append(rng)
    else:
        from ._ran_binomial import seed_ran_binomial, ran_int
        for i in range(0, nthreads):
            seed = ran_int(rng)
            print(f"Random seed for thread {i} equals {seed}")
            rngs.append(seed_ran_binomial(seed))

    return array('L', rngs)