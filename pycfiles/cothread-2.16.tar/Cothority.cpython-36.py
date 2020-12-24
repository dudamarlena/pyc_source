# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/site-packages/cothority/Cothority.py
# Compiled at: 2017-05-19 03:15:52
# Size of source mod 2**32: 2294 bytes
import os, sys
sys.path.append(os.path.dirname(__file__))
import asyncio, websockets
from status import status_pb2
from skipchain import skipchain_pb2

async def getStatusAsync--- This code section failed: ---

 L.  13         0  LOAD_GLOBAL              websockets
                2  LOAD_ATTR                connect
                4  LOAD_FAST                'url'
                6  LOAD_STR                 '/Status/Request'
                8  BINARY_ADD       
               10  CALL_FUNCTION_1       1  ''
               12  BEFORE_ASYNC_WITH
               14  GET_AWAITABLE    
               16  LOAD_CONST               None
               18  YIELD_FROM       
               20  SETUP_ASYNC_WITH     92  'to 92'
               22  STORE_FAST               'websocket'

 L.  14        24  LOAD_GLOBAL              status_pb2
               26  LOAD_ATTR                Request
               28  CALL_FUNCTION_0       0  ''
               30  STORE_FAST               'request'

 L.  15        32  LOAD_FAST                'request'
               34  LOAD_ATTR                SerializeToString
               36  CALL_FUNCTION_0       0  ''
               38  STORE_FAST               'out'

 L.  16        40  LOAD_FAST                'websocket'
               42  LOAD_ATTR                send
               44  LOAD_FAST                'out'
               46  CALL_FUNCTION_1       1  ''
               48  GET_AWAITABLE    
               50  LOAD_CONST               None
               52  YIELD_FROM       
               54  POP_TOP          

 L.  18        56  LOAD_FAST                'websocket'
               58  LOAD_ATTR                recv
               60  CALL_FUNCTION_0       0  ''
               62  GET_AWAITABLE    
               64  LOAD_CONST               None
               66  YIELD_FROM       
               68  STORE_FAST               'stat'

 L.  19        70  LOAD_GLOBAL              status_pb2
               72  LOAD_ATTR                Response
               74  CALL_FUNCTION_0       0  ''
               76  STORE_FAST               'status'

 L.  20        78  LOAD_FAST                'status'
               80  LOAD_ATTR                ParseFromString
               82  LOAD_FAST                'stat'
               84  CALL_FUNCTION_1       1  ''
               86  POP_TOP          

 L.  21        88  LOAD_FAST                'status'
               90  RETURN_VALUE     
             92_0  COME_FROM_ASYNC_WITH    20  '20'
               92  WITH_CLEANUP_START
               94  GET_AWAITABLE    
               96  LOAD_CONST               None
               98  YIELD_FROM       
              100  WITH_CLEANUP_FINISH
              102  END_FINALLY      

Parse error at or near `WITH_CLEANUP_FINISH' instruction at offset 100


def getStatus(url):
    return asyncio.get_event_loop.run_until_complete(getStatusAsync(url))


async def getBlocksAsync--- This code section failed: ---

 L.  27         0  LOAD_GLOBAL              websockets
                2  LOAD_ATTR                connect
                4  LOAD_FAST                'url'
                6  LOAD_STR                 '/Skipchain/GetBlocks'
                8  BINARY_ADD       
               10  CALL_FUNCTION_1       1  ''
               12  BEFORE_ASYNC_WITH
               14  GET_AWAITABLE    
               16  LOAD_CONST               None
               18  YIELD_FROM       
               20  SETUP_ASYNC_WITH    106  'to 106'
               22  STORE_FAST               'websocket'

 L.  28        24  LOAD_GLOBAL              skipchain_pb2
               26  LOAD_ATTR                GetBlocksRequest
               28  CALL_FUNCTION_0       0  ''
               30  STORE_FAST               'request'

 L.  29        32  LOAD_FAST                'block_start'
               34  LOAD_FAST                'request'
               36  STORE_ATTR               Start

 L.  30        38  LOAD_FAST                'block_end'
               40  LOAD_FAST                'request'
               42  STORE_ATTR               End

 L.  31        44  LOAD_FAST                'max_height'
               46  LOAD_FAST                'request'
               48  STORE_ATTR               MaxHeight

 L.  32        50  LOAD_FAST                'websocket'
               52  LOAD_ATTR                send
               54  LOAD_FAST                'request'
               56  LOAD_ATTR                SerializeToString
               58  CALL_FUNCTION_0       0  ''
               60  CALL_FUNCTION_1       1  ''
               62  GET_AWAITABLE    
               64  LOAD_CONST               None
               66  YIELD_FROM       
               68  POP_TOP          

 L.  34        70  LOAD_FAST                'websocket'
               72  LOAD_ATTR                recv
               74  CALL_FUNCTION_0       0  ''
               76  GET_AWAITABLE    
               78  LOAD_CONST               None
               80  YIELD_FROM       
               82  STORE_FAST               'reply'

 L.  35        84  LOAD_GLOBAL              skipchain_pb2
               86  LOAD_ATTR                GetBlocksResponse
               88  CALL_FUNCTION_0       0  ''
               90  STORE_FAST               'block_reply'

 L.  36        92  LOAD_FAST                'block_reply'
               94  LOAD_ATTR                ParseFromString
               96  LOAD_FAST                'reply'
               98  CALL_FUNCTION_1       1  ''
              100  POP_TOP          

 L.  37       102  LOAD_FAST                'block_reply'
              104  RETURN_VALUE     
            106_0  COME_FROM_ASYNC_WITH    20  '20'
              106  WITH_CLEANUP_START
              108  GET_AWAITABLE    
              110  LOAD_CONST               None
              112  YIELD_FROM       
              114  WITH_CLEANUP_FINISH
              116  END_FINALLY      

Parse error at or near `WITH_CLEANUP_FINISH' instruction at offset 114


def getBlocks(url, block_start, block_end='', max_height=1):
    return asyncio.get_event_loop.run_until_complete(getBlocksAsync(url, block_start, block_end, max_height)).Reply


async def storeBlockAsync--- This code section failed: ---

 L.  44         0  LOAD_GLOBAL              websockets
                2  LOAD_ATTR                connect
                4  LOAD_FAST                'url'
                6  LOAD_STR                 '/Skipchain/StoreSkipBlock'
                8  BINARY_ADD       
               10  CALL_FUNCTION_1       1  ''
               12  BEFORE_ASYNC_WITH
               14  GET_AWAITABLE    
               16  LOAD_CONST               None
               18  YIELD_FROM       
               20  SETUP_ASYNC_WITH    100  'to 100'
               22  STORE_FAST               'websocket'

 L.  45        24  LOAD_GLOBAL              skipchain_pb2
               26  LOAD_ATTR                StoreSkipBlockRequest
               28  CALL_FUNCTION_0       0  ''
               30  STORE_FAST               'request'

 L.  46        32  LOAD_FAST                'request'
               34  LOAD_ATTR                NewBlock
               36  LOAD_ATTR                CopyFrom
               38  LOAD_FAST                'block'
               40  CALL_FUNCTION_1       1  ''
               42  POP_TOP          

 L.  47        44  LOAD_FAST                'websocket'
               46  LOAD_ATTR                send
               48  LOAD_FAST                'request'
               50  LOAD_ATTR                SerializeToString
               52  CALL_FUNCTION_0       0  ''
               54  CALL_FUNCTION_1       1  ''
               56  GET_AWAITABLE    
               58  LOAD_CONST               None
               60  YIELD_FROM       
               62  POP_TOP          

 L.  49        64  LOAD_FAST                'websocket'
               66  LOAD_ATTR                recv
               68  CALL_FUNCTION_0       0  ''
               70  GET_AWAITABLE    
               72  LOAD_CONST               None
               74  YIELD_FROM       
               76  STORE_FAST               'reply'

 L.  50        78  LOAD_GLOBAL              skipchain_pb2
               80  LOAD_ATTR                StoreSkipBlockResponse
               82  CALL_FUNCTION_0       0  ''
               84  STORE_FAST               'block_reply'

 L.  51        86  LOAD_FAST                'block_reply'
               88  LOAD_ATTR                ParseFromString
               90  LOAD_FAST                'reply'
               92  CALL_FUNCTION_1       1  ''
               94  POP_TOP          

 L.  52        96  LOAD_FAST                'block_reply'
               98  RETURN_VALUE     
            100_0  COME_FROM_ASYNC_WITH    20  '20'
              100  WITH_CLEANUP_START
              102  GET_AWAITABLE    
              104  LOAD_CONST               None
              106  YIELD_FROM       
              108  WITH_CLEANUP_FINISH
              110  END_FINALLY      

Parse error at or near `WITH_CLEANUP_FINISH' instruction at offset 108


def storeBlock(url, block):
    ret = asyncio.get_event_loop.run_until_complete(storeBlockAsync(url, block))
    return (
     ret.Previous, ret.Latest)


def createNextBlock(last, data):
    block = skipchain_pb2.SkipBlock
    if last.GenesisID == '':
        block.GenesisID = last.Hash
    else:
        block.GenesisID = last.GenesisID
    block.Data = data
    block.Index = last.Index + 1
    block.Roster.CopyFrom(last.Roster)
    return block