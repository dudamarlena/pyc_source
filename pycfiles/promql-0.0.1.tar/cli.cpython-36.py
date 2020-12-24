# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/filters/cli.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 9227 bytes
__doc__ = '\nFilters that accept a `CommandLineInterface` as argument.\n'
from __future__ import unicode_literals
from .base import Filter
from prompt_tool_kit.enums import EditingMode
from prompt_tool_kit.key_binding.vi_state import InputMode as ViInputMode
from prompt_tool_kit.cache import memoized
__all__ = ('HasArg', 'HasCompletions', 'HasFocus', 'InFocusStack', 'HasSearch', 'HasSelection',
           'HasValidationError', 'IsAborting', 'IsDone', 'IsMultiline', 'IsReadOnly',
           'IsReturning', 'RendererHeightIsKnown', 'InEditingMode', 'ViMode', 'ViNavigationMode',
           'ViInsertMode', 'ViInsertMultipleMode', 'ViReplaceMode', 'ViSelectionMode',
           'ViWaitingForTextObjectMode', 'ViDigraphMode', 'EmacsMode', 'EmacsInsertMode',
           'EmacsSelectionMode')

@memoized()
class HasFocus(Filter):
    """HasFocus"""

    def __init__(self, buffer_name):
        self._buffer_name = buffer_name

    @property
    def buffer_name(self):
        """ The given buffer name. (Read-only) """
        return self._buffer_name

    def __call__(self, cli):
        return cli.current_buffer_name == self.buffer_name

    def __repr__(self):
        return 'HasFocus(%r)' % self.buffer_name


@memoized()
class InFocusStack(Filter):
    """InFocusStack"""

    def __init__(self, buffer_name):
        self._buffer_name = buffer_name

    @property
    def buffer_name(self):
        """ The given buffer name. (Read-only) """
        return self._buffer_name

    def __call__(self, cli):
        return self.buffer_name in cli.buffers.focus_stack

    def __repr__(self):
        return 'InFocusStack(%r)' % self.buffer_name


@memoized()
class HasSelection(Filter):
    """HasSelection"""

    def __call__(self, cli):
        return bool(cli.current_buffer.selection_state)

    def __repr__(self):
        return 'HasSelection()'


@memoized()
class HasCompletions(Filter):
    """HasCompletions"""

    def __call__(self, cli):
        return cli.current_buffer.complete_state is not None

    def __repr__(self):
        return 'HasCompletions()'


@memoized()
class IsMultiline(Filter):
    """IsMultiline"""

    def __call__(self, cli):
        return cli.current_buffer.is_multiline()

    def __repr__(self):
        return 'IsMultiline()'


@memoized()
class IsReadOnly(Filter):
    """IsReadOnly"""

    def __call__(self, cli):
        return cli.current_buffer.read_only()

    def __repr__(self):
        return 'IsReadOnly()'


@memoized()
class HasValidationError(Filter):
    """HasValidationError"""

    def __call__(self, cli):
        return cli.current_buffer.validation_error is not None

    def __repr__(self):
        return 'HasValidationError()'


@memoized()
class HasArg(Filter):
    """HasArg"""

    def __call__(self, cli):
        return cli.input_processor.arg is not None

    def __repr__(self):
        return 'HasArg()'


@memoized()
class HasSearch(Filter):
    """HasSearch"""

    def __call__(self, cli):
        return cli.is_searching

    def __repr__(self):
        return 'HasSearch()'


@memoized()
class IsReturning(Filter):
    """IsReturning"""

    def __call__(self, cli):
        return cli.is_returning

    def __repr__(self):
        return 'IsReturning()'


@memoized()
class IsAborting(Filter):
    """IsAborting"""

    def __call__(self, cli):
        return cli.is_aborting

    def __repr__(self):
        return 'IsAborting()'


@memoized()
class IsExiting(Filter):
    """IsExiting"""

    def __call__(self, cli):
        return cli.is_exiting

    def __repr__(self):
        return 'IsExiting()'


@memoized()
class IsDone(Filter):
    """IsDone"""

    def __call__(self, cli):
        return cli.is_done

    def __repr__(self):
        return 'IsDone()'


@memoized()
class RendererHeightIsKnown(Filter):
    """RendererHeightIsKnown"""

    def __call__(self, cli):
        return cli.renderer.height_is_known

    def __repr__(self):
        return 'RendererHeightIsKnown()'


@memoized()
class InEditingMode(Filter):
    """InEditingMode"""

    def __init__(self, editing_mode):
        self._editing_mode = editing_mode

    @property
    def editing_mode(self):
        """ The given editing mode. (Read-only) """
        return self._editing_mode

    def __call__(self, cli):
        return cli.editing_mode == self.editing_mode

    def __repr__(self):
        return 'InEditingMode(%r)' % (self.editing_mode,)


@memoized()
class ViMode(Filter):

    def __call__(self, cli):
        return cli.editing_mode == EditingMode.VI

    def __repr__(self):
        return 'ViMode()'


@memoized()
class ViNavigationMode(Filter):
    """ViNavigationMode"""

    def __call__(self, cli):
        if cli.editing_mode != EditingMode.VI or cli.vi_state.operator_func or cli.vi_state.waiting_for_digraph or cli.current_buffer.selection_state:
            return False
        else:
            return cli.vi_state.input_mode == ViInputMode.NAVIGATION or cli.current_buffer.read_only()

    def __repr__(self):
        return 'ViNavigationMode()'


@memoized()
class ViInsertMode(Filter):

    def __call__(self, cli):
        if cli.editing_mode != EditingMode.VI or cli.vi_state.operator_func or cli.vi_state.waiting_for_digraph or cli.current_buffer.selection_state or cli.current_buffer.read_only():
            return False
        else:
            return cli.vi_state.input_mode == ViInputMode.INSERT

    def __repr__(self):
        return 'ViInputMode()'


@memoized()
class ViInsertMultipleMode(Filter):

    def __call__(self, cli):
        if cli.editing_mode != EditingMode.VI or cli.vi_state.operator_func or cli.vi_state.waiting_for_digraph or cli.current_buffer.selection_state or cli.current_buffer.read_only():
            return False
        else:
            return cli.vi_state.input_mode == ViInputMode.INSERT_MULTIPLE

    def __repr__(self):
        return 'ViInsertMultipleMode()'


@memoized()
class ViReplaceMode(Filter):

    def __call__(self, cli):
        if cli.editing_mode != EditingMode.VI or cli.vi_state.operator_func or cli.vi_state.waiting_for_digraph or cli.current_buffer.selection_state or cli.current_buffer.read_only():
            return False
        else:
            return cli.vi_state.input_mode == ViInputMode.REPLACE

    def __repr__(self):
        return 'ViReplaceMode()'


@memoized()
class ViSelectionMode(Filter):

    def __call__(self, cli):
        if cli.editing_mode != EditingMode.VI:
            return False
        else:
            return bool(cli.current_buffer.selection_state)

    def __repr__(self):
        return 'ViSelectionMode()'


@memoized()
class ViWaitingForTextObjectMode(Filter):

    def __call__(self, cli):
        if cli.editing_mode != EditingMode.VI:
            return False
        else:
            return cli.vi_state.operator_func is not None

    def __repr__(self):
        return 'ViWaitingForTextObjectMode()'


@memoized()
class ViDigraphMode(Filter):

    def __call__(self, cli):
        if cli.editing_mode != EditingMode.VI:
            return False
        else:
            return cli.vi_state.waiting_for_digraph

    def __repr__(self):
        return 'ViDigraphMode()'


@memoized()
class EmacsMode(Filter):
    """EmacsMode"""

    def __call__(self, cli):
        return cli.editing_mode == EditingMode.EMACS

    def __repr__(self):
        return 'EmacsMode()'


@memoized()
class EmacsInsertMode(Filter):

    def __call__(self, cli):
        if cli.editing_mode != EditingMode.EMACS or cli.current_buffer.selection_state or cli.current_buffer.read_only():
            return False
        else:
            return True

    def __repr__(self):
        return 'EmacsInsertMode()'


@memoized()
class EmacsSelectionMode(Filter):

    def __call__(self, cli):
        return cli.editing_mode == EditingMode.EMACS and cli.current_buffer.selection_state

    def __repr__(self):
        return 'EmacsSelectionMode()'