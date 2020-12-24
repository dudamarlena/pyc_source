# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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