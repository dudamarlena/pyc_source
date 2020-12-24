# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/buffer_mapping.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 2891 bytes
__doc__ = '\nThe BufferMapping contains all the buffers for a command line interface, and it\nkeeps track of which buffer gets the focus.\n'
from __future__ import unicode_literals
from .enums import DEFAULT_BUFFER, SEARCH_BUFFER, SYSTEM_BUFFER, DUMMY_BUFFER
from .buffer import Buffer, AcceptAction
from .history import InMemoryHistory
import six
__all__ = ('BufferMapping', )

class BufferMapping(dict):
    """BufferMapping"""

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