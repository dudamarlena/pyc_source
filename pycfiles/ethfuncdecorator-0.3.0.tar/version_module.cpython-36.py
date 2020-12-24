# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/utils/module_testing/version_module.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 395 bytes
from eth_utils import is_string

class VersionModuleTest:

    def test_net_version(self, web3):
        version = web3.version.network
        if not is_string(version):
            raise AssertionError
        elif not version.isdigit():
            raise AssertionError

    def test_eth_protocolVersion(self, web3):
        protocol_version = web3.version.ethereum
        if not is_string(protocol_version):
            raise AssertionError
        elif not protocol_version.isdigit():
            raise AssertionError