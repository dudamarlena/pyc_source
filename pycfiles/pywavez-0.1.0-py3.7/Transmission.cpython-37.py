# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pywavez/Transmission.py
# Compiled at: 2019-12-28 13:39:44
# Size of source mod 2**32: 3620 bytes
import asyncio, bisect, collections, enum, time
from pywavez.util import waitForOne

class Priority(enum.IntEnum):
    POLLING = -100
    INITALIZATION = -10
    DEFAULT = 0
    INTERACTIVE = 100
    WAKE_UP = 99999


class TransmissionBase(asyncio.Future):

    def __init__(self, message, *, nodeId=None, endpoint=0, priority=Priority.DEFAULT, response_handler=None):
        super().__init__()
        self.message = message
        self.nodeId = nodeId
        self.endpoint = endpoint
        self.priority = priority
        self.responseHandler = response_handler
        self.transmitting = False
        self.retransmission = 0
        self.maxRetransmissions = 3
        self.pauseUntil = None

    def __lt__(self, other):
        return other.priority < self.priority


class MessageTransmission(TransmissionBase):
    pass


class CommandTransmission(TransmissionBase):
    pass


class SimpleQueue:

    def __init__(self):
        self._SimpleQueue__messages = collections.deque()
        self._SimpleQueue__event = asyncio.Event()

    def append(self, message):
        self._SimpleQueue__messages.append(message)
        self._SimpleQueue__event.set()

    def hasMessage(self):
        return bool(self._SimpleQueue__messages)

    async def waitForMessage(self):
        while not self._SimpleQueue__messages:
            self._SimpleQueue__event.clear()
            await self._SimpleQueue__event.wait()

    def takeMessage(self):
        message = self._SimpleQueue__messages.popleft()
        return message

    async def getMessage(self):
        await self.waitForMessage()
        return self.takeMessage()


class MessageQueue:

    def __init__(self):
        self._MessageQueue__messages = []
        self._MessageQueue__event = asyncio.Event()

    def add(self, message):
        bisect.insort_right(self._MessageQueue__messages, message)
        self._MessageQueue__event.set()

    def addFirst(self, message):
        bisect.insort_left(self._MessageQueue__messages, message)
        self._MessageQueue__event.set()

    def hasMessage(self):
        now = time.monotonic()
        for m in self._MessageQueue__messages:
            if m.pauseUntil is None or m.pauseUntil < now:
                return m.cancelled() or True

        return False

    async def waitForMessage(self, timeout=None):
        if timeout is not None:
            expires = time.monotonic() + timeout
        else:
            expires = None
        while True:
            now = time.monotonic()
            if expires is not None:
                if now >= expires:
                    return
            pause_until = expires
            for m in self._MessageQueue__messages:
                if m.cancelled():
                    continue
                if not m.pauseUntil is None:
                    if m.pauseUntil < now:
                        return
                    if pause_until is None or pause_until > m.pauseUntil:
                        pause_until = m.pauseUntil

            self._MessageQueue__event.clear()
            if pause_until is None:
                await self._MessageQueue__event.wait()
            else:
                await waitForOne((self._MessageQueue__event.wait()),
                  timeout=(pause_until - now))

    def takeMessage(self):
        now = time.monotonic()
        idx = 0
        while idx < len(self._MessageQueue__messages):
            m = self._MessageQueue__messages[idx]
            if m.cancelled():
                self._MessageQueue__messages.pop(idx)
                continue
            if not m.pauseUntil is None:
                if m.pauseUntil < now:
                    return self._MessageQueue__messages.pop(idx)
            idx += 1

        raise IndexError('no message available')

    async def getMessage(self):
        await self.waitForMessage()
        return self.takeMessage()