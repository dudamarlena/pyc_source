# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/olxbr/BarterDude/barterdude/__init__.py
# Compiled at: 2020-03-20 15:15:22
# Size of source mod 2**32: 3138 bytes
from asyncio import gather
from asyncworker import App, RouteTypes
from asyncworker.options import Options
from asyncworker.connections import AMQPConnection
from asyncworker.rabbitmq.message import RabbitMQMessage
from collections import MutableMapping
from typing import Iterable
from barterdude.monitor import Monitor

class BarterDude(MutableMapping):

    def __init__(self, hostname: str='127.0.0.1', username: str='guest', password: str='guest', prefetch: int=10, connection_name: str='default'):
        self._BarterDude__connection = AMQPConnection(name=connection_name,
          hostname=hostname,
          username=username,
          password=password,
          prefetch=prefetch)
        self._BarterDude__app = App(connections=[self._BarterDude__connection])

    def add_endpoint(self, routes, methods, hook):
        self._BarterDude__app.route(routes=routes,
          methods=methods,
          type=(RouteTypes.HTTP))(hook)

    def consume_amqp(self, queues: Iterable[str], monitor: Monitor=Monitor(), coroutines: int=10, bulk_flush_interval: float=60.0, requeue_on_fail: bool=True):

        def decorator(f):

            async def process_message(message):
                await monitor.dispatch_before_consume(message)
                try:
                    await f(message)
                except Exception as error:
                    await monitor.dispatch_on_fail(message, error)
                    message.reject(requeue_on_fail)
                else:
                    await monitor.dispatch_on_success(message)

            @self._BarterDude__app.route(queues,
              type=(RouteTypes.AMQP_RABBITMQ),
              options={Options.BULK_SIZE: coroutines, 
             Options.BULK_FLUSH_INTERVAL: bulk_flush_interval, 
             Options.CONNECTION_FAIL_CALLBACK: monitor.dispatch_on_connection_fail})
            async def wrapper(messages):
                await gather(*map(process_message, messages))

            return wrapper

        return decorator

    async def publish_amqp(self, exchange: str, data: dict, properties: dict=None, routing_key: str='', **kwargs):
        await (self._BarterDude__connection.put)(exchange=exchange, 
         data=data, 
         properties=properties, 
         routing_key=routing_key, **kwargs)

    async def startup(self):
        await self._BarterDude__app.startup()

    async def shutdown(self):
        await self._BarterDude__app.shutdown()

    def run(self):
        self._BarterDude__app.run()

    def __getitem__(self, key):
        return self._BarterDude__app[key]

    def __setitem__(self, key, value):
        self._BarterDude__app[key] = value

    def __delitem__(self, key):
        del self._BarterDude__app[key]

    def __len__(self):
        return len(self._BarterDude__app)

    def __iter__(self):
        return iter(self._BarterDude__app)