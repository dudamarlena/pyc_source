# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage_forams/conf/distributed3d/common.py
# Compiled at: 2014-11-03 18:13:03
import Pyro4
from pyage.core import address
from pyage.core.stop_condition import StepLimitStopCondition
from pyage_forams.solutions.distributed.neighbour_matcher import Neighbour3dMatcher
from pyage_forams.solutions.distributed.request import create_dispatcher
from pyage_forams.solutions.environment import environment_factory, Environment3d
from pyage_forams.solutions.foram import create_forams
from pyage_forams.solutions.genom import GenomFactory
from pyage_forams.solutions.insolation_meter import StaticInsolation
from pyage_forams.solutions.statistics import MultipleStatistics, PsiStatistics, CsvStatistics
factory = GenomFactory(chambers_limit=5)
genom_factory = lambda : factory.generate
forams = create_forams(1, initial_energy=5)
insolation_meter = StaticInsolation
size = lambda : 50
reproduction_minimum = lambda : 50
movement_energy = lambda : 0.5
growth_minimum = lambda : 30
energy_need = lambda : 0.2
algae_limit = lambda : 20
algae_growth_probability = lambda : 0.3
newborn_limit = lambda : 6
reproduction_probability = lambda : 0.5
growth_probability = lambda : 0.5
growth_cost_factor = lambda : 0.8
capacity_factor = lambda : 1.1
initial_algae_probability = lambda : 0.2
environment = environment_factory(regeneration_factor=0.1, clazz=Environment3d)
stop_condition = lambda : StepLimitStopCondition(500)
stats = lambda : MultipleStatistics([CsvStatistics(), PsiStatistics()])
cell_capacity = lambda : 1
address_provider = address.SequenceAddressProvider
request_dispatcher = create_dispatcher()
neighbour_matcher = Neighbour3dMatcher
ns_hostname = lambda : '127.0.0.1'
pyro_daemon = Pyro4.Daemon()
daemon = lambda : pyro_daemon