# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/valdergallo/Sandbox/easychain/.env/lib/python2.7/site-packages/easychain/blockchain.py
# Compiled at: 2018-03-13 08:45:37
from __future__ import absolute_import, unicode_literals
import hashlib, time
from .exception import InvalidMessage, InvalidBlock, InvalidBlockchain

def memoize(f):
    memo = {}

    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]

    return helper


@memoize
def bit_encode(msg):
    """Create one hash valid"""
    return hashlib.sha256(bytearray(msg, b'utf-8')).hexdigest()


def _parse_args(*args):
    payload = b''
    for arg in args:
        if arg:
            payload += str(arg)

    return payload


class Message(object):
    """
    Sender digitally signs payload. (and recipient too?)
    """

    def __init__(self, data, sender=None, receiver=None, link=None):
        self.prev_msg = link
        self.sender = sender
        self.receiver = receiver
        self.data = data
        self.timestamp = time.time()

    @property
    def size(self):
        return len(self.data.encode(b'utf-8'))

    def encode(self, msg):
        return bit_encode(msg)

    @property
    def prev_hash(self):
        if hasattr(self, b'prev_msg') and self.prev_msg:
            return self.prev_msg.hash

    @property
    def payload_hash(self):
        payload = _parse_args(self.timestamp, self.data, self.sender, self.receiver)
        return self.encode(payload)

    @property
    def hash(self):
        if not self.data:
            return None
        else:
            payload_hash = _parse_args(self.prev_hash, self.payload_hash)
            return self.encode(payload_hash)

    def link(self, msg):
        self.prev_msg = msg
        return self

    def __repr__(self):
        return (b'Message<hash: {}, prev_hash: {}, sender: {}, receiver: {}, data: {}>').format(self.hash, self.prev_hash, self.sender, self.receiver, self.data[:25])


class Block(Message):

    def __init__(self, *args):
        self.messages = []
        self.timestamp = time.time()
        for arg in args:
            self.add_message(arg)

    @property
    def hash(self):
        try:
            prev_hash = self.messages[(-1)].hash
        except IndexError:
            return

        payload_hash = _parse_args(self.prev_hash, self.timestamp, prev_hash)
        return self.encode(payload_hash)

    def add_message(self, msg, sender=None, receiver=None):
        if not isinstance(msg, Message):
            raise InvalidMessage(b'add_message should recive one Message')
        if len(self.messages):
            msg.link(self.messages[(-1)])
        self.messages.append(msg)

    def validate(self):
        for index, msg in enumerate(self.messages):
            if index <= 1:
                continue
            try:
                if msg.prev_hash != self.messages[(index - 1)].hash:
                    raise InvalidBlock((b'Invalid block: Message #{} has invalid message link in block: {}').format(index, str(self)))
            except InvalidMessage as error:
                raise InvalidBlock((b'Invalid block: Message #{} failed validation: {}. In block: {}').format(index, str(error), str(self)))
            except IndexError:
                pass

        return True

    def __repr__(self):
        return (b'Block<hash: {}, prev_hash: {}, messages: {}, time: {}>').format(self.hash, self.prev_hash, len(self.messages), self.timestamp)


class Blockchain(Message):

    def __init__(self):
        self.blocks = []

    def add_block(self, block):
        if len(self.blocks) > 0:
            block.prev_hash = self.blocks[(-1)].hash
        block.validate()
        self.blocks.append(block)

    def validate(self):
        """
        Validates each block, in order.
        An invalid block invalidates the whole chain. (well, from that point
        forward anyway)
        """
        for index, block in enumerate(self.blocks):
            try:
                block.validate()
            except InvalidBlock as error:
                raise InvalidBlockchain((b'Invalid blockchain at block {} caused by: {}').format(index, str(error)))

        return True

    def __repr__(self):
        return (b'Blockchain<blocks: {}>').format(len(self.blocks))