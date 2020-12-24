# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/middleware/simulate_unmined_transaction.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 615 bytes
import collections, itertools
counter = itertools.count()
INVOCATIONS_BEFORE_RESULT = 5

def unmined_receipt_simulator_middleware(make_request, web3):
    receipt_counters = collections.defaultdict(itertools.count)

    def middleware(method, params):
        if method == 'eth_getTransactionReceipt':
            txn_hash = params[0]
            if next(receipt_counters[txn_hash]) < INVOCATIONS_BEFORE_RESULT:
                return {'result': None}
            else:
                return make_request(method, params)
        else:
            return make_request(method, params)

    return middleware