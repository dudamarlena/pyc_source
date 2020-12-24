# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kutana/backends/terminal.py
# Compiled at: 2020-05-02 08:54:53
# Size of source mod 2**32: 1167 bytes
import sys, time
from ..backend import Backend
from ..update import Message, ReceiverType, UpdateType
if sys.platform == 'win32':
    import msvcrt

    def attempt_to_read_message():
        if msvcrt.kbhit():
            return sys.stdin.readline().strip()


else:
    import select

    def attempt_to_read_message():
        ready_objects, _, _ = select.select([sys.stdin], [], [], 0.05)
        if ready_objects:
            return sys.stdin.readline().strip()


class Terminal(Backend):

    def _make_update(self, text, sender_id=1):
        return Message(raw=None,
          type=(UpdateType.MSG),
          text=text,
          attachments=(),
          sender_id=sender_id,
          receiver_id=1,
          receiver_type=(ReceiverType.SOLO),
          date=(time.time()))

    async def perform_updates_request(self, submit_update):
        message = attempt_to_read_message()
        if message:
            await submit_update(self._make_update(message))

    async def perform_send(self, target_id, message, attachments, kwargs):
        print('>', message)