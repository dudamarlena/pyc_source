# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/synchronizer.py
# Compiled at: 2019-08-25 06:29:58
# Size of source mod 2**32: 12384 bytes
import asyncio, hashlib
from typing import Dict, List, TYPE_CHECKING, Tuple
from collections import defaultdict
import logging
from aiorpcx import TaskGroup, run_in_thread, RPCError
from .transaction import Transaction
from .util import bh2u, make_aiohttp_session, NetworkJobOnDefaultServer
from .bitcoin import address_to_scripthash, is_address
from .network import UntrustedServerReturnedError
from .logging import Logger
from .interface import GracefulDisconnect
if TYPE_CHECKING:
    from .network import Network
    from .address_synchronizer import AddressSynchronizer

class SynchronizerFailure(Exception):
    pass


def history_status(h):
    if not h:
        return
    status = ''
    for tx_hash, height in h:
        status += tx_hash + ':%d:' % height

    return bh2u(hashlib.sha256(status.encode('ascii')).digest())


class SynchronizerBase(NetworkJobOnDefaultServer):
    __doc__ = 'Subscribe over the network to a set of addresses, and monitor their statuses.\n    Every time a status changes, run a coroutine provided by the subclass.\n    '

    def __init__(self, network: 'Network'):
        self.asyncio_loop = network.asyncio_loop
        NetworkJobOnDefaultServer.__init__(self, network)
        self._reset_request_counters()

    def _reset(self):
        super()._reset()
        self.requested_addrs = set()
        self.scripthash_to_address = {}
        self._processed_some_notifications = False
        self._reset_request_counters()
        self.add_queue = asyncio.Queue()
        self.status_queue = asyncio.Queue()

    async def _start_tasks(self):
        try:
            async with self.group as group:
                await group.spawn(self.send_subscriptions())
                await group.spawn(self.handle_status())
                await group.spawn(self.main())
        finally:
            self.session.unsubscribe(self.status_queue)

    def _reset_request_counters(self):
        self._requests_sent = 0
        self._requests_answered = 0

    def add(self, addr):
        asyncio.run_coroutine_threadsafe(self._add_address(addr), self.asyncio_loop)

    async def _add_address(self, addr: str):
        if not is_address(addr):
            raise ValueError(f"invalid address {addr}")
        if addr in self.requested_addrs:
            return
        self.requested_addrs.add(addr)
        await self.add_queue.put(addr)

    async def _on_address_status(self, addr, status):
        """Handle the change of the status of an address."""
        raise NotImplementedError()

    async def send_subscriptions(self):

        async def subscribe_to_address(addr):
            h = address_to_scripthash(addr)
            self.scripthash_to_address[h] = addr
            self._requests_sent += 1
            try:
                await self.session.subscribe('blockchain.scripthash.subscribe', [h], self.status_queue)
            except RPCError as e:
                try:
                    if e.message == 'history too large':
                        raise GracefulDisconnect(e, log_level=(logging.ERROR)) from e
                    raise
                finally:
                    e = None
                    del e

            self._requests_answered += 1
            self.requested_addrs.remove(addr)

        while True:
            addr = await self.add_queue.get()
            await self.group.spawn(subscribe_to_address, addr)

    async def handle_status(self):
        while True:
            h, status = await self.status_queue.get()
            addr = self.scripthash_to_address[h]
            await self.group.spawn(self._on_address_status, addr, status)
            self._processed_some_notifications = True

    def num_requests_sent_and_answered(self) -> Tuple[(int, int)]:
        return (self._requests_sent, self._requests_answered)

    async def main(self):
        raise NotImplementedError()


class Synchronizer(SynchronizerBase):
    __doc__ = "The synchronizer keeps the wallet up-to-date with its set of\n    addresses and their transactions.  It subscribes over the network\n    to wallet addresses, gets the wallet to generate new addresses\n    when necessary, requests the transaction history of any addresses\n    we don't have the full history of, and requests binary transaction\n    data of any transactions the wallet doesn't have.\n    "

    def __init__(self, wallet: 'AddressSynchronizer'):
        self.wallet = wallet
        SynchronizerBase.__init__(self, wallet.network)

    def _reset(self):
        super()._reset()
        self.requested_tx = {}
        self.requested_histories = set()

    def diagnostic_name(self):
        return self.wallet.diagnostic_name()

    def is_up_to_date(self):
        return not self.requested_addrs and not self.requested_histories and not self.requested_tx

    async def _on_address_status(self, addr, status):
        history = self.wallet.db.get_addr_history(addr)
        if history_status(history) == status:
            return
        if (
         addr, status) in self.requested_histories:
            return
        self.requested_histories.add((addr, status))
        h = address_to_scripthash(addr)
        self._requests_sent += 1
        result = await self.network.get_history_for_scripthash(h)
        self._requests_answered += 1
        self.logger.info(f"receiving history {addr} {len(result)}")
        hashes = set(map(lambda item: item['tx_hash'], result))
        hist = list(map(lambda item: (item['tx_hash'], item['height']), result))
        tx_fees = [(item['tx_hash'], item.get('fee')) for item in result]
        tx_fees = dict(filter(lambda x: x[1] is not None, tx_fees))
        if len(hashes) != len(result):
            self.logger.info(f"error: server history has non-unique txids: {addr}")
        else:
            if history_status(hist) != status:
                self.logger.info(f"error: status mismatch: {addr}")
            else:
                self.wallet.receive_history_callback(addr, hist, tx_fees)
                await self._request_missing_txs(hist)
        self.requested_histories.discard((addr, status))

    async def _request_missing_txs(self, hist, *, allow_server_not_finding_tx=False):
        transaction_hashes = []
        for tx_hash, tx_height in hist:
            if tx_hash in self.requested_tx:
                continue
            if self.wallet.db.get_transaction(tx_hash):
                continue
            transaction_hashes.append(tx_hash)
            self.requested_tx[tx_hash] = tx_height

        if not transaction_hashes:
            return
        async with TaskGroup() as group:
            for tx_hash in transaction_hashes:
                await group.spawn(self._get_transaction(tx_hash, allow_server_not_finding_tx=allow_server_not_finding_tx))

    async def _get_transaction(self, tx_hash, *, allow_server_not_finding_tx=False):
        self._requests_sent += 1
        try:
            try:
                result = await self.network.get_transaction(tx_hash)
            except UntrustedServerReturnedError as e:
                try:
                    if allow_server_not_finding_tx:
                        self.requested_tx.pop(tx_hash)
                        return
                    raise
                finally:
                    e = None
                    del e

        finally:
            self._requests_answered += 1

        tx = Transaction(result)
        try:
            tx.deserialize()
        except Exception as e:
            try:
                raise SynchronizerFailure(f"cannot deserialize transaction {tx_hash}") from e
            finally:
                e = None
                del e

        if tx_hash != tx.txid():
            raise SynchronizerFailure(f"received tx does not match expected txid ({tx_hash} != {tx.txid()})")
        tx_height = self.requested_tx.pop(tx_hash)
        self.wallet.receive_tx_callback(tx_hash, tx, tx_height)
        self.logger.info(f"received tx {tx_hash} height: {tx_height} bytes: {len(tx.raw)}")
        self.wallet.network.trigger_callback('new_transaction', self.wallet, tx)

    async def main(self):
        self.wallet.set_up_to_date(False)
        for addr in self.wallet.db.get_history():
            history = self.wallet.db.get_addr_history(addr)
            if history == ['*']:
                continue
            await self._request_missing_txs(history, allow_server_not_finding_tx=True)

        for addr in self.wallet.get_addresses():
            await self._add_address(addr)

        while 1:
            await asyncio.sleep(0.1)
            await run_in_thread(self.wallet.synchronize)
            up_to_date = self.is_up_to_date()
            if not up_to_date != self.wallet.is_up_to_date():
                if up_to_date:
                    if self._processed_some_notifications:
                        self._processed_some_notifications = False
                        if up_to_date:
                            self._reset_request_counters()
                    self.wallet.set_up_to_date(up_to_date)
                    self.wallet.network.trigger_callback('wallet_updated', self.wallet)


class Notifier(SynchronizerBase):
    __doc__ = 'Watch addresses. Every time the status of an address changes,\n    an HTTP POST is sent to the corresponding URL.\n    '

    def __init__(self, network):
        SynchronizerBase.__init__(self, network)
        self.watched_addresses = defaultdict(list)
        self.start_watching_queue = asyncio.Queue()

    async def main(self):
        for addr in self.watched_addresses:
            await self._add_address(addr)

        while True:
            addr, url = await self.start_watching_queue.get()
            self.watched_addresses[addr].append(url)
            await self._add_address(addr)

    async def _on_address_status(self, addr, status):
        self.logger.info(f"new status for addr {addr}")
        headers = {'content-type': 'application/json'}
        data = {'address':addr,  'status':status}
        for url in self.watched_addresses[addr]:
            try:
                async with make_aiohttp_session(proxy=(self.network.proxy), headers=headers) as session:
                    async with session.post(url, json=data, headers=headers) as resp:
                        await resp.text()
            except Exception as e:
                try:
                    self.logger.info(repr(e))
                finally:
                    e = None
                    del e

            else:
                self.logger.info(f"Got Response for {addr}")