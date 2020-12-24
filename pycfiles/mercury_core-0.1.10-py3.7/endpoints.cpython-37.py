# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/common/asyncio/endpoints.py
# Compiled at: 2018-01-22 15:39:21
# Size of source mod 2**32: 1567 bytes
"""
async_endpoints is a singleton, allowing dispatch endpoints to be
specified using a decorator. Controllers can define endpoints any way
they see fit. This is here for convenience only.

For an example usage, see mercury.inventory.controller.InventoryController
"""
import inspect, logging
from mercury.common.exceptions import MercuryClientException
log = logging.getLogger(__name__)
async_endpoints = dict()

def async_endpoint(name):

    def add(f):
        log.debug('Adding async runtime endpoint {} ({})'.format(f.__name__, name))
        if not inspect.iscoroutinefunction(f):
            log.error('{} is not a coroutine'.format(f.__name__))
        else:
            if name in async_endpoints:
                log.error('{} already exists in table'.format(name))
            else:
                async_endpoints[name] = f
        return f

    return add


class StaticEndpointController(object):
    __doc__ = 'Use this if you want to be lazy'

    def __init__(self):
        self.endpoints = async_endpoints

    @staticmethod
    def get_key(key, d):
        try:
            return d[key]
        except KeyError:
            raise MercuryClientException('{} is missing from request'.format(key))

    @staticmethod
    def validate_required(required, data):
        missing = []
        for key in required:
            if key not in data:
                missing.append(key)

        if missing:
            raise MercuryClientException('Message is missing required data: {}'.format(missing))