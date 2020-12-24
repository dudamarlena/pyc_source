# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/layout/controls.py
# Compiled at: 2019-08-15 23:53:39
# Size of source mod 2**32: 28548 bytes
__doc__ = '\nUser interface Controls for the layout.\n'
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from six import with_metaclass
from six.moves import range
from prompt_tool_kit.cache import SimpleCache
from prompt_tool_kit.enums import DEFAULT_BUFFER, SEARCH_BUFFER
from prompt_tool_kit.filters import to_cli_filter
from prompt_tool_kit.mouse_events import MouseEventType
from prompt_tool_kit.search_state import SearchState
from prompt_tool_kit.selection import SelectionType
from prompt_tool_kit.token import Token
from prompt_tool_kit.utils import get_cwidth
from .lexers import Lexer, SimpleLexer
from .processors import Processor
from .screen import Char, Point
from .utils import token_list_width, split_lines, token_list_to_text
import six, time
__all__ = ('BufferControl', 'FillControl', 'TokenListControl', 'UIControl', 'UIContent')

class UIControl(with_metaclass(ABCMeta, object)):
    """UIControl"""

    def reset(self):
        pass

    def preferred_width(self, cli, max_available_width):
        pass

    def preferred_height(self, cli, width, max_available_height, wrap_lines):
        pass

    def has_focus(self, cli):
        """
        Return ``True`` when this user control has the focus.

        If so, the cursor will be displayed according to the cursor position
        reported by :meth:`.UIControl.create_content`. If the created content
        has the property ``show_cursor=False``, the cursor will be hidden from
        the output.
        """
        return False

    @abstractmethod
    def create_content(self, cli, width, height):
        """
        Generate the content for this user control.

        Returns a :class:`.UIContent` instance.
        """
        pass

    def mouse_handler(self, cli, mouse_event):
        """
        Handle mouse events.

        When `NotImplemented` is returned, it means that the given event is not
        handled by the `UIControl` itself. The `Window` or key bindings can
        decide to handle this event as scrolling or changing focus.

        :param cli: `CommandLineInterface` instance.
        :param mouse_event: `MouseEvent` instance.
        """
        return NotImplemented

    def move_cursor_down(self, cli):
        """
        Request to move the cursor down.
        This happens when scrolling down and the cursor is completely at the
        top.
        """
        pass

    def move_cursor_up(self, cli):
        """
        Request to move the cursor up.
        """
        pass


class UIContent(object):
    """UIContent"""

    def __init__(self, get_line=None, line_count=0, cursor_position=None, menu_position=None, show_cursor=True, default_char=None):
        if not callable(get_line):
            raise AssertionError
        elif not isinstance(line_count, six.integer_types):
            raise AssertionError
        else:
            if not cursor_position is None:
                if not isinstance(cursor_position, Point):
                    raise AssertionError
            if not menu_position is None:
                if not isinstance(menu_position, Point):
                    raise AssertionError
            if not default_char is None:
                assert isinstance(default_char, Char)
        self.get_line = get_line
        self.line_count = line_count
        self.cursor_position = cursor_position or Point(0, 0)
        self.menu_position = menu_position
        self.show_cursor = show_cursor
        self.default_char = default_char
        self._line_heights = {}

    def __getitem__(self, lineno):
        """ Make it iterable (iterate line by line). """
        if lineno < self.line_count:
            return self.get_line(lineno)
        raise IndexError

    def get_height_for_line(self, lineno, width):
        """
        Return the height that a given line would need if it is rendered in a
        space with the given width.
        """
        try:
            return self._line_heights[(lineno, width)]
        except KeyError:
            text = token_list_to_text(self.get_line(lineno))
            result = self.get_height_for_text(text, width)
            self._line_heights[(lineno, width)] = result
            return result

    @staticmethod
    def get_height_for_text(text, width):
        line_width = get_cwidth(text)
        try:
            quotient, remainder = divmod(line_width, width)
        except ZeroDivisionError:
            return 10000000000
        else:
            if remainder:
                quotient += 1
            return max(1, quotient)


class TokenListControl(UIControl):
    """TokenListControl"""

    def __init__(self, get_tokens, default_char=None, get_default_char=None, align_right=False, align_center=False, has_focus=False):
        if not callable(get_tokens):
            raise AssertionError
        elif not default_char is None:
            if not isinstance(default_char, Char):
                raise AssertionError
        else:
            if not get_default_char is None:
                if not callable(get_default_char):
                    raise AssertionError
            elif not not (default_char and get_default_char):
                raise AssertionError
            self.align_right = to_cli_filter(align_right)
            self.align_center = to_cli_filter(align_center)
            self._has_focus_filter = to_cli_filter(has_focus)
            self.get_tokens = get_tokens
            if default_char:
                get_default_char = lambda _: default_char
            elif not get_default_char:
                get_default_char = lambda _: Char(' ', Token.Transparent)
        self.get_default_char = get_default_char
        self._content_cache = SimpleCache(maxsize=18)
        self._token_cache = SimpleCache(maxsize=1)
        self._tokens = None

    def reset(self):
        self._tokens = None

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.get_tokens)

    def _get_tokens_cached(self, cli):
        """
        Get tokens, but only retrieve tokens once during one render run.
        (This function is called several times during one rendering, because
        we also need those for calculating the dimensions.)
        """
        return self._token_cache.get(cli.render_counter, lambda : self.get_tokens(cli))

    def has_focus(self, cli):
        return self._has_focus_filter(cli)

    def preferred_width(self, cli, max_available_width):
        """
        Return the preferred width for this control.
        That is the width of the longest line.
        """
        text = token_list_to_text(self._get_tokens_cached(cli))
        line_lengths = [get_cwidth(l) for l in text.split('\n')]
        return max(line_lengths)

    def preferred_height(self, cli, width, max_available_height, wrap_lines):
        content = self.create_content(cli, width, None)
        return content.line_count

    def create_content(self, cli, width, height):
        tokens_with_mouse_handlers = self._get_tokens_cached(cli)
        default_char = self.get_default_char(cli)
        right = self.align_right(cli)
        center = self.align_center(cli)

        def process_line(line):
            used_width = token_list_width(line)
            padding = width - used_width
            if center:
                padding = int(padding / 2)
            return [(default_char.token, default_char.char * padding)] + line

        if right or center:
            token_lines_with_mouse_handlers = []
            for line in split_lines(tokens_with_mouse_handlers):
                token_lines_with_mouse_handlers.append(process_line(line))

        else:
            token_lines_with_mouse_handlers = list(split_lines(tokens_with_mouse_handlers))
        token_lines = [[tuple(item[:2]) for item in line] for line in token_lines_with_mouse_handlers]
        self._tokens = tokens_with_mouse_handlers

        def get_cursor_position():
            SetCursorPosition = Token.SetCursorPosition
            for y, line in enumerate(token_lines):
                x = 0
                for token, text in line:
                    if token == SetCursorPosition:
                        return Point(x=x, y=y)
                    x += len(text)

        key = (
         default_char.char, default_char.token,
         tuple(tokens_with_mouse_handlers), width, right, center)

        def get_content():
            return UIContent(get_line=(lambda i: token_lines[i]), line_count=(len(token_lines)),
              default_char=default_char,
              cursor_position=(get_cursor_position()))

        return self._content_cache.get(key, get_content)

    @classmethod
    def static(cls, tokens):

        def get_static_tokens(cli):
            return tokens

        return cls(get_static_tokens)

    def mouse_handler(self, cli, mouse_event):
        """
        Handle mouse events.

        (When the token list contained mouse handlers and the user clicked on
        on any of these, the matching handler is called. This handler can still
        return `NotImplemented` in case we want the `Window` to handle this
        particular event.)
        """
        if self._tokens:
            tokens_for_line = list(split_lines(self._tokens))
            try:
                tokens = tokens_for_line[mouse_event.position.y]
            except IndexError:
                return NotImplemented
            else:
                xpos = mouse_event.position.x
                count = 0
                for item in tokens:
                    count += len(item[1])
                    if count >= xpos:
                        if len(item) >= 3:
                            handler = item[2]
                            return handler(cli, mouse_event)
                        break

        return NotImplemented


class FillControl(UIControl):
    """FillControl"""

    def __init__(self, character=None, token=Token, char=None, get_char=None):
        if not char is None:
            assert isinstance(char, Char)
            if not get_char is None:
                if not callable(get_char):
                    raise AssertionError
            assert not (char and get_char)
        else:
            self.char = char
            if character:
                self.character = character
                self.token = token
                self.get_char = lambda cli: Char(character, token)
            else:
                if get_char:
                    self.get_char = get_char
                else:
                    self.char = self.char or Char()
                    self.get_char = lambda cli: self.char
                    self.char = char

    def __repr__(self):
        if self.char:
            return '%s(char=%r)' % (self.__class__.__name__, self.char)
        else:
            return '%s(get_char=%r)' % (self.__class__.__name__, self.get_char)

    def reset(self):
        pass

    def has_focus(self, cli):
        return False

    def create_content(self, cli, width, height):

        def get_line(i):
            return []

        return UIContent(get_line=get_line,
          line_count=(100 ** 100),
          default_char=(self.get_char(cli)))


_ProcessedLine = namedtuple('_ProcessedLine', 'tokens source_to_display display_to_source')

class BufferControl(UIControl):
    """BufferControl"""

    def __init__(self, buffer_name=DEFAULT_BUFFER, input_processors=None, lexer=None, preview_search=False, search_buffer_name=SEARCH_BUFFER, get_search_state=None, menu_position=None, default_char=None, focus_on_click=False):
        if not input_processors is None:
            assert all(isinstance(i, Processor) for i in input_processors)
            if not menu_position is None:
                if not callable(menu_position):
                    raise AssertionError
            if not lexer is None:
                assert isinstance(lexer, Lexer)
        elif not get_search_state is None:
            if not callable(get_search_state):
                raise AssertionError
        elif not default_char is None:
            assert isinstance(default_char, Char)
        self.preview_search = to_cli_filter(preview_search)
        self.get_search_state = get_search_state
        self.focus_on_click = to_cli_filter(focus_on_click)
        self.input_processors = input_processors or []
        self.buffer_name = buffer_name
        self.menu_position = menu_position
        self.lexer = lexer or SimpleLexer()
        self.default_char = default_char or Char(token=(Token.Transparent))
        self.search_buffer_name = search_buffer_name
        self._token_cache = SimpleCache(maxsize=8)
        self._xy_to_cursor_position = None
        self._last_click_timestamp = None
        self._last_get_processed_line = None

    def _buffer(self, cli):
        """
        The buffer object that contains the 'main' content.
        """
        return cli.buffers[self.buffer_name]

    def has_focus(self, cli):
        return cli.current_buffer_name == self.buffer_name or any(i.has_focus(cli) for i in self.input_processors)

    def preferred_width(self, cli, max_available_width):
        """
        This should return the preferred width.

        Note: We don't specify a preferred width according to the content,
              because it would be too expensive. Calculating the preferred
              width can be done by calculating the longest line, but this would
              require applying all the processors to each line. This is
              unfeasible for a larger document, and doing it for small
              documents only would result in inconsistent behaviour.
        """
        pass

    def preferred_height(self, cli, width, max_available_height, wrap_lines):
        height = 0
        content = self.create_content(cli, width, None)
        if not wrap_lines:
            return content.line_count
        else:
            if content.line_count >= max_available_height:
                return max_available_height
            for i in range(content.line_count):
                height += content.get_height_for_line(i, width)
                if height >= max_available_height:
                    return max_available_height

            return height

    def _get_tokens_for_line_func(self, cli, document):
        """
        Create a function that returns the tokens for a given line.
        """

        def get_tokens_for_line():
            return self.lexer.lex_document(cli, document)

        return self._token_cache.get(document.text, get_tokens_for_line)

    def _create_get_processed_line_func(self, cli, document):
        """
        Create a function that takes a line number of the current document and
        returns a _ProcessedLine(processed_tokens, source_to_display, display_to_source)
        tuple.
        """

        def transform(lineno, tokens):
            source_to_display_functions = []
            display_to_source_functions = []
            if document.cursor_position_row == lineno:
                cursor_column = document.cursor_position_col
            else:
                cursor_column = None

            def source_to_display(i):
                for f in source_to_display_functions:
                    i = f(i)

                return i

            for p in self.input_processors:
                transformation = p.apply_transformation(cli, document, lineno, source_to_display, tokens)
                tokens = transformation.tokens
                if cursor_column:
                    cursor_column = transformation.source_to_display(cursor_column)
                display_to_source_functions.append(transformation.display_to_source)
                source_to_display_functions.append(transformation.source_to_display)

            def display_to_source(i):
                for f in reversed(display_to_source_functions):
                    i = f(i)

                return i

            return _ProcessedLine(tokens, source_to_display, display_to_source)

        def create_func():
            get_line = self._get_tokens_for_line_func(cli, document)
            cache = {}

            def get_processed_line(i):
                try:
                    return cache[i]
                except KeyError:
                    processed_line = transform(i, get_line(i))
                    cache[i] = processed_line
                    return processed_line

            return get_processed_line

        return create_func()

    def create_content(self, cli, width, height):
        """
        Create a UIContent.
        """
        buffer = self._buffer(cli)

        def preview_now():
            return bool(self.preview_search(cli) and cli.buffers[self.search_buffer_name].text)

        if preview_now():
            if self.get_search_state:
                ss = self.get_search_state(cli)
            else:
                ss = cli.search_state
            document = buffer.document_for_search(SearchState(text=(cli.current_buffer.text),
              direction=(ss.direction),
              ignore_case=(ss.ignore_case)))
        else:
            document = buffer.document
        get_processed_line = self._create_get_processed_line_func(cli, document)
        self._last_get_processed_line = get_processed_line

        def translate_rowcol(row, col):
            return Point(y=row, x=(get_processed_line(row).source_to_display(col)))

        def get_line(i):
            tokens = get_processed_line(i).tokens
            tokens = tokens + [(self.default_char.token, ' ')]
            return tokens

        content = UIContent(get_line=get_line,
          line_count=(document.line_count),
          cursor_position=(translate_rowcol(document.cursor_position_row, document.cursor_position_col)),
          default_char=(self.default_char))
        if cli.current_buffer_name == self.buffer_name:
            menu_position = self.menu_position(cli) if self.menu_position else None
            if menu_position is not None:
                assert isinstance(menu_position, int)
                menu_row, menu_col = buffer.document.translate_index_to_position(menu_position)
                content.menu_position = translate_rowcol(menu_row, menu_col)
            else:
                if buffer.complete_state:
                    menu_row, menu_col = buffer.document.translate_index_to_position(min(buffer.cursor_position, buffer.complete_state.original_document.cursor_position))
                    content.menu_position = translate_rowcol(menu_row, menu_col)
                else:
                    content.menu_position = None
        return content

    def mouse_handler(self, cli, mouse_event):
        """
        Mouse handler for this control.
        """
        buffer = self._buffer(cli)
        position = mouse_event.position
        if self.has_focus(cli):
            if self._last_get_processed_line:
                processed_line = self._last_get_processed_line(position.y)
                xpos = processed_line.display_to_source(position.x)
                index = buffer.document.translate_row_col_to_index(position.y, xpos)
                if mouse_event.event_type == MouseEventType.MOUSE_DOWN:
                    buffer.exit_selection()
                    buffer.cursor_position = index
                elif mouse_event.event_type == MouseEventType.MOUSE_UP:
                    if abs(buffer.cursor_position - index) > 1:
                        buffer.start_selection(selection_type=(SelectionType.CHARACTERS))
                        buffer.cursor_position = index
                else:
                    double_click = self._last_click_timestamp and time.time() - self._last_click_timestamp < 0.3
                    self._last_click_timestamp = time.time()
                    if double_click:
                        start, end = buffer.document.find_boundaries_of_current_word()
                        buffer.cursor_position += start
                        buffer.start_selection(selection_type=(SelectionType.CHARACTERS))
                        buffer.cursor_position += end - start
            else:
                return NotImplemented
        elif self.focus_on_click(cli):
            if mouse_event.event_type == MouseEventType.MOUSE_UP:
                cli.focus(self.buffer_name)
        else:
            return NotImplemented

    def move_cursor_down(self, cli):
        b = self._buffer(cli)
        b.cursor_position += b.document.get_cursor_down_position()

    def move_cursor_up(self, cli):
        b = self._buffer(cli)
        b.cursor_position += b.document.get_cursor_up_position()