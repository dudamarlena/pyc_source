# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mailer/manager/immediate.py
# Compiled at: 2019-09-13 21:23:39
# Size of source mod 2**32: 2318 bytes
from marrow.mailer.exc import TransportExhaustedException, TransportFailedException, DeliveryFailedException, MessageFailedException
from marrow.mailer.manager.util import TransportPool
__all__ = [
 'ImmediateManager']
log = __import__('logging').getLogger(__name__)

class ImmediateManager(object):
    __slots__ = ('transport', )

    def __init__(self, config, Transport):
        self.transport = TransportPool(Transport)
        super(ImmediateManager, self).__init__()

    def startup(self):
        """Perform startup actions.
        
        This just chains down to the transport layer.
        """
        log.info('Immediate delivery manager starting.')
        log.debug('Initializing transport queue.')
        self.transport.startup()
        log.info('Immediate delivery manager started.')

    def deliver(self, message):
        result = None
        while True:
            with self.transport() as (transport):
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

    def shutdown(self):
        log.info('Immediate delivery manager stopping.')
        log.debug('Draining transport queue.')
        self.transport.shutdown()
        log.info('Immediate delivery manager stopped.')