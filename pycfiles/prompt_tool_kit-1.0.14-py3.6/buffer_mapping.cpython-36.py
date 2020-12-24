# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/buffer_mapping.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 2891 bytes
"""
The BufferMapping contains all the buffers for a command line interface, and it
keeps track of which buffer gets the focus.
"""
from __future__ import unicode_literals
from .enums import DEFAULT_BUFFER, SEARCH_BUFFER, SYSTEM_BUFFER, DUMMY_BUFFER
from .buffer import Buffer, AcceptAction
from .history import InMemoryHistory
import six
__all__ = ('BufferMapping', )

class BufferMapping(dict):
    __doc__ = "\n    Dictionary that maps the name of the buffers to the\n    :class:`~prompt_tool_kit.buffer.Buffer` instances.\n\n    This mapping also keeps track of which buffer currently has the focus.\n    (Some methods receive a 'cli' parameter. This is useful for applications\n    where this `BufferMapping` is shared between several applications.)\n    "

    def __init__(self, buffers=None, initial=DEFAULT_BUFFER):
        if not buffers is None:
            if not isinstance(buffers, dict):
                raise AssertionError
        super(BufferMapping, self).__init__()
        self.update({DEFAULT_BUFFER: Buffer(accept_action=(AcceptAction.RETURN_DOCUMENT)), 
         SEARCH_BUFFER: Buffer(history=(InMemoryHistory()), accept_action=(AcceptAction.IGNORE)), 
         SYSTEM_BUFFER: Buffer(history=(InMemoryHistory()), accept_action=(AcceptAction.IGNORE)), 
         DUMMY_BUFFER: Buffer(read_only=True)})
        if buffers is not None:
            self.update(buffers)
        self.focus_stack = [
         initial or DEFAULT_BUFFER]

    def current(self, cli):
        """
        The active :class:`.Buffer`.
        """
        return self[self.focus_stack[(-1)]]

    def current_name(self, cli):
        """
        The name of the active :class:`.Buffer`.
        """
        return self.focus_stack[(-1)]

    def previous(self, cli):
        """
        Return the previously focussed :class:`.Buffer` or `None`.
        """
        if len(self.focus_stack) > 1:
            try:
                return self[self.focus_stack[(-2)]]
            except KeyError:
                pass

    def focus(self, cli, buffer_name):
        """
        Focus the buffer with the given name.
        """
        assert isinstance(buffer_name, six.text_type)
        self.focus_stack = [buffer_name]

    def push_focus(self, cli, buffer_name):
        """
        Push buffer on the focus stack.
        """
        assert isinstance(buffer_name, six.text_type)
        self.focus_stack.append(buffer_name)

    def pop_focus(self, cli):
        """
        Pop buffer from the focus stack.
        """
        if len(self.focus_stack) > 1:
            self.focus_stack.pop()
        else:
            raise IndexError('Cannot pop last item from the focus stack.')