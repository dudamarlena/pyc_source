# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/layout/margins.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 8858 bytes
__doc__ = '\nMargin implementations for a :class:`~prompt_tool_kit.layout.containers.Window`.\n'
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from six import with_metaclass
from six.moves import range
from prompt_tool_kit.filters import to_cli_filter
from prompt_tool_kit.token import Token
from prompt_tool_kit.utils import get_cwidth
from .utils import token_list_to_text
__all__ = ('Margin', 'NumberredMargin', 'ScrollbarMargin', 'ConditionalMargin', 'PromptMargin')

class Margin(with_metaclass(ABCMeta, object)):
    """Margin"""

    @abstractmethod
    def get_width(self, cli, get_ui_content):
        """
        Return the width that this margin is going to consume.

        :param cli: :class:`.CommandLineInterface` instance.
        :param get_ui_content: Callable that asks the user control to create
            a :class:`.UIContent` instance. This can be used for instance to
            obtain the number of lines.
        """
        return 0

    @abstractmethod
    def create_margin(self, cli, window_render_info, width, height):
        """
        Creates a margin.
        This should return a list of (Token, text) tuples.

        :param cli: :class:`.CommandLineInterface` instance.
        :param window_render_info:
            :class:`~prompt_tool_kit.layout.containers.WindowRenderInfo`
            instance, generated after rendering and copying the visible part of
            the :class:`~prompt_tool_kit.layout.controls.UIControl` into the
            :class:`~prompt_tool_kit.layout.containers.Window`.
        :param width: The width that's available for this margin. (As reported
            by :meth:`.get_width`.)
        :param height: The height that's available for this margin. (The height
            of the :class:`~prompt_tool_kit.layout.containers.Window`.)
        """
        return []


class NumberredMargin(Margin):
    """NumberredMargin"""

    def __init__(self, relative=False, display_tildes=False):
        self.relative = to_cli_filter(relative)
        self.display_tildes = to_cli_filter(display_tildes)

    def get_width(self, cli, get_ui_content):
        line_count = get_ui_content().line_count
        return max(3, len('%s' % line_count) + 1)

    def create_margin(self, cli, window_render_info, width, height):
        relative = self.relative(cli)
        token = Token.LineNumber
        token_current = Token.LineNumber.Current
        current_lineno = window_render_info.ui_content.cursor_position.y
        result = []
        last_lineno = None
        for y, lineno in enumerate(window_render_info.displayed_lines):
            if lineno != last_lineno:
                if lineno is None:
                    pass
                else:
                    if lineno == current_lineno:
                        if relative:
                            result.append((token_current, '%i' % (lineno + 1)))
                        else:
                            result.append((token_current, ('%i ' % (lineno + 1)).rjust(width)))
                    else:
                        if relative:
                            lineno = abs(lineno - current_lineno) - 1
                        result.append((token, ('%i ' % (lineno + 1)).rjust(width)))
            last_lineno = lineno
            result.append((Token, '\n'))

        if self.display_tildes(cli):
            while y < window_render_info.window_height:
                result.append((Token.Tilde, '~\n'))
                y += 1

        return result


class ConditionalMargin(Margin):
    """ConditionalMargin"""

    def __init__(self, margin, filter):
        assert isinstance(margin, Margin)
        self.margin = margin
        self.filter = to_cli_filter(filter)

    def get_width(self, cli, ui_content):
        if self.filter(cli):
            return self.margin.get_width(cli, ui_content)
        else:
            return 0

    def create_margin(self, cli, window_render_info, width, height):
        if width:
            if self.filter(cli):
                return self.margin.create_margin(cli, window_render_info, width, height)
        return []


class ScrollbarMargin(Margin):
    """ScrollbarMargin"""

    def __init__(self, display_arrows=False):
        self.display_arrows = to_cli_filter(display_arrows)

    def get_width(self, cli, ui_content):
        return 1

    def create_margin(self, cli, window_render_info, width, height):
        total_height = window_render_info.content_height
        display_arrows = self.display_arrows(cli)
        window_height = window_render_info.window_height
        if display_arrows:
            window_height -= 2
        try:
            items_per_row = float(total_height) / min(total_height, window_height)
        except ZeroDivisionError:
            return []
        else:

            def is_scroll_button(row):
                current_row_middle = int((row + 0.5) * items_per_row)
                return current_row_middle in window_render_info.displayed_lines

            result = []
            if display_arrows:
                result.extend([
                 (
                  Token.Scrollbar.Arrow, '^'),
                 (
                  Token.Scrollbar, '\n')])
            for i in range(window_height):
                if is_scroll_button(i):
                    result.append((Token.Scrollbar.Button, ' '))
                else:
                    result.append((Token.Scrollbar, ' '))
                result.append((Token, '\n'))

            if display_arrows:
                result.append((Token.Scrollbar.Arrow, 'v'))
            return result


class PromptMargin(Margin):
    """PromptMargin"""

    def __init__(self, get_prompt_tokens, get_continuation_tokens=None, show_numbers=False):
        assert callable(get_prompt_tokens)
        if not get_continuation_tokens is None:
            if not callable(get_continuation_tokens):
                raise AssertionError
        show_numbers = to_cli_filter(show_numbers)
        self.get_prompt_tokens = get_prompt_tokens
        self.get_continuation_tokens = get_continuation_tokens
        self.show_numbers = show_numbers

    def get_width(self, cli, ui_content):
        """ Width to report to the `Window`. """
        text = token_list_to_text(self.get_prompt_tokens(cli))
        return get_cwidth(text)

    def create_margin(self, cli, window_render_info, width, height):
        tokens = self.get_prompt_tokens(cli)[:]
        if self.get_continuation_tokens:
            tokens2 = list(self.get_continuation_tokens(cli, width))
        else:
            tokens2 = []
        show_numbers = self.show_numbers(cli)
        last_y = None
        for y in window_render_info.displayed_lines[1:]:
            tokens.append((Token, '\n'))
            if show_numbers:
                if y != last_y:
                    tokens.append((Token.LineNumber, ('%i ' % (y + 1)).rjust(width)))
            else:
                tokens.extend(tokens2)
            last_y = y

        return tokens