# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/application.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 8759 bytes
from __future__ import unicode_literals
from .buffer import Buffer, AcceptAction
from .buffer_mapping import BufferMapping
from .clipboard import Clipboard, InMemoryClipboard
from .enums import DEFAULT_BUFFER, EditingMode
from .filters import CLIFilter, to_cli_filter
from .key_binding.bindings.basic import load_basic_bindings
from .key_binding.bindings.emacs import load_emacs_bindings
from .key_binding.bindings.vi import load_vi_bindings
from .key_binding.registry import BaseRegistry
from .key_binding.defaults import load_key_bindings
from .layout import Window
from .layout.containers import Container
from .layout.controls import BufferControl
from .styles import DEFAULT_STYLE, Style
import six
__all__ = ('AbortAction', 'Application')

class AbortAction(object):
    __doc__ = '\n    Actions to take on an Exit or Abort exception.\n    '
    RETRY = 'retry'
    RAISE_EXCEPTION = 'raise-exception'
    RETURN_NONE = 'return-none'
    _all = (
     RETRY, RAISE_EXCEPTION, RETURN_NONE)


class Application(object):
    __doc__ = "\n    Application class to be passed to a\n    :class:`~prompt_tool_kit.interface.CommandLineInterface`.\n\n    This contains all customizable logic that is not I/O dependent.\n    (So, what is independent of event loops, input and output.)\n\n    This way, such an :class:`.Application` can run easily on several\n    :class:`~prompt_tool_kit.interface.CommandLineInterface` instances, each\n    with a different I/O backends. that runs for instance over telnet, SSH or\n    any other I/O backend.\n\n    :param layout: A :class:`~prompt_tool_kit.layout.containers.Container` instance.\n    :param buffer: A :class:`~prompt_tool_kit.buffer.Buffer` instance for the default buffer.\n    :param initial_focussed_buffer: Name of the buffer that is focussed during start-up.\n    :param key_bindings_registry:\n        :class:`~prompt_tool_kit.key_binding.registry.BaseRegistry` instance for\n        the key bindings.\n    :param clipboard: :class:`~prompt_tool_kit.clipboard.base.Clipboard` to use.\n    :param on_abort: What to do when Control-C is pressed.\n    :param on_exit: What to do when Control-D is pressed.\n    :param use_alternate_screen: When True, run the application on the alternate screen buffer.\n    :param get_title: Callable that returns the current title to be displayed in the terminal.\n    :param erase_when_done: (bool) Clear the application output when it finishes.\n    :param reverse_vi_search_direction: Normally, in Vi mode, a '/' searches\n        forward and a '?' searches backward. In readline mode, this is usually\n        reversed.\n\n    Filters:\n\n    :param mouse_support: (:class:`~prompt_tool_kit.filters.CLIFilter` or\n        boolean). When True, enable mouse support.\n    :param paste_mode: :class:`~prompt_tool_kit.filters.CLIFilter` or boolean.\n    :param ignore_case: :class:`~prompt_tool_kit.filters.CLIFilter` or boolean.\n    :param editing_mode: :class:`~prompt_tool_kit.enums.EditingMode`.\n\n    Callbacks (all of these should accept a\n    :class:`~prompt_tool_kit.interface.CommandLineInterface` object as input.)\n\n    :param on_input_timeout: Called when there is no input for x seconds.\n                    (Fired when any eventloop.onInputTimeout is fired.)\n    :param on_start: Called when reading input starts.\n    :param on_stop: Called when reading input ends.\n    :param on_reset: Called during reset.\n    :param on_buffer_changed: Called when the content of a buffer has been changed.\n    :param on_initialize: Called after the\n        :class:`~prompt_tool_kit.interface.CommandLineInterface` initializes.\n    :param on_render: Called right after rendering.\n    :param on_invalidate: Called when the UI has been invalidated.\n    "

    def __init__(self, layout=None, buffer=None, buffers=None, initial_focussed_buffer=DEFAULT_BUFFER, style=None, key_bindings_registry=None, clipboard=None, on_abort=AbortAction.RAISE_EXCEPTION, on_exit=AbortAction.RAISE_EXCEPTION, use_alternate_screen=False, mouse_support=False, get_title=None, paste_mode=False, ignore_case=False, editing_mode=EditingMode.EMACS, erase_when_done=False, reverse_vi_search_direction=False, on_input_timeout=None, on_start=None, on_stop=None, on_reset=None, on_initialize=None, on_buffer_changed=None, on_render=None, on_invalidate=None):
        paste_mode = to_cli_filter(paste_mode)
        ignore_case = to_cli_filter(ignore_case)
        mouse_support = to_cli_filter(mouse_support)
        reverse_vi_search_direction = to_cli_filter(reverse_vi_search_direction)
        if not layout is None:
            if not isinstance(layout, Container):
                raise AssertionError
        if not buffer is None:
            if not isinstance(buffer, Buffer):
                raise AssertionError
        if not buffers is None:
            if not isinstance(buffers, (dict, BufferMapping)):
                raise AssertionError
        if not key_bindings_registry is None:
            if not isinstance(key_bindings_registry, BaseRegistry):
                raise AssertionError
        if not clipboard is None:
            if not isinstance(clipboard, Clipboard):
                raise AssertionError
        if not on_abort in AbortAction._all:
            raise AssertionError
        else:
            if not on_exit in AbortAction._all:
                raise AssertionError
            else:
                if not isinstance(use_alternate_screen, bool):
                    raise AssertionError
                else:
                    if not get_title is None:
                        if not callable(get_title):
                            raise AssertionError
                    assert isinstance(paste_mode, CLIFilter)
                assert isinstance(ignore_case, CLIFilter)
            assert isinstance(editing_mode, six.string_types)
        if not on_input_timeout is None:
            if not callable(on_input_timeout):
                raise AssertionError
        if not style is None:
            if not isinstance(style, Style):
                raise AssertionError
        if not isinstance(erase_when_done, bool):
            raise AssertionError
        else:
            if not on_start is None:
                if not callable(on_start):
                    raise AssertionError
                elif not on_stop is None:
                    if not callable(on_stop):
                        raise AssertionError
                else:
                    if not on_reset is None:
                        if not callable(on_reset):
                            raise AssertionError
                    if not on_buffer_changed is None:
                        assert callable(on_buffer_changed)
                if not on_initialize is None:
                    assert callable(on_initialize)
            elif not on_render is None:
                if not callable(on_render):
                    raise AssertionError
            elif not on_invalidate is None:
                assert callable(on_invalidate)
            self.layout = layout or Window(BufferControl())
            self.buffer = buffer or Buffer(accept_action=(AcceptAction.IGNORE))
            if not buffers or not isinstance(buffers, BufferMapping):
                self.buffers = BufferMapping(buffers, initial=initial_focussed_buffer)
            else:
                self.buffers = buffers
        if buffer:
            self.buffers[DEFAULT_BUFFER] = buffer
        self.initial_focussed_buffer = initial_focussed_buffer
        self.style = style or DEFAULT_STYLE
        if key_bindings_registry is None:
            key_bindings_registry = load_key_bindings()
        if get_title is None:
            get_title = lambda : None
        self.key_bindings_registry = key_bindings_registry
        self.clipboard = clipboard or InMemoryClipboard()
        self.on_abort = on_abort
        self.on_exit = on_exit
        self.use_alternate_screen = use_alternate_screen
        self.mouse_support = mouse_support
        self.get_title = get_title
        self.paste_mode = paste_mode
        self.ignore_case = ignore_case
        self.editing_mode = editing_mode
        self.erase_when_done = erase_when_done
        self.reverse_vi_search_direction = reverse_vi_search_direction

        def dummy_handler(cli):
            """ Dummy event handler. """
            pass

        self.on_input_timeout = on_input_timeout or dummy_handler
        self.on_start = on_start or dummy_handler
        self.on_stop = on_stop or dummy_handler
        self.on_reset = on_reset or dummy_handler
        self.on_initialize = on_initialize or dummy_handler
        self.on_buffer_changed = on_buffer_changed or dummy_handler
        self.on_render = on_render or dummy_handler
        self.on_invalidate = on_invalidate or dummy_handler
        self.pre_run_callables = []