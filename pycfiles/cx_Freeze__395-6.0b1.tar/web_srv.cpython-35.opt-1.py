# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \.\cx_Freeze\samples\importlib\web_srv.py
# Compiled at: 2019-08-29 22:24:38
# Size of source mod 2**32: 1370 bytes
__doc__ = 'Example for aiohttp.web basic server\n'
import textwrap
from aiohttp import web

async def intro(request):
    txt = textwrap.dedent('        Type {url}/hello/John  {url}/simple or {url}/change_body\n        in browser url bar\n    ').format(url='127.0.0.1:8080')
    binary = txt.encode('utf8')
    resp = web.StreamResponse()
    resp.content_length = len(binary)
    resp.content_type = 'text/plain'
    await resp.prepare(request)
    await resp.write(binary)
    return resp


async def simple(request):
    return web.Response(text='Simple answer')


async def change_body(request):
    resp = web.Response()
    resp.body = 'Body changed'
    resp.content_type = 'text/plain'
    return resp


async def hello(request):
    resp = web.StreamResponse()
    name = request.match_info.get('name', 'Anonymous')
    answer = ('Hello, ' + name).encode('utf8')
    resp.content_length = len(answer)
    resp.content_type = 'text/plain'
    await resp.prepare(request)
    await resp.write(answer)
    await resp.write_eof()
    return resp


def init():
    app = web.Application()
    app.router.add_get('/', intro)
    app.router.add_get('/simple', simple)
    app.router.add_get('/change_body', change_body)
    app.router.add_get('/hello/{name}', hello)
    app.router.add_get('/hello', hello)
    return app


web.run_app(init())