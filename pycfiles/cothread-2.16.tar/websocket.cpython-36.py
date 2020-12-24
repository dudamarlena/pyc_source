# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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