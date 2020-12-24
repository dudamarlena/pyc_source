# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/surfcity/app/net.py
# Compiled at: 2019-04-01 18:24:45
# Size of source mod 2**32: 13398 bytes
import asyncio, base64, hashlib, inspect, json, os, socket, struct, sys, time, traceback
from ssb.rpc.muxrpc import MuxRPCAPI, MuxRPCAPIException, MuxRPCRequest
from ssb.rpc.packet_stream import PacketStream, PSMessage, PSMessageType
from ssb.shs.network import SHSClient, SHSServer
import ssb.local.config, logging
logger = logging.getLogger('ssb_app_net')
api = MuxRPCAPI()
my_feed_id = None
my_feed_send_queue = None

def init(feedID, send_queue):
    global my_feed_id
    global my_feed_send_queue
    my_feed_id = feedID
    my_feed_send_queue = send_queue


async def connect(host, port, feedID, keypair):
    appKey = base64.b64decode('1KHLiKZvAvjbY1ziZEHMXawbCEIM6qwjCDm3VYRan/s=')
    client = SHSClient(host, port, keypair, (base64.b64decode(feedID[1:-8])), application_key=appKey)
    packet_stream = PacketStream(client)
    await client.open()
    s = client.writer._protocol._stream_reader._transport._extra['socket']
    if sys.platform == 'darwin':
        TCP_KEEPALIVE = 16
        s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        s.setsockopt(socket.IPPROTO_TCP, TCP_KEEPALIVE, 2)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 5)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
    else:
        if sys.platform == 'linux':
            s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 2)
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 5)
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
    api.add_connection(packet_stream)
    return api


def disconnect():
    api.connection.disconnect()


async def get_msgs(msgName, limit=1):
    async for reply in api.call('createHistoryStream', [
     {'id':msgName[0], 
      'seq':msgName[1], 
      'limit':limit, 
      'live':False, 
      'keys':True}], 'source'):
        yield reply.data


watch_list = {}

async def do_cb(feedid, handler, cb):
    watch_list[feedid] = handler
    async for reply in handler:
        try:
            cb(reply.data)
        except Exception as e:
            try:
                logger.info('** do_cb: exception %s', str(e))
                logger.info(traceback.format_exc())
            finally:
                e = None
                del e

    del watch_list[feedid]


def start_feed_watching(msgName, cb):
    if msgName[0] in watch_list:
        return
    handler = api.call('createHistoryStream', [
     {'id':msgName[0], 
      'seq':msgName[1], 
      'live':True, 
      'keys':True}], 'source')
    asyncio.ensure_future(do_cb(msgName[0], handler, cb))


async def stop_feed_watching(msgName):
    feedID = msgName[0]
    if feedID not in watch_list:
        return
    handler = watch_list[feedID]
    handler.send(True, end_err=True, req=(-watch_list[feedID].req))


def my_notify(connection, req_msg, m):
    logger.info('app_net: my_notify()')
    a = req_msg.body['args'][0]
    if 'key' in a and a['key']:
        connection.send(m, req=(-req_msg.req))
    else:
        connection.send((m['value']), req=(-req_msg.req))


drainers = {}

async def drain(connection, req):
    while True:
        logger.info('drain loop')
        msg = await my_feed_send_queue.get()
        logger.info('drain loop woke up')
        try:
            connection.send(msg, stream=True, req=(-req))
        except:
            s = traceback.format_exc()
            logger.info(s)


@api.define('createHistoryStream')
def create_history_stream(connection, req_msg, sess=None):
    a = req_msg.body['args'][0]
    logger.info('RECV [%d] createHistoryStream id=%s', req_msg.req, a['id'])
    if not (my_feed_id and a['id'] != my_feed_id or my_feed_send_queue):
        connection.send(True, end_err=True, req=(-req_msg.req))
        return
    lim = -1 if 'limit' not in a else a['limit']
    seqno = 1 if 'sequence' not in a else a['sequence']
    try:
        asyncio.ensure_future(drain(connection, req_msg.req))
    except:
        s = traceback.format_exc()
        logger.info(s)


@api.define('blobs.createWants')
def blobs_createWants(connection, req_msg, sess=None):
    logger.info('** createWants %s', str(req_msg))
    connection.send(True, end_err=True, req=(-req_msg.req))


@api.define('blobs.get')
def blobs_get(connection, req_msg, sess=None):
    a = req_msg.body['args'][0]
    logger.info('RECV [%d] blobs.get %s', req_msg.req, a)
    connection.send(True, end_err=True, req=(-req_msg.req))


async def fetch_blob--- This code section failed: ---

 L. 227         0  LOAD_GLOBAL              logger
                2  LOAD_METHOD              info
                4  LOAD_STR                 'me fetching blob %s'
                6  LOAD_FAST                'id'
                8  CALL_METHOD_2         2  '2 positional arguments'
               10  POP_TOP          

 L. 228        12  LOAD_GLOBAL              bytes
               14  LOAD_CONST               0
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  STORE_FAST               'data'

 L. 229        20  SETUP_LOOP          116  'to 116'
               22  LOAD_GLOBAL              api
               24  LOAD_METHOD              call
               26  LOAD_STR                 'blobs.get'
               28  LOAD_FAST                'id'
               30  BUILD_LIST_1          1 
               32  LOAD_STR                 'source'
               34  CALL_METHOD_3         3  '3 positional arguments'
               36  GET_AITER        
             38_0  COME_FROM            92  '92'
               38  SETUP_EXCEPT         52  'to 52'
               40  GET_ANEXT        
               42  LOAD_CONST               None
               44  YIELD_FROM       
               46  STORE_FAST               'msg'
               48  POP_BLOCK        
               50  JUMP_FORWARD         62  'to 62'
             52_0  COME_FROM_EXCEPT     38  '38'
               52  DUP_TOP          
               54  LOAD_GLOBAL              StopAsyncIteration
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_TRUE    104  'to 104'
               60  END_FINALLY      
             62_0  COME_FROM            50  '50'

 L. 230        62  LOAD_FAST                'msg'
               64  LOAD_ATTR                data
               66  STORE_FAST               'chunk'

 L. 231        68  LOAD_GLOBAL              logger
               70  LOAD_METHOD              debug
               72  LOAD_STR                 'RESP: %d (%d bytes)'
               74  LOAD_FAST                'msg'
               76  LOAD_ATTR                req
               78  LOAD_GLOBAL              len
               80  LOAD_FAST                'chunk'
               82  CALL_FUNCTION_1       1  '1 positional argument'
               84  CALL_METHOD_3         3  '3 positional arguments'
               86  POP_TOP          

 L. 232        88  LOAD_FAST                'msg'
               90  LOAD_ATTR                end_err
               92  POP_JUMP_IF_TRUE     38  'to 38'

 L. 233        94  LOAD_FAST                'data'
               96  LOAD_FAST                'chunk'
               98  INPLACE_ADD      
              100  STORE_FAST               'data'
              102  JUMP_BACK            38  'to 38'
            104_0  COME_FROM            58  '58'
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          
              110  POP_EXCEPT       
              112  POP_TOP          
              114  POP_BLOCK        
            116_0  COME_FROM_LOOP       20  '20'

 L. 234       116  LOAD_GLOBAL              hashlib
              118  LOAD_METHOD              sha256
              120  LOAD_FAST                'data'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  LOAD_METHOD              digest
              126  CALL_METHOD_0         0  '0 positional arguments'
              128  STORE_FAST               'nm'

 L. 235       130  LOAD_STR                 '&'
              132  LOAD_GLOBAL              base64
              134  LOAD_METHOD              b64encode
              136  LOAD_FAST                'nm'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  LOAD_METHOD              decode
              142  LOAD_STR                 'ascii'
              144  CALL_METHOD_1         1  '1 positional argument'
              146  BINARY_ADD       
              148  STORE_FAST               'nm'

 L. 236       150  LOAD_FAST                'nm'
              152  LOAD_FAST                'id'
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   172  'to 172'

 L. 237       158  LOAD_FAST                'sess'
              160  LOAD_ATTR                worm
              162  LOAD_METHOD              writeBlob
              164  LOAD_FAST                'data'
              166  CALL_METHOD_1         1  '1 positional argument'
              168  POP_TOP          
              170  JUMP_FORWARD        190  'to 190'
            172_0  COME_FROM           156  '156'

 L. 239       172  LOAD_GLOBAL              logger
              174  LOAD_METHOD              info
              176  LOAD_STR                 'fetchBlob: mismatch %s (%d bytes)'
              178  LOAD_FAST                'nm'
              180  LOAD_GLOBAL              len
              182  LOAD_FAST                'data'
              184  CALL_FUNCTION_1       1  '1 positional argument'
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          
            190_0  COME_FROM           170  '170'

Parse error at or near `COME_FROM' instruction at offset 38_0


# global drainers ## Warning: Unused global