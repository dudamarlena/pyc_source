# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/common/adhoc/disconnect.py
# Compiled at: 2018-01-29 12:10:54
# Size of source mod 2**32: 1339 bytes
import asyncio, logging, zmq.asyncio
from mercury.common.asyncio.transport import AsyncRouterReqService
log = logging.getLogger('disconnect')
logging.basicConfig(level=(logging.DEBUG))

class WorkService(AsyncRouterReqService):

    async def process(self, message):
        if message['action'] == 'sleep':
            await asyncio.sleep(15)
            log.debug('Slept')
            return {'message': 'I slept'}
        if message['action'] == 'fast':
            log.debug('Fast')
            return {'message': 'I was fast'}
        if message['action'] == 'self-destruct':
            for i in reversed(range(6)):
                log.info('Self-destructing in t-minus {} seconds'.format(i))
                await asyncio.sleep(1)

            raise Exception('Have a nice day!')


loop = zmq.asyncio.ZMQEventLoop()
loop.set_debug(True)
asyncio.set_event_loop(loop)
service = WorkService('tcp://0.0.0.0:9090', linger=0)
try:
    try:
        loop.run_until_complete(service.start())
    except KeyboardInterrupt:
        log.info('Shutting down')
        service.kill()

finally:
    pending = asyncio.Task.all_tasks(loop=loop)
    log.debug('Waiting on {} pending tasks'.format(len(pending)))
    loop.run_until_complete((asyncio.gather)(*pending))
    log.debug('Shutting down event loop')
    loop.close()