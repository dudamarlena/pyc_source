# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/auxpow.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 13426 bytes
import binascii
from . import blockchain
from .bitcoin import hash_encode, hash_decode
from .crypto import sha256d
from . import transaction
from .transaction import BCDataStream, Transaction, TYPE_SCRIPT
from .util import bfh, bh2u
MAX_INDEX_PC_BACKWARDS_COMPATIBILITY = 20
COINBASE_MERGED_MINING_HEADER = bfh('fabe') + b'mm'
CHAIN_ID = 1829

class AuxPowVerifyError(Exception):
    pass


class AuxPoWNotGenerateError(AuxPowVerifyError):
    pass


class AuxPoWChainMerkleTooLongError(AuxPowVerifyError):
    pass


class AuxPoWBadCoinbaseMerkleBranchError(AuxPowVerifyError):
    pass


class AuxPoWCoinbaseNoInputsError(AuxPowVerifyError):
    pass


class AuxPoWCoinbaseRootTooLate(AuxPowVerifyError):
    pass


class AuxPoWCoinbaseRootMissingError(AuxPowVerifyError):
    pass


def deserialize_auxpow_header(s, start_position=0) -> (dict, int):
    """Deserialises an AuxPoW instance.

    Returns the deserialised AuxPoW dict and the end position in the byte
    array as a pair."""
    auxpow_header = {}
    parent_coinbase_tx = Transaction(None, expect_trailing_data=True, raw_bytes=s, expect_trailing_bytes=True, copy_input=False, start_position=start_position)
    parent_coinbase_tx_dict, start_position = fast_tx_deserialize(parent_coinbase_tx)
    auxpow_header['parent_coinbase_tx'] = parent_coinbase_tx
    start_position = start_position + 32
    auxpow_header['coinbase_merkle_branch'], auxpow_header['coinbase_merkle_index'], start_position = deserialize_merkle_branch(s, start_position=start_position)
    auxpow_header['chain_merkle_branch'], auxpow_header['chain_merkle_index'], start_position = deserialize_merkle_branch(s, start_position=start_position)
    parent_header_bytes = s[start_position:start_position + blockchain.PURE_HEADER_SIZE]
    auxpow_header['parent_header'] = blockchain.deserialize_pure_header(parent_header_bytes, None)
    start_position += blockchain.PURE_HEADER_SIZE
    del auxpow_header['parent_header']['block_height']
    return (
     auxpow_header, start_position)


def deserialize_merkle_branch(s, start_position=0):
    vds = BCDataStream()
    vds.input = s
    vds.read_cursor = start_position
    hashes = []
    n_hashes = vds.read_compact_size()
    for i in range(n_hashes):
        _hash = vds.read_bytes(32)
        hashes.append(hash_encode(_hash))

    index = vds.read_int32()
    return (hashes, index, vds.read_cursor)


def calculate_merkle_root(leaf, merkle_branch, index):
    target = hash_decode(leaf)
    mask = index
    for merkle_step in merkle_branch:
        if mask & 1 == 0:
            data_to_hash = target + hash_decode(merkle_step)
        else:
            data_to_hash = hash_decode(merkle_step) + target
        target = sha256d(data_to_hash)
        mask = mask >> 1

    return hash_encode(target)


def calc_merkle_index(chain_id, nonce, merkle_size):
    rand = nonce
    rand = rand * 1103515245 + 12345 & 4294967295
    rand += chain_id
    rand = rand * 1103515245 + 12345 & 4294967295
    return rand % merkle_size


def verify_auxpow(auxpow, auxhash):
    parent_block = auxpow['parent_header']
    coinbase = auxpow['parent_coinbase_tx']
    coinbase_hash = fast_txid(coinbase)
    chain_merkle_branch = auxpow['chain_merkle_branch']
    chain_index = auxpow['chain_merkle_index']
    coinbase_merkle_branch = auxpow['coinbase_merkle_branch']
    coinbase_index = auxpow['coinbase_merkle_index']
    if coinbase_index != 0:
        raise AuxPoWNotGenerateError()
    else:
        if len(chain_merkle_branch) > 30:
            raise AuxPoWChainMerkleTooLongError()
        root_hash_bytes = bfh(calculate_merkle_root(auxhash, chain_merkle_branch, chain_index))
        if calculate_merkle_root(coinbase_hash, coinbase_merkle_branch, coinbase_index) != parent_block['merkle_root']:
            raise AuxPoWBadCoinbaseMerkleBranchError()
        if len(coinbase.inputs()) == 0:
            raise AuxPoWCoinbaseNoInputsError()
        script_bytes = bfh(coinbase.inputs()[0]['scriptSig'])
        pos_header = script_bytes.find(COINBASE_MERGED_MINING_HEADER)
        pos = script_bytes.find(root_hash_bytes)
        if pos == -1:
            raise AuxPoWCoinbaseRootMissingError('Aux POW missing chain merkle root in parent coinbase')
        if pos_header != -1:
            pass
        elif pos > 20:
            raise AuxPoWCoinbaseRootTooLate()
    pos = pos + len(root_hash_bytes)
    if len(script_bytes) - pos < 8:
        raise Exception('Aux POW missing chain merkle tree size and nonce in parent coinbase')

    def bytes_to_int(b):
        return int.from_bytes(b, byteorder='little')

    size = bytes_to_int(script_bytes[pos:pos + 4])
    nonce = bytes_to_int(script_bytes[pos + 4:pos + 8])
    if size != 1 << len(chain_merkle_branch):
        raise Exception('Aux POW merkle branch size does not match parent coinbase')
    index = calc_merkle_index(CHAIN_ID, nonce, size)
    if chain_index != index:
        raise Exception('Aux POW wrong index')


def fast_txid(tx):
    return bh2u(sha256d(tx.raw_bytes)[::-1])


def stub_parse_output(vds, i):
    vds.read_int64()
    vds.read_bytes(vds.read_compact_size())
    return {'type':TYPE_SCRIPT,  'address':None,  'value':0,  'name_op':None}


def fast_tx_deserialize(tx):
    real_parse_output, transaction.parse_output = transaction.parse_output, stub_parse_output
    try:
        result = tx.deserialize()
    finally:
        transaction.parse_output = real_parse_output

    return result