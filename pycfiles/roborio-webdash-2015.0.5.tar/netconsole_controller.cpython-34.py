# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/christian/PycharmProjects/RoboRIO-webdash/webdash/netconsole_controller.py
# Compiled at: 2015-02-09 09:55:06
# Size of source mod 2**32: 3021 bytes
import asyncio
from aiohttp import web, errors as weberrors
import socket, threading, atexit, sys, time
from queue import Queue, Empty
UDP_IN_PORT = 6666
UDP_OUT_PORT = 6668
received_logs = list()
log_store_limit = 200
log_resend_limit = 25

@asyncio.coroutine
def netconsole_monitor():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', UDP_IN_PORT))

    def atexit_func():
        sock.close()

    atexit.register(atexit_func)
    sock_queue = Queue()

    def enqueue_output_sock(s, q):
        while True:
            q.put(s.recv(4096))

    sock_reader = threading.Thread(target=enqueue_output_sock, args=(sock, sock_queue))
    sock_reader.daemon = True
    sock_reader.start()
    while True:
        try:
            msg = str(sock_queue.get_nowait(), 'utf-8')
        except Empty:
            pass
        else:
            try:
                process_log(msg)
            except web.WSClientDisconnectedError as exc:
                print(exc.code, exc.message)
                return

            yield from asyncio.sleep(0.05)


def process_log(message):
    log_data = {'message': message,  'timestamp': time.monotonic()}
    received_logs.append(log_data)
    while len(received_logs) > log_store_limit:
        received_logs.remove(received_logs[0])

    for websocket in websocket_connections[:]:
        try:
            websocket.send_str(message)
        except weberrors.ClientDisconnectedError or weberrors.WSClientDisconnectedError:
            pass


websocket_connections = list()

@asyncio.coroutine
def netconsole_websocket(request):
    websocket = web.WebSocketResponse()
    websocket.start(request)
    websocket_id = len(websocket_connections)
    websocket_connections.append(websocket)
    start_id = min(len(received_logs), log_resend_limit)
    for log in received_logs[-start_id:]:
        websocket.send_str(log['message'])

    print('NC Websocket {} Connected'.format(websocket_id))
    yield from netconsole_websocket_keepalive(websocket)
    print('NC Websocket {} Disonnected'.format(websocket_id))
    return websocket


@asyncio.coroutine
def netconsole_websocket_keepalive(ws):
    while True:
        try:
            data = yield from ws.receive_str()
        except Exception:
            websocket_connections.remove(ws)
            return

        print(data)


@asyncio.coroutine
def netconsole_log_dump(request):
    print('Dumping logs to request.')
    data = '\n'.join(l['message'] for l in received_logs)
    return web.Response(body=data.encode('utf-8'))