# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/raymond/Projects/TutorGen/python-client/env/lib/python3.4/site-packages/hpitclient/tutor.py
# Compiled at: 2014-10-09 21:08:04
# Size of source mod 2**32: 1439 bytes
import time
from .message_sender_mixin import MessageSenderMixin
from .exceptions import ResponseDispatchError

class Tutor(MessageSenderMixin):

    def __init__(self, entity_id, api_key, callback, **kwargs):
        super().__init__()
        self.run_loop = True
        self.entity_id = str(entity_id)
        self.api_key = str(api_key)
        self.callback = callback
        self.poll_wait = 500
        self.time_last_poll = time.time() * 1000
        for k, v in kwargs.items():
            setattr(self, k, v)

    def start(self):
        """
        Starts the tutor in event-driven mode.
        """
        self.connect()
        try:
            while self.run_loop:
                if not self.callback():
                    break
                cur_time = time.time() * 1000
                if cur_time - self.time_last_poll < self.poll_wait:
                    continue
                self.time_last_poll = cur_time
                if not self._try_hook('pre_poll_responses'):
                    break
                responses = self._poll_responses()
                if not self._try_hook('post_poll_responses'):
                    break
                if not self._dispatch_responses(responses):
                    break

        except KeyboardInterrupt:
            pass

        self.disconnect()

    def stop(self):
        self.run_loop = False