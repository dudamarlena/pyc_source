# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mailer/manager/futures.py
# Compiled at: 2019-09-13 21:23:39
# Size of source mod 2**32: 2950 bytes
from functools import partial
from marrow.mailer.exc import TransportFailedException, TransportExhaustedException, MessageFailedException, DeliveryFailedException
from marrow.mailer.manager.util import TransportPool
try:
    from concurrent import futures
except ImportError:
    raise ImportError('You must install the futures package to use background delivery.')

__all__ = [
 'FuturesManager']
log = __import__('logging').getLogger(__name__)

def worker(pool, message):
    result = None
    while True:
        with pool() as (transport):
            try:
                result = transport.deliver(message)
            except MessageFailedException as e:
                try:
                    raise DeliveryFailedException(message, e.args[0] if e.args else 'No reason given.')
                finally:
                    e = None
                    del e

            except TransportFailedException:
                transport.ephemeral = True
                continue
            except TransportExhaustedException:
                transport.ephemeral = True

        break

    return (
     message, result)


class FuturesManager(object):
    __slots__ = ('workers', 'executor', 'transport')

    def __init__(self, config, transport):
        self.workers = config.get('workers', 1)
        self.executor = None
        self.transport = TransportPool(transport)
        super(FuturesManager, self).__init__()

    def startup(self):
        log.info('Futures delivery manager starting.')
        log.debug('Initializing transport queue.')
        self.transport.startup()
        workers = self.workers
        log.debug('Starting thread pool with %d workers.' % (workers,))
        self.executor = futures.ThreadPoolExecutor(workers)
        log.info('Futures delivery manager ready.')

    def deliver(self, message):
        return self.executor.submit(partial(worker, self.transport), message)

    def shutdown(self, wait=True):
        log.info('Futures delivery manager stopping.')
        log.debug('Stopping thread pool.')
        self.executor.shutdown(wait=wait)
        log.debug('Draining transport queue.')
        self.transport.shutdown()
        log.info('Futures delivery manager stopped.')