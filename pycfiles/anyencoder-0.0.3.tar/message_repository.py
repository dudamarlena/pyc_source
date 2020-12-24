# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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