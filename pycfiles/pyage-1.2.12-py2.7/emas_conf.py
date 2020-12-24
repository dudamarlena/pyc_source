# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/conf/emas_conf.py
# Compiled at: 2015-12-21 16:57:03
import Pyro4
from pyage.core import address
from pyage.core.agent import agents_factory, aggregate_agents_factory
from pyage.core.emas import EmasService
from pyage.core.locator import RandomLocator
from pyage.core.migration import Pyro4Migration
from pyage.core.statistics import SimpleStatistics
from pyage.solutions.evolution.crossover import AverageCrossover
from pyage.solutions.evolution.evaluation import RastriginEvaluation
from pyage.solutions.evolution.initializer import PointInitializer, emas_initializer
from pyage.solutions.evolution.mutation import UniformPointMutation
from pyage.solutions.evolution.selection import TournamentSelection
agents = aggregate_agents_factory('aggregate')
step_limit = lambda : 50
aggregated_agents = lambda : emas_initializer(energy=10, size=100, lowerbound=-100, upperbound=100)
emas = EmasService
minimal_energy = lambda : 2
reproduction_minimum = lambda : 12
migration_minimum = lambda : 12
newborn_energy = lambda : 10
evaluation = RastriginEvaluation
crossover = AverageCrossover
mutation = UniformPointMutation
address_provider = address.HashAddressProvider
migration = Pyro4Migration
locator = RandomLocator
ns_hostname = lambda : '192.168.0.103'
pyro_daemon = Pyro4.Daemon()
daemon = lambda : pyro_daemon
stats = SimpleStatistics