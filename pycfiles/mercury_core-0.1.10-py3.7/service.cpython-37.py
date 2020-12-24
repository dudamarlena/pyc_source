# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/rpc/service.py
# Compiled at: 2018-02-05 11:44:36
# Size of source mod 2**32: 3759 bytes
import asyncio, logging, zmq.asyncio
from mercury.common.asyncio.clients.inventory import InventoryClient
from mercury.common.asyncio import transport, dispatcher
from mercury.rpc.controller import RPCController
from mercury.rpc.jobs.monitor import Monitor
from mercury.rpc.mongo import init_rpc_collections
from mercury.rpc.options import parse_options
log = logging.getLogger(__name__)

class RPCService(transport.AsyncRouterReqService):

    def __init__(self, bind_address, inventory_client, jobs_collection, tasks_collection):
        super(RPCService, self).__init__(bind_address)
        controller = RPCController(inventory_client, jobs_collection, tasks_collection)
        self.dispatcher = dispatcher.AsyncDispatcher(controller)

    async def process(self, message):
        return await self.dispatcher.dispatch(message)


def configure_logging(config):
    """ Configure logging for application
    :param config: A namespace provided from MercuryConfiguration.parse_args
    """
    logging.basicConfig(level=(logging.getLevelName(config.logging.level)), format=(config.logging.format))
    if config.subtask_debug:
        logging.getLogger('mercury.rpc.jobs.monitor').setLevel(logging.DEBUG)


def main():
    config = parse_options()
    configure_logging(config)
    loop = zmq.asyncio.ZMQEventLoop()
    loop.set_debug(config.asyncio_debug)
    asyncio.set_event_loop(loop)
    collections = init_rpc_collections(servers=(config.rpc.database.servers),
      database=(config.rpc.database.name),
      jobs_collection=(config.rpc.database.jobs_collection),
      tasks_collection=(config.rpc.database.tasks_collection),
      replica_name=(config.rpc.database.replica_name),
      username=(config.rpc.database.username),
      password=(config.rpc.database.password),
      use_asyncio=True)
    inventory_client = InventoryClient((config.rpc.inventory_router),
      linger=10,
      response_timeout=5,
      rcv_retry=3)
    collections.jobs_collection.create_index('ttl_time_completed', expireAfterSeconds=3600)
    collections.tasks_collection.create_index('ttl_time_completed', expireAfterSeconds=3600)
    monitor = Monitor((collections.jobs_collection), (collections.tasks_collection), loop=loop)
    asyncio.ensure_future((monitor.loop()), loop=loop)
    service = RPCService(config.rpc.bind_address, inventory_client, collections.jobs_collection, collections.tasks_collection)
    log.info('Starting Mercury Backend Service')
    try:
        try:
            loop.run_until_complete(service.start())
        except KeyboardInterrupt:
            log.info('Sending kill signals')
            monitor.kill()
            service.kill()

    finally:
        pending = asyncio.Task.all_tasks(loop=loop)
        log.debug('Waiting on {} pending tasks'.format(len(pending)))
        loop.run_until_complete((asyncio.gather)(*pending))
        log.debug('Shutting down event loop')
        loop.close()


if __name__ == '__main__':
    main()