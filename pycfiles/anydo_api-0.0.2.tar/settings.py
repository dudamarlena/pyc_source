# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/pyipv8/ipv8/attestation/trustchain/settings.py
# Compiled at: 2019-05-16 09:27:10


class TrustChainSettings(object):
    """
    This class holds various settings regarding TrustChain.
    """

    def __init__(self):
        self.broadcast_blocks = True
        self.broadcast_fanout = 25
        self.validation_range = 5
        self.max_db_blocks = 1000000
        self.crawler = False