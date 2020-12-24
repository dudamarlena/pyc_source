# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/pyipv8/ipv8/attestation/trustchain/listener.py
# Compiled at: 2019-05-16 09:27:10
from __future__ import absolute_import
import abc, six
from .block import TrustChainBlock

class BlockListener(six.with_metaclass(abc.ABCMeta, object)):
    """
    This class defines a listener for TrustChain blocks with a specific type.
    """
    BLOCK_CLASS = TrustChainBlock

    @abc.abstractmethod
    def should_sign(self, block):
        """
        Method to indicate whether this listener wants a specific block signed or not.
        """
        pass

    @abc.abstractmethod
    def received_block(self, block):
        """
        This method is called when a listener receives a block that matches the BLOCK_CLASS.
        :return:
        """
        pass