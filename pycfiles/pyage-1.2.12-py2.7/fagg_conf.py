# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/conf/fagg_conf.py
# Compiled at: 2015-12-21 17:12:57
import logging, os, Pyro4
from pyage.core import address
from pyage.core.agent.agent import generate_agents, unnamed_agents, Agent
from pyage.core.agent.aggregate import AggregateAgent
from pyage.core.locator import RandomLocator
from pyage.core.migration import Pyro4Migration
from pyage.core.statistics import TimeStatistics
from pyage.core.stop_condition import StepLimitStopCondition
from pyage.solutions.evolution.crossover import AverageFloatCrossover
from pyage.solutions.evolution.evaluation import FloatRastriginEvaluation
from pyage.solutions.evolution.initializer import FloatInitializer
from pyage.solutions.evolution.mutation import UniformFloatMutation
from pyage.solutions.evolution.selection import TournamentSelection
logger = logging.getLogger(__name__)
agents_count = int(os.environ['AGENTS'])
logger.debug('AGGREGATE, %s agents', agents_count)
agents = generate_agents('agent', agents_count, AggregateAgent)
aggregated_agents = unnamed_agents(2, Agent)
stop_condition = lambda : StepLimitStopCondition(100)
size = 500
operators = lambda : [FloatRastriginEvaluation(), TournamentSelection(size=55, tournament_size=30),
 AverageFloatCrossover(size=size), UniformFloatMutation(probability=0.05, radius=1)]
initializer = lambda : FloatInitializer(500, size, -10, 10)
address_provider = address.SequenceAddressProvider
migration = Pyro4Migration
locator = RandomLocator
ns_hostname = lambda : os.environ['NS_HOSTNAME']
pyro_daemon = Pyro4.Daemon()
daemon = lambda : pyro_daemon
stats = TimeStatistics