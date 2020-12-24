# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lance/.virtualenvs/wolverine/lib/python3.5/site-packages/examples/ping_pong/service.py
# Compiled at: 2015-10-20 17:43:38
# Size of source mod 2**32: 943 bytes
import asyncio, logging
from wolverine.module.service import ServiceMessage, MicroService
logger = logging.getLogger(__name__)

class PingPongService(MicroService):

    def __init__(self, app, **options):
        self.delay = options.pop('delay', 1)
        self.routing = options.pop('routing', False)
        super(PingPongService, self).__init__(app, 'ping', **options)

    def ping1(self, data):
        logger.debug('--ping1 handler--')
        logger.debug('data: ' + str(data))
        yield from asyncio.sleep(self.delay)
        return data

    def ping(self, data):
        logger.debug('data: ' + str(data))
        yield from asyncio.sleep(self.delay)
        response = ServiceMessage()
        response.data = data
        return response

    def ping2(self, data):
        logger.debug('--ping1 handler--')
        logger.debug('data: ' + str(data))
        yield from asyncio.sleep(self.delay)
        return data