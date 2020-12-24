# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/iterators/_advance_additional.py
# Compiled at: 2020-05-10 15:00:16
# Size of source mod 2**32: 6221 bytes
from typing import Union as _Union
from .._network import Network
from .._networks import Networks
from .._population import Population
from utils._profiler import Profiler
from .._infections import Infections
__all__ = [
 'setup_additional_seeds',
 'advance_additional',
 'advance_additional_serial',
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
            words = line.strip().split()
            if len(words) == 0:
                line = FILE.readline()
                continue
            elif len(words) == 4:
                seeds.append((int(words[0]), int(words[2]),
                 int(words[1]), words[3]))
            else:
                seeds.append((int(words[0]), int(words[2]),
                 int(words[1]), None))
            print(seeds[(-1)])
            line = FILE.readline()

    return seeds


_additional_seeds = None

def setup_additional_seeds(network: _Union[(Network, Networks)], profiler: Profiler, **kwargs):
    """Setup function that reads in the additional seeds held
       in `params.additional_seeds` and puts them ready to
       be used by `advance_additional` to import additional
       infections at specified times in specified wards
       during the outbreak

       Parameters
       ----------
       network: Network or Networks
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


def advance_additional_serial(network: _Union[(Network, Networks)], population: Population, infections: Infections, profiler: Profiler, **kwargs):
    """Advance the infection by infecting additional wards based
       on a pre-determined pattern based on the additional seeds

       Parameters
       ----------
       network: Network or Networks
         The network being modelled
       population: Population
         The population experiencing the outbreak - also contains the day
         of the outbreak
       infections: Infections
         Space to hold the infections
       profiler: Profiler
         Used to profile this function
       kwargs
         Arguments that aren't used by this advancer
    """
    p = profiler.start('additional_seeds')
    for seed in _additional_seeds:
        if seed[0] == population.day:
            ward = seed[1]
            num = seed[2]
            if isinstance(network, Networks):
                demographic = seed[3]
                if demographic is None:
                    demographic = 0
                else:
                    demographic = network.demographics.get_index(demographic)
                wards = network.subnets[demographic].nodes
                play_infections = infections.subinfs[demographic].play
            else:
                demographic = None
                wards = network.nodes
                play_infections = infections.play
            if wards.play_suscept[ward] < num:
                print('Not enough susceptibles in ward for seeding')
            else:
                wards.play_suscept[ward] -= num
                if demographic is not None:
                    print(f"seeding demographic {demographic} play_infections[0][{ward}] += {num}")
                else:
                    print(f"seeding play_infections[0][{ward}] += {num}")
                play_infections[0][ward] += num

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
       infections: Infections
         Space to hold the infections
       profiler: Profiler
         Used to profile this function
       kwargs
         Arguments that aren't used by this advancer
    """
    kwargs['nthreads'] = 1
    advance_additional(**kwargs)


def advance_additional(nthreads, **kwargs):
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
       infections: Infections
         Space to hold the infections
       profiler: Profiler
         Used to profile this function
       kwargs
         Arguments that aren't used by this advancer
    """
    advance_additional_serial(**kwargs)