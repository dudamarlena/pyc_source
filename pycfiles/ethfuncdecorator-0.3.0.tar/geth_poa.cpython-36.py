# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/middleware/geth_poa.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 680 bytes
from eth_utils.curried import apply_formatters_to_dict, apply_key_map
from hexbytes import HexBytes
from web3.middleware.formatting import construct_formatting_middleware
from web3.utils.toolz import compose
remap_geth_poa_fields = apply_key_map({'extraData': 'proofOfAuthorityData'})
pythonic_geth_poa = apply_formatters_to_dict({'proofOfAuthorityData': HexBytes})
geth_poa_cleanup = compose(pythonic_geth_poa, remap_geth_poa_fields)
geth_poa_middleware = construct_formatting_middleware(result_formatters={'eth_getBlockByHash':geth_poa_cleanup, 
 'eth_getBlockByNumber':geth_poa_cleanup})