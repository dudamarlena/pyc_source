# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/__init__.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 821 bytes
import pkg_resources, sys
if sys.version_info < (3, 5):
    raise EnvironmentError('Python 3.5 or above is required')
from eth_account import Account
from web3.main import Web3
from web3.providers.rpc import HTTPProvider
from web3.providers.eth_tester import EthereumTesterProvider
from web3.providers.tester import TestRPCProvider
from web3.providers.ipc import IPCProvider
from web3.providers.websocket import WebsocketProvider
__version__ = pkg_resources.get_distribution('web3').version
__all__ = [
 '__version__',
 'Web3',
 'HTTPProvider',
 'IPCProvider',
 'WebsocketProvider',
 'TestRPCProvider',
 'EthereumTesterProvider',
 'Account']