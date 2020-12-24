# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webvis/ws_server.py
# Compiled at: 2019-11-05 22:03:55
# Size of source mod 2**32: 991 bytes
import trio
from trio_websocket import serve_websocket, ConnectionClosed

def _print(*args):
    print(*('WebSocket::\t', ), *args)


def stop():
    print('Stopping ws not yet implemented')


async def ws_serve(addr, port, handler_func):

    async def server(request):
        ws = await request.accept()
        while True:
            try:
                message = await ws.get_message()
                resp = handler_func(message)
                resp = str(resp)
                await ws.send_message(resp)
            except ConnectionClosed:
                _print('Connection closed')
                break

    await serve_websocket(server, addr, port, ssl_context=None)
    _print('Websocket terminates')


def start_server(addr, port, handler_func=None):
    print(f"Starting ws server at {addr}:{port}")
    trio.run(ws_serve, addr, port, handler_func)


def main():
    start_server('127.0.0.1', 8000)


if __name__ == '__main__':
    main()