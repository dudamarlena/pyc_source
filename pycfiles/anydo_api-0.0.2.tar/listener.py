# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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