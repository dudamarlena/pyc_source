# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/utils/module_testing/net_module.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 475 bytes
from eth_utils import is_boolean, is_integer, is_string

class NetModuleTest:

    def test_net_version(self, web3):
        version = web3.net.version
        if not is_string(version):
            raise AssertionError
        elif not version.isdigit():
            raise AssertionError

    def test_net_listening(self, web3):
        listening = web3.net.listening
        assert is_boolean(listening)

    def test_net_peerCount(self, web3):
        peer_count = web3.net.peerCount
        assert is_integer(peer_count)