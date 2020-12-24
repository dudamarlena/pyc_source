# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/middleware/exception_retry_request.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 2382 bytes
from requests.exceptions import ConnectionError, HTTPError, Timeout, TooManyRedirects
whitelist = [
 'admin',
 'shh',
 'miner',
 'net',
 'txpooltesting',
 'evm',
 'eth_protocolVersion',
 'eth_syncing',
 'eth_coinbase',
 'eth_mining',
 'eth_hashrate',
 'eth_gasPrice',
 'eth_accounts',
 'eth_blockNumber',
 'eth_getBalance',
 'eth_getStorageAt',
 'eth_getCode',
 'eth_getBlockByNumber',
 'eth_getBlockByHash',
 'eth_getBlockTransactionCountByNumber',
 'eth_getBlockTransactionCountByHash',
 'eth_getUncleCountByBlockNumber',
 'eth_getUncleCountByBlockHash',
 'eth_getTransactionByHash',
 'eth_getTransactionByBlockHashAndIndex',
 'eth_getTransactionByBlockNumberAndIndex',
 'eth_getTransactionReceipt',
 'eth_getTransactionCount',
 'eth_call',
 'eth_estimateGas',
 'eth_newBlockFilter',
 'eth_newPendingTransactionFilter',
 'eth_newFilter',
 'eth_getFilterChanges',
 'eth_getFilterLogs',
 'eth_getLogs',
 'eth_uninstallFilter',
 'eth_getCompilers',
 'eth_getWork',
 'eth_sign',
 'eth_sendRawTransaction',
 'personal_importRawKey',
 'personal_newAccount',
 'personal_listAccounts',
 'personal_lockAccount',
 'personal_unlockAccount',
 'personal_ecRecover',
 'personal_sign']

def check_if_retry_on_failure(method):
    root = method.split('_')[0]
    if root in whitelist:
        return True
    else:
        if method in whitelist:
            return True
        return False


def exception_retry_middleware(make_request, web3, errors, retries=5):
    """
    Creates middleware that retries failed HTTP requests. Is a default
    middleware for HTTPProvider.
    """

    def middleware(method, params):
        if check_if_retry_on_failure(method):
            for i in range(retries):
                try:
                    return make_request(method, params)
                except errors:
                    if i < retries - 1:
                        continue
                    else:
                        raise

        else:
            return make_request(method, params)

    return middleware


def http_retry_request_middleware(make_request, web3):
    return exception_retry_middleware(make_request, web3, (
     ConnectionError, HTTPError, Timeout, TooManyRedirects))