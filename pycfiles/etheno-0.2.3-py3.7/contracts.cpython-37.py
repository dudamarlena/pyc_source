# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/etheno/contracts.py
# Compiled at: 2019-06-27 23:49:12
# Size of source mod 2**32: 481 bytes
from .client import RpcProxyClient
from .etheno import EthenoPlugin
from .utils import format_hex_address

class ContractSynchronizer(EthenoPlugin):

    def __init__(self, source_client, contract_address):
        if isintsance(source_client, str):
            source_client = RpcProxyClient(source_client)
        self.source = source_client
        self.contract = format_hex_address(contract_address, True)

    def added(self):
        pass