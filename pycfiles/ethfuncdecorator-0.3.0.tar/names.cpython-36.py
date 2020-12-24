# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/middleware/names.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 421 bytes
from web3.utils.normalizers import abi_ens_resolver
from web3.utils.rpc_abi import RPC_ABIS, abi_request_formatters
from .formatting import construct_formatting_middleware

def name_to_address_middleware(w3):
    normalizers = [
     abi_ens_resolver(w3)]
    return construct_formatting_middleware(request_formatters=(abi_request_formatters(normalizers, RPC_ABIS)))