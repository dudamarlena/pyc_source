# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/server/extensions/rate_limit/manager.py
# Compiled at: 2016-09-14 12:38:35
# Size of source mod 2**32: 2663 bytes
"""
A custom manager that manages the shared rate limit counters
"""
import logging, multiprocessing, time
from multiprocessing.managers import BaseManager
logger = logging.getLogger(__name__)

class RateLimitCounters:
    __doc__ = '\n    Counters for rate limiting of DHCPv6 requests\n    '

    def __init__(self, rate: int, per: int, burst: int=None):
        self.counters = {}
        self.rate_per_second = rate / per
        self.burst = burst or rate

    def check_request(self, key: str) -> bool:
        """
        Check whether this request is within limits. This method uses the algorithm described on
        http://stackoverflow.com/questions/667508/whats-a-good-rate-limiting-algorithm#668327

        :param key: The key for this client
        :return: Whether we should allow this
        """
        global logger
        now = time.time()
        allowance, last_check = self.counters.setdefault(key, (self.burst, now))
        time_passed = now - last_check
        allowance += time_passed * self.rate_per_second
        if allowance > self.burst:
            allowance = self.burst
        logger.debug('{}: {} allowance = {:0.2f}'.format(multiprocessing.current_process().name, key, allowance))
        if allowance < 1:
            allow = False
        else:
            allow = True
            allowance -= 1
        self.counters[key] = (
         allowance, now)
        return allow


def init_manager_process(parent_logger, initializer=None, initargs=()):
    """
    Migrate the logger of the parent to the child. It will be a queue logger anyway.

    :param parent_logger: The logger from the parent
    :param initializer: Optional extra initializer
    :param initargs: Optional initializer arguments
    """
    global logger
    logger = parent_logger
    if initializer:
        initializer(*initargs)


class RateLimitManager(BaseManager):
    __doc__ = '\n    A custom manager that manages the shared rate limit counters\n    '

    def start(self, initializer=None, initargs=()):
        """
        Start the rate limit counter manager
        """
        super().start(initializer=init_manager_process, initargs=(logger,))


RateLimitManager.register('RateLimitCounters', RateLimitCounters)