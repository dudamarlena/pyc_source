# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage_conf/emas_migration.py
# Compiled at: 2015-12-21 16:57:02
import logging, os, Pyro4
from pyage.core import address
from pyage.core.agent.agent import unnamed_agents
from pyage.core.agent.aggregate import AggregateAgent
from pyage.core.emas import EmasService
from pyage.core.locator import RowLocator
from pyage.core.stop_condition import StepLimitStopCondition
from pyage.solutions.evolution.crossover import SinglePointCrossover
from pyage.solutions.evolution.evaluation import FloatRastriginEvaluation
from pyage.solutions.evolution.initializer import float_emas_initializer
from pyage.solutions.evolution.mutation import UniformFloatMutation
from pyage_conf.migration import CountingPyro4Migration
from pyage_conf.stats import MigrationNotificationStatistics
logger = logging.getLogger(__name__)
agents_count = int(os.environ['AGENTS'])
logger.debug('EMAS, %s agents', agents_count)
agents = unnamed_agents(agents_count, AggregateAgent)
stop_condition = lambda : StepLimitStopCondition(500)
aggregated_agents = lambda : float_emas_initializer(int(os.environ['DIMS']), energy=100, size=50, lowerbound=-10, upperbound=10)
emas = EmasService
minimal_energy = lambda : 0
reproduction_minimum = lambda : 90
migration_minimum = lambda : 120
newborn_energy = lambda : 100
transferred_energy = lambda : 40
evaluation = FloatRastriginEvaluation
crossover = SinglePointCrossover
mutation = lambda : UniformFloatMutation(probability=1, radius=1)
address_provider = address.SequenceAddressProvider
migration_probability = lambda : float(os.environ['PR'])
migration = CountingPyro4Migration
locator = RowLocator
ns_hostname = lambda : os.environ['NS_HOSTNAME']
pyro_daemon = Pyro4.Daemon()
daemon = lambda : pyro_daemon
notification_url = lambda : 'http://student.agh.edu.pl/~kmaciej/pyage.php'
stats = MigrationNotificationStatistics