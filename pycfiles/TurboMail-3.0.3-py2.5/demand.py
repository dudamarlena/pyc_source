# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/turbomail/managers/demand.py
# Compiled at: 2009-08-26 20:48:43
"""On-demand threaded queue manager.

Worker threads are spawned based on demand at the time a message is added to the queue."""
import copy, logging, math
from Queue import Queue, Empty
from threading import Event, Thread
from turbomail.api import Manager
from turbomail.exceptions import TransportExhaustedException
from turbomail.control import interface
__all__ = [
 'load']
log = logging.getLogger('turbomail.manager')

def load():
    return DemandManager()


class DemandManager(Manager):
    name = 'demand'

    def __init__(self):
        log.info('Demand manager starting up.')
        super(DemandManager, self).__init__()
        self.pool = 0
        self.queue = Queue()
        self.finished = Event()
        self.threads = interface.config.get('mail.demand.threads', 4)
        self.divisor = interface.config.get('mail.demand.divisor', 10)
        self.timeout = interface.config.get('mail.demand.timeout', 60)
        log.info('Demand manager ready.')

    def stop(self):
        log.info('Demand manager shutting down.')
        self.finished.set()

    def spawn(self):
        thread = Thread(target=self.wrapper)
        thread.start()
        self.pool += 1

    def deliver(self, message):
        log.info('Adding message %s to the queue for background delivery.' % message.id)
        self.queue.put(copy.deepcopy(message))
        message._processed = True
        message._dirty = True
        if not self.queue.empty() and self.pool < self.optimum:
            tospawn = int(self.optimum - self.pool)
            log.debug('Spawning %d thread%s.' % (tospawn, tospawn != 1 and 's' or ''))
            for i in range(tospawn):
                self.spawn()

        return True

    def wrapper(self):
        log.debug('Mail queue worker starting up.')
        try:
            self.worker()
        except:
            log.exception('Internal error in worker thread.')

        self.pool -= 1
        log.debug('Mail queue worker finished.')

    def worker(self):
        log.debug('Requesting new transport instance from.')
        transport = self.get_new_transport()
        while True:
            try:
                message = self.queue.get(True, self.timeout)
                transport.deliver(message)
            except Empty:
                log.debug('Worker death from starvation.')
                break
            except TransportExhaustedException:
                log.debug('Worker death from transport exhaustion - spawning child.')
                self.deliver(message)
                self.spawn()
                break
            except:
                log.exception('Delivery of message %s failed.' % message.id)
                break
            else:
                log.info('Delivery of message %s successful or deferred.' % message.id)

        transport.stop()

    def optimum(self):
        return min(self.threads, math.ceil(self.queue.qsize() / float(self.divisor)))

    optimum = property(optimum)