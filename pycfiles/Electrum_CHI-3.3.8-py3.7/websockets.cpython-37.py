# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/websockets.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 4730 bytes
import threading, os, json
from collections import defaultdict
import asyncio
from typing import Dict, List, Tuple, TYPE_CHECKING
import traceback, sys
try:
    from SimpleWebSocketServer import WebSocket, SimpleSSLWebSocketServer
except ImportError:
    sys.exit('install SimpleWebSocketServer')

from . import bitcoin
from .synchronizer import SynchronizerBase
from .logging import Logger
if TYPE_CHECKING:
    from .network import Network
    from .simple_config import SimpleConfig
request_queue = asyncio.Queue()

class ElectrumWebSocket(WebSocket, Logger):

    def __init__(self):
        WebSocket.__init__(self)
        Logger.__init__(self)

    def handleMessage(self):
        assert self.data[0:3] == 'id:'
        self.logger.info(f"message received {self.data}")
        request_id = self.data[3:]
        asyncio.run_coroutine_threadsafe(request_queue.put((self, request_id)), asyncio.get_event_loop())

    def handleConnected(self):
        self.logger.info(f"connected {self.address}")

    def handleClose(self):
        self.logger.info(f"closed {self.address}")


class BalanceMonitor(SynchronizerBase):

    def __init__(self, config: 'SimpleConfig', network: 'Network'):
        SynchronizerBase.__init__(self, network)
        self.config = config
        self.expected_payments = defaultdict(list)

    def make_request(self, request_id):
        rdir = self.config.get('requests_dir')
        n = os.path.join(rdir, 'req', request_id[0], request_id[1], request_id, request_id + '.json')
        with open(n, encoding='utf-8') as (f):
            s = f.read()
        d = json.loads(s)
        addr = d.get('address')
        amount = d.get('amount')
        return (addr, amount)

    async def main(self):
        for addr in self.expected_payments:
            await self._add_address(addr)

        while True:
            ws, request_id = await request_queue.get()
            try:
                addr, amount = self.make_request(request_id)
            except Exception:
                self.logger.exception('')
                continue

            self.expected_payments[addr].append((ws, amount))
            await self._add_address(addr)

    async def _on_address_status(self, addr, status):
        self.logger.info(f"new status for addr {addr}")
        sh = bitcoin.address_to_scripthash(addr)
        balance = await self.network.get_balance_for_scripthash(sh)
        for ws, amount in self.expected_payments[addr]:
            if ws.closed or sum(balance.values()) >= amount:
                ws.sendMessage('paid')


class WebSocketServer(threading.Thread):

    def __init__(self, config: 'SimpleConfig', network: 'Network'):
        threading.Thread.__init__(self)
        self.config = config
        self.network = network
        asyncio.set_event_loop(network.asyncio_loop)
        self.daemon = True
        self.balance_monitor = BalanceMonitor(self.config, self.network)
        self.start()

    def run(self):
        asyncio.set_event_loop(self.network.asyncio_loop)
        host = self.config.get('websocket_server')
        port = self.config.get('websocket_port', 9999)
        certfile = self.config.get('ssl_chain')
        keyfile = self.config.get('ssl_privkey')
        self.server = SimpleSSLWebSocketServer(host, port, ElectrumWebSocket, certfile, keyfile)
        self.server.serveforever()