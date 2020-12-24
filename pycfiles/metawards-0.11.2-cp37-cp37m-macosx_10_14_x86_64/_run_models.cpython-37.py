# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/utils/_run_models.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 14332 bytes
from typing import Union as _Union
from typing import List as _List
from typing import Tuple as _Tuple
from .._network import Network
from .._networks import Networks
from .._population import Population
from .._variableset import VariableSets, VariableSet
from .._outputfiles import OutputFiles
from ._profiler import Profiler
from ._get_functions import get_functions, MetaFunction
from contextlib import contextmanager as _contextmanager
import os as _os, sys as _sys
__all__ = [
 'get_number_of_processes', 'run_models', 'redirect_output']

def get_number_of_processes(parallel_scheme: str, nprocs: int=None):
    """This function works out how many processes have been set
       by the paralellisation system called 'parallel_scheme'
    """
    if nprocs is None:
        if parallel_scheme == 'multiprocessing':
            return 1
        elif parallel_scheme == 'mpi4py':
            from mpi4py import MPI
            comm = MPI.COMM_WORLD
            nprocs = comm.Get_size()
            return nprocs
            if parallel_scheme == 'scoop':
                raise ValueError('You must specify the number of processes for scoop to parallelise over')
        else:
            raise ValueError(f"You must specify the number of processes to use for parallel scheme '{parallel_scheme}'")
    elif parallel_scheme == 'mpi4py':
        from mpi4py import MPI
        comm = MPI.COMM_WORLD
        n = comm.Get_size()
        if n < nprocs:
            return n
        return nprocs
    else:
        if parallel_scheme == 'scoop':
            return 4
        if parallel_scheme == 'multiprocessing':
            return nprocs
        raise ValueError(f"Unrecognised parallelisation scheme {parallel_scheme}")


@_contextmanager
def redirect_output(outdir):
    """Nice way to redirect stdout and stderr - thanks to
       Emil Stenström in
       https://stackoverflow.com/questions/6735917/redirecting-stdout-to-nothing-in-python
    """
    new_out = open(_os.path.join(outdir, 'output.txt'), 'w')
    old_out = _sys.stdout
    _sys.stdout = new_out
    new_err = open(_os.path.join(outdir, 'output.err'), 'w')
    old_err = _sys.stderr
    _sys.stderr = new_err
    try:
        yield new_out
    finally:
        _sys.stdout = old_out
        _sys.stderr = old_err
        new_out.close()
        new_err.close()


def run_models(network: _Union[(Network, Networks)], variables: VariableSets, population: Population, nprocs: int, nthreads: int, seed: int, nsteps: int, output_dir: OutputFiles, iterator: MetaFunction=None, extractor: MetaFunction=None, mixer: MetaFunction=None, mover: MetaFunction=None, profiler: Profiler=None, parallel_scheme: str='multiprocessing', debug_seeds=False) -> _List[_Tuple[(VariableSet, Population)]]:
    """Run all of the models on the passed Network that are described
       by the passed VariableSets

       Parameters
       ----------
       network: Network or Networks
         The network(s) to model
       variables: VariableSets
         The sets of VariableSet that represent all of the model
         runs to perform
       population: Population
         The initial population for all of the model runs. This also
         contains the starting date and day for the model outbreak
       nprocs: int
         The number of model runs to perform in parallel
       nthreads: int
         The number of threads to parallelise each model run over
       seed: int
         Random number seed which is used to generate random seeds
         for all model runs
       nsteps: int
         The maximum number of steps to perform for each model - this
         will run until the outbreak is over if this is None
       output_dir: OutputFiles
         The OutputFiles that represents the directory in which all
         output should be placed
       iterator: str
         Iterator to load that will be used to iterate the outbreak
       extractor: str
         Extractor to load that will be used to extract information
       mixer: str
         Mixer to load that will be used to mix demographic data
       mover: str
         Mover to load that will be used to move the population between
         different demographics
       profiler: Profiler
         Profiler used to profile the model run
       parallel_scheme: str
         Which parallel scheme (multiprocessing, mpi4py or scoop) to use
         to run multiple model runs in parallel
       debug_seeds: bool (False)
         Set this parameter to force all runs to use the same seed
         (seed) - this is used for debugging and should never be set
         in production runs

       Returns
       -------
       results: List[ tuple(VariableSet, Population)]
         The set of adjustable variables and final population at the
         end of each run
    """
    if len(variables) == 1:
        params = network.params.set_variables(variables[0])
        network.update(params, profiler=profiler)
        trajectory = network.run(population=population, seed=seed, nsteps=nsteps,
          output_dir=output_dir,
          iterator=iterator,
          extractor=extractor,
          mixer=mixer,
          mover=mover,
          profiler=profiler,
          nthreads=nthreads)
        results = [
         (
          variables[0], trajectory)]
        from ._get_functions import get_summary_functions
        if extractor is None:
            from extractors._extract_default import extract_default
            extractor = extract_default
        else:
            from extractors._extract_custom import build_custom_extractor
            extractor = build_custom_extractor(extractor)
        funcs = get_summary_functions(network=network, results=results, output_dir=output_dir,
          extractor=extractor,
          nthreads=nthreads)
        for func in funcs:
            func(network=network, output_dir=output_dir, results=results)

        return results
        seeds = []
        if seed == 0:
            print('** WARNING: Using special mode to fix all random number')
            print('** WARNING: seeds to 15324. DO NOT USE IN PRODUCTION!!!')
            for i in range(0, len(variables)):
                seeds.append(15324)

    elif debug_seeds:
        print('** WARNING: Using special model to make all jobs use the')
        print(f"** WARNING: Same random number seed {seed}.")
        print('** WARNING: DO NOT USE IN PRODUCTION!')
        for i in range(0, len(variables)):
            seeds.append(seed)

    else:
        from ._ran_binomial import seed_ran_binomial, ran_int
        rng = seed_ran_binomial(seed)
        for i in range(0, len(variables)):
            seeds.append(ran_int(rng, 10000, 99999999))

    outdirs = []
    for v in variables:
        f = v.fingerprint(include_index=True)
        d = _os.path.join(output_dir.get_path(), f)
        outdirs.append(d)

    outputs = []
    print(f"\nRunning {len(variables)} jobs using {nprocs} process(es)")
    if nprocs == 1:
        save_network = network.copy()
        for i, variable in enumerate(variables):
            seed = seeds[i]
            outdir = outdirs[i]
            with output_dir.open_subdir(outdir) as (subdir):
                print(f"\nRunning parameter set {i + 1} of {len(variables)} using seed {seed}")
                print(f"All output written to {subdir.get_path()}")
                with redirect_output(subdir.get_path()):
                    print(f"Running variable set {i + 1}")
                    print(f"Variables: {variable}")
                    print(f"Random seed: {seed}")
                    print(f"nthreads: {nthreads}")
                    params = network.params.set_variables(variable)
                    network.update(params, profiler=profiler)
                    output = network.run(population=population, seed=seed, nsteps=nsteps,
                      output_dir=subdir,
                      iterator=iterator,
                      extractor=extractor,
                      mixer=mixer,
                      mover=mover,
                      profiler=profiler,
                      nthreads=nthreads)
                    outputs.append((variable, output))
                print(f"Completed job {i + 1} of {len(variables)}")
                print(variable)
                print(output[(-1)])
            if i != len(variables) - 1:
                network = save_network.copy()

    else:
        from ._worker import run_worker
        arguments = []
        if isinstance(network, Networks):
            max_nodes = network.overall.nnodes + 1
            max_links = max(network.overall.nlinks, network.overall.nplay) + 1
        else:
            max_nodes = network.nnodes + 1
            max_links = max(network.nlinks, network.nplay) + 1
        try:
            demographics = network.demographics
        except Exception:
            demographics = None

        if profiler is None:
            worker_profiler = None
        else:
            worker_profiler = profiler.__class__()
        for i, variable in enumerate(variables):
            seed = seeds[i]
            outdir = outdirs[i]
            arguments.append({'params':network.params.set_variables(variable), 
             'demographics':demographics, 
             'options':{'seed':seed, 
              'output_dir':outdir, 
              'auto_bzip':output_dir.auto_bzip(), 
              'population':population, 
              'nsteps':nsteps, 
              'iterator':iterator, 
              'extractor':extractor, 
              'mixer':mixer, 
              'mover':mover, 
              'profiler':worker_profiler, 
              'nthreads':nthreads, 
              'max_nodes':max_nodes, 
              'max_links':max_links}})

        if parallel_scheme == 'multiprocessing':
            print('\nRunning jobs in parallel using a multiprocessing pool...')
            from multiprocessing import Pool
            with Pool(processes=nprocs) as (pool):
                results = pool.map(run_worker, arguments)
                for i, result in enumerate(results):
                    print(f"\nCompleted job {i + 1} of {len(variables)}")
                    print(variables[i])
                    print(result[(-1)])
                    outputs.append((variables[i], result))

        else:
            if parallel_scheme == 'mpi4py':
                print('\nRunning jobs in parallel using a mpi4py pool...')
                from mpi4py import futures
                with futures.MPIPoolExecutor(max_workers=nprocs) as (pool):
                    results = pool.map(run_worker, arguments)
                    for i, result in enumerate(results):
                        print(f"\nCompleted job {i + 1} of {len(variables)}")
                        print(variables[i])
                        print(result[(-1)])
                        outputs.append((variables[i], result))

            else:
                if parallel_scheme == 'scoop':
                    print('\nRunning jobs in parallel using a scoop pool...')
                    from scoop import futures
                    results = futures.map(run_worker, arguments)
                    for i, result in enumerate(results):
                        print(f"\nCompleted job {i + 1} of {len(variables)}")
                        print(variables[i])
                        print(result[(-1)])
                        outputs.append((variables[i], result))

                else:
                    raise ValueError(f"Unrecognised parallelisation scheme {parallel_scheme}.")
    from ._get_functions import get_summary_functions
    if extractor is None:
        from extractors._extract_default import extract_default
        extractor = extract_default
    else:
        from extractors._extract_custom import build_custom_extractor
        extractor = build_custom_extractor(extractor)
    funcs = get_summary_functions(network=network, results=outputs, output_dir=output_dir,
      extractor=extractor,
      nthreads=nthreads)
    for func in funcs:
        func(network=network, output_dir=output_dir, results=outputs,
          nthreads=nthreads)

    return outputs