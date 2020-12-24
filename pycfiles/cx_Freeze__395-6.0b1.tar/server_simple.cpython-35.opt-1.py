# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \.\cx_Freeze\samples\importlib\server_simple.py
# Compiled at: 2019-08-29 22:24:38
# Size of source mod 2**32: 752 bytes
from aiohttp import web

async def handle(request):
    name = request.match_info.get('name', 'Anonymous')
    text = 'Hello, ' + name
    return web.Response(text=text)


async def wshandle(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
            await ws.send_str('Hello, {}'.format(msg.data))
        else:
            if msg.type == web.WSMsgType.BINARY:
                await ws.send_bytes(msg.data)
            elif msg.type == web.WSMsgType.CLOSE:
                break

    return ws


app = web.Application()
app.add_routes([web.get('/', handle),
 web.get('/echo', wshandle),
 web.get('/{name}', handle)])
web.run_app(app)