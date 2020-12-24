# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mailer/transport/mock.py
# Compiled at: 2019-09-13 21:23:39
# Size of source mod 2**32: 1894 bytes
import random
from marrow.mailer.exc import TransportFailedException, TransportExhaustedException
from marrow.util.bunch import Bunch
__all__ = [
 'MockTransport']
log = __import__('logging').getLogger(__name__)

class MockTransport(object):
    __doc__ = 'A no-op dummy transport.\n    \n    Accepts two configuration directives:\n    \n     * success - probability of successful delivery\n     * failure - probability of failure\n     * exhaustion - probability of exhaustion\n    \n    All are represented as percentages between 0.0 and 1.0, inclusive.\n    (Setting failure or exhaustion to 1.0 means every delivery will fail\n    badly; do not do this except under controlled, unit testing scenarios!)\n    '
    __slots__ = ('ephemeral', 'config')

    def __init__(self, config):
        base = {'success':1.0, 
         'failure':0.0,  'exhaustion':0.0}
        base.update(dict(config))
        self.config = Bunch(base)

    def startup(self):
        pass

    def deliver(self, message):
        """Concrete message delivery."""
        config = self.config
        success = config.success
        failure = config.failure
        exhaustion = config.exhaustion
        if getattr(message, 'die', False):
            1 / 0
        if failure:
            chance = random.randint(0, 100001) / 100000.0
            if chance < failure:
                raise TransportFailedException('Mock failure.')
        if exhaustion:
            chance = random.randint(0, 100001) / 100000.0
            if chance < exhaustion:
                raise TransportExhaustedException('Mock exhaustion.')
        if success == 1.0:
            return True
        chance = random.randint(0, 100001) / 100000.0
        if chance <= success:
            return True
        return False

    def shutdown(self):
        pass