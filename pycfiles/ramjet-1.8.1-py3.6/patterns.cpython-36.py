# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/ramjet/patterns.py
# Compiled at: 2017-11-06 21:55:06
# Size of source mod 2**32: 795 bytes
from abc import abstractmethod
from ramjet.settings import logger as base_logger

class BaseWorker(object):

    def __init__(self, logger=None):
        self.logger = logger or base_logger

    @abstractmethod
    def gen_docu(self):
        pass

    def filter(self, docu):
        return docu

    @abstractmethod
    def worker(self, docu):
        pass

    def close(self):
        pass

    def done(self):
        pass

    def run(self):
        self.logger.debug('run BaseChecker')
        for docu in self.gen_docu():
            self.logger.debug('check docu {}'.format(docu))
            docu = self.filter(docu)
            if docu:
                self.worker(docu)

        self.logger.info('BaseChecker done')
        self.done()

    def __del__(self):
        self.close()