# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/olxbr/BarterDude/barterdude/hooks/healthcheck.py
# Compiled at: 2020-04-29 12:15:10
# Size of source mod 2**32: 2720 bytes
import json
from barterdude import BarterDude
from barterdude.hooks import HttpHook
from asyncworker.rabbitmq.message import RabbitMQMessage
from aiohttp import web
from time import time
from collections import deque
from bisect import bisect_left

def _remove_old(instants: deque, old_timestamp: float):
    pos = bisect_left(instants, old_timestamp)
    for i in range(0, pos):
        instants.popleft()

    return len(instants)


def _response(status, body):
    body['status'] = 'ok' if status == 200 else 'fail'
    return web.Response(status=status, body=(json.dumps(body)))


class Healthcheck(HttpHook):

    def __init__(self, barterdude, path='/healthcheck', success_rate=0.95, health_window=60.0, max_connection_fails=3):
        self._Healthcheck__success_rate = success_rate
        self._Healthcheck__health_window = health_window
        self._Healthcheck__success = deque()
        self._Healthcheck__fail = deque()
        self._Healthcheck__force_fail = False
        self._Healthcheck__connection_fails = 0
        self._Healthcheck__max_connection_fails = max_connection_fails
        super(Healthcheck, self).__init__(barterdude, path)

    def force_fail(self):
        self._Healthcheck__force_fail = True

    async def before_consume(self, message: RabbitMQMessage):
        pass

    async def on_success(self, message: RabbitMQMessage):
        self._Healthcheck__success.append(time())

    async def on_fail(self, message: RabbitMQMessage, error: Exception):
        self._Healthcheck__fail.append(time())

    async def on_connection_fail(self, error: Exception, retries: int):
        self._Healthcheck__connection_fails = retries

    async def __call__(self, req: web.Request):
        if self._Healthcheck__force_fail:
            return _response(500, {'message': 'Healthcheck fail called manually'})
        else:
            if self._Healthcheck__connection_fails >= self._Healthcheck__max_connection_fails:
                return _response(500, {'message': f"Reached max connection fails ({self._Healthcheck__max_connection_fails})"})
            old_timestamp = time() - self._Healthcheck__health_window
            success = _remove_old(self._Healthcheck__success, old_timestamp)
            fail = _remove_old(self._Healthcheck__fail, old_timestamp)
            if success == 0:
                if fail == 0:
                    return _response(200, {'message': f"No messages in last {self._Healthcheck__health_window}s"})
            rate = success / (success + fail)
            return _response(200 if rate >= self._Healthcheck__success_rate else 500, {'message':f"Success rate: {rate} (expected: {self._Healthcheck__success_rate})", 
             'fail':fail, 
             'success':success})