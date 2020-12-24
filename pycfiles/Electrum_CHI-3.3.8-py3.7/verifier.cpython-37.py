# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/verifier.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 9480 bytes
import asyncio
from typing import Sequence, Optional, TYPE_CHECKING
import aiorpcx
from .util import bh2u, TxMinedInfo, NetworkJobOnDefaultServer
from .crypto import sha256d
from .bitcoin import hash_decode, hash_encode
from .transaction import Transaction
from .blockchain import hash_header
from .interface import GracefulDisconnect
from .network import UntrustedServerReturnedError
from . import constants
if TYPE_CHECKING:
    from .network import Network
    from .address_synchronizer import AddressSynchronizer

class MerkleVerificationFailure(Exception):
    pass


class MissingBlockHeader(MerkleVerificationFailure):
    pass


class MerkleRootMismatch(MerkleVerificationFailure):
    pass


class InnerNodeOfSpvProofIsValidTx(MerkleVerificationFailure):
    pass


class SPV(NetworkJobOnDefaultServer):
    __doc__ = ' Simple Payment Verification '

    def __init__(self, network: 'Network', wallet: 'AddressSynchronizer'):
        self.wallet = wallet
        NetworkJobOnDefaultServer.__init__(self, network)

    def _reset(self):
        super()._reset()
        self.merkle_roots = {}
        self.requested_merkle = set()

    async def _start_tasks(self):
        async with self.group as group:
            await group.spawn(self.main)

    def diagnostic_name(self):
        return self.wallet.diagnostic_name()

    async def main(self):
        self.blockchain = self.network.blockchain()
        while True:
            await self._maybe_undo_verifications()
            await self._request_proofs()
            await asyncio.sleep(0.1)

    async def _request_proofs(self):
        local_height = self.blockchain.height()
        unverified = self.wallet.get_unverified_txs()
        for tx_hash, tx_height in unverified.items():
            if tx_hash in self.requested_merkle or tx_hash in self.merkle_roots:
                continue
            if tx_height <= 0 or tx_height > local_height:
                continue
            header = self.blockchain.read_header(tx_height)
            if header is None:
                if tx_height < constants.net.max_checkpoint():
                    await self.group.spawn(self.network.request_chunk(tx_height, None, can_return_early=True))
                    continue
                self.logger.info(f"requested merkle {tx_hash}")
                self.requested_merkle.add(tx_hash)
                await self.group.spawn(self._request_and_verify_single_proof, tx_hash, tx_height)

    async def _request_and_verify_single_proof(self, tx_hash, tx_height):
        try:
            merkle = await self.network.get_merkle_for_transaction(tx_hash, tx_height)
        except UntrustedServerReturnedError as e:
            try:
                if not isinstance(e.original_exception, aiorpcx.jsonrpc.RPCError):
                    raise
                self.logger.info(f"tx {tx_hash} not at height {tx_height}")
                self.wallet.remove_unverified_tx(tx_hash, tx_height)
                self.requested_merkle.discard(tx_hash)
                return
            finally:
                e = None
                del e

        if tx_height != merkle.get('block_height'):
            self.logger.info('requested tx_height {} differs from received tx_height {} for txid {}'.format(tx_height, merkle.get('block_height'), tx_hash))
        tx_height = merkle.get('block_height')
        pos = merkle.get('pos')
        merkle_branch = merkle.get('merkle')
        async with self.network.bhi_lock:
            header = self.network.blockchain().read_header(tx_height)
        try:
            verify_tx_is_in_block(tx_hash, merkle_branch, pos, header, tx_height)
        except MerkleVerificationFailure as e:
            try:
                if self.network.config.get('skipmerklecheck'):
                    self.logger.info(f"skipping merkle proof check {tx_hash}")
                else:
                    self.logger.info(repr(e))
                    raise GracefulDisconnect(e)
            finally:
                e = None
                del e

        self.merkle_roots[tx_hash] = header.get('merkle_root')
        self.requested_merkle.discard(tx_hash)
        self.logger.info(f"verified {tx_hash}")
        header_hash = hash_header(header)
        tx_info = TxMinedInfo(height=tx_height, timestamp=(header.get('timestamp')),
          txpos=pos,
          header_hash=header_hash)
        self.wallet.add_verified_tx(tx_hash, tx_info)

    @classmethod
    def hash_merkle_root(cls, merkle_branch: Sequence[str], tx_hash: str, leaf_pos_in_tree: int):
        """Return calculated merkle root."""
        try:
            h = hash_decode(tx_hash)
            merkle_branch_bytes = [hash_decode(item) for item in merkle_branch]
            leaf_pos_in_tree = int(leaf_pos_in_tree)
        except Exception as e:
            try:
                raise MerkleVerificationFailure(e)
            finally:
                e = None
                del e

        if leaf_pos_in_tree < 0:
            raise MerkleVerificationFailure('leaf_pos_in_tree must be non-negative')
        index = leaf_pos_in_tree
        for item in merkle_branch_bytes:
            if len(item) != 32:
                raise MerkleVerificationFailure('all merkle branch items have to 32 bytes long')
            h = sha256d(item + h) if index & 1 else sha256d(h + item)
            index >>= 1
            cls._raise_if_valid_tx(bh2u(h))

        if index != 0:
            raise MerkleVerificationFailure('leaf_pos_in_tree too large for branch')
        return hash_encode(h)

    @classmethod
    def _raise_if_valid_tx(cls, raw_tx: str):
        tx = Transaction(raw_tx)
        try:
            tx.deserialize()
        except:
            pass
        else:
            raise InnerNodeOfSpvProofIsValidTx()

    async def _maybe_undo_verifications(self):
        old_chain = self.blockchain
        cur_chain = self.network.blockchain()
        if cur_chain != old_chain:
            self.blockchain = cur_chain
            above_height = cur_chain.get_height_of_last_common_block_with_chain(old_chain)
            self.logger.info(f"undoing verifications above height {above_height}")
            tx_hashes = self.wallet.undo_verifications(self.blockchain, above_height)
            for tx_hash in tx_hashes:
                self.logger.info(f"redoing {tx_hash}")
                self.remove_spv_proof_for_tx(tx_hash)

    def remove_spv_proof_for_tx(self, tx_hash):
        self.merkle_roots.pop(tx_hash, None)
        self.requested_merkle.discard(tx_hash)

    def is_up_to_date(self):
        return not self.requested_merkle


def verify_tx_is_in_block(tx_hash: str, merkle_branch: Sequence[str], leaf_pos_in_tree: int, block_header: Optional[dict], block_height: int) -> None:
    """Raise MerkleVerificationFailure if verification fails."""
    if not block_header:
        raise MissingBlockHeader('merkle verification failed for {} (missing header {})'.format(tx_hash, block_height))
    if len(merkle_branch) > 30:
        raise MerkleVerificationFailure(f"merkle branch too long: {len(merkle_branch)}")
    calc_merkle_root = SPV.hash_merkle_root(merkle_branch, tx_hash, leaf_pos_in_tree)
    if block_header.get('merkle_root') != calc_merkle_root:
        raise MerkleRootMismatch('merkle verification failed for {} ({} != {})'.format(tx_hash, block_header.get('merkle_root'), calc_merkle_root))