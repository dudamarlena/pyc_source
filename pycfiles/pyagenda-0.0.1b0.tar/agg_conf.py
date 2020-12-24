# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/conf/agg_conf.py
# Compiled at: 2015-12-21 16:57:03
import Pyro4
from pyage.core import address
from pyage.core.agent import agents_factory, aggregate_agents_factory
from pyage.core.locator import RandomLocator
from pyage.core.migration import Pyro4Migration
from pyage.core.statistics import SimpleStatistics
from pyage.solutions.evolution.crossover import AverageCrossover
from pyage.solutions.evolution.evaluation import RastriginEvaluation
from pyage.solutions.evolution.initializer import PointInitializer
from pyage.solutions.evolution.mutation import UniformPointMutation
from pyage.solutions.evolution.selection import TournamentSelection
agents = aggregate_agents_factory('aggregate')
aggregated_agents = agents_factory('max', 'makz', 'm', 'a')
step_limit = lambda : 100
size = 50
operators = lambda : [RastriginEvaluation(), TournamentSelection(25, tournament_size=20),
 AverageCrossover(size=size), UniformPointMutation(0.4, 100)]
initializer = lambda : PointInitializer(size, -10, 1000)
address_provider = address.HashAddressProvider
migration = Pyro4Migration
locator = RandomLocator
ns_hostname = lambda : '10.22.112.235'
pyro_daemon = Pyro4.Daemon(ns_hostname())
daemon = lambda : pyro_daemon
stats = SimpleStatistics