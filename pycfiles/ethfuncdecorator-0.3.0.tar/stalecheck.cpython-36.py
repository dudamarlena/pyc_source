# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/middleware/stalecheck.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 1583 bytes
import time
from web3.exceptions import StaleBlockchain
SKIP_STALECHECK_FOR_METHODS = set([
 'eth_getBlockByNumber'])

def _isfresh(block, allowable_delay):
    return block and time.time() - block['timestamp'] <= allowable_delay


def make_stalecheck_middleware(allowable_delay, skip_stalecheck_for_methods=SKIP_STALECHECK_FOR_METHODS):
    """
    Use to require that a function will run only of the blockchain is recently updated.

    This middleware takes an argument, so unlike other middleware, you must make the middleware
    with a method call.
    For example: `make_stalecheck_middleware(60*5)`

    If the latest block in the chain is older than 5 minutes in this example, then the
    middleware will raise a StaleBlockchain exception.
    """
    if allowable_delay <= 0:
        raise ValueError('You must set a positive allowable_delay in seconds for this middleware')

    def stalecheck_middleware(make_request, web3):
        cache = {'latest': None}

        def middleware(method, params):
            if method not in skip_stalecheck_for_methods:
                if _isfresh(cache['latest'], allowable_delay):
                    pass
                else:
                    latest = web3.eth.getBlock('latest')
                    if _isfresh(latest, allowable_delay):
                        cache['latest'] = latest
                    else:
                        raise StaleBlockchain(latest, allowable_delay)
            return make_request(method, params)

        return middleware

    return stalecheck_middleware