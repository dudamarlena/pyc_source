# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/GaPy/event_args.py
# Compiled at: 2019-06-14 11:47:45
# Size of source mod 2**32: 555 bytes
from GaPy.population import *
from typing import List, Set, Dict, Tuple, Optional

class GaEventArgs:

    def __init__(self, population: Population, generation_count: int, evaluation_count: int):
        self.population = population
        self.generation_count = generation_count
        self.evaluation_count = evaluation_count


class CrossoverEventArgs:

    def __init__(self, parents: List[Chromosome], children: List[Chromosome], points: List[int]):
        self.parents = parents
        self.children = children
        self.points = points