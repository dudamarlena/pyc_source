# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/testing.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 800 bytes
from web3.module import Module

class Testing(Module):

    def timeTravel(self, timestamp):
        return self.web3.manager.request_blocking('testing_timeTravel', [timestamp])

    def mine(self, num_blocks=1):
        return self.web3.manager.request_blocking('evm_mine', [num_blocks])

    def snapshot(self):
        self.last_snapshot_idx = self.web3.manager.request_blocking('evm_snapshot', [])
        return self.last_snapshot_idx

    def reset(self):
        return self.web3.manager.request_blocking('evm_reset', [])

    def revert(self, snapshot_idx=None):
        if snapshot_idx is None:
            revert_target = self.last_snapshot_idx
        else:
            revert_target = snapshot_idx
        return self.web3.manager.request_blocking('evm_revert', [revert_target])