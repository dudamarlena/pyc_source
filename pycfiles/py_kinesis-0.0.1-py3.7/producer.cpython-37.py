# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kinesis/producer.py
# Compiled at: 2019-05-20 19:30:35
# Size of source mod 2**32: 7482 bytes
import asyncio, logging, time, json, objsize
from aiohttp import ClientConnectionError
from asyncio.queues import QueueEmpty
from asyncio_throttle import Throttler
from botocore.exceptions import ClientError
from .base import Base
from . import exceptions
log = logging.getLogger(__name__)

class Producer(Base):

    async def _flush(self):
        while 1:
            await asyncio.sleep((self.buffer_time), loop=(self.loop))
            if not self.is_flushing:
                await self.flush()

    def __init__(self, stream_name, loop=None, endpoint_url=None, region_name=None, buffer_time=0.5, put_rate_limit_per_shard=1000, after_flush_fun=None, batch_size=500, max_queue_size=10000):
        super(Producer, self).__init__(stream_name,
          loop=loop, endpoint_url=endpoint_url, region_name=region_name)
        self.buffer_time = buffer_time
        self.queue = asyncio.Queue(maxsize=max_queue_size, loop=(self.loop))
        self.batch_size = batch_size
        self.put_rate_limit_per_shard = put_rate_limit_per_shard
        self.put_rate_throttle = None
        self.flush_task = asyncio.Task((self._flush()), loop=(self.loop))
        self.is_flushing = False
        self.after_flush_fun = after_flush_fun

    async def create_stream(self, shards=1, ignore_exists=True):
        log.debug('Creating (or ignoring) stream {} with {} shards'.format(self.stream_name, shards))
        if shards < 1:
            raise Exception('Min shard count is one')
        try:
            await self.client.create_stream(StreamName=(self.stream_name),
              ShardCount=shards)
        except ClientError as err:
            try:
                code = err.response['Error']['Code']
                if code == 'ResourceInUseException':
                    raise ignore_exists or exceptions.StreamExists("Stream '{}' exists, cannot create it".format(self.stream_name)) from None
                else:
                    if code == 'LimitExceededException':
                        raise exceptions.StreamShardLimit("Stream '{}' exceeded shard limit".format(self.stream_name))
                    else:
                        raise
            finally:
                err = None
                del err

    def set_put_rate_throttle(self):
        self.put_rate_throttle = Throttler(rate_limit=(self.put_rate_limit_per_shard * len(self.shards)),
          period=1,
          loop=(self.loop))

    async def put(self, data):
        if not self.stream_status == 'ACTIVE':
            await self.start()
            self.set_put_rate_throttle()
        if self.queue.qsize() >= self.batch_size:
            await self.flush()
        data_str = json.dumps(data)
        if len(data_str) > 1048576:
            raise exceptions.ExceededPutLimit('Put of {} bytes exceeded 1MB limit'.format(len(data_str)))
        await self.queue.put(data_str)

    async def close(self):
        self.flush_task.cancel()
        await self.client.close()

    async def flush(self):
        self.is_flushing = True
        overflow = []
        while 1:
            items = []
            num = min(self.batch_size, self.queue.qsize() + len(overflow))
            for _ in range(num):
                async with self.put_rate_throttle:
                    if overflow:
                        items.append(overflow.pop())
                        continue
                    try:
                        items.append(self.queue.get_nowait())
                    except QueueEmpty:
                        break

            if not items:
                break
            log.debug('doing flush with {} items'.format(len(items)))
            try:
                result = await self.client.put_records(Records=[{'Data':item,  'PartitionKey':'{0}{1}'.format(time.clock(), time.time())} for item in items],
                  StreamName=(self.stream_name))
            except ClientError as err:
                try:
                    code = err.response['Error']['Code']
                    if code == 'ValidationException':
                        if 'must have length less than or equal' in err.response['Error']['Message']:
                            log.warning('Batch size {} exceeded the limit. retrying with 10% less'.format(len(items)))
                            overflow = items
                            self.batch_size -= round(self.batch_size / 10)
                            continue
                        else:
                            raise
                    else:
                        if code == 'ResourceNotFoundException':
                            raise exceptions.StreamDoesNotExist("Stream '{}' does not exist".format(self.stream_name)) from None
                        else:
                            raise
                finally:
                    err = None
                    del err

            except ClientConnectionError:
                log.warning('Connection error. sleeping..')
                overflow = items
                await asyncio.sleep(3, loop=(self.loop))
                continue
            else:
                if result['FailedRecordCount']:
                    errors = list(set([r.get('ErrorCode') for r in result['Records'] if r.get('ErrorCode')]))
                    if not errors:
                        raise exceptions.UnknownException('Failed to put records but no errorCodes return in results')
                    elif 'ProvisionedThroughputExceededException' in errors:
                        log.warning('Throughput exceeding, slowing down the rate by 10%')
                        overflow = items
                        self.put_rate_limit_per_shard -= round(self.put_rate_limit_per_shard / 10)
                        self.set_put_rate_throttle()
                        await asyncio.sleep(0.25, loop=(self.loop))
                        continue
                    else:
                        raise exceptions.UnknownException('Failed to put records but not due to throughput exceeded: {}'.format(', '.join(errors)))
                elif self.after_flush_fun:
                    await self.after_flush_fun(items)

        self.is_flushing = False