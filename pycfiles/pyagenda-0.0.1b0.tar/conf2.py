# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/conf/conf2.py
# Compiled at: 2015-12-21 16:57:02
import Pyro4
from pyage.core import address
from pyage.core.agent import agents_factory
from pyage.core.locator import Pyro4Locator
from pyage.core.migration import NoMigration
from pyage.core.statistics import SimpleStatistics
from pyage.solutions.evolution.crossover import AverageCrossover
from pyage.solutions.evolution.evaluation import RastriginEvaluation
from pyage.solutions.evolution.initializer import PointInitializer
from pyage.solutions.evolution.mutation import UniformPointMutation
from pyage.solutions.evolution.selection import TournamentSelection
agents = agents_factory('makz')
step_limit = lambda : 100
makz__operators = lambda : [
 RastriginEvaluation(), TournamentSelection(size=2, tournament_size=2),
 AverageCrossover(size=4), UniformPointMutation()]
initializer = lambda : PointInitializer(4, 0, 100)
address_provider = address.HashAddressProvider
migration = NoMigration
locator = Pyro4Locator
pyro_daemon = Pyro4.Daemon()
daemon = lambda : pyro_daemon
ns_hostname = lambda : '192.168.0.103'
stats = SimpleStatistics