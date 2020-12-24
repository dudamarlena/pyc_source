# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/filters/cli.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 9227 bytes
"""
Filters that accept a `CommandLineInterface` as argument.
"""
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
    __doc__ = '\n    Enable when this buffer has the focus.\n    '

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
    __doc__ = '\n    Enable when this buffer appears on the focus stack.\n    '

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
    __doc__ = '\n    Enable when the current buffer has a selection.\n    '

    def __call__(self, cli):
        return bool(cli.current_buffer.selection_state)

    def __repr__(self):
        return 'HasSelection()'


@memoized()
class HasCompletions(Filter):
    __doc__ = '\n    Enable when the current buffer has completions.\n    '

    def __call__(self, cli):
        return cli.current_buffer.complete_state is not None

    def __repr__(self):
        return 'HasCompletions()'


@memoized()
class IsMultiline(Filter):
    __doc__ = '\n    Enable in multiline mode.\n    '

    def __call__(self, cli):
        return cli.current_buffer.is_multiline()

    def __repr__(self):
        return 'IsMultiline()'


@memoized()
class IsReadOnly(Filter):
    __doc__ = '\n    True when the current buffer is read only.\n    '

    def __call__(self, cli):
        return cli.current_buffer.read_only()

    def __repr__(self):
        return 'IsReadOnly()'


@memoized()
class HasValidationError(Filter):
    __doc__ = '\n    Current buffer has validation error.\n    '

    def __call__(self, cli):
        return cli.current_buffer.validation_error is not None

    def __repr__(self):
        return 'HasValidationError()'


@memoized()
class HasArg(Filter):
    __doc__ = "\n    Enable when the input processor has an 'arg'.\n    "

    def __call__(self, cli):
        return cli.input_processor.arg is not None

    def __repr__(self):
        return 'HasArg()'


@memoized()
class HasSearch(Filter):
    __doc__ = '\n    Incremental search is active.\n    '

    def __call__(self, cli):
        return cli.is_searching

    def __repr__(self):
        return 'HasSearch()'


@memoized()
class IsReturning(Filter):
    __doc__ = '\n    When a return value has been set.\n    '

    def __call__(self, cli):
        return cli.is_returning

    def __repr__(self):
        return 'IsReturning()'


@memoized()
class IsAborting(Filter):
    __doc__ = '\n    True when aborting. (E.g. Control-C pressed.)\n    '

    def __call__(self, cli):
        return cli.is_aborting

    def __repr__(self):
        return 'IsAborting()'


@memoized()
class IsExiting(Filter):
    __doc__ = '\n    True when exiting. (E.g. Control-D pressed.)\n    '

    def __call__(self, cli):
        return cli.is_exiting

    def __repr__(self):
        return 'IsExiting()'


@memoized()
class IsDone(Filter):
    __doc__ = '\n    True when the CLI is returning, aborting or exiting.\n    '

    def __call__(self, cli):
        return cli.is_done

    def __repr__(self):
        return 'IsDone()'


@memoized()
class RendererHeightIsKnown(Filter):
    __doc__ = "\n    Only True when the renderer knows it's real height.\n\n    (On VT100 terminals, we have to wait for a CPR response, before we can be\n    sure of the available height between the cursor position and the bottom of\n    the terminal. And usually it's nicer to wait with drawing bottom toolbars\n    until we receive the height, in order to avoid flickering -- first drawing\n    somewhere in the middle, and then again at the bottom.)\n    "

    def __call__(self, cli):
        return cli.renderer.height_is_known

    def __repr__(self):
        return 'RendererHeightIsKnown()'


@memoized()
class InEditingMode(Filter):
    __doc__ = '\n    Check whether a given editing mode is active. (Vi or Emacs.)\n    '

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
    __doc__ = '\n    Active when the set for Vi navigation key bindings are active.\n    '

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
    __doc__ = ' When the Emacs bindings are active. '

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