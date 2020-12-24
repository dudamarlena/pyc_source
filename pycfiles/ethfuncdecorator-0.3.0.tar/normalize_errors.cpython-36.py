# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/middleware/normalize_errors.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 849 bytes
from web3.utils.toolz import assoc, dissoc

def normalize_errors_middleware(make_request, web3):

    def middleware(method, params):
        result = make_request(method, params)
        if method == 'eth_getTransactionReceipt':
            if 'error' in result:
                is_geth = web3.version.node.startswith('Geth')
                if is_geth:
                    if result['error']['code'] == -32000:
                        return assoc(dissoc(result, 'error'), 'result', None)
                return result
        else:
            return result

    return middleware