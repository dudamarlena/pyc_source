# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martijndevos/Documents/tribler/Tribler/community/market/core/message_repository.py
# Compiled at: 2018-07-05 10:25:48
from Tribler.community.market.core.tick import TraderId, MessageNumber, MessageId

class MessageRepository(object):
    """A repository interface for messages in the order book"""

    def next_identity(self):
        return NotImplemented


class MemoryMessageRepository(MessageRepository):
    """A repository for messages in the order book stored in memory"""

    def __init__(self, mid):
        """
        :param mid: Hex encoded version of the member id of this node
        :type mid: str
        """
        super(MemoryMessageRepository, self).__init__()
        try:
            int(mid, 16)
        except ValueError:
            raise ValueError('Encoded public key must be hexadecimal')

        self._mid = mid
        self._next_id = 0

    def next_identity(self):
        """
        :rtype: MessageId
        """
        self._next_id += 1
        return MessageId(TraderId(self._mid), MessageNumber(self._next_id))