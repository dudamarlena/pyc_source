# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/paul/Documents/projects/poolhub/poolhub/server/server.py
# Compiled at: 2017-04-11 08:14:05
# Size of source mod 2**32: 1589 bytes
import asyncio, threading, socketio, aiohttp, aiohttp.web, aiohttp_cors
from aiohttp import web
from ..frontend.utils import launch_index_page
from ..threads.threadsAPI import API

def start_server():
    """Should be run a different thread"""
    sio = socketio.AsyncServer(async_mode='aiohttp')

    @sio.on('update')
    async def update_threads(sid, message):
        thread_tree = threads_api.report_threads()
        await sio.emit('reply', room=sid, data={'threads': thread_tree})

    async def terminate_thread(request):
        data = await request.json()
        ident = data['ident']
        response = threads_api.terminate_thread(ident)
        return web.Response(text=response)

    threads_api = API()
    t = threading.Thread(name='PoolHub Watcher', target=threads_api.watch_threads, daemon=True)
    t.start()

    def init_app():
        app = web.Application()
        app.router.add_put('/terminateThread', terminate_thread)
        cors = aiohttp_cors.setup(app, defaults={'*': aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers='*', allow_headers='*')})
        for route in list(app.router.routes()):
            cors.add(route)

        return app

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = init_app()
    sio.attach(app)
    launch_index_page()
    aiohttp.web.run_app(app, port=9876)