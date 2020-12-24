# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/eventloop/callbacks.py
# Compiled at: 2019-08-15 23:53:39
# Size of source mod 2**32: 738 bytes
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from six import with_metaclass
__all__ = ('EventLoopCallbacks', )

class EventLoopCallbacks(with_metaclass(ABCMeta, object)):
    """EventLoopCallbacks"""

    @abstractmethod
    def terminal_size_changed(self):
        pass

    @abstractmethod
    def input_timeout(self):
        pass

    @abstractmethod
    def feed_key(self, key):
        pass