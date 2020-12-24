# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/eventloop/asyncio_base.py
# Compiled at: 2019-08-15 23:31:02
# Size of source mod 2**32: 1152 bytes
__doc__ = '\nEventloop for integration with Python3 asyncio.\n\nNote that we can\'t use "yield from", because the package should be installable\nunder Python 2.6 as well, and it should contain syntactically valid Python 2.6\ncode.\n'
from __future__ import unicode_literals
__all__ = ('AsyncioTimeout', )

class AsyncioTimeout(object):
    """AsyncioTimeout"""

    def __init__(self, timeout, callback, loop):
        self.timeout = timeout
        self.callback = callback
        self.loop = loop
        self.counter = 0
        self.running = True

    def reset(self):
        """
        Reset the timeout. Starts a new timer.
        """
        self.counter += 1
        local_counter = self.counter

        def timer_timeout():
            if self.counter == local_counter:
                if self.running:
                    self.callback()

        self.loop.call_later(self.timeout, timer_timeout)

    def stop(self):
        """
        Ignore timeout. Don't call the callback anymore.
        """
        self.running = False