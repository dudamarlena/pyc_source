# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/shortcuts.py
# Compiled at: 2019-08-15 23:53:39
# Size of source mod 2**32: 28189 bytes
"""
Shortcuts for retrieving input from the user.

If you are using this library for retrieving some input from the user (as a
pure Python replacement for GNU readline), probably for 90% of the use cases,
the :func:`.prompt` function is all you need. It's the easiest shortcut which
does a lot of the underlying work like creating a
:class:`~prompt_tool_kit.interface.CommandLineInterface` instance for you.

When is this not sufficient:
    - When you want to have more complicated layouts (maybe with sidebars or
      multiple toolbars. Or visibility of certain user interface controls
      according to some conditions.)
    - When you wish to have multiple input buffers. (If you would create an
      editor like a Vi clone.)
    - Something else that requires more customization than what is possible
      with the parameters of `prompt`.

In that case, study the code in this file and build your own
`CommandLineInterface` instance. It's not too complicated.
"""
from __future__ import unicode_literals
from .buffer import Buffer, AcceptAction
from .document import Document
from .enums import DEFAULT_BUFFER, SEARCH_BUFFER, EditingMode
from .filters import IsDone, HasFocus, RendererHeightIsKnown, to_simple_filter, to_cli_filter, Condition
from .history import InMemoryHistory
from .interface import CommandLineInterface, Application, AbortAction
from .key_binding.defaults import load_key_bindings_for_prompt
from .key_binding.registry import Registry
from .keys import Keys
from .layout import Window, HSplit, FloatContainer, Float
from .layout.containers import ConditionalContainer
from .layout.controls import BufferControl, TokenListControl
from .layout.dimension import LayoutDimension
from .layout.lexers import PygmentsLexer
from .layout.margins import PromptMargin, ConditionalMargin
from .layout.menus import CompletionsMenu, MultiColumnCompletionsMenu
from .layout.processors import PasswordProcessor, ConditionalProcessor, AppendAutoSuggestion, HighlightSearchProcessor, HighlightSelectionProcessor, DisplayMultipleCursors
from .layout.prompt import DefaultPrompt
from .layout.screen import Char
from .layout.toolbars import ValidationToolbar, SystemToolbar, ArgToolbar, SearchToolbar
from .layout.utils import explode_tokens
from .renderer import print_tokens as renderer_print_tokens
from .styles import DEFAULT_STYLE, Style, style_from_dict
from .token import Token
from .utils import is_conemu_ansi, is_windows, DummyContext
from six import text_type, exec_, PY2
import os, sys, textwrap, threading, time
try:
    from pygments.lexer import Lexer as pygments_Lexer
    from pygments.style import Style as pygments_Style
except ImportError:
    pygments_Lexer = None
    pygments_Style = None

if is_windows():
    from .terminal.win32_output import Win32Output
    from .terminal.conemu_output import ConEmuOutput
else:
    from .terminal.vt100_output import Vt100_Output
__all__ = ('create_eventloop', 'create_output', 'create_prompt_layout', 'create_prompt_application',
           'prompt', 'prompt_async', 'create_confirm_application', 'run_application',
           'confirm', 'print_tokens', 'clear')

def create_eventloop(inputhook=None, recognize_win32_paste=True):
    """
    Create and return an
    :class:`~prompt_tool_kit.eventloop.base.EventLoop` instance for a
    :class:`~prompt_tool_kit.interface.CommandLineInterface`.
    """
    if is_windows():
        from prompt_tool_kit.eventloop.win32 import Win32EventLoop as Loop
        return Loop(inputhook=inputhook, recognize_paste=recognize_win32_paste)
    else:
        from prompt_tool_kit.eventloop.posix import PosixEventLoop as Loop
        return Loop(inputhook=inputhook)


def create_output(stdout=None, true_color=False, ansi_colors_only=None):
    """
    Return an :class:`~prompt_tool_kit.output.Output` instance for the command
    line.

    :param true_color: When True, use 24bit colors instead of 256 colors.
        (`bool` or :class:`~prompt_tool_kit.filters.SimpleFilter`.)
    :param ansi_colors_only: When True, restrict to 16 ANSI colors only.
        (`bool` or :class:`~prompt_tool_kit.filters.SimpleFilter`.)
    """
    stdout = stdout or sys.__stdout__
    true_color = to_simple_filter(true_color)
    if is_windows():
        if is_conemu_ansi():
            return ConEmuOutput(stdout)
        else:
            return Win32Output(stdout)
    else:
        term = os.environ.get('TERM', '')
        if PY2:
            term = term.decode('utf-8')
        return Vt100_Output.from_pty(stdout,
          true_color=true_color, ansi_colors_only=ansi_colors_only,
          term=term)


def create_asyncio_eventloop(loop=None):
    """
    Returns an asyncio :class:`~prompt_tool_kit.eventloop.EventLoop` instance
    for usage in a :class:`~prompt_tool_kit.interface.CommandLineInterface`. It
    is a wrapper around an asyncio loop.

    :param loop: The asyncio eventloop (or `None` if the default asyncioloop
                 should be used.)
    """
    if is_windows():
        from prompt_tool_kit.eventloop.asyncio_win32 import Win32AsyncioEventLoop as AsyncioEventLoop
    else:
        from prompt_tool_kit.eventloop.asyncio_posix import PosixAsyncioEventLoop as AsyncioEventLoop
    return AsyncioEventLoop(loop)


def _split_multiline_prompt(get_prompt_tokens):
    """
    Take a `get_prompt_tokens` function and return three new functions instead.
    One that tells whether this prompt consists of multiple lines; one that
    returns the tokens to be shown on the lines above the input; and another
    one with the tokens to be shown at the first line of the input.
    """

    def has_before_tokens(cli):
        for token, char in get_prompt_tokens(cli):
            if '\n' in char:
                return True

        return False

    def before(cli):
        result = []
        found_nl = False
        for token, char in reversed(explode_tokens(get_prompt_tokens(cli))):
            if found_nl:
                result.insert(0, (token, char))
            else:
                if char == '\n':
                    found_nl = True

        return result

    def first_input_line(cli):
        result = []
        for token, char in reversed(explode_tokens(get_prompt_tokens(cli))):
            if char == '\n':
                break
            else:
                result.insert(0, (token, char))

        return result

    return (
     has_before_tokens, before, first_input_line)


class _RPrompt(Window):
    __doc__ = ' The prompt that is displayed on the right side of the Window. '

    def __init__(self, get_tokens=None):
        get_tokens = get_tokens or (lambda cli: [])
        super(_RPrompt, self).__init__(TokenListControl(get_tokens, align_right=True))


def create_prompt_layout(message='', lexer=None, is_password=False, reserve_space_for_menu=8, get_prompt_tokens=None, get_continuation_tokens=None, get_rprompt_tokens=None, get_bottom_toolbar_tokens=None, display_completions_in_columns=False, extra_input_processors=None, multiline=False, wrap_lines=True):
    """
    Create a :class:`.Container` instance for a prompt.

    :param message: Text to be used as prompt.
    :param lexer: :class:`~prompt_tool_kit.layout.lexers.Lexer` to be used for
        the highlighting.
    :param is_password: `bool` or :class:`~prompt_tool_kit.filters.CLIFilter`.
        When True, display input as '*'.
    :param reserve_space_for_menu: Space to be reserved for the menu. When >0,
        make sure that a minimal height is allocated in the terminal, in order
        to display the completion menu.
    :param get_prompt_tokens: An optional callable that returns the tokens to be
        shown in the menu. (To be used instead of a `message`.)
    :param get_continuation_tokens: An optional callable that takes a
        CommandLineInterface and width as input and returns a list of (Token,
        text) tuples to be used for the continuation.
    :param get_bottom_toolbar_tokens: An optional callable that returns the
        tokens for a toolbar at the bottom.
    :param display_completions_in_columns: `bool` or
        :class:`~prompt_tool_kit.filters.CLIFilter`. Display the completions in
        multiple columns.
    :param multiline: `bool` or :class:`~prompt_tool_kit.filters.CLIFilter`.
        When True, prefer a layout that is more adapted for multiline input.
        Text after newlines is automatically indented, and search/arg input is
        shown below the input, instead of replacing the prompt.
    :param wrap_lines: `bool` or :class:`~prompt_tool_kit.filters.CLIFilter`.
        When True (the default), automatically wrap long lines instead of
        scrolling horizontally.
    """
    if not isinstance(message, text_type):
        raise AssertionError('Please provide a unicode string.')
    else:
        if not get_bottom_toolbar_tokens is None:
            if not callable(get_bottom_toolbar_tokens):
                raise AssertionError
            else:
                if not get_prompt_tokens is None:
                    if not callable(get_prompt_tokens):
                        raise AssertionError
                if not get_rprompt_tokens is None:
                    if not callable(get_rprompt_tokens):
                        raise AssertionError
                assert not (message and get_prompt_tokens)
            display_completions_in_columns = to_cli_filter(display_completions_in_columns)
            multiline = to_cli_filter(multiline)
            if get_prompt_tokens is None:
                get_prompt_tokens = lambda _: [
                 (
                  Token.Prompt, message)]
        else:
            has_before_tokens, get_prompt_tokens_1, get_prompt_tokens_2 = _split_multiline_prompt(get_prompt_tokens)
            try:
                if pygments_Lexer:
                    if issubclass(lexer, pygments_Lexer):
                        lexer = PygmentsLexer(lexer, sync_from_start=True)
            except TypeError:
                pass

            input_processors = [
             ConditionalProcessor(HighlightSearchProcessor(preview_search=True), HasFocus(SEARCH_BUFFER)),
             HighlightSelectionProcessor(),
             ConditionalProcessor(AppendAutoSuggestion(), HasFocus(DEFAULT_BUFFER) & ~IsDone()),
             ConditionalProcessor(PasswordProcessor(), is_password),
             DisplayMultipleCursors(DEFAULT_BUFFER)]
            if extra_input_processors:
                input_processors.extend(extra_input_processors)
        input_processors.append(ConditionalProcessor(DefaultPrompt(get_prompt_tokens_2), ~multiline))
        if get_bottom_toolbar_tokens:
            toolbars = [
             ConditionalContainer(Window(TokenListControl(get_bottom_toolbar_tokens, default_char=(Char(' ', Token.Toolbar))),
               height=(LayoutDimension.exact(1))),
               filter=(~IsDone() & RendererHeightIsKnown()))]
        else:
            toolbars = []

    def get_height(cli):
        if reserve_space_for_menu:
            if not cli.is_done:
                buff = cli.current_buffer
                if buff.complete_while_typing() or buff.complete_state is not None:
                    return LayoutDimension(min=reserve_space_for_menu)
        return LayoutDimension()

    return HSplit([
     FloatContainer(HSplit([
      ConditionalContainer(Window((TokenListControl(get_prompt_tokens_1)),
        dont_extend_height=True), Condition(has_before_tokens)),
      Window(BufferControl(input_processors=input_processors,
        lexer=lexer,
        preview_search=True),
        get_height=get_height,
        left_margins=[
       ConditionalMargin((PromptMargin(get_prompt_tokens_2, get_continuation_tokens)),
         filter=multiline)],
        wrap_lines=wrap_lines)]), [
      Float(xcursor=True, ycursor=True,
        content=CompletionsMenu(max_height=16,
        scroll_offset=1,
        extra_filter=(HasFocus(DEFAULT_BUFFER) & ~display_completions_in_columns))),
      Float(xcursor=True, ycursor=True,
        content=MultiColumnCompletionsMenu(extra_filter=(HasFocus(DEFAULT_BUFFER) & display_completions_in_columns),
        show_meta=True)),
      Float(right=0, top=0, hide_when_covering_content=True, content=(_RPrompt(get_rprompt_tokens)))]),
     ValidationToolbar(),
     SystemToolbar(),
     ConditionalContainer(ArgToolbar(), multiline),
     ConditionalContainer(SearchToolbar(), multiline)] + toolbars)


def create_prompt_application(message, multiline, wrap_lines, is_password, vi_mode, editing_mode, complete_while_typing, enable_history_search, lexer, enable_system_bindings, enable_open_in_editor, validator, completer, reserve_space_for_menu, auto_suggest, style, history, clipboard, get_prompt_tokens, get_continuation_tokens, get_rprompt_tokens, get_bottom_toolbar_tokens, display_completions_in_columns, get_title, mouse_support, extra_input_processors, key_bindings_registry, on_abort, on_exit, accept_action, erase_when_done, default=''FalseTrueFalseFalseEditingMode.EMACSTrueFalseNoneFalseFalseNoneNone8NoneNoneNoneNoneNoneNoneNoneNoneFalseNoneFalseNoneNoneAbortAction.RAISE_EXCEPTIONAbortAction.RAISE_EXCEPTIONAcceptAction.RETURN_DOCUMENTFalse''):
    """
    Create an :class:`~Application` instance for a prompt.

    (It is meant to cover 90% of the prompt use cases, where no extreme
    customization is required. For more complex input, it is required to create
    a custom :class:`~Application` instance.)

    :param message: Text to be shown before the prompt.
    :param mulitiline: Allow multiline input. Pressing enter will insert a
                       newline. (This requires Meta+Enter to accept the input.)
    :param wrap_lines: `bool` or :class:`~prompt_tool_kit.filters.CLIFilter`.
        When True (the default), automatically wrap long lines instead of
        scrolling horizontally.
    :param is_password: Show asterisks instead of the actual typed characters.
    :param editing_mode: ``EditingMode.VI`` or ``EditingMode.EMACS``.
    :param vi_mode: `bool`, if True, Identical to ``editing_mode=EditingMode.VI``.
    :param complete_while_typing: `bool` or
        :class:`~prompt_tool_kit.filters.SimpleFilter`. Enable autocompletion
        while typing.
    :param enable_history_search: `bool` or
        :class:`~prompt_tool_kit.filters.SimpleFilter`. Enable up-arrow parting
        string matching.
    :param lexer: :class:`~prompt_tool_kit.layout.lexers.Lexer` to be used for
        the syntax highlighting.
    :param validator: :class:`~prompt_tool_kit.validation.Validator` instance
        for input validation.
    :param completer: :class:`~prompt_tool_kit.completion.Completer` instance
        for input completion.
    :param reserve_space_for_menu: Space to be reserved for displaying the menu.
        (0 means that no space needs to be reserved.)
    :param auto_suggest: :class:`~prompt_tool_kit.auto_suggest.AutoSuggest`
        instance for input suggestions.
    :param style: :class:`.Style` instance for the color scheme.
    :param enable_system_bindings: `bool` or
        :class:`~prompt_tool_kit.filters.CLIFilter`. Pressing Meta+'!' will show
        a system prompt.
    :param enable_open_in_editor: `bool` or
        :class:`~prompt_tool_kit.filters.CLIFilter`. Pressing 'v' in Vi mode or
        C-X C-E in emacs mode will open an external editor.
    :param history: :class:`~prompt_tool_kit.history.History` instance.
    :param clipboard: :class:`~prompt_tool_kit.clipboard.base.Clipboard` instance.
        (e.g. :class:`~prompt_tool_kit.clipboard.in_memory.InMemoryClipboard`)
    :param get_bottom_toolbar_tokens: Optional callable which takes a
        :class:`~prompt_tool_kit.interface.CommandLineInterface` and returns a
        list of tokens for the bottom toolbar.
    :param display_completions_in_columns: `bool` or
        :class:`~prompt_tool_kit.filters.CLIFilter`. Display the completions in
        multiple columns.
    :param get_title: Callable that returns the title to be displayed in the
        terminal.
    :param mouse_support: `bool` or :class:`~prompt_tool_kit.filters.CLIFilter`
        to enable mouse support.
    :param default: The default text to be shown in the input buffer. (This can
        be edited by the user.)
    """
    if key_bindings_registry is None:
        key_bindings_registry = load_key_bindings_for_prompt(enable_system_bindings=enable_system_bindings,
          enable_open_in_editor=enable_open_in_editor)
    else:
        if vi_mode:
            editing_mode = EditingMode.VI
        complete_while_typing = to_simple_filter(complete_while_typing)
        enable_history_search = to_simple_filter(enable_history_search)
        multiline = to_simple_filter(multiline)
        complete_while_typing = complete_while_typing & ~enable_history_search
        try:
            if pygments_Style:
                if issubclass(style, pygments_Style):
                    style = style_from_dict(style.styles)
        except TypeError:
            pass

    return Application(layout=create_prompt_layout(message=message,
      lexer=lexer,
      is_password=is_password,
      reserve_space_for_menu=(reserve_space_for_menu if completer is not None else 0),
      multiline=(Condition(lambda cli: multiline())),
      get_prompt_tokens=get_prompt_tokens,
      get_continuation_tokens=get_continuation_tokens,
      get_rprompt_tokens=get_rprompt_tokens,
      get_bottom_toolbar_tokens=get_bottom_toolbar_tokens,
      display_completions_in_columns=display_completions_in_columns,
      extra_input_processors=extra_input_processors,
      wrap_lines=wrap_lines),
      buffer=Buffer(enable_history_search=enable_history_search,
      complete_while_typing=complete_while_typing,
      is_multiline=multiline,
      history=(history or InMemoryHistory()),
      validator=validator,
      completer=completer,
      auto_suggest=auto_suggest,
      accept_action=accept_action,
      initial_document=(Document(default))),
      style=(style or DEFAULT_STYLE),
      clipboard=clipboard,
      key_bindings_registry=key_bindings_registry,
      get_title=get_title,
      mouse_support=mouse_support,
      editing_mode=editing_mode,
      erase_when_done=erase_when_done,
      reverse_vi_search_direction=True,
      on_abort=on_abort,
      on_exit=on_exit)


def prompt(message='', **kwargs):
    """
    Get input from the user and return it.

    This is a wrapper around a lot of ``prompt_tool_kit`` functionality and can
    be a replacement for `raw_input`. (or GNU readline.)

    If you want to keep your history across several calls, create one
    :class:`~prompt_tool_kit.history.History` instance and pass it every time.

    This function accepts many keyword arguments. Except for the following,
    they are a proxy to the arguments of :func:`.create_prompt_application`.

    :param patch_stdout: Replace ``sys.stdout`` by a proxy that ensures that
            print statements from other threads won't destroy the prompt. (They
            will be printed above the prompt instead.)
    :param return_asyncio_coroutine: When True, return a asyncio coroutine. (Python >3.3)
    :param true_color: When True, use 24bit colors instead of 256 colors.
    :param refresh_interval: (number; in seconds) When given, refresh the UI
        every so many seconds.
    """
    patch_stdout = kwargs.pop('patch_stdout', False)
    return_asyncio_coroutine = kwargs.pop('return_asyncio_coroutine', False)
    true_color = kwargs.pop('true_color', False)
    refresh_interval = kwargs.pop('refresh_interval', 0)
    eventloop = kwargs.pop('eventloop', None)
    application = create_prompt_application(message, **kwargs)
    return run_application(application, patch_stdout=patch_stdout,
      return_asyncio_coroutine=return_asyncio_coroutine,
      true_color=true_color,
      refresh_interval=refresh_interval,
      eventloop=eventloop)


def run_application(application, patch_stdout=False, return_asyncio_coroutine=False, true_color=False, refresh_interval=0, eventloop=None):
    """
    Run a prompt toolkit application.

    :param patch_stdout: Replace ``sys.stdout`` by a proxy that ensures that
            print statements from other threads won't destroy the prompt. (They
            will be printed above the prompt instead.)
    :param return_asyncio_coroutine: When True, return a asyncio coroutine. (Python >3.3)
    :param true_color: When True, use 24bit colors instead of 256 colors.
    :param refresh_interval: (number; in seconds) When given, refresh the UI
        every so many seconds.
    """
    if not isinstance(application, Application):
        raise AssertionError
    else:
        if return_asyncio_coroutine:
            eventloop = create_asyncio_eventloop()
        else:
            eventloop = eventloop or create_eventloop()
        cli = CommandLineInterface(application=application,
          eventloop=eventloop,
          output=create_output(true_color=true_color))
        if refresh_interval:
            done = [
             False]

            def start_refresh_loop(cli):

                def run():
                    while not done[0]:
                        time.sleep(refresh_interval)
                        cli.request_redraw()

                t = threading.Thread(target=run)
                t.daemon = True
                t.start()

            def stop_refresh_loop(cli):
                done[0] = True

            cli.on_start += start_refresh_loop
            cli.on_stop += stop_refresh_loop
        patch_context = cli.patch_stdout_context(raw=True) if patch_stdout else DummyContext()
        if return_asyncio_coroutine:
            exec_context = {'patch_context':patch_context,  'cli':cli,  'Document':Document}
            exec_(textwrap.dedent('\n        def prompt_coro():\n            # Inline import, because it slows down startup when asyncio is not\n            # needed.\n            import asyncio\n\n            @asyncio.coroutine\n            def run():\n                with patch_context:\n                    result = yield from cli.run_async()\n\n                if isinstance(result, Document):  # Backwards-compatibility.\n                    return result.text\n                return result\n            return run()\n        '), exec_context)
            return exec_context['prompt_coro']()
    try:
        with patch_context:
            result = cli.run()
        if isinstance(result, Document):
            return result.text
        return result
    finally:
        eventloop.close()


def prompt_async(message='', **kwargs):
    """
    Similar to :func:`.prompt`, but return an asyncio coroutine instead.
    """
    kwargs['return_asyncio_coroutine'] = True
    return prompt(message, **kwargs)


def create_confirm_application(message):
    """
    Create a confirmation `Application` that returns True/False.
    """
    registry = Registry()

    @registry.add_binding('y')
    @registry.add_binding('Y')
    def _(event):
        event.cli.buffers[DEFAULT_BUFFER].text = 'y'
        event.cli.set_return_value(True)

    @registry.add_binding('n')
    @registry.add_binding('N')
    @registry.add_binding(Keys.ControlC)
    def _(event):
        event.cli.buffers[DEFAULT_BUFFER].text = 'n'
        event.cli.set_return_value(False)

    return create_prompt_application(message, key_bindings_registry=registry)


def confirm(message='Confirm (y or n) '):
    """
    Display a confirmation prompt.
    """
    assert isinstance(message, text_type)
    app = create_confirm_application(message)
    return run_application(app)


def print_tokens(tokens, style=None, true_color=False, file=None):
    """
    Print a list of (Token, text) tuples in the given style to the output.
    E.g.::

        style = style_from_dict({
            Token.Hello: '#ff0066',
            Token.World: '#884444 italic',
        })
        tokens = [
            (Token.Hello, 'Hello'),
            (Token.World, 'World'),
        ]
        print_tokens(tokens, style=style)

    :param tokens: List of ``(Token, text)`` tuples.
    :param style: :class:`.Style` instance for the color scheme.
    :param true_color: When True, use 24bit colors instead of 256 colors.
    :param file: The output file. This can be `sys.stdout` or `sys.stderr`.
    """
    if style is None:
        style = DEFAULT_STYLE
    elif not isinstance(style, Style):
        raise AssertionError
    output = create_output(true_color=true_color, stdout=file)
    renderer_print_tokens(output, tokens, style)


def clear():
    """
    Clear the screen.
    """
    out = create_output()
    out.erase_screen()
    out.cursor_goto(0, 0)
    out.flush()


get_input = prompt
create_default_layout = create_prompt_layout
create_default_application = create_prompt_application