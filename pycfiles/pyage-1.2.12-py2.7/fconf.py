# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/conf/fconf.py
# Compiled at: 2015-12-21 17:12:57
import logging, os, Pyro4
from pyage.core import address
from pyage.core.agent import generate_agents, Agent
from pyage.core.locator import Pyro4Locator
from pyage.core.migration import NoMigration
from pyage.core.statistics import SimpleStatistics
from pyage.core.stop_condition import StepLimitStopCondition
from pyage.solutions.evolution.crossover import AverageFloatCrossover
from pyage.solutions.evolution.evaluation import FloatRastriginEvaluation
from pyage.solutions.evolution.initializer import FloatInitializer
from pyage.solutions.evolution.mutation import UniformFloatMutation
from pyage.solutions.evolution.selection import TournamentSelection
logger = logging.getLogger(__name__)
agents_count = int(os.environ['AGENTS'])
logger.debug('EVO, %s agents', agents_count)
agents = generate_agents('agent', agents_count, Agent)
stop_condition = lambda : StepLimitStopCondition(500)
size = 500
operators = lambda : [FloatRastriginEvaluation(), TournamentSelection(size=125, tournament_size=125),
 AverageFloatCrossover(size=size), UniformFloatMutation(probability=0.1, radius=1)]
initializer = lambda : FloatInitializer(500, size, -10, 10)
address_provider = address.SequenceAddressProvider
migration = NoMigration
locator = Pyro4Locator
ns_hostname = lambda : os.environ['NS_HOSTNAME']
pyro_daemon = Pyro4.Daemon()
daemon = lambda : pyro_daemon
stats = SimpleStatistics