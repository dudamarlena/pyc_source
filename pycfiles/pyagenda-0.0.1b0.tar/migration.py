# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage_conf/migration.py
# Compiled at: 2015-12-21 16:57:02
import logging
from pyage.core.inject import InjectOptional
from pyage.core.migration import Pyro4Migration
logger = logging.getLogger(__name__)

class CountingPyro4Migration(Pyro4Migration):
    counter = 0

    @InjectOptional('migration_probability')
    def __init__(self):
        if hasattr(self, 'migration_probability'):
            probability = self.migration_probability
        else:
            probability = 0.05
        super(CountingPyro4Migration, self).__init__(probability)

    def migrate(self, agent):
        if super(CountingPyro4Migration, self).migrate(agent):
            CountingPyro4Migration.counter += 1