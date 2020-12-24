# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/eventloop/asyncio_base.py
# Compiled at: 2019-08-15 23:31:02
# Size of source mod 2**32: 1152 bytes
"""
Eventloop for integration with Python3 asyncio.

Note that we can't use "yield from", because the package should be installable
under Python 2.6 as well, and it should contain syntactically valid Python 2.6
code.
"""
from __future__ import unicode_literals
__all__ = ('AsyncioTimeout', )

class AsyncioTimeout(object):
    __doc__ = '\n    Call the `timeout` function when the timeout expires.\n    Every call of the `reset` method, resets the timeout and starts a new\n    timer.\n    '

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