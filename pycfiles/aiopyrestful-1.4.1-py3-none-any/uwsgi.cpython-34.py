# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/housl/workspaces/develop/aiopyramid/aiopyramid/websocket/config/uwsgi.py
# Compiled at: 2015-03-23 14:52:24
# Size of source mod 2**32: 2898 bytes
import inspect, asyncio, greenlet
from aiopyramid.config import AsyncioMapperBase
from aiopyramid.helpers import run_in_greenlet
from aiopyramid.websocket.exceptions import WebsocketClosed
try:
    import uwsgi
except ImportError:
    pass

def uwsgi_recv_msg(g):
    g.has_message = True
    g.switch()


class UWSGIWebsocket:

    def __init__(self, back, q_in, q_out):
        self.back = back
        self.q_in = q_in
        self.q_out = q_out
        self.open = True

    @asyncio.coroutine
    def recv(self):
        return (yield from self.q_in.get())

    @asyncio.coroutine
    def send(self, message):
        yield from self.q_out.put(message)
        self.back.switch()

    @asyncio.coroutine
    def close(self):
        yield from self.q_in.put(None)
        self.back.throw(WebsocketClosed)


class UWSGIWebsocketMapper(AsyncioMapperBase):

    def launch_websocket_view(self, view):

        def websocket_view(context, request):
            uwsgi.websocket_handshake()
            this = greenlet.getcurrent()
            this.has_message = False
            q_in = asyncio.Queue()
            q_out = asyncio.Queue()
            if inspect.isclass(view):
                view_callable = view(context, request)
            else:
                view_callable = view
            ws = UWSGIWebsocket(this, q_in, q_out)
            asyncio.get_event_loop().add_reader(uwsgi.connection_fd(), uwsgi_recv_msg, this)
            future = asyncio.Future()
            asyncio.async(run_in_greenlet(this, future, view_callable, ws))
            this.parent.switch()
            while 1:
                if future.done():
                    raise WebsocketClosed
                if this.has_message:
                    this.has_message = False
                    try:
                        msg = uwsgi.websocket_recv_nb()
                    except OSError:
                        msg = None

                    if msg or msg is None:
                        q_in.put_nowait(msg)
                    if not q_out.empty():
                        msg = q_out.get_nowait()
                        try:
                            uwsgi.websocket_send(msg)
                        except OSError:
                            q_in.put_nowait(None)

                    this.parent.switch()

        return websocket_view

    def __call__(self, view):
        """ Accepts a view_callable class. """
        return self.launch_websocket_view(view)