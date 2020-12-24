# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/housl/workspaces/develop/aiopyramid/aiopyramid/gunicorn/worker.py
# Compiled at: 2015-05-15 11:19:55
# Size of source mod 2**32: 2103 bytes
import asyncio, time, io
from gunicorn.workers.gaiohttp import AiohttpWorker
from aiohttp.wsgi import WSGIServerHttpProtocol
from aiopyramid.helpers import spawn_greenlet, spawn_greenlet_on_scope_error, synchronize

class AiopyramidHttpServerProtocol(WSGIServerHttpProtocol):

    @asyncio.coroutine
    def handle_request(self, message, payload):
        """ Patched from aiohttp. """
        now = time.time()
        if self.readpayload:
            wsgiinput = io.BytesIO()
            wsgiinput.write((yield from payload.read()))
            wsgiinput.seek(0)
            payload = wsgiinput
        else:
            payload.read = synchronize(payload.read)
            payload.read = spawn_greenlet_on_scope_error(payload.read)
        environ = self.create_wsgi_environ(message, payload)
        environ['async.protocol'] = self
        response = self.create_wsgi_response(message)
        riter = yield from spawn_greenlet(self.wsgi, environ, response.start_response)
        resp = response.response
        try:
            for item in riter:
                if isinstance(item, asyncio.Future):
                    item = yield from item
                yield from resp.write(item)

            yield from resp.write_eof()
        finally:
            if hasattr(riter, 'close'):
                riter.close()

        if resp.keep_alive():
            self.keep_alive(True)
        self.log_access(message, environ, response.response, time.time() - now)


class AsyncGunicornWorker(AiohttpWorker):

    def factory(self, wsgi, *args):
        proto = AiopyramidHttpServerProtocol(wsgi, loop=self.loop, readpayload=True, log=self.log, keep_alive=self.cfg.keepalive, access_log=self.log.access_log, access_log_format=self.cfg.access_log_format)
        return self.wrap_protocol(proto)