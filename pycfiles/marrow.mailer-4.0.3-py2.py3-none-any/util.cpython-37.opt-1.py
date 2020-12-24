# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mailer/manager/util.py
# Compiled at: 2019-09-13 21:23:39
# Size of source mod 2**32: 2445 bytes
try:
    import queue
except ImportError:
    import Queue as queue

__all__ = [
 'TransportPool']
log = __import__('logging').getLogger(__name__)

class TransportPool(object):
    __slots__ = ('factory', 'transports')

    def __init__(self, factory):
        self.factory = factory
        self.transports = queue.Queue()

    def startup(self):
        pass

    def shutdown(self):
        try:
            while True:
                transport = self.transports.get(False)
                transport.shutdown()

        except queue.Empty:
            pass

    class Context(object):
        __slots__ = ('pool', 'transport')

        def __init__(self, pool):
            self.pool = pool
            self.transport = None

        def __enter__(self):
            pool = self.pool
            transport = None
            while not transport:
                try:
                    transport = pool.transports.get(False)
                    log.debug('Acquired existing transport instance.')
                except queue.Empty:
                    log.debug('Unable to acquire existing transport, initalizing new instance.')
                    transport = pool.factory()
                    transport.startup()

            self.transport = transport
            return transport

        def __exit__(self, type, value, traceback):
            transport = self.transport
            ephemeral = getattr(transport, 'ephemeral', False)
            if type is not None:
                log.error('Shutting down transport due to unhandled exception.', exc_info=True)
                transport.shutdown()
                return
            if not ephemeral:
                log.debug('Scheduling transport instance for re-use.')
                self.pool.transports.put(transport)
            else:
                log.debug('Transport marked as ephemeral, shutting down instance.')
                transport.shutdown()

    def __call__(self):
        return self.Context(self)