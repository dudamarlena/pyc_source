# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/middleware/gas_price_strategy.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 677 bytes
from web3.utils.toolz import assoc

def gas_price_strategy_middleware(make_request, web3):
    """
    Includes a gas price using the gas price strategy
    """

    def middleware(method, params):
        if method == 'eth_sendTransaction':
            transaction = params[0]
            if 'gasPrice' not in transaction:
                generated_gas_price = web3.eth.generateGasPrice(transaction)
                if generated_gas_price is not None:
                    transaction = assoc(transaction, 'gasPrice', generated_gas_price)
                    return make_request(method, [transaction])
        return make_request(method, params)

    return middleware