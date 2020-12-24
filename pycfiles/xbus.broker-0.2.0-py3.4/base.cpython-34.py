# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/broker/core/base.py
# Compiled at: 2016-06-27 03:37:50
# Size of source mod 2**32: 2146 bytes
import aioredis, uuid, asyncio
from aiozmq import rpc
__author__ = 'faide'

class XbusBrokerBase(rpc.AttrHandler):
    __doc__ = 'The XbusBrokerBase is the boilerplate code we need for both our\n    broker front and broker back (ie: initialize redis etc...)\n    '

    def __init__(self, db, loop=None):
        self.db = db
        self.loop = loop
        self.redis_pool = None
        super(rpc.AttrHandler, self).__init__()

    @asyncio.coroutine
    def prepare_redis(self, redis_host, redis_port):
        self.redis_pool = yield from aioredis.create_pool((
         redis_host, redis_port), loop=self.loop)

    @staticmethod
    def new_token() -> str:
        return uuid.uuid4().hex

    @staticmethod
    def new_envelope() -> str:
        return uuid.uuid4().hex

    @staticmethod
    def new_event() -> str:
        return uuid.uuid4().hex

    @asyncio.coroutine
    def save_key(self, key: str, info: str) -> bool:
        """Save a key with some data into Redis.
        """
        try:
            with (yield from self.redis_pool) as (conn):
                yield from conn.set(key, info)
        except (aioredis.ReplyError, aioredis.ProtocolError):
            return False

        return True

    @asyncio.coroutine
    def get_key_info(self, key: str) -> str:
        """Retrieve data about a key from Redis, or None if unavailable.
        """
        try:
            with (yield from self.redis_pool) as (conn):
                info = yield from conn.get(key)
        except (aioredis.ReplyError, aioredis.ProtocolError):
            return

        if info is None:
            return
        return info.decode('utf-8')

    @asyncio.coroutine
    def destroy_key(self, key: str) -> bool:
        try:
            with (yield from self.redis_pool) as (conn):
                yield from conn.delete(key)
        except (aioredis.ReplyError, aioredis.ProtocolError):
            return False

        return True