# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/renderer.py
# Compiled at: 2019-08-15 23:53:39
# Size of source mod 2**32: 19233 bytes
"""
Renders the command line on the console.
(Redraws parts of the input line that were changed.)
"""
from __future__ import unicode_literals
from prompt_tool_kit.filters import to_cli_filter
from prompt_tool_kit.layout.mouse_handlers import MouseHandlers
from prompt_tool_kit.layout.screen import Point, Screen, WritePosition
from prompt_tool_kit.output import Output
from prompt_tool_kit.styles import Style
from prompt_tool_kit.token import Token
from prompt_tool_kit.utils import is_windows
from six.moves import range
__all__ = ('Renderer', 'print_tokens')

def _output_screen_diff(output, screen, current_pos, previous_screen=None, last_token=None, is_done=False, attrs_for_token=None, size=None, previous_width=0):
    """
    Render the diff between this screen and the previous screen.

    This takes two `Screen` instances. The one that represents the output like
    it was during the last rendering and one that represents the current
    output raster. Looking at these two `Screen` instances, this function will
    render the difference by calling the appropriate methods of the `Output`
    object that only paint the changes to the terminal.

    This is some performance-critical code which is heavily optimized.
    Don't change things without profiling first.

    :param current_pos: Current cursor position.
    :param last_token: `Token` instance that represents the output attributes of
            the last drawn character. (Color/attributes.)
    :param attrs_for_token: :class:`._TokenToAttrsCache` instance.
    :param width: The width of the terminal.
    :param prevous_width: The width of the terminal during the last rendering.
    """
    width, height = size.columns, size.rows
    last_token = [
     last_token]
    write = output.write
    write_raw = output.write_raw
    _output_set_attributes = output.set_attributes
    _output_reset_attributes = output.reset_attributes
    _output_cursor_forward = output.cursor_forward
    _output_cursor_up = output.cursor_up
    _output_cursor_backward = output.cursor_backward
    output.hide_cursor()

    def reset_attributes():
        _output_reset_attributes()
        last_token[0] = None

    def move_cursor(new):
        current_x, current_y = current_pos.x, current_pos.y
        if new.y > current_y:
            reset_attributes()
            write('\r\n' * (new.y - current_y))
            current_x = 0
            _output_cursor_forward(new.x)
            return new
        else:
            if new.y < current_y:
                _output_cursor_up(current_y - new.y)
            if current_x >= width - 1:
                write('\r')
                _output_cursor_forward(new.x)
            else:
                if new.x < current_x or current_x >= width - 1:
                    _output_cursor_backward(current_x - new.x)
                else:
                    if new.x > current_x:
                        _output_cursor_forward(new.x - current_x)
            return new

    def output_char(char):
        the_last_token = last_token[0]
        if the_last_token:
            if the_last_token == char.token:
                write(char.char)
        else:
            _output_set_attributes(attrs_for_token[char.token])
            write(char.char)
            last_token[0] = char.token

    if not previous_screen:
        output.disable_autowrap()
        reset_attributes()
    if is_done or not previous_screen or previous_width != width:
        current_pos = move_cursor(Point(0, 0))
        reset_attributes()
        output.erase_down()
        previous_screen = Screen()
    else:
        current_height = min(screen.height, height)
        row_count = min(max(screen.height, previous_screen.height), height)
        c = 0
        for y in range(row_count):
            new_row = screen.data_buffer[y]
            previous_row = previous_screen.data_buffer[y]
            zero_width_escapes_row = screen.zero_width_escapes[y]
            new_max_line_len = min(width - 1, max(new_row.keys()) if new_row else 0)
            previous_max_line_len = min(width - 1, max(previous_row.keys()) if previous_row else 0)
            c = 0
            while c < new_max_line_len + 1:
                new_char = new_row[c]
                old_char = previous_row[c]
                char_width = new_char.width or 1
                if new_char.char != old_char.char or new_char.token != old_char.token:
                    current_pos = move_cursor(Point(y=y, x=c))
                    if c in zero_width_escapes_row:
                        write_raw(zero_width_escapes_row[c])
                    output_char(new_char)
                    current_pos = current_pos._replace(x=(current_pos.x + char_width))
                c += char_width

            if previous_screen and new_max_line_len < previous_max_line_len:
                current_pos = move_cursor(Point(y=y, x=(new_max_line_len + 1)))
                reset_attributes()
                output.erase_end_of_line()

        if current_height > previous_screen.height:
            current_pos = move_cursor(Point(y=(current_height - 1), x=0))
        if is_done:
            current_pos = move_cursor(Point(y=current_height, x=0))
            output.erase_down()
        else:
            current_pos = move_cursor(screen.cursor_position)
    if is_done:
        output.enable_autowrap()
    reset_attributes()
    if screen.show_cursor or is_done:
        output.show_cursor()
    return (current_pos, last_token[0])


class HeightIsUnknownError(Exception):
    __doc__ = ' Information unavailable. Did not yet receive the CPR response. '


class _TokenToAttrsCache(dict):
    __doc__ = '\n    A cache structure that maps Pygments Tokens to :class:`.Attr`.\n    (This is an important speed up.)\n    '

    def __init__(self, get_style_for_token):
        self.get_style_for_token = get_style_for_token

    def __missing__(self, token):
        try:
            result = self.get_style_for_token(token)
        except KeyError:
            result = None

        self[token] = result
        return result


class Renderer(object):
    __doc__ = '\n    Typical usage:\n\n    ::\n\n        output = Vt100_Output.from_pty(sys.stdout)\n        r = Renderer(style, output)\n        r.render(cli, layout=...)\n    '

    def __init__(self, style, output, use_alternate_screen=False, mouse_support=False):
        if not isinstance(style, Style):
            raise AssertionError
        elif not isinstance(output, Output):
            raise AssertionError
        self.style = style
        self.output = output
        self.use_alternate_screen = use_alternate_screen
        self.mouse_support = to_cli_filter(mouse_support)
        self._in_alternate_screen = False
        self._mouse_support_enabled = False
        self._bracketed_paste_enabled = False
        self.waiting_for_cpr = False
        self.reset(_scroll=True)

    def reset(self, _scroll=False, leave_alternate_screen=True):
        self._cursor_pos = Point(x=0, y=0)
        self._last_screen = None
        self._last_size = None
        self._last_token = None
        self._last_style_hash = None
        self._attrs_for_token = None
        self.mouse_handlers = MouseHandlers()
        self._last_title = None
        self._min_available_height = 0
        if is_windows():
            if _scroll:
                self.output.scroll_buffer_to_prompt()
        if self._in_alternate_screen:
            if leave_alternate_screen:
                self.output.quit_alternate_screen()
                self._in_alternate_screen = False
        if self._mouse_support_enabled:
            self.output.disable_mouse_support()
            self._mouse_support_enabled = False
        if self._bracketed_paste_enabled:
            self.output.disable_bracketed_paste()
            self._bracketed_paste_enabled = False
        self.output.flush()

    @property
    def height_is_known(self):
        """
        True when the height from the cursor until the bottom of the terminal
        is known. (It's often nicer to draw bottom toolbars only if the height
        is known, in order to avoid flickering when the CPR response arrives.)
        """
        return self.use_alternate_screen or self._min_available_height > 0 or is_windows()

    @property
    def rows_above_layout(self):
        """
        Return the number of rows visible in the terminal above the layout.
        """
        if self._in_alternate_screen:
            return 0
        if self._min_available_height > 0:
            total_rows = self.output.get_size().rows
            last_screen_height = self._last_screen.height if self._last_screen else 0
            return total_rows - max(self._min_available_height, last_screen_height)
        raise HeightIsUnknownError('Rows above layout is unknown.')

    def request_absolute_cursor_position(self):
        """
        Get current cursor position.
        For vt100: Do CPR request. (answer will arrive later.)
        For win32: Do API call. (Answer comes immediately.)
        """
        if not self._cursor_pos.y == 0:
            raise AssertionError
        else:
            if is_windows():
                self._min_available_height = self.output.get_rows_below_cursor_position()
            else:
                if self.use_alternate_screen:
                    self._min_available_height = self.output.get_size().rows
                else:
                    self.waiting_for_cpr = True
                    self.output.ask_for_cpr()

    def report_absolute_cursor_row(self, row):
        """
        To be called when we know the absolute cursor position.
        (As an answer of a "Cursor Position Request" response.)
        """
        total_rows = self.output.get_size().rows
        rows_below_cursor = total_rows - row + 1
        self._min_available_height = rows_below_cursor
        self.waiting_for_cpr = False

    def render(self, cli, layout, is_done=False):
        """
        Render the current interface to the output.

        :param is_done: When True, put the cursor at the end of the interface. We
                won't print any changes to this part.
        """
        output = self.output
        if self.use_alternate_screen:
            if not self._in_alternate_screen:
                self._in_alternate_screen = True
                output.enter_alternate_screen()
        if not self._bracketed_paste_enabled:
            self.output.enable_bracketed_paste()
            self._bracketed_paste_enabled = True
        else:
            needs_mouse_support = self.mouse_support(cli)
            if needs_mouse_support:
                if not self._mouse_support_enabled:
                    output.enable_mouse_support()
                    self._mouse_support_enabled = True
            if not needs_mouse_support:
                if self._mouse_support_enabled:
                    output.disable_mouse_support()
                    self._mouse_support_enabled = False
            size = output.get_size()
            screen = Screen()
            screen.show_cursor = False
            mouse_handlers = MouseHandlers()
            if is_done:
                height = 0
            else:
                height = self._last_screen.height if self._last_screen else 0
            height = max(self._min_available_height, height)
        if self._last_size != size:
            self._last_screen = None
        if self.style.invalidation_hash() != self._last_style_hash:
            self._last_screen = None
            self._attrs_for_token = None
        if self._attrs_for_token is None:
            self._attrs_for_token = _TokenToAttrsCache(self.style.get_attrs_for_token)
        self._last_style_hash = self.style.invalidation_hash()
        layout.write_to_screen(cli, screen, mouse_handlers, WritePosition(xpos=0,
          ypos=0,
          width=(size.columns),
          height=(size.rows if self.use_alternate_screen else height),
          extended_height=(size.rows)))
        if cli.is_aborting or cli.is_exiting:
            screen.replace_all_tokens(Token.Aborted)
        self._cursor_pos, self._last_token = _output_screen_diff(output,
          screen, (self._cursor_pos), (self._last_screen),
          (self._last_token), is_done, attrs_for_token=(self._attrs_for_token),
          size=size,
          previous_width=(self._last_size.columns if self._last_size else 0))
        self._last_screen = screen
        self._last_size = size
        self.mouse_handlers = mouse_handlers
        new_title = cli.terminal_title
        if new_title != self._last_title:
            if new_title is None:
                self.output.clear_title()
            else:
                self.output.set_title(new_title)
            self._last_title = new_title
        output.flush()

    def erase(self, leave_alternate_screen=True, erase_title=True):
        """
        Hide all output and put the cursor back at the first line. This is for
        instance used for running a system command (while hiding the CLI) and
        later resuming the same CLI.)

        :param leave_alternate_screen: When True, and when inside an alternate
            screen buffer, quit the alternate screen.
        :param erase_title: When True, clear the title from the title bar.
        """
        output = self.output
        output.cursor_backward(self._cursor_pos.x)
        output.cursor_up(self._cursor_pos.y)
        output.erase_down()
        output.reset_attributes()
        output.flush()
        if self._last_title:
            if erase_title:
                output.clear_title()
        self.reset(leave_alternate_screen=leave_alternate_screen)

    def clear(self):
        """
        Clear screen and go to 0,0
        """
        self.erase()
        output = self.output
        output.erase_screen()
        output.cursor_goto(0, 0)
        output.flush()
        self.request_absolute_cursor_position()


def print_tokens(output, tokens, style):
    """
    Print a list of (Token, text) tuples in the given style to the output.
    """
    if not isinstance(output, Output):
        raise AssertionError
    elif not isinstance(style, Style):
        raise AssertionError
    output.reset_attributes()
    output.enable_autowrap()
    attrs_for_token = _TokenToAttrsCache(style.get_attrs_for_token)
    for token, text in tokens:
        attrs = attrs_for_token[token]
        if attrs:
            output.set_attributes(attrs)
        else:
            output.reset_attributes()
        output.write(text)

    output.reset_attributes()
    output.flush()