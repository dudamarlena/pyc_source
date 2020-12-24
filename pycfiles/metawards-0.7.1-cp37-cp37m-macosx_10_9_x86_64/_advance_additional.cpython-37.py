# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/GitHub/MetaWards/build/lib.macosx-10.9-x86_64-3.7/metawards/iterators/_advance_additional.py
# Compiled at: 2020-04-17 13:53:44
# Size of source mod 2**32: 4322 bytes
from .._network import Network
from .._population import Population
from utils._profiler import Profiler
__all__ = [
 'setup_additional_seeds',
 'advance_additional',
 'advance_additional_omp']

def _load_additional_seeds(filename: str):
    """Load additional seeds from the passed filename. This returns
       the added seeds
    """
    print(f"Loading additional seeds from {filename}...")
    with open(filename, 'r') as (FILE):
        line = FILE.readline()
        seeds = []
        while line:
            words = line.split()
            seeds.append((int(words[0]), int(words[2]), int(words[1])))
            print(seeds[(-1)])
            line = FILE.readline()

    return seeds


_additional_seeds = None

def setup_additional_seeds(network: Network, profiler: Profiler, **kwargs):
    """Setup function that reads in the additional seeds held
       in `params.additional_seeds` and puts them ready to
       be used by `advance_additional` to import additional
       infections at specified times in specified wards
       during the outbreak

       Parameters
       ----------
       network: Network
         The network to be seeded
       profiler: Profiler
         Profiler used to profile this function
       kwargs
         Arguments that are not used by this setup function
    """
    global _additional_seeds
    params = network.params
    p = profiler.start('load_additional_seeds')
    _additional_seeds = []
    if params.additional_seeds is not None:
        for additional in params.additional_seeds:
            _additional_seeds += _load_additional_seeds(additional)

    p = p.stop()


def advance_additional(network: Network, population: Population, infections, play_infections, profiler: Profiler, **kwargs):
    """Advance the infection by infecting additional wards based
       on a pre-determined pattern based on the additional seeds

       Parameters
       ----------
       network: Network
         The network being modelled
       population: Population
         The population experiencing the outbreak - also contains the day
         of the outbreak
       infections
         Space to hold the 'work' infections
       play_infections
         Space to hold the 'play' infections
       profiler: Profiler
         Used to profile this function
       kwargs
         Arguments that aren't used by this advancer
    """
    wards = network.nodes
    p = profiler.start('additional_seeds')
    for seed in _additional_seeds:
        if seed[0] == population.day:
            if wards.play_suscept[seed[1]] < seed[2]:
                print('Not enough susceptibles in ward for seeding')
            else:
                wards.play_suscept[seed[1]] -= seed[2]
                print(f"seeding play_infections[0][{seed[1]}] += {seed[2]}")
                play_infections[0][seed[1]] += seed[2]

    p.stop()


def advance_additional_omp(**kwargs):
    """Advance the infection by infecting additional wards based
       on a pre-determined pattern based on the additional seeds
       (parallel version)

       Parameters
       ----------
       network: Network
         The network being modelled
       population: Population
         The population experiencing the outbreak - also contains the day
         of the outbreak
       infections
         Space to hold the 'work' infections
       play_infections
         Space to hold the 'play' infections
       profiler: Profiler
         Used to profile this function
       kwargs
         Arguments that aren't used by this advancer
    """
    kwargs['nthreads'] = 1
    advance_additional(**kwargs)