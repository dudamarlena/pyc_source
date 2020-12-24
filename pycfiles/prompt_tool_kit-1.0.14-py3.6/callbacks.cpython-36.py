# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/eventloop/callbacks.py
# Compiled at: 2019-08-15 23:53:39
# Size of source mod 2**32: 738 bytes
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from six import with_metaclass
__all__ = ('EventLoopCallbacks', )

class EventLoopCallbacks(with_metaclass(ABCMeta, object)):
    __doc__ = '\n    This is the glue between the :class:`~prompt_tool_kit.eventloop.base.EventLoop`\n    and :class:`~prompt_tool_kit.interface.CommandLineInterface`.\n\n    :meth:`~prompt_tool_kit.eventloop.base.EventLoop.run` takes an\n    :class:`.EventLoopCallbacks` instance and operates on that one, driving the\n    interface.\n    '

    @abstractmethod
    def terminal_size_changed(self):
        pass

    @abstractmethod
    def input_timeout(self):
        pass

    @abstractmethod
    def feed_key(self, key):
        pass