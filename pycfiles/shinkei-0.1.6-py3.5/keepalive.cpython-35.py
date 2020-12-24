# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shinkei/keepalive.py
# Compiled at: 2019-12-14 12:45:46
# Size of source mod 2**32: 1978 bytes
import asyncio, concurrent, logging, threading, time
try:
    import ujson as json
except ImportError:
    import json

log = logging.getLogger(__name__)

class KeepAlivePls(threading.Thread):

    def __init__(self, *args, **kwargs):
        self.ws = kwargs.pop('ws')
        self.interval = self.ws.hb_interval
        super().__init__(*args, **kwargs)
        self.daemon = True
        self.stop_event = threading.Event()
        self._last_ack = time.perf_counter()
        self._last_send = time.perf_counter()
        self.latency = float('inf')

    def run(self):
        data = json.dumps({'op': self.ws.OP_HEARTBEAT, 
         'd': {'client_id': self.ws.client_id}})
        while not self.stop_event.wait(self.interval):
            future = asyncio.run_coroutine_threadsafe(self.ws.send(data), loop=self.ws.loop)
            try:
                total = 0
                while True:
                    try:
                        log.debug('Sending heartbeat for client with id %s', self.ws.client_id)
                        future.result(timeout=5)
                        break
                    except concurrent.futures.TimeoutError:
                        total += 5
                        log.warning('Heartbeat blocked for more then %s', total)

            except Exception:
                self.stop()
            else:
                self._last_send = time.perf_counter()

    def stop(self):
        self.stop_event.set()

    def ack(self):
        self._last_ack = time.perf_counter()
        self.latency = self._last_ack - self._last_send
        log.debug('Acked heartbeat for client with id %s', self.ws.client_id)
        if self.latency > 10:
            log.warning('Websocket is %.1fs behind.', self.latency)