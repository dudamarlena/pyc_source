# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/cothority/websocket.py
# Compiled at: 2017-05-18 05:04:29
# Size of source mod 2**32: 952 bytes
import asyncio, websockets, status_pb2

async def getStatus(url):
    async with websockets.connect(url + '/Status/Request') as websocket:
        request = status_pb2.Request()
        out = request.SerializeToString()
        await websocket.send(out)
        print('> {}'.format(out))
        stat = await websocket.recv()
        status = status_pb2.Response()
        status.ParseFromString(stat)
        print('< {}'.format(status))


async def getBlocks(url):
    async with websockets.connect(url + '/Status/Request') as websocket:
        request = status_pb2.Request()
        out = request.SerializeToString()
        await websocket.send(out)
        print('> {}'.format(out))
        stat = await websocket.recv()
        status = status_pb2.Response()
        status.ParseFromString(stat)
        print('< {}'.format(status))


asyncio.get_event_loop().run_until_complete(getStatus('ws://dedis.ch:7003'))