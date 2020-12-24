# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/utils/_run_model.py
# Compiled at: 2020-05-10 15:00:16
# Size of source mod 2**32: 9612 bytes
from typing import Union as _Union
from .._network import Network
from .._networks import Networks
from .._infections import Infections
from .._outputfiles import OutputFiles
from .._workspace import Workspace
from .._population import Population, Populations
from ._profiler import Profiler
from ._get_functions import get_initialise_functions, get_model_loop_functions, get_finalise_functions, MetaFunction
__all__ = [
 'run_model']

def run_model(network: _Union[(Network, Networks)], infections: Infections, rngs, output_dir: OutputFiles, population: Population=Population(initial=57104043), nsteps: int=None, profiler: Profiler=None, nthreads: int=None, iterator: _Union[(str, MetaFunction)]=None, extractor: _Union[(str, MetaFunction)]=None, mixer: _Union[(str, MetaFunction)]=None, mover: _Union[(str, MetaFunction)]=None) -> Populations:
    """Actually run the model... Real work happens here. The model
       will run until completion or until 'nsteps' have been
       completed (whichever happens first)

        Parameters
        ----------
        network: Network or Networks
            The network(s) on which to run the model
        infections: Infections
            The space used to record the infections
        rngs: list
            The list of random number generators to use, one per thread
        population: Population
            The initial population at the start of the model outbreak.
            This is also used to set the date and day of the start of
            the model outbreak
        seed: int
            The random number seed used for this model run. If this is
            None then a very random random number seed will be used
        output_dir: OutputFiles
            The directory to write all of the output into
        nsteps: int
            The maximum number of steps to run in the outbreak. If None
            then run until the outbreak has finished
        profiler: Profiler
            The profiler to use to profile - a new one is created if
            one isn't passed
        nthreads: int
            Number of threads over which to parallelise this model run
        iterator: MetaFunction or string
            Function that will be used to dynamically get the functions
            that will be used at each iteration to advance the
            model. Any additional files or parameters needed by these
            functions should be included in the `network.params` object.
        extractor: MetaFunction or string
            Function that will be used to dynamically get the functions
            that will be used at each iteration to extract data from
            the model run
        mixer: MetaFunction or string
            Function that will mix data from multiple demographics
            so that this is shared during a model run
        mover: MetaFunction or string
            Function that can move the population between different
            demographics

        Returns
        -------
        trajectory: Populations
            The trajectory of the population for every day of the model run
    """
    if isinstance(iterator, str):
        from iterators._iterate_custom import build_custom_iterator
        iterator = build_custom_iterator(iterator, __name__)
    else:
        if iterator is None:
            from iterators._iterate_default import iterate_default
            iterator = iterate_default
        else:
            if isinstance(extractor, str):
                from extractors._extract_custom import build_custom_extractor
                extractor = build_custom_extractor(extractor, __name__)
            else:
                if extractor is None:
                    from extractors._extract_default import extract_default
                    extractor = extract_default
            if isinstance(mixer, str):
                from mixers._mix_custom import build_custom_mixer
                mixer = build_custom_mixer(mixer, __name__)
            else:
                if mixer is None:
                    from mixers._mix_default import mix_default
                    mixer = mix_default
        if isinstance(mover, str):
            from movers._move_custom import build_custom_mover
            mover = build_custom_mover(mover, __name__)
        else:
            if mover is None:
                from movers._move_default import move_default
                mover = move_default
            else:
                if profiler is None:
                    from ._profiler import NullProfiler
                    profiler = NullProfiler()
                p = profiler.start('run_model')
                params = network.params
                if params is None:
                    return population
                from copy import deepcopy
                population = deepcopy(population)
                trajectory = Populations()
                p = p.start('clear_all_infections')
                infections.clear(nthreads=nthreads)
                p = p.stop()
                workspace = Workspace.build(network=network)
                p = p.start('initialise_funcs')
                funcs = get_initialise_functions(network=network, population=population, infections=infections,
                  output_dir=output_dir,
                  workspace=workspace,
                  rngs=rngs,
                  iterator=iterator,
                  extractor=extractor,
                  mixer=mixer,
                  mover=mover,
                  nthreads=nthreads,
                  profiler=p)
                for func in funcs:
                    p = p.start(str(func))
                    func(network=network, population=population, infections=infections,
                      output_dir=output_dir,
                      workspace=workspace,
                      rngs=rngs,
                      nthreads=nthreads,
                      profiler=p)
                    p = p.stop()

                p = p.stop()
                infecteds = population.infecteds
                trajectory.append(population)
                p = p.start('run_model_loop')
                iteration_count = 0
                while infecteds != 0 or iteration_count < 5:
                    p2 = profiler.__class__()
                    p2 = p2.start(f"timing for day {population.day}")
                    start_population = population.population
                    funcs = get_model_loop_functions(network=network,
                      population=population,
                      infections=infections,
                      output_dir=output_dir,
                      workspace=workspace,
                      rngs=rngs,
                      iterator=iterator,
                      extractor=extractor,
                      mixer=mixer,
                      mover=mover,
                      nthreads=nthreads,
                      profiler=p)
                    for func in funcs:
                        p2 = p2.start(str(func))
                        func(network=network, population=population, infections=infections,
                          output_dir=output_dir,
                          workspace=workspace,
                          rngs=rngs,
                          nthreads=nthreads,
                          profiler=p2)
                        p2 = p2.stop()

                    print(f"\n {population.day} {infecteds}\n")
                    if population.population != start_population:
                        raise AssertionError(f"The total population changed during the day. This should not happen and indicates a program bug. The starting population was {start_population}, while the end population is {population.population}. Detail is {population}")
                    infecteds = population.infecteds
                    iteration_count += 1
                    population.day += 1
                    if population.date:
                        from datetime import timedelta
                        population.date += timedelta(days=1)
                    if nsteps is not None:
                        if iteration_count >= nsteps:
                            trajectory.append(population)
                            print(f"Exiting model run early at nsteps = {nsteps}")
                            break
                    p2 = p2.stop()
                    if not p2.is_null():
                        print(f"\n{p2}\n")
                    trajectory.append(population)

                p = p.stop()
                p = p.start('finalise_funcs')
                funcs = get_finalise_functions(network=network, population=population, infections=infections,
                  output_dir=output_dir,
                  workspace=workspace,
                  rngs=rngs,
                  iterator=iterator,
                  extractor=extractor,
                  mixer=mixer,
                  mover=mover,
                  nthreads=nthreads,
                  trajectory=trajectory,
                  profiler=p)
                for func in funcs:
                    p = p.start(str(func))
                    func(network=network, population=population, infections=infections,
                      output_dir=output_dir,
                      workspace=workspace,
                      rngs=rngs,
                      nthreads=nthreads,
                      trajectory=trajectory,
                      profiler=p)
                    p = p.stop()

                p = p.stop()
                p.stop()
                p.is_null() or print(f"\nOVERALL MODEL TIMING\n{p}")
            print(f"Infection died ... Ending on day {population.day}")
            return trajectory.strip_demographics()