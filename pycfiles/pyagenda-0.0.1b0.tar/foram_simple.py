# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/conf/foram/foram_simple.py
# Compiled at: 2015-12-21 16:57:03
from pyage.core import address
from pyage.core.statistics import NoStatistics
from pyage.core.stop_condition import StepLimitStopCondition
from pyage.solutions.forams.environment import Environment
from pyage.solutions.forams.foram import create_forams, create_agent
from pyage.solutions.forams.genom import GenomFactory
from pyage.solutions.forams.statistics import PlottingStatistics
from pyage.solutions.forams.thermometer import Thermometer
factory = GenomFactory(chambers_limit=5)
genom_factory = lambda : factory.generate
forams = create_forams(8, initial_energy=5)
agents = create_agent
thermometer = Thermometer
size = lambda : 20
e = None

def environ():
    global e
    if e is None:
        e = Environment()
    return e


environment = environ
stop_condition = lambda : StepLimitStopCondition(100)
address_provider = address.SequenceAddressProvider
stats = PlottingStatistics