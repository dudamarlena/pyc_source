# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sldap3\core\instance.py
# Compiled at: 2015-04-22 18:09:30
"""
"""
import logging
from .. import EXEC_PROCESS, EXEC_THREAD
from .. import NATIVE_ASYNCIO
from time import sleep
if NATIVE_ASYNCIO:
    import asyncio
else:
    import trollius as asyncio
    from trollius import From, Return

class Instance(object):

    def __init__(self, dsa, name=None, executor=EXEC_THREAD):
        self.dsa = dsa
        self.dsa.instance = self
        self.loop = None
        self.name = self.dsa.name if not name else name
        if executor == EXEC_THREAD:
            from threading import Thread
            self.executor = Thread(target=self.dsa.start)
        elif executor == EXEC_PROCESS:
            from multiprocessing import Process
            self.executor = Process(target=self.dsa.start)
        else:
            raise Exception('unknown executor')
        self.started = False
        return

    def start(self):
        if not self.started:
            logging.info('starting instance %s' % self.name)
            self.executor.start()
            self.started = True

    def stop(self):
        if self.started:
            logging.info('stopping instance %s' % self.name)
            self.dsa.stop()
            logging.debug('stopping loop for instance %s' % self.name)
            self.loop.call_soon_threadsafe(self.loop.stop)
            logging.debug('closing loop for instance %s' % self.name)
            while self.loop.is_running():
                logging.debug('waiting for Instance %s loop to stop' % self.name)
                sleep(0.2)

            self.loop.call_soon_threadsafe(self.loop.close)
            logging.info('Instance %s loop halted and closed' % self.name)
            logging.debug('waiting for instance %s executor to join' % self.name)
            self.executor.join()
            logging.debug('instance %s joined' % self.name)
            self.started = False
            logging.info('stopped instance %s' % self.name)