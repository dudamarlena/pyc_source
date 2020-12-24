# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/address_synchronizer.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 35879 bytes
import threading, asyncio, itertools
from collections import defaultdict
from typing import TYPE_CHECKING, Dict, Optional, Set, Tuple
from . import bitcoin
from .bitcoin import COINBASE_MATURITY, TYPE_ADDRESS, TYPE_PUBKEY
from .util import profiler, bfh, TxMinedInfo
from .transaction import Transaction, TxOutput
from .synchronizer import Synchronizer
from .verifier import SPV
from .blockchain import hash_header
from .i18n import _
from .logging import Logger
if TYPE_CHECKING:
    from .network import Network
    from .json_db import JsonDB
TX_HEIGHT_LOCAL = -2
TX_HEIGHT_UNCONF_PARENT = -1
TX_HEIGHT_UNCONFIRMED = 0

class AddTransactionException(Exception):
    pass


class UnrelatedTransactionException(AddTransactionException):

    def __str__(self):
        return _('Transaction is unrelated to this wallet.')


class AddressSynchronizer(Logger):
    __doc__ = '\n    inherited by wallet\n    '

    def __init__(self, db: 'JsonDB'):
        self.db = db
        self.network = None
        Logger.__init__(self)
        self.synchronizer = None
        self.verifier = None
        self.lock = threading.RLock()
        self.transaction_lock = threading.RLock()
        self.unverified_tx = defaultdict(int)
        self.up_to_date = False
        self.threadlocal_cache = threading.local()
        self._get_addr_balance_cache = {}
        self.load_and_cleanup()

    def with_transaction_lock(func):

        def func_wrapper(self, *args, **kwargs):
            with self.transaction_lock:
                return func(self, *args, **kwargs)

        return func_wrapper

    def load_and_cleanup(self):
        self.load_local_history()
        self.check_history()
        self.load_unverified_transactions()
        self.remove_local_transactions_we_dont_have()

    def is_mine(self, address):
        return self.db.is_addr_in_history(address)

    def get_addresses(self):
        return sorted(self.db.get_history())

    def get_address_history(self, addr):
        h = []
        with self.lock:
            with self.transaction_lock:
                related_txns = self._history_local.get(addr, set())
                for tx_hash in related_txns:
                    tx_height = self.get_tx_height(tx_hash).height
                    h.append((tx_hash, tx_height))

        return h

    def get_address_history_len(self, addr: str) -> int:
        """Return number of transactions where address is involved."""
        return len(self._history_local.get(addr, ()))

    def get_txin_address(self, txi):
        addr = txi.get('address')
        if addr:
            if addr != '(pubkey)':
                return addr
        prevout_hash = txi.get('prevout_hash')
        prevout_n = txi.get('prevout_n')
        for addr in self.db.get_txo(prevout_hash):
            l = self.db.get_txo_addr(prevout_hash, addr)
            for n, v, is_cb in l:
                if n == prevout_n:
                    return addr

    def get_txout_address(self, txo: TxOutput):
        if txo.type == TYPE_ADDRESS:
            addr = txo.address
        else:
            if txo.type == TYPE_PUBKEY:
                addr = bitcoin.public_key_to_p2pkh(bfh(txo.address))
            else:
                addr = None
        return addr

    def load_unverified_transactions(self):
        for addr in self.db.get_history():
            hist = self.db.get_addr_history(addr)
            for tx_hash, tx_height in hist:
                self.add_unverified_tx(tx_hash, tx_height)

    def start_network(self, network):
        self.network = network
        if self.network is not None:
            self.synchronizer = Synchronizer(self)
            self.verifier = SPV(self.network, self)
            self.network.register_callback(self.on_blockchain_updated, ['blockchain_updated'])

    def on_blockchain_updated(self, event, *args):
        self._get_addr_balance_cache = {}

    def stop_threads(self):
        if self.network:
            if self.synchronizer:
                asyncio.run_coroutine_threadsafe(self.synchronizer.stop(), self.network.asyncio_loop)
                self.synchronizer = None
            if self.verifier:
                asyncio.run_coroutine_threadsafe(self.verifier.stop(), self.network.asyncio_loop)
                self.verifier = None
            self.network.unregister_callback(self.on_blockchain_updated)
            self.db.put('stored_height', self.get_local_height())

    def add_address(self, address):
        if not self.db.get_addr_history(address):
            self.db.history[address] = []
            self.set_up_to_date(False)
        if self.synchronizer:
            self.synchronizer.add(address)

    def get_conflicting_transactions(self, tx_hash, tx):
        """Returns a set of transaction hashes from the wallet history that are
        directly conflicting with tx, i.e. they have common outpoints being
        spent with tx. If the tx is already in wallet history, that will not be
        reported as a conflict.
        """
        conflicting_txns = set()
        with self.transaction_lock:
            for txin in tx.inputs():
                if txin['type'] == 'coinbase':
                    continue
                prevout_hash = txin['prevout_hash']
                prevout_n = txin['prevout_n']
                spending_tx_hash = self.db.get_spent_outpoint(prevout_hash, prevout_n)
                if spending_tx_hash is None:
                    continue
                assert self.db.get_transaction(spending_tx_hash), 'spending tx not in wallet db'
                conflicting_txns |= {spending_tx_hash}

            if tx_hash in conflicting_txns:
                if len(conflicting_txns) > 1:
                    raise Exception('Found conflicting transactions already in wallet history.')
                conflicting_txns -= {tx_hash}
            return conflicting_txns

    def add_transaction(self, tx_hash, tx, allow_unrelated=False):
        assert tx_hash, tx_hash
        assert tx, tx
        assert tx.is_complete()
        with self.lock:
            with self.transaction_lock:
                is_coinbase = tx.inputs()[0]['type'] == 'coinbase'
                tx_height = self.get_tx_height(tx_hash).height
                if not allow_unrelated:
                    is_mine = any([self.is_mine(self.get_txin_address(txin)) for txin in tx.inputs()])
                    is_for_me = any([self.is_mine(self.get_txout_address(txo)) for txo in tx.outputs()])
                    if not is_mine:
                        if not is_for_me:
                            raise UnrelatedTransactionException()
                conflicting_txns = self.get_conflicting_transactions(tx_hash, tx)
                if conflicting_txns:
                    existing_mempool_txn = any((self.get_tx_height(tx_hash2).height in (TX_HEIGHT_UNCONFIRMED, TX_HEIGHT_UNCONF_PARENT) for tx_hash2 in conflicting_txns))
                    existing_confirmed_txn = any((self.get_tx_height(tx_hash2).height > 0 for tx_hash2 in conflicting_txns))
                    if existing_confirmed_txn:
                        if tx_height <= 0:
                            return False
                    if existing_mempool_txn:
                        if tx_height == TX_HEIGHT_LOCAL:
                            return False
                    to_remove = set()
                    to_remove |= conflicting_txns
                    for conflicting_tx_hash in conflicting_txns:
                        to_remove |= self.get_depending_transactions(conflicting_tx_hash)

                    for tx_hash2 in to_remove:
                        self.remove_transaction(tx_hash2)

                def add_value_from_prev_output():
                    for addr in self.db.get_txo(prevout_hash):
                        outputs = self.db.get_txo_addr(prevout_hash, addr)
                        for n, v, is_cb in outputs:
                            if n == prevout_n:
                                if addr:
                                    if self.is_mine(addr):
                                        self.db.add_txi_addr(tx_hash, addr, ser, v)
                                        self._get_addr_balance_cache.pop(addr, None)
                                return

                for txi in tx.inputs():
                    if txi['type'] == 'coinbase':
                        continue
                    prevout_hash = txi['prevout_hash']
                    prevout_n = txi['prevout_n']
                    ser = prevout_hash + ':%d' % prevout_n
                    self.db.set_spent_outpoint(prevout_hash, prevout_n, tx_hash)
                    add_value_from_prev_output()

                for n, txo in enumerate(tx.outputs()):
                    v = txo.value
                    ser = tx_hash + ':%d' % n
                    addr = self.get_txout_address(txo)
                    if addr and self.is_mine(addr):
                        self.db.add_txo_addr(tx_hash, addr, n, v, is_coinbase)
                        self._get_addr_balance_cache.pop(addr, None)
                        next_tx = self.db.get_spent_outpoint(tx_hash, n)
                        if next_tx is not None:
                            self.db.add_txi_addr(next_tx, addr, ser, v)
                            self._add_tx_to_local_history(next_tx)

                self._add_tx_to_local_history(tx_hash)
                self.db.add_transaction(tx_hash, tx)
                return True

    def queue_transaction(self, tx_hash, tx_queue_item):
        with self.transaction_lock:
            self.db.queued_transactions[tx_hash] = tx_queue_item
        return True

    def unqueue_transaction(self, tx_hash):
        with self.transaction_lock:
            if tx_hash in self.db.queued_transactions:
                del self.db.queued_transactions[tx_hash]
        return True

    def remove_transaction(self, tx_hash):

        def remove_from_spent_outpoints():
            if tx is not None:
                for txin in tx.inputs():
                    if txin['type'] == 'coinbase':
                        continue
                    prevout_hash = txin['prevout_hash']
                    prevout_n = txin['prevout_n']
                    self.db.remove_spent_outpoint(prevout_hash, prevout_n)

            else:
                for prevout_hash, prevout_n in self.db.list_spent_outpoints():
                    spending_txid = self.db.get_spent_outpoint(prevout_hash, prevout_n)
                    if spending_txid == tx_hash:
                        self.db.remove_spent_outpoint(prevout_hash, prevout_n)

        with self.transaction_lock:
            self.logger.info(f"removing tx from history {tx_hash}")
            tx = self.db.remove_transaction(tx_hash)
            remove_from_spent_outpoints()
            self._remove_tx_from_local_history(tx_hash)
            for addr in itertools.chain(self.db.get_txi(tx_hash), self.db.get_txo(tx_hash)):
                self._get_addr_balance_cache.pop(addr, None)

            self.db.remove_txi(tx_hash)
            self.db.remove_txo(tx_hash)

    def get_depending_transactions(self, tx_hash):
        """Returns all (grand-)children of tx_hash in this wallet."""
        with self.transaction_lock:
            children = set()
            for n in self.db.get_spent_outpoints(tx_hash):
                other_hash = self.db.get_spent_outpoint(tx_hash, n)
                children.add(other_hash)
                children |= self.get_depending_transactions(other_hash)

            return children

    def receive_tx_callback(self, tx_hash, tx, tx_height):
        self.add_unverified_tx(tx_hash, tx_height)
        self.add_transaction(tx_hash, tx, allow_unrelated=True)

    def receive_history_callback(self, addr, hist, tx_fees):
        with self.lock:
            old_hist = self.get_address_history(addr)
            for tx_hash, height in old_hist:
                if (
                 tx_hash, height) not in hist:
                    self.unverified_tx.pop(tx_hash, None)
                    self.db.remove_verified_tx(tx_hash)
                    if self.verifier:
                        self.verifier.remove_spv_proof_for_tx(tx_hash)

            self.db.set_addr_history(addr, hist)
        for tx_hash, tx_height in hist:
            self.add_unverified_tx(tx_hash, tx_height)
            tx = self.db.get_transaction(tx_hash)
            if tx is None:
                continue
            self.add_transaction(tx_hash, tx, allow_unrelated=True)

        self.db.update_tx_fees(tx_fees)

    @profiler
    def load_local_history(self):
        self._history_local = {}
        self._address_history_changed_events = defaultdict(asyncio.Event)
        for txid in itertools.chain(self.db.list_txi(), self.db.list_txo()):
            self._add_tx_to_local_history(txid)

    @profiler
    def check_history(self):
        hist_addrs_mine = list(filter(lambda k: self.is_mine(k), self.db.get_history()))
        hist_addrs_not_mine = list(filter(lambda k: not self.is_mine(k), self.db.get_history()))
        for addr in hist_addrs_not_mine:
            self.db.remove_addr_history(addr)

        for addr in hist_addrs_mine:
            hist = self.db.get_addr_history(addr)
            for tx_hash, tx_height in hist:
                if self.db.get_txi(tx_hash) or self.db.get_txo(tx_hash):
                    continue
                tx = self.db.get_transaction(tx_hash)
                if tx is not None:
                    self.add_transaction(tx_hash, tx, allow_unrelated=True)

    def remove_local_transactions_we_dont_have(self):
        for txid in itertools.chain(self.db.list_txi(), self.db.list_txo()):
            tx_height = self.get_tx_height(txid).height
            if tx_height == TX_HEIGHT_LOCAL:
                self.db.get_transaction(txid) or self.remove_transaction(txid)

    def clear_history(self):
        with self.lock:
            with self.transaction_lock:
                self.db.clear_history()

    def get_txpos(self, tx_hash):
        """Returns (height, txpos) tuple, even if the tx is unverified."""
        with self.lock:
            verified_tx_mined_info = self.db.get_verified_tx(tx_hash)
            if verified_tx_mined_info:
                return (
                 verified_tx_mined_info.height, verified_tx_mined_info.txpos)
            if tx_hash in self.unverified_tx:
                height = self.unverified_tx[tx_hash]
                if height > 0:
                    return (height, 0)
                return (1000000000.0 - height, 0)
            return (1000000001.0, 0)

    def with_local_height_cached(func):

        def f(self, *args, **kwargs):
            orig_val = getattr(self.threadlocal_cache, 'local_height', None)
            self.threadlocal_cache.local_height = orig_val or self.get_local_height()
            try:
                return func(self, *args, **kwargs)
            finally:
                self.threadlocal_cache.local_height = orig_val

        return f

    @with_local_height_cached
    def get_history(self, domain=None):
        if domain is None:
            domain = self.get_addresses()
        domain = set(domain)
        tx_deltas = defaultdict(int)
        for addr in domain:
            h = self.get_address_history(addr)
            for tx_hash, height in h:
                delta = self.get_tx_delta(tx_hash, addr)
                if delta is None or tx_deltas[tx_hash] is None:
                    tx_deltas[tx_hash] = None
                else:
                    tx_deltas[tx_hash] += delta

        history = []
        for tx_hash in tx_deltas:
            delta = tx_deltas[tx_hash]
            tx_mined_status = self.get_tx_height(tx_hash)
            history.append((tx_hash, tx_mined_status, delta))

        history.sort(key=(lambda x: self.get_txpos(x[0])), reverse=True)
        c, u, x = self.get_balance(domain)
        balance = c + u + x
        h2 = []
        for tx_hash, tx_mined_status, delta in history:
            h2.append((tx_hash, tx_mined_status, delta, balance))
            if balance is None or delta is None:
                balance = None
            else:
                balance -= delta

        h2.reverse()
        if balance not in (None, 0):
            self.logger.info('Error: history not synchronized')
            return []
        return h2

    def _add_tx_to_local_history(self, txid):
        with self.transaction_lock:
            for addr in itertools.chain(self.db.get_txi(txid), self.db.get_txo(txid)):
                cur_hist = self._history_local.get(addr, set())
                cur_hist.add(txid)
                self._history_local[addr] = cur_hist
                self._mark_address_history_changed(addr)

    def _remove_tx_from_local_history(self, txid):
        with self.transaction_lock:
            for addr in itertools.chain(self.db.get_txi(txid), self.db.get_txo(txid)):
                cur_hist = self._history_local.get(addr, set())
                try:
                    cur_hist.remove(txid)
                except KeyError:
                    pass

                self._history_local[addr] = cur_hist

    def _mark_address_history_changed(self, addr: str) -> None:
        self._address_history_changed_events[addr].set()
        self._address_history_changed_events[addr].clear()

    async def wait_for_address_history_to_change(self, addr: str) -> None:
        """Wait until the server tells us about a new transaction related to addr.

        Unconfirmed and confirmed transactions are not distinguished, and so e.g. SPV
        is not taken into account.
        """
        assert self.is_mine(addr), 'address needs to be is_mine to be watched'
        await self._address_history_changed_events[addr].wait()

    def add_unverified_tx(self, tx_hash, tx_height):
        if self.db.is_in_verified_tx(tx_hash):
            if tx_height in (TX_HEIGHT_UNCONFIRMED, TX_HEIGHT_UNCONF_PARENT):
                with self.lock:
                    self.db.remove_verified_tx(tx_hash)
                if self.verifier:
                    self.verifier.remove_spv_proof_for_tx(tx_hash)
        else:
            with self.lock:
                self.unverified_tx[tx_hash] = tx_height

    def remove_unverified_tx(self, tx_hash, tx_height):
        with self.lock:
            new_height = self.unverified_tx.get(tx_hash)
            if new_height == tx_height:
                self.unverified_tx.pop(tx_hash, None)

    def add_verified_tx(self, tx_hash: str, info: TxMinedInfo):
        with self.lock:
            self.unverified_tx.pop(tx_hash, None)
            self.db.add_verified_tx(tx_hash, info)
        tx_mined_status = self.get_tx_height(tx_hash)
        self.network.trigger_callback('verified', self, tx_hash, tx_mined_status)

    def get_unverified_txs(self):
        """Returns a map from tx hash to transaction height"""
        with self.lock:
            return dict(self.unverified_tx)

    def undo_verifications(self, blockchain, above_height):
        """Used by the verifier when a reorg has happened"""
        txs = set()
        with self.lock:
            for tx_hash in self.db.list_verified_tx():
                info = self.db.get_verified_tx(tx_hash)
                tx_height = info.height
                if tx_height > above_height:
                    header = blockchain.read_header(tx_height)
                    if not header or hash_header(header) != info.header_hash:
                        self.db.remove_verified_tx(tx_hash)
                        self.unverified_tx[tx_hash] = tx_height
                        txs.add(tx_hash)

        return txs

    def get_local_height(self):
        """ return last known height if we are offline """
        cached_local_height = getattr(self.threadlocal_cache, 'local_height', None)
        if cached_local_height is not None:
            return cached_local_height
        if self.network:
            return self.network.get_local_height()
        return self.db.get('stored_height', 0)

    def get_tx_height(self, tx_hash: str) -> TxMinedInfo:
        with self.lock:
            verified_tx_mined_info = self.db.get_verified_tx(tx_hash)
            if verified_tx_mined_info:
                conf = max(self.get_local_height() - verified_tx_mined_info.height + 1, 0)
                return verified_tx_mined_info._replace(conf=conf)
            if tx_hash in self.unverified_tx:
                height = self.unverified_tx[tx_hash]
                return TxMinedInfo(height=height, conf=0)
            return TxMinedInfo(height=TX_HEIGHT_LOCAL, conf=0)

    def set_up_to_date(self, up_to_date):
        with self.lock:
            self.up_to_date = up_to_date
        if self.network:
            self.network.notify('status')

    def is_up_to_date(self):
        with self.lock:
            return self.up_to_date

    def get_history_sync_state_details(self) -> Tuple[(int, int)]:
        if self.synchronizer:
            return self.synchronizer.num_requests_sent_and_answered()
        return (0, 0)

    @with_transaction_lock
    def get_tx_delta(self, tx_hash, address):
        """effect of tx on address"""
        delta = 0
        d = self.db.get_txi_addr(tx_hash, address)
        for n, v in d:
            delta -= v

        d = self.db.get_txo_addr(tx_hash, address)
        for n, v, cb in d:
            delta += v

        return delta

    @with_transaction_lock
    def get_tx_value(self, txid):
        """effect of tx on the entire domain"""
        delta = 0
        for addr in self.db.get_txi(txid):
            d = self.db.get_txi_addr(txid, addr)
            for n, v in d:
                delta -= v

        for addr in self.db.get_txo(txid):
            d = self.db.get_txo_addr(txid, addr)
            for n, v, cb in d:
                delta += v

        return delta

    def get_wallet_delta(self, tx: Transaction):
        """ effect of tx on wallet """
        is_relevant = False
        is_mine = False
        is_pruned = False
        is_partial = False
        v_in = v_out = v_out_mine = 0
        for txin in tx.inputs():
            addr = self.get_txin_address(txin)
            if self.is_mine(addr):
                is_mine = True
                is_relevant = True
                d = self.db.get_txo_addr(txin['prevout_hash'], addr)
                for n, v, cb in d:
                    if n == txin['prevout_n']:
                        value = v
                        break
                else:
                    value = None

                if value is None:
                    is_pruned = True
                else:
                    v_in += value
            else:
                is_partial = True

        if not is_mine:
            is_partial = False
        else:
            for o in tx.outputs():
                v_out += o.value
                if self.is_mine(o.address):
                    v_out_mine += o.value
                    is_relevant = True

            if is_pruned:
                fee = None
                if is_mine:
                    v = v_out_mine - v_out
                else:
                    v = v_out_mine
            else:
                v = v_out_mine - v_in
                if is_partial:
                    fee = None
                else:
                    fee = v_in - v_out
        if not is_mine:
            fee = None
        return (
         is_relevant, is_mine, v, fee)

    def get_tx_fee(self, tx: Transaction) -> Optional[int]:
        if not tx:
            return
        if hasattr(tx, '_cached_fee'):
            return tx._cached_fee
        with self.lock:
            with self.transaction_lock:
                is_relevant, is_mine, v, fee = self.get_wallet_delta(tx)
                if fee is None:
                    txid = tx.txid()
                    fee = self.db.get_tx_fee(txid)
                if fee is not None:
                    tx._cached_fee = fee
        return fee

    def get_addr_io(self, address):
        with self.lock:
            with self.transaction_lock:
                h = self.get_address_history(address)
                received = {}
                sent = {}
                for tx_hash, height in h:
                    l = self.db.get_txo_addr(tx_hash, address)
                    for n, v, is_cb in l:
                        received[tx_hash + ':%d' % n] = (
                         height, v, is_cb)

                for tx_hash, height in h:
                    l = self.db.get_txi_addr(tx_hash, address)
                    for txi, v in l:
                        sent[txi] = height

        return (
         received, sent)

    def get_addr_utxo(self, address):
        coins, spent = self.get_addr_io(address)
        for txi in spent:
            coins.pop(txi)

        out = {}
        for txo, v in coins.items():
            tx_height, value, is_cb = v
            prevout_hash, prevout_n = txo.split(':')
            x = {'address':address, 
             'value':value, 
             'prevout_n':int(prevout_n), 
             'prevout_hash':prevout_hash, 
             'height':tx_height, 
             'coinbase':is_cb}
            out[txo] = x

        return out

    def get_addr_received(self, address):
        received, sent = self.get_addr_io(address)
        return sum([v for height, v, is_cb in received.values()])

    @with_local_height_cached
    def get_addr_balance(self, address, *, excluded_coins: Set[str]=None):
        """Return the balance of a bitcoin address:
        confirmed and matured, unconfirmed, unmatured
        """
        if not excluded_coins:
            cached_value = self._get_addr_balance_cache.get(address)
            if cached_value:
                return cached_value
        else:
            if excluded_coins is None:
                excluded_coins = set()
            assert isinstance(excluded_coins, set), f"excluded_coins should be set, not {type(excluded_coins)}"
            received, sent = self.get_addr_io(address)
            c = u = x = 0
            local_height = self.get_local_height()
            for txo, (tx_height, v, is_cb) in received.items():
                if txo in excluded_coins:
                    continue
                if is_cb and tx_height + COINBASE_MATURITY > local_height:
                    x += v
                else:
                    if tx_height > 0:
                        c += v
                    else:
                        u += v
                if txo in sent:
                    if sent[txo] > 0:
                        c -= v
                    else:
                        u -= v

            result = (
             c, u, x)
            self._get_addr_balance_cache[address] = excluded_coins or result
        return result

    @with_local_height_cached
    def get_utxos(self, domain=None, *, excluded_addresses=None, mature_only: bool=False, confirmed_only: bool=False, nonlocal_only: bool=False, include_names: bool=True, only_uno_txids=None, only_uno_identifiers=None):
        coins = []
        if domain is None:
            domain = self.get_addresses()
        domain = set(domain)
        if excluded_addresses:
            domain = set(domain) - set(excluded_addresses)
        for addr in domain:
            utxos = self.get_addr_utxo(addr)
            for x in utxos.values():
                if confirmed_only:
                    if x['height'] <= 0:
                        continue
                else:
                    if nonlocal_only:
                        if x['height'] == TX_HEIGHT_LOCAL:
                            continue
                    if mature_only:
                        if x['coinbase'] and x['height'] + COINBASE_MATURITY > self.get_local_height():
                            continue
                if not include_names:
                    txid = x['prevout_hash']
                    vout = x['prevout_n']
                    name_op = self.db.transactions[txid].outputs()[vout].name_op
                    if name_op is not None:
                        continue
                    elif only_uno_txids is not None:
                        txid = x['prevout_hash']
                        vout = x['prevout_n']
                        name_op = self.db.transactions[txid].outputs()[vout].name_op
                        if name_op is None:
                            continue
                        if txid not in only_uno_txids:
                            continue
                    if only_uno_identifiers is not None:
                        txid = x['prevout_hash']
                        vout = x['prevout_n']
                        name_op = self.db.transactions[txid].outputs()[vout].name_op
                        if name_op is None:
                            continue
                        if 'name' not in name_op:
                            continue
                        if name_op['name'] not in only_uno_identifiers:
                            continue
                    coins.append(x)
                    continue

        return coins

    def get_balance(self, domain=None, *, excluded_addresses: Set[str]=None, excluded_coins: Set[str]=None) -> Tuple[(int, int, int)]:
        if domain is None:
            domain = self.get_addresses()
        if excluded_addresses is None:
            excluded_addresses = set()
        assert isinstance(excluded_addresses, set), f"excluded_addresses should be set, not {type(excluded_addresses)}"
        domain = set(domain) - excluded_addresses
        cc = uu = xx = 0
        for addr in domain:
            c, u, x = self.get_addr_balance(addr, excluded_coins=excluded_coins)
            cc += c
            uu += u
            xx += x

        return (
         cc, uu, xx)

    def is_used(self, address):
        h = self.db.get_addr_history(address)
        return len(h) != 0

    def is_empty(self, address):
        c, u, x = self.get_addr_balance(address)
        return c + u + x == 0

    def synchronize(self):
        pass