# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cert_issuer/blockchain_handlers/ethereum/tx_utils.py
# Compiled at: 2018-12-05 14:02:34
# Size of source mod 2**32: 1085 bytes
import logging
from cert_issuer.errors import UnverifiedTransactionError

def create_ethereum_trx(issuing_address, nonce, to_address, blockchain_bytes, gasprice, gaslimit):
    from ethereum.transactions import Transaction
    value = 0
    tx = Transaction(nonce=nonce, gasprice=gasprice, startgas=gaslimit, to=to_address, value=value, data=blockchain_bytes)
    return tx


def verify_eth_transaction(signed_hextx, eth_data_field):
    """
    Verify ethDataField field in transaction
    :param signed_hextx:
    :param eth_data_field:
    :return:
    """
    logging.info('verifying ethDataField value for transaction')
    ethdata_hash = []
    for s in signed_hextx.split('80a0'):
        ethdata_hash.append(s)

    ethdata_hash = ethdata_hash[1][:64]
    result = eth_data_field == ethdata_hash
    if not result:
        error_message = 'There was a problem verifying the transaction'
        raise UnverifiedTransactionError(error_message)
    logging.info('verified ethDataField')