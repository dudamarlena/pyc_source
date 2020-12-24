# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage_forams/conf/foram_pt.py
# Compiled at: 2014-09-04 18:42:17
from pyage.core import address
from pyage.core.stop_condition import StepLimitStopCondition
from pyage_forams.solutions.environment import environment_factory, Environment3d
from pyage_forams.solutions.foram import create_forams, create_agent
from pyage_forams.solutions.genom import GenomFactory
from pyage_forams.solutions.insolation_meter import StaticInsolation, DynamicInsolation
from pyage_forams.solutions.statistics import SimpleStatistics, PsiStatistics
factory = GenomFactory(chambers_limit=5)
genom_factory = lambda : factory.generate
forams = create_forams(8, initial_energy=5)
agents = create_agent
insolation_meter = lambda : StaticInsolation(surface_insolation=5, insolation_factor=0.1)
size = lambda : 60
reproduction_minimum = lambda : 35
movement_energy = lambda : 0.15
growth_minimum = lambda : 15
energy_need = lambda : 0.5
algae_limit = lambda : 100000000
newborn_limit = lambda : 29
initial_algae_probability = lambda : 0.3
environment = environment_factory(regeneration_factor=0.5, clazz=Environment3d)
stop_condition = lambda : StepLimitStopCondition(290)
address_provider = address.SequenceAddressProvider
stats = SimpleStatistics