# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/GitHub/MetaWards/build/lib.macosx-10.9-x86_64-3.7/metawards/utils/_iterate.py
# Compiled at: 2020-04-21 14:40:03
# Size of source mod 2**32: 2370 bytes
from .._network import Network
from .._population import Population
from ._profiler import Profiler, NullProfiler
__all__ = [
 'iterate']

def iterate(network: Network, population: Population, infections, play_infections, rngs, nthreads: int, get_advance_functions, profiler: Profiler=None):
    """Advance the infection by one day for the passed Network,
       acting on the passed Population.

       Parameters
       ----------
       network: Network
         The network in which the disease outbreak will be modelled
       population: Population
         The population experiencing the outbreak. This contains
         an overview of the current population, plus the day and
         date of the outbreak
       infections
         Space in which the 'work' (fixed) infections are recorded
       play_infections
         Space in which the 'play' (random) infections are recorded
       rngs
         List of the thread-safe random number generators (one per thread)
       nthreads: int
         The number of threads over which to parallelise the calculation
       get_advance_functions: function
         This is a function that should return the set of "advance_XXX"
         functions that will be applied as part of this iteration
       profiler: Profiler
         The profiler to use to profile this calculation. Pass "None"
         if you want to disable profiling
    """
    if profiler is None:
        profiler = NullProfiler()
    p = profiler.start('iterate')
    advance_functions = get_advance_functions(network=network, population=population,
      infections=infections,
      play_infections=play_infections,
      rngs=rngs,
      nthreads=nthreads,
      profiler=p)
    for advance_function in advance_functions:
        p = p.start(str(advance_function))
        advance_function(network=network, population=population,
          infections=infections,
          play_infections=play_infections,
          rngs=rngs,
          nthreads=nthreads,
          profiler=p)
        p = p.stop()

    p.stop()