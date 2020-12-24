# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aioetcd3/lease.py
# Compiled at: 2018-05-26 21:48:07
# Size of source mod 2**32: 3252 bytes
from aioetcd3._etcdv3 import rpc_pb2 as rpc
from aioetcd3.base import StubMixin
import functools, inspect, asyncio, aioetcd3._etcdv3.rpc_pb2_grpc as stub

def call_grpc(request, response_func, method):

    def _f(f):

        @functools.wraps(f)
        async def call(self, *args, **kwargs):
            params = (inspect.getcallargs)(f, self, *args, **kwargs)
            params.pop('self')
            r = await self.grpc_call(method(self), request(**params))
            return response_func(r, client=self)

        return call

    return _f


class RLease(object):

    def __init__(self, ttl, id, client):
        self.ttl = ttl
        self.id = id
        self.client = client

    async def __aenter__(self):
        lease = await self.client.grant_lease(ttl=(self.ttl))
        self.ttl = lease.ttl
        self.id = lease.id
        refresh_ttl = self.ttl // 2

        async def task(cycle):
            while True:
                await asyncio.sleep(cycle)
                await self.refresh()

        self.refresh_task = asyncio.ensure_future(task(refresh_ttl))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'refresh_task'):
            self.refresh_task.cancel()
            asyncio.wait(self.refresh_task)
        await self.revoke()

    async def revoke(self):
        return await self.client.revoke_lease(self.id)

    async def refresh(self):
        return await self.client.refresh_lease(self.id)

    async def info(self):
        return await self.client.get_lease_info(self.id)


class Lease(StubMixin):

    def _update_channel(self, channel):
        super()._update_channel(channel)
        self._lease_stub = stub.LeaseStub(channel)

    @call_grpc(lambda ttl, id: rpc.LeaseGrantRequest(TTL=ttl, ID=id), lambda r, client: RLease(r.TTL, r.ID, client), lambda s: s._lease_stub.LeaseGrant)
    async def grant_lease(self, ttl, id=0):
        pass

    def grant_lease_scope(self, ttl, id=0):
        return RLease(ttl, id, self)

    @call_grpc(lambda lease: rpc.LeaseRevokeRequest(ID=(get_lease_id(lease))), lambda r, client: None, lambda s: s._lease_stub.LeaseRevoke)
    async def revoke_lease(self, lease):
        pass

    async def refresh_lease--- This code section failed: ---

 L.  83         0  LOAD_GLOBAL              get_lease_id
                2  LOAD_FAST                'lease'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'lease_id'

 L.  84         8  LOAD_GLOBAL              rpc
               10  LOAD_ATTR                LeaseKeepAliveRequest
               12  LOAD_FAST                'lease_id'
               14  LOAD_CONST               ('ID',)
               16  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               18  STORE_FAST               'lease_request'

 L.  86        20  LOAD_CODE                <code_object generate_request>
               22  LOAD_STR                 'Lease.refresh_lease.<locals>.generate_request'
               24  MAKE_FUNCTION_0          ''
               26  STORE_FAST               'generate_request'

 L.  90        28  LOAD_CONST               None
               30  STORE_FAST               'new_lease'

 L.  91        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _lease_stub
               36  LOAD_ATTR                LeaseKeepAlive
               38  LOAD_ATTR                with_scope
               40  LOAD_FAST                'generate_request'
               42  LOAD_FAST                'lease_request'
               44  CALL_FUNCTION_1       1  ''
               46  CALL_FUNCTION_1       1  ''
               48  BEFORE_ASYNC_WITH
               50  GET_AWAITABLE    
               52  LOAD_CONST               None
               54  YIELD_FROM       
               56  SETUP_ASYNC_WITH    144  'to 144'
               58  STORE_FAST               'result'

 L.  92        60  SETUP_LOOP          140  'to 140'
               62  LOAD_FAST                'result'
               64  GET_AITER        
               66  LOAD_CONST               None
               68  YIELD_FROM       
               70  SETUP_EXCEPT         84  'to 84'
               72  GET_ANEXT        
               74  LOAD_CONST               None
               76  YIELD_FROM       
               78  STORE_FAST               'r'
               80  POP_BLOCK        
               82  JUMP_FORWARD        106  'to 106'
             84_0  COME_FROM_EXCEPT     70  '70'
               84  DUP_TOP          
               86  LOAD_GLOBAL              StopAsyncIteration
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   104  'to 104'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          
               98  POP_EXCEPT       
              100  POP_BLOCK        
              102  JUMP_ABSOLUTE       140  'to 140'
              104  END_FINALLY      
            106_0  COME_FROM            82  '82'

 L.  93       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _update_cluster_info
              110  LOAD_FAST                'r'
              112  LOAD_ATTR                header
              114  CALL_FUNCTION_1       1  ''
              116  POP_TOP          

 L.  94       118  LOAD_GLOBAL              RLease
              120  LOAD_FAST                'r'
              122  LOAD_ATTR                TTL
              124  LOAD_FAST                'r'
              126  LOAD_ATTR                ID
              128  LOAD_FAST                'self'
              130  CALL_FUNCTION_3       3  ''
              132  STORE_FAST               'new_lease'
              134  JUMP_BACK            70  'to 70'
              136  POP_BLOCK        
              138  JUMP_ABSOLUTE       140  'to 140'
            140_0  COME_FROM_LOOP       60  '60'
              140  POP_BLOCK        
              142  LOAD_CONST               None
            144_0  COME_FROM_ASYNC_WITH    56  '56'
              144  WITH_CLEANUP_START
              146  GET_AWAITABLE    
              148  LOAD_CONST               None
              150  YIELD_FROM       
              152  WITH_CLEANUP_FINISH
              154  END_FINALLY      

 L.  96       156  LOAD_FAST                'new_lease'
              158  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 138

    @call_grpc(lambda lease: rpc.LeaseTimeToLiveRequest(ID=(get_lease_id(lease)), keys=True), lambda r, client: (RLease(r.TTL, r.ID, client),
     [k for k in r.keys]) if r.TTL >= 0 else (None, []), lambda s: s._lease_stub.LeaseTimeToLive)
    async def get_lease_info(self, lease):
        pass


def get_lease_id(lease):
    if hasattr(lease, 'id'):
        return lease.id
    else:
        return lease