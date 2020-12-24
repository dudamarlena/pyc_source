# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchm8/__init__.py
# Compiled at: 2017-09-11 10:07:09
from . import watchers
from . import actions

class Watchm8(object):

    def __init__(self, config):
        self._config = config
        from logging import getLogger
        self._jobs = []
        self._log = getLogger('Watchm8')
        self._stop_watchm8 = False

    def start(self):
        from .factories.job import job_factory
        self._log.info('Starting ...')
        for job in self._config['jobs']:
            self._jobs.append(job_factory(job))

        self._log.debug('Created jobs')
        self.run()

    def run(self):
        from time import sleep
        self._log.debug('Starting jobs')
        for job in self._jobs:
            job.start()

        self._log.info('Started.')
        while not self._stop_watchm8:
            sleep(3)

        self._log.info('Stopping ...')
        for job in self._jobs:
            job.stop()

        for job in self._jobs:
            job.join()

        self._log.info('Stopped.')

    def stop(self):
        self._stop_watchm8 = True