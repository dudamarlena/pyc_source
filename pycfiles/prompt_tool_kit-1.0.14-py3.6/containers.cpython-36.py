# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/layout/containers.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 67812 bytes
"""
Container for the layout.
(Containers can contain other containers or user interface controls.)
"""
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from six import with_metaclass
from six.moves import range
from .controls import UIControl, TokenListControl, UIContent
from .dimension import LayoutDimension, sum_layout_dimensions, max_layout_dimensions
from .margins import Margin
from .screen import Point, WritePosition, _CHAR_CACHE
from .utils import token_list_to_text, explode_tokens
from prompt_tool_kit.cache import SimpleCache
from prompt_tool_kit.filters import to_cli_filter, ViInsertMode, EmacsInsertMode
from prompt_tool_kit.mouse_events import MouseEvent, MouseEventType
from prompt_tool_kit.reactive import Integer
from prompt_tool_kit.token import Token
from prompt_tool_kit.utils import take_using_weights, get_cwidth
__all__ = ('Container', 'HSplit', 'VSplit', 'FloatContainer', 'Float', 'Window', 'WindowRenderInfo',
           'ConditionalContainer', 'ScrollOffsets', 'ColorColumn')
Transparent = Token.Transparent

class Container(with_metaclass(ABCMeta, object)):
    __doc__ = '\n    Base class for user interface layout.\n    '

    @abstractmethod
    def reset(self):
        """
        Reset the state of this container and all the children.
        (E.g. reset scroll offsets, etc...)
        """
        pass

    @abstractmethod
    def preferred_width(self, cli, max_available_width):
        """
        Return a :class:`~prompt_tool_kit.layout.dimension.LayoutDimension` that
        represents the desired width for this container.

        :param cli: :class:`~prompt_tool_kit.interface.CommandLineInterface`.
        """
        pass

    @abstractmethod
    def preferred_height(self, cli, width, max_available_height):
        """
        Return a :class:`~prompt_tool_kit.layout.dimension.LayoutDimension` that
        represents the desired height for this container.

        :param cli: :class:`~prompt_tool_kit.interface.CommandLineInterface`.
        """
        pass

    @abstractmethod
    def write_to_screen(self, cli, screen, mouse_handlers, write_position):
        """
        Write the actual content to the screen.

        :param cli: :class:`~prompt_tool_kit.interface.CommandLineInterface`.
        :param screen: :class:`~prompt_tool_kit.layout.screen.Screen`
        :param mouse_handlers: :class:`~prompt_tool_kit.layout.mouse_handlers.MouseHandlers`.
        """
        pass

    @abstractmethod
    def walk(self, cli):
        """
        Walk through all the layout nodes (and their children) and yield them.
        """
        pass


def _window_too_small():
    """ Create a `Window` that displays the 'Window too small' text. """
    return Window(TokenListControl.static([
     (
      Token.WindowTooSmall, ' Window too small... ')]))


class HSplit(Container):
    __doc__ = '\n    Several layouts, one stacked above/under the other.\n\n    :param children: List of child :class:`.Container` objects.\n    :param window_too_small: A :class:`.Container` object that is displayed if\n        there is not enough space for all the children. By default, this is a\n        "Window too small" message.\n    :param get_dimensions: (`None` or a callable that takes a\n        `CommandLineInterface` and returns a list of `LayoutDimension`\n        instances.) By default the dimensions are taken from the children and\n        divided by the available space. However, when `get_dimensions` is specified,\n        this is taken instead.\n    :param report_dimensions_callback: When rendering, this function is called\n        with the `CommandLineInterface` and the list of used dimensions. (As a\n        list of integers.)\n    '

    def __init__(self, children, window_too_small=None, get_dimensions=None, report_dimensions_callback=None):
        if not all(isinstance(c, Container) for c in children):
            raise AssertionError
        elif not window_too_small is None:
            if not isinstance(window_too_small, Container):
                raise AssertionError
        else:
            if not get_dimensions is None:
                if not callable(get_dimensions):
                    raise AssertionError
            if not report_dimensions_callback is None:
                assert callable(report_dimensions_callback)
        self.children = children
        self.window_too_small = window_too_small or _window_too_small()
        self.get_dimensions = get_dimensions
        self.report_dimensions_callback = report_dimensions_callback

    def preferred_width(self, cli, max_available_width):
        if self.children:
            dimensions = [c.preferred_width(cli, max_available_width) for c in self.children]
            return max_layout_dimensions(dimensions)
        else:
            return LayoutDimension(0)

    def preferred_height(self, cli, width, max_available_height):
        dimensions = [c.preferred_height(cli, width, max_available_height) for c in self.children]
        return sum_layout_dimensions(dimensions)

    def reset(self):
        for c in self.children:
            c.reset()

    def write_to_screen(self, cli, screen, mouse_handlers, write_position):
        """
        Render the prompt to a `Screen` instance.

        :param screen: The :class:`~prompt_tool_kit.layout.screen.Screen` class
            to which the output has to be written.
        """
        sizes = self._divide_heigths(cli, write_position)
        if self.report_dimensions_callback:
            self.report_dimensions_callback(cli, sizes)
        else:
            if sizes is None:
                self.window_too_small.write_to_screen(cli, screen, mouse_handlers, write_position)
            else:
                ypos = write_position.ypos
                xpos = write_position.xpos
                width = write_position.width
                for s, c in zip(sizes, self.children):
                    c.write_to_screen(cli, screen, mouse_handlers, WritePosition(xpos, ypos, width, s))
                    ypos += s

    def _divide_heigths(self, cli, write_position):
        """
        Return the heights for all rows.
        Or None when there is not enough space.
        """
        if not self.children:
            return []
        else:
            given_dimensions = self.get_dimensions(cli) if self.get_dimensions else None

            def get_dimension_for_child(c, index):
                if given_dimensions:
                    if given_dimensions[index] is not None:
                        return given_dimensions[index]
                return c.preferred_height(cli, write_position.width, write_position.extended_height)

            dimensions = [get_dimension_for_child(c, index) for index, c in enumerate(self.children)]
            sum_dimensions = sum_layout_dimensions(dimensions)
            if sum_dimensions.min > write_position.extended_height:
                return
            sizes = [d.min for d in dimensions]
            child_generator = take_using_weights(items=(list(range(len(dimensions)))),
              weights=[d.weight for d in dimensions])
            i = next(child_generator)
            while sum(sizes) < min(write_position.extended_height, sum_dimensions.preferred):
                if sizes[i] < dimensions[i].preferred:
                    sizes[i] += 1
                i = next(child_generator)

            if not any([cli.is_returning, cli.is_exiting, cli.is_aborting]):
                while sum(sizes) < min(write_position.height, sum_dimensions.max):
                    if sizes[i] < dimensions[i].max:
                        sizes[i] += 1
                    i = next(child_generator)

            return sizes

    def walk(self, cli):
        """ Walk through children. """
        yield self
        for c in self.children:
            for i in c.walk(cli):
                yield i


class VSplit(Container):
    __doc__ = '\n    Several layouts, one stacked left/right of the other.\n\n    :param children: List of child :class:`.Container` objects.\n    :param window_too_small: A :class:`.Container` object that is displayed if\n        there is not enough space for all the children. By default, this is a\n        "Window too small" message.\n    :param get_dimensions: (`None` or a callable that takes a\n        `CommandLineInterface` and returns a list of `LayoutDimension`\n        instances.) By default the dimensions are taken from the children and\n        divided by the available space. However, when `get_dimensions` is specified,\n        this is taken instead.\n    :param report_dimensions_callback: When rendering, this function is called\n        with the `CommandLineInterface` and the list of used dimensions. (As a\n        list of integers.)\n    '

    def __init__(self, children, window_too_small=None, get_dimensions=None, report_dimensions_callback=None):
        if not all(isinstance(c, Container) for c in children):
            raise AssertionError
        elif not window_too_small is None:
            if not isinstance(window_too_small, Container):
                raise AssertionError
        else:
            if not get_dimensions is None:
                if not callable(get_dimensions):
                    raise AssertionError
            if not report_dimensions_callback is None:
                assert callable(report_dimensions_callback)
        self.children = children
        self.window_too_small = window_too_small or _window_too_small()
        self.get_dimensions = get_dimensions
        self.report_dimensions_callback = report_dimensions_callback

    def preferred_width(self, cli, max_available_width):
        dimensions = [c.preferred_width(cli, max_available_width) for c in self.children]
        return sum_layout_dimensions(dimensions)

    def preferred_height(self, cli, width, max_available_height):
        sizes = self._divide_widths(cli, width)
        if sizes is None:
            return LayoutDimension()
        else:
            dimensions = [c.preferred_height(cli, s, max_available_height) for s, c in zip(sizes, self.children)]
            return max_layout_dimensions(dimensions)

    def reset(self):
        for c in self.children:
            c.reset()

    def _divide_widths(self, cli, width):
        """
        Return the widths for all columns.
        Or None when there is not enough space.
        """
        if not self.children:
            return []
        else:
            given_dimensions = self.get_dimensions(cli) if self.get_dimensions else None

            def get_dimension_for_child(c, index):
                if given_dimensions:
                    if given_dimensions[index] is not None:
                        return given_dimensions[index]
                return c.preferred_width(cli, width)

            dimensions = [get_dimension_for_child(c, index) for index, c in enumerate(self.children)]
            sum_dimensions = sum_layout_dimensions(dimensions)
            if sum_dimensions.min > width:
                return
            sizes = [d.min for d in dimensions]
            child_generator = take_using_weights(items=(list(range(len(dimensions)))),
              weights=[d.weight for d in dimensions])
            i = next(child_generator)
            while sum(sizes) < min(width, sum_dimensions.preferred):
                if sizes[i] < dimensions[i].preferred:
                    sizes[i] += 1
                i = next(child_generator)

            while sum(sizes) < min(width, sum_dimensions.max):
                if sizes[i] < dimensions[i].max:
                    sizes[i] += 1
                i = next(child_generator)

            return sizes

    def write_to_screen(self, cli, screen, mouse_handlers, write_position):
        """
        Render the prompt to a `Screen` instance.

        :param screen: The :class:`~prompt_tool_kit.layout.screen.Screen` class
            to which the output has to be written.
        """
        if not self.children:
            return
        else:
            sizes = self._divide_widths(cli, write_position.width)
            if self.report_dimensions_callback:
                self.report_dimensions_callback(cli, sizes)
            if sizes is None:
                self.window_too_small.write_to_screen(cli, screen, mouse_handlers, write_position)
                return
        heights = [child.preferred_height(cli, width, write_position.extended_height).preferred for width, child in zip(sizes, self.children)]
        height = max(write_position.height, min(write_position.extended_height, max(heights)))
        ypos = write_position.ypos
        xpos = write_position.xpos
        for s, c in zip(sizes, self.children):
            c.write_to_screen(cli, screen, mouse_handlers, WritePosition(xpos, ypos, s, height))
            xpos += s

    def walk(self, cli):
        """ Walk through children. """
        yield self
        for c in self.children:
            for i in c.walk(cli):
                yield i


class FloatContainer(Container):
    __doc__ = '\n    Container which can contain another container for the background, as well\n    as a list of floating containers on top of it.\n\n    Example Usage::\n\n        FloatContainer(content=Window(...),\n                       floats=[\n                           Float(xcursor=True,\n                                ycursor=True,\n                                layout=CompletionMenu(...))\n                       ])\n    '

    def __init__(self, content, floats):
        if not isinstance(content, Container):
            raise AssertionError
        elif not all(isinstance(f, Float) for f in floats):
            raise AssertionError
        self.content = content
        self.floats = floats

    def reset(self):
        self.content.reset()
        for f in self.floats:
            f.content.reset()

    def preferred_width(self, cli, write_position):
        return self.content.preferred_width(cli, write_position)

    def preferred_height(self, cli, width, max_available_height):
        """
        Return the preferred height of the float container.
        (We don't care about the height of the floats, they should always fit
        into the dimensions provided by the container.)
        """
        return self.content.preferred_height(cli, width, max_available_height)

    def write_to_screen(self, cli, screen, mouse_handlers, write_position):
        self.content.write_to_screen(cli, screen, mouse_handlers, write_position)
        for fl in self.floats:
            cursor_position = screen.menu_position or screen.cursor_position
            cursor_position = Point(x=(cursor_position.x - write_position.xpos), y=(cursor_position.y - write_position.ypos))
            fl_width = fl.get_width(cli)
            fl_height = fl.get_height(cli)
            if fl.left is not None:
                if fl_width is not None:
                    xpos = fl.left
                    width = fl_width
            if fl.left is not None:
                if fl.right is not None:
                    xpos = fl.left
                    width = write_position.width - fl.left - fl.right
            if fl_width is not None:
                if fl.right is not None:
                    xpos = write_position.width - fl.right - fl_width
                    width = fl_width
            if fl.xcursor:
                width = fl_width
                if width is None:
                    width = fl.content.preferred_width(cli, write_position.width).preferred
                    width = min(write_position.width, width)
                xpos = cursor_position.x
                if xpos + width > write_position.width:
                    xpos = max(0, write_position.width - width)
            else:
                if fl_width:
                    xpos = int((write_position.width - fl_width) / 2)
                    width = fl_width
                else:
                    width = fl.content.preferred_width(cli, write_position.width).preferred
                    if fl.left is not None:
                        xpos = fl.left
                    else:
                        if fl.right is not None:
                            xpos = max(0, write_position.width - width - fl.right)
                        else:
                            xpos = max(0, int((write_position.width - width) / 2))
                        width = min(width, write_position.width - xpos)
            if fl.top is not None:
                if fl_height is not None:
                    ypos = fl.top
                    height = fl_height
            if fl.top is not None:
                if fl.bottom is not None:
                    ypos = fl.top
                    height = write_position.height - fl.top - fl.bottom
                elif fl_height is not None and fl.bottom is not None:
                    ypos = write_position.height - fl_height - fl.bottom
                    height = fl_height
                else:
                    if fl.ycursor:
                        ypos = cursor_position.y + 1
                        height = fl_height
                        if height is None:
                            height = fl.content.preferred_height(cli, width, write_position.extended_height).preferred
                        if height > write_position.extended_height - ypos:
                            if write_position.extended_height - ypos + 1 >= ypos:
                                height = write_position.extended_height - ypos
                            else:
                                height = min(height, cursor_position.y)
                                ypos = cursor_position.y - height
                    else:
                        if fl_width:
                            ypos = int((write_position.height - fl_height) / 2)
                            height = fl_height
                        else:
                            height = fl.content.preferred_height(cli, width, write_position.extended_height).preferred
                    if fl.top is not None:
                        ypos = fl.top
                    else:
                        if fl.bottom is not None:
                            ypos = max(0, write_position.height - height - fl.bottom)
                        else:
                            ypos = max(0, int((write_position.height - height) / 2))
                        height = min(height, write_position.height - ypos)
                if height > 0 and width > 0:
                    wp = WritePosition(xpos=(xpos + write_position.xpos), ypos=(ypos + write_position.ypos),
                      width=width,
                      height=height)
                    if not fl.hide_when_covering_content or self._area_is_empty(screen, wp):
                        fl.content.write_to_screen(cli, screen, mouse_handlers, wp)

    def _area_is_empty(self, screen, write_position):
        """
        Return True when the area below the write position is still empty.
        (For floats that should not hide content underneath.)
        """
        wp = write_position
        Transparent = Token.Transparent
        for y in range(wp.ypos, wp.ypos + wp.height):
            if y in screen.data_buffer:
                row = screen.data_buffer[y]
                for x in range(wp.xpos, wp.xpos + wp.width):
                    c = row[x]
                    if c.char != ' ' or c.token != Transparent:
                        return False

        return True

    def walk(self, cli):
        """ Walk through children. """
        yield self
        for i in self.content.walk(cli):
            yield i

        for f in self.floats:
            for i in f.content.walk(cli):
                yield i


class Float(object):
    __doc__ = '\n    Float for use in a :class:`.FloatContainer`.\n\n    :param content: :class:`.Container` instance.\n    :param hide_when_covering_content: Hide the float when it covers content underneath.\n    '

    def __init__(self, top=None, right=None, bottom=None, left=None, width=None, height=None, get_width=None, get_height=None, xcursor=False, ycursor=False, content=None, hide_when_covering_content=False):
        if not isinstance(content, Container):
            raise AssertionError
        elif not width is None:
            if not get_width is None:
                raise AssertionError
        elif not height is None:
            assert get_height is None
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self._width = width
        self._height = height
        self._get_width = get_width
        self._get_height = get_height
        self.xcursor = xcursor
        self.ycursor = ycursor
        self.content = content
        self.hide_when_covering_content = hide_when_covering_content

    def get_width(self, cli):
        if self._width:
            return self._width
        if self._get_width:
            return self._get_width(cli)

    def get_height(self, cli):
        if self._height:
            return self._height
        if self._get_height:
            return self._get_height(cli)

    def __repr__(self):
        return 'Float(content=%r)' % self.content


class WindowRenderInfo(object):
    __doc__ = "\n    Render information, for the last render time of this control.\n    It stores mapping information between the input buffers (in case of a\n    :class:`~prompt_tool_kit.layout.controls.BufferControl`) and the actual\n    render position on the output screen.\n\n    (Could be used for implementation of the Vi 'H' and 'L' key bindings as\n    well as implementing mouse support.)\n\n    :param ui_content: The original :class:`.UIContent` instance that contains\n        the whole input, without clipping. (ui_content)\n    :param horizontal_scroll: The horizontal scroll of the :class:`.Window` instance.\n    :param vertical_scroll: The vertical scroll of the :class:`.Window` instance.\n    :param window_width: The width of the window that displays the content,\n        without the margins.\n    :param window_height: The height of the window that displays the content.\n    :param configured_scroll_offsets: The scroll offsets as configured for the\n        :class:`Window` instance.\n    :param visible_line_to_row_col: Mapping that maps the row numbers on the\n        displayed screen (starting from zero for the first visible line) to\n        (row, col) tuples pointing to the row and column of the :class:`.UIContent`.\n    :param rowcol_to_yx: Mapping that maps (row, column) tuples representing\n        coordinates of the :class:`UIContent` to (y, x) absolute coordinates at\n        the rendered screen.\n    "

    def __init__(self, ui_content, horizontal_scroll, vertical_scroll, window_width, window_height, configured_scroll_offsets, visible_line_to_row_col, rowcol_to_yx, x_offset, y_offset, wrap_lines):
        if not isinstance(ui_content, UIContent):
            raise AssertionError
        else:
            if not isinstance(horizontal_scroll, int):
                raise AssertionError
            else:
                if not isinstance(vertical_scroll, int):
                    raise AssertionError
                else:
                    if not isinstance(window_width, int):
                        raise AssertionError
                    else:
                        if not isinstance(window_height, int):
                            raise AssertionError
                        else:
                            assert isinstance(configured_scroll_offsets, ScrollOffsets)
                            assert isinstance(visible_line_to_row_col, dict)
                        assert isinstance(rowcol_to_yx, dict)
                    assert isinstance(x_offset, int)
                assert isinstance(y_offset, int)
            assert isinstance(wrap_lines, bool)
        self.ui_content = ui_content
        self.vertical_scroll = vertical_scroll
        self.window_width = window_width
        self.window_height = window_height
        self.configured_scroll_offsets = configured_scroll_offsets
        self.visible_line_to_row_col = visible_line_to_row_col
        self.wrap_lines = wrap_lines
        self._rowcol_to_yx = rowcol_to_yx
        self._x_offset = x_offset
        self._y_offset = y_offset

    @property
    def visible_line_to_input_line(self):
        return dict((visible_line, rowcol[0]) for visible_line, rowcol in self.visible_line_to_row_col.items())

    @property
    def cursor_position(self):
        """
        Return the cursor position coordinates, relative to the left/top corner
        of the rendered screen.
        """
        cpos = self.ui_content.cursor_position
        y, x = self._rowcol_to_yx[(cpos.y, cpos.x)]
        return Point(x=(x - self._x_offset), y=(y - self._y_offset))

    @property
    def applied_scroll_offsets(self):
        """
        Return a :class:`.ScrollOffsets` instance that indicates the actual
        offset. This can be less than or equal to what's configured. E.g, when
        the cursor is completely at the top, the top offset will be zero rather
        than what's configured.
        """
        if self.displayed_lines[0] == 0:
            top = 0
        else:
            y = self.input_line_to_visible_line[self.ui_content.cursor_position.y]
            top = min(y, self.configured_scroll_offsets.top)
        return ScrollOffsets(top=top,
          bottom=(min(self.ui_content.line_count - self.displayed_lines[(-1)] - 1, self.configured_scroll_offsets.bottom)),
          left=0,
          right=0)

    @property
    def displayed_lines(self):
        """
        List of all the visible rows. (Line numbers of the input buffer.)
        The last line may not be entirely visible.
        """
        return sorted(row for row, col in self.visible_line_to_row_col.values())

    @property
    def input_line_to_visible_line(self):
        """
        Return the dictionary mapping the line numbers of the input buffer to
        the lines of the screen. When a line spans several rows at the screen,
        the first row appears in the dictionary.
        """
        result = {}
        for k, v in self.visible_line_to_input_line.items():
            if v in result:
                result[v] = min(result[v], k)
            else:
                result[v] = k

        return result

    def first_visible_line(self, after_scroll_offset=False):
        """
        Return the line number (0 based) of the input document that corresponds
        with the first visible line.
        """
        if after_scroll_offset:
            return self.displayed_lines[self.applied_scroll_offsets.top]
        else:
            return self.displayed_lines[0]

    def last_visible_line(self, before_scroll_offset=False):
        """
        Like `first_visible_line`, but for the last visible line.
        """
        if before_scroll_offset:
            return self.displayed_lines[(-1 - self.applied_scroll_offsets.bottom)]
        else:
            return self.displayed_lines[(-1)]

    def center_visible_line(self, before_scroll_offset=False, after_scroll_offset=False):
        """
        Like `first_visible_line`, but for the center visible line.
        """
        return self.first_visible_line(after_scroll_offset) + (self.last_visible_line(before_scroll_offset) - self.first_visible_line(after_scroll_offset)) // 2

    @property
    def content_height(self):
        """
        The full height of the user control.
        """
        return self.ui_content.line_count

    @property
    def full_height_visible(self):
        """
        True when the full height is visible (There is no vertical scroll.)
        """
        return self.vertical_scroll == 0 and self.last_visible_line() == self.content_height

    @property
    def top_visible(self):
        """
        True when the top of the buffer is visible.
        """
        return self.vertical_scroll == 0

    @property
    def bottom_visible(self):
        """
        True when the bottom of the buffer is visible.
        """
        return self.last_visible_line() == self.content_height - 1

    @property
    def vertical_scroll_percentage(self):
        """
        Vertical scroll as a percentage. (0 means: the top is visible,
        100 means: the bottom is visible.)
        """
        if self.bottom_visible:
            return 100
        else:
            return 100 * self.vertical_scroll // self.content_height

    def get_height_for_line(self, lineno):
        """
        Return the height of the given line.
        (The height that it would take, if this line became visible.)
        """
        if self.wrap_lines:
            return self.ui_content.get_height_for_line(lineno, self.window_width)
        else:
            return 1


class ScrollOffsets(object):
    __doc__ = '\n    Scroll offsets for the :class:`.Window` class.\n\n    Note that left/right offsets only make sense if line wrapping is disabled.\n    '

    def __init__(self, top=0, bottom=0, left=0, right=0):
        if not isinstance(top, Integer):
            raise AssertionError
        else:
            if not isinstance(bottom, Integer):
                raise AssertionError
            elif not isinstance(left, Integer):
                raise AssertionError
            assert isinstance(right, Integer)
        self._top = top
        self._bottom = bottom
        self._left = left
        self._right = right

    @property
    def top(self):
        return int(self._top)

    @property
    def bottom(self):
        return int(self._bottom)

    @property
    def left(self):
        return int(self._left)

    @property
    def right(self):
        return int(self._right)

    def __repr__(self):
        return 'ScrollOffsets(top=%r, bottom=%r, left=%r, right=%r)' % (
         self.top, self.bottom, self.left, self.right)


class ColorColumn(object):

    def __init__(self, position, token=Token.ColorColumn):
        self.position = position
        self.token = token


_in_insert_mode = ViInsertMode() | EmacsInsertMode()

class Window(Container):
    __doc__ = "\n    Container that holds a control.\n\n    :param content: :class:`~prompt_tool_kit.layout.controls.UIControl` instance.\n    :param width: :class:`~prompt_tool_kit.layout.dimension.LayoutDimension` instance.\n    :param height: :class:`~prompt_tool_kit.layout.dimension.LayoutDimension` instance.\n    :param get_width: callable which takes a `CommandLineInterface` and returns a `LayoutDimension`.\n    :param get_height: callable which takes a `CommandLineInterface` and returns a `LayoutDimension`.\n    :param dont_extend_width: When `True`, don't take up more width then the\n                              preferred width reported by the control.\n    :param dont_extend_height: When `True`, don't take up more width then the\n                               preferred height reported by the control.\n    :param left_margins: A list of :class:`~prompt_tool_kit.layout.margins.Margin`\n        instance to be displayed on the left. For instance:\n        :class:`~prompt_tool_kit.layout.margins.NumberredMargin` can be one of\n        them in order to show line numbers.\n    :param right_margins: Like `left_margins`, but on the other side.\n    :param scroll_offsets: :class:`.ScrollOffsets` instance, representing the\n        preferred amount of lines/columns to be always visible before/after the\n        cursor. When both top and bottom are a very high number, the cursor\n        will be centered vertically most of the time.\n    :param allow_scroll_beyond_bottom: A `bool` or\n        :class:`~prompt_tool_kit.filters.CLIFilter` instance. When True, allow\n        scrolling so far, that the top part of the content is not visible\n        anymore, while there is still empty space available at the bottom of\n        the window. In the Vi editor for instance, this is possible. You will\n        see tildes while the top part of the body is hidden.\n    :param wrap_lines: A `bool` or :class:`~prompt_tool_kit.filters.CLIFilter`\n        instance. When True, don't scroll horizontally, but wrap lines instead.\n    :param get_vertical_scroll: Callable that takes this window\n        instance as input and returns a preferred vertical scroll.\n        (When this is `None`, the scroll is only determined by the last and\n        current cursor position.)\n    :param get_horizontal_scroll: Callable that takes this window\n        instance as input and returns a preferred vertical scroll.\n    :param always_hide_cursor: A `bool` or\n        :class:`~prompt_tool_kit.filters.CLIFilter` instance. When True, never\n        display the cursor, even when the user control specifies a cursor\n        position.\n    :param cursorline: A `bool` or :class:`~prompt_tool_kit.filters.CLIFilter`\n        instance. When True, display a cursorline.\n    :param cursorcolumn: A `bool` or :class:`~prompt_tool_kit.filters.CLIFilter`\n        instance. When True, display a cursorcolumn.\n    :param get_colorcolumns: A callable that takes a `CommandLineInterface` and\n        returns a a list of :class:`.ColorColumn` instances that describe the\n        columns to be highlighted.\n    :param cursorline_token: The token to be used for highlighting the current line,\n        if `cursorline` is True.\n    :param cursorcolumn_token: The token to be used for highlighting the current line,\n        if `cursorcolumn` is True.\n    "

    def __init__(self, content, width=None, height=None, get_width=None, get_height=None, dont_extend_width=False, dont_extend_height=False, left_margins=None, right_margins=None, scroll_offsets=None, allow_scroll_beyond_bottom=False, wrap_lines=False, get_vertical_scroll=None, get_horizontal_scroll=None, always_hide_cursor=False, cursorline=False, cursorcolumn=False, get_colorcolumns=None, cursorline_token=Token.CursorLine, cursorcolumn_token=Token.CursorColumn):
        if not isinstance(content, UIControl):
            raise AssertionError
        elif not width is None:
            if not isinstance(width, LayoutDimension):
                raise AssertionError
            elif not height is None:
                if not isinstance(height, LayoutDimension):
                    raise AssertionError
                elif not get_width is None:
                    if not callable(get_width):
                        raise AssertionError
                else:
                    if not get_height is None:
                        if not callable(get_height):
                            raise AssertionError
                    if not width is None:
                        assert get_width is None
                if not height is None:
                    assert get_height is None
            else:
                if not scroll_offsets is None:
                    if not isinstance(scroll_offsets, ScrollOffsets):
                        raise AssertionError
                if not left_margins is None:
                    assert all(isinstance(m, Margin) for m in left_margins)
            if not right_margins is None:
                assert all(isinstance(m, Margin) for m in right_margins)
        else:
            if not get_vertical_scroll is None:
                if not callable(get_vertical_scroll):
                    raise AssertionError
            elif not (get_horizontal_scroll is None or callable(get_horizontal_scroll)):
                raise AssertionError
            if not get_colorcolumns is None:
                assert callable(get_colorcolumns)
        self.allow_scroll_beyond_bottom = to_cli_filter(allow_scroll_beyond_bottom)
        self.always_hide_cursor = to_cli_filter(always_hide_cursor)
        self.wrap_lines = to_cli_filter(wrap_lines)
        self.cursorline = to_cli_filter(cursorline)
        self.cursorcolumn = to_cli_filter(cursorcolumn)
        self.content = content
        self.dont_extend_width = dont_extend_width
        self.dont_extend_height = dont_extend_height
        self.left_margins = left_margins or []
        self.right_margins = right_margins or []
        self.scroll_offsets = scroll_offsets or ScrollOffsets()
        self.get_vertical_scroll = get_vertical_scroll
        self.get_horizontal_scroll = get_horizontal_scroll
        self._width = get_width or (lambda cli: width)
        self._height = get_height or (lambda cli: height)
        self.get_colorcolumns = get_colorcolumns or (lambda cli: [])
        self.cursorline_token = cursorline_token
        self.cursorcolumn_token = cursorcolumn_token
        self._ui_content_cache = SimpleCache(maxsize=8)
        self._margin_width_cache = SimpleCache(maxsize=1)
        self.reset()

    def __repr__(self):
        return 'Window(content=%r)' % self.content

    def reset(self):
        self.content.reset()
        self.vertical_scroll = 0
        self.horizontal_scroll = 0
        self.vertical_scroll_2 = 0
        self.render_info = None

    def _get_margin_width(self, cli, margin):
        """
        Return the width for this margin.
        (Calculate only once per render time.)
        """

        def get_ui_content():
            return self._get_ui_content(cli, width=0, height=0)

        def get_width():
            return margin.get_width(cli, get_ui_content)

        key = (
         margin, cli.render_counter)
        return self._margin_width_cache.get(key, get_width)

    def preferred_width(self, cli, max_available_width):
        total_margin_width = sum(self._get_margin_width(cli, m) for m in self.left_margins + self.right_margins)
        preferred_width = self.content.preferred_width(cli, max_available_width - total_margin_width)
        if preferred_width is not None:
            preferred_width += total_margin_width
        return self._merge_dimensions(dimension=(self._width(cli)),
          preferred=preferred_width,
          dont_extend=(self.dont_extend_width))

    def preferred_height(self, cli, width, max_available_height):
        total_margin_width = sum(self._get_margin_width(cli, m) for m in self.left_margins + self.right_margins)
        wrap_lines = self.wrap_lines(cli)
        return self._merge_dimensions(dimension=(self._height(cli)),
          preferred=(self.content.preferred_height(cli, width - total_margin_width, max_available_height, wrap_lines)),
          dont_extend=(self.dont_extend_height))

    @staticmethod
    def _merge_dimensions(dimension, preferred=None, dont_extend=False):
        """
        Take the LayoutDimension from this `Window` class and the received
        preferred size from the `UIControl` and return a `LayoutDimension` to
        report to the parent container.
        """
        dimension = dimension or LayoutDimension()
        if dimension.preferred_specified:
            preferred = dimension.preferred
        else:
            if preferred is not None:
                if dimension.max:
                    preferred = min(preferred, dimension.max)
                if dimension.min:
                    preferred = max(preferred, dimension.min)
            if dont_extend:
                if preferred is not None:
                    max_ = min(dimension.max, preferred)
            max_ = dimension.max
        return LayoutDimension(min=(dimension.min),
          max=max_,
          preferred=preferred,
          weight=(dimension.weight))

    def _get_ui_content(self, cli, width, height):
        """
        Create a `UIContent` instance.
        """

        def get_content():
            return self.content.create_content(cli, width=width, height=height)

        key = (
         cli.render_counter, width, height)
        return self._ui_content_cache.get(key, get_content)

    def _get_digraph_char(self, cli):
        """ Return `False`, or the Digraph symbol to be used. """
        if cli.quoted_insert:
            return '^'
        else:
            if cli.vi_state.waiting_for_digraph:
                if cli.vi_state.digraph_symbol1:
                    return cli.vi_state.digraph_symbol1
                else:
                    return '?'
            return False

    def write_to_screen(self, cli, screen, mouse_handlers, write_position):
        """
        Write window to screen. This renders the user control, the margins and
        copies everything over to the absolute position at the given screen.
        """
        left_margin_widths = [self._get_margin_width(cli, m) for m in self.left_margins]
        right_margin_widths = [self._get_margin_width(cli, m) for m in self.right_margins]
        total_margin_width = sum(left_margin_widths + right_margin_widths)
        ui_content = self.content.create_content(cli, write_position.width - total_margin_width, write_position.height)
        assert isinstance(ui_content, UIContent)
        wrap_lines = self.wrap_lines(cli)
        scroll_func = self._scroll_when_linewrapping if wrap_lines else self._scroll_without_linewrapping
        scroll_func(ui_content, write_position.width - total_margin_width, write_position.height, cli)
        visible_line_to_row_col, rowcol_to_yx = self._copy_body(cli,
          ui_content, screen, write_position, (sum(left_margin_widths)),
          (write_position.width - total_margin_width), (self.vertical_scroll),
          (self.horizontal_scroll), has_focus=(self.content.has_focus(cli)),
          wrap_lines=wrap_lines,
          highlight_lines=True,
          vertical_scroll_2=(self.vertical_scroll_2),
          always_hide_cursor=(self.always_hide_cursor(cli)))
        x_offset = write_position.xpos + sum(left_margin_widths)
        y_offset = write_position.ypos
        self.render_info = WindowRenderInfo(ui_content=ui_content,
          horizontal_scroll=(self.horizontal_scroll),
          vertical_scroll=(self.vertical_scroll),
          window_width=(write_position.width - total_margin_width),
          window_height=(write_position.height),
          configured_scroll_offsets=(self.scroll_offsets),
          visible_line_to_row_col=visible_line_to_row_col,
          rowcol_to_yx=rowcol_to_yx,
          x_offset=x_offset,
          y_offset=y_offset,
          wrap_lines=wrap_lines)

        def mouse_handler(cli, mouse_event):
            yx_to_rowcol = dict((v, k) for k, v in rowcol_to_yx.items())
            y = mouse_event.position.y
            x = mouse_event.position.x
            max_y = write_position.ypos + len(visible_line_to_row_col) - 1
            y = min(max_y, y)
            while x >= 0:
                try:
                    row, col = yx_to_rowcol[(y, x)]
                except KeyError:
                    x -= 1
                else:
                    result = self.content.mouse_handler(cli, MouseEvent(position=Point(x=col, y=row), event_type=(mouse_event.event_type)))
                    break
            else:
                result = self.content.mouse_handler(cli, MouseEvent(position=Point(x=0, y=0), event_type=(mouse_event.event_type)))

            if result == NotImplemented:
                return self._mouse_handler(cli, mouse_event)
            else:
                return result

        mouse_handlers.set_mouse_handler_for_range(x_min=(write_position.xpos + sum(left_margin_widths)),
          x_max=(write_position.xpos + write_position.width - total_margin_width),
          y_min=(write_position.ypos),
          y_max=(write_position.ypos + write_position.height),
          handler=mouse_handler)
        move_x = 0

        def render_margin(m, width):
            tokens = m.create_margin(cli, self.render_info, width, write_position.height)
            return TokenListControl.static(tokens).create_content(cli, width + 1, write_position.height)

        for m, width in zip(self.left_margins, left_margin_widths):
            margin_screen = render_margin(m, width)
            self._copy_margin(cli, margin_screen, screen, write_position, move_x, width)
            move_x += width

        move_x = write_position.width - sum(right_margin_widths)
        for m, width in zip(self.right_margins, right_margin_widths):
            margin_screen = render_margin(m, width)
            self._copy_margin(cli, margin_screen, screen, write_position, move_x, width)
            move_x += width

    def _copy_body(self, cli, ui_content, new_screen, write_position, move_x, width, vertical_scroll=0, horizontal_scroll=0, has_focus=False, wrap_lines=False, highlight_lines=False, vertical_scroll_2=0, always_hide_cursor=False):
        """
        Copy the UIContent into the output screen.
        """
        xpos = write_position.xpos + move_x
        ypos = write_position.ypos
        line_count = ui_content.line_count
        new_buffer = new_screen.data_buffer
        empty_char = _CHAR_CACHE[('', Token)]
        ZeroWidthEscape = Token.ZeroWidthEscape
        visible_line_to_row_col = {}
        rowcol_to_yx = {}
        default_char = ui_content.default_char
        if default_char:
            for y in range(ypos, ypos + write_position.height):
                new_buffer_row = new_buffer[y]
                for x in range(xpos, xpos + width):
                    new_buffer_row[x] = default_char

        def copy():
            y = -vertical_scroll_2
            lineno = vertical_scroll
            while y < write_position.height and lineno < line_count:
                line = ui_content.get_line(lineno)
                col = 0
                x = -horizontal_scroll
                visible_line_to_row_col[y] = (
                 lineno, horizontal_scroll)
                new_buffer_row = new_buffer[(y + ypos)]
                for token, text in line:
                    if token == ZeroWidthEscape:
                        new_screen.zero_width_escapes[(y + ypos)][(x + xpos)] += text
                    else:
                        for c in text:
                            char = _CHAR_CACHE[(c, token)]
                            char_width = char.width
                            if wrap_lines:
                                if x + char_width > width:
                                    visible_line_to_row_col[y + 1] = (
                                     lineno, visible_line_to_row_col[y][1] + x)
                                    y += 1
                                    x = -horizontal_scroll
                                    new_buffer_row = new_buffer[(y + ypos)]
                                    if y >= write_position.height:
                                        return y
                            if x >= 0:
                                if y >= 0:
                                    if x < write_position.width:
                                        new_buffer_row[x + xpos] = char
                                        if char_width > 1:
                                            for i in range(1, char_width):
                                                new_buffer_row[x + xpos + i] = empty_char

                                        else:
                                            if char_width == 0:
                                                if x - 1 >= 0:
                                                    prev_char = new_buffer_row[(x + xpos - 1)]
                                                    char2 = _CHAR_CACHE[(prev_char.char + c, prev_char.token)]
                                                    new_buffer_row[x + xpos - 1] = char2
                                            rowcol_to_yx[(lineno, col)] = (y + ypos, x + xpos)
                            col += 1
                            x += char_width

                lineno += 1
                y += 1

            return y

        y = copy()

        def cursor_pos_to_screen_pos(row, col):
            try:
                y, x = rowcol_to_yx[(row, col)]
            except KeyError:
                return Point(y=0, x=0)
            else:
                return Point(y=y, x=x)

        if ui_content.cursor_position:
            screen_cursor_position = cursor_pos_to_screen_pos(ui_content.cursor_position.y, ui_content.cursor_position.x)
            if has_focus:
                new_screen.cursor_position = screen_cursor_position
                if always_hide_cursor:
                    new_screen.show_cursor = False
                else:
                    new_screen.show_cursor = ui_content.show_cursor
                self._highlight_digraph(cli, new_screen)
            if highlight_lines:
                self._highlight_cursorlines(cli, new_screen, screen_cursor_position, xpos, ypos, width, write_position.height)
        if has_focus:
            if ui_content.cursor_position:
                self._show_input_processor_key_buffer(cli, new_screen)
        if not new_screen.menu_position:
            if ui_content.menu_position:
                new_screen.menu_position = cursor_pos_to_screen_pos(ui_content.menu_position.y, ui_content.menu_position.x)
        new_screen.height = max(new_screen.height, ypos + write_position.height)
        return (
         visible_line_to_row_col, rowcol_to_yx)

    def _highlight_digraph(self, cli, new_screen):
        """
        When we are in Vi digraph mode, put a question mark underneath the
        cursor.
        """
        digraph_char = self._get_digraph_char(cli)
        if digraph_char:
            cpos = new_screen.cursor_position
            new_screen.data_buffer[cpos.y][cpos.x] = _CHAR_CACHE[(digraph_char, Token.Digraph)]

    def _show_input_processor_key_buffer(self, cli, new_screen):
        """
        When the user is typing a key binding that consists of several keys,
        display the last pressed key if the user is in insert mode and the key
        is meaningful to be displayed.
        E.g. Some people want to bind 'jj' to escape in Vi insert mode. But the
             first 'j' needs to be displayed in order to get some feedback.
        """
        key_buffer = cli.input_processor.key_buffer
        if key_buffer:
            if _in_insert_mode(cli):
                if not cli.is_done:
                    data = key_buffer[(-1)].data
                    if get_cwidth(data) == 1:
                        cpos = new_screen.cursor_position
                        new_screen.data_buffer[cpos.y][cpos.x] = _CHAR_CACHE[(data, Token.PartialKeyBinding)]

    def _highlight_cursorlines(self, cli, new_screen, cpos, x, y, width, height):
        """
        Highlight cursor row/column.
        """
        cursor_line_token = (':', ) + self.cursorline_token
        cursor_column_token = (':', ) + self.cursorcolumn_token
        data_buffer = new_screen.data_buffer
        if self.cursorline(cli):
            row = data_buffer[cpos.y]
            for x in range(x, x + width):
                original_char = row[x]
                row[x] = _CHAR_CACHE[(
                 original_char.char, original_char.token + cursor_line_token)]

        if self.cursorcolumn(cli):
            for y2 in range(y, y + height):
                row = data_buffer[y2]
                original_char = row[cpos.x]
                row[cpos.x] = _CHAR_CACHE[(
                 original_char.char, original_char.token + cursor_column_token)]

        for cc in self.get_colorcolumns(cli):
            assert isinstance(cc, ColorColumn)
            color_column_token = (':', ) + cc.token
            column = cc.position
            for y2 in range(y, y + height):
                row = data_buffer[y2]
                original_char = row[column]
                row[column] = _CHAR_CACHE[(
                 original_char.char, original_char.token + color_column_token)]

    def _copy_margin(self, cli, lazy_screen, new_screen, write_position, move_x, width):
        """
        Copy characters from the margin screen to the real screen.
        """
        xpos = write_position.xpos + move_x
        ypos = write_position.ypos
        margin_write_position = WritePosition(xpos, ypos, width, write_position.height)
        self._copy_body(cli, lazy_screen, new_screen, margin_write_position, 0, width)

    def _scroll_when_linewrapping(self, ui_content, width, height, cli):
        """
        Scroll to make sure the cursor position is visible and that we maintain
        the requested scroll offset.

        Set `self.horizontal_scroll/vertical_scroll`.
        """
        scroll_offsets_bottom = self.scroll_offsets.bottom
        scroll_offsets_top = self.scroll_offsets.top
        self.horizontal_scroll = 0
        if ui_content.get_height_for_line(ui_content.cursor_position.y, width) > height - scroll_offsets_top:
            line = explode_tokens(ui_content.get_line(ui_content.cursor_position.y))
            text_before_cursor = token_list_to_text(line[:ui_content.cursor_position.x + 1])
            text_before_height = UIContent.get_height_for_text(text_before_cursor, width)
            self.vertical_scroll = ui_content.cursor_position.y
            self.vertical_scroll_2 = min(text_before_height - 1, self.vertical_scroll_2)
            self.vertical_scroll_2 = max(0, text_before_height - height, self.vertical_scroll_2)
            return
        self.vertical_scroll_2 = 0

        def get_min_vertical_scroll():
            used_height = 0
            prev_lineno = ui_content.cursor_position.y
            for lineno in range(ui_content.cursor_position.y, -1, -1):
                used_height += ui_content.get_height_for_line(lineno, width)
                if used_height > height - scroll_offsets_bottom:
                    return prev_lineno
                prev_lineno = lineno

            return 0

        def get_max_vertical_scroll():
            prev_lineno = ui_content.cursor_position.y
            used_height = 0
            for lineno in range(ui_content.cursor_position.y - 1, -1, -1):
                used_height += ui_content.get_height_for_line(lineno, width)
                if used_height > scroll_offsets_top:
                    return prev_lineno
                prev_lineno = lineno

            return prev_lineno

        def get_topmost_visible():
            prev_lineno = ui_content.line_count - 1
            used_height = 0
            for lineno in range(ui_content.line_count - 1, -1, -1):
                used_height += ui_content.get_height_for_line(lineno, width)
                if used_height > height:
                    return prev_lineno
                prev_lineno = lineno

            return prev_lineno

        topmost_visible = get_topmost_visible()
        self.vertical_scroll = max(self.vertical_scroll, min(topmost_visible, get_min_vertical_scroll()))
        self.vertical_scroll = min(self.vertical_scroll, get_max_vertical_scroll())
        if not self.allow_scroll_beyond_bottom(cli):
            self.vertical_scroll = min(self.vertical_scroll, topmost_visible)

    def _scroll_without_linewrapping(self, ui_content, width, height, cli):
        """
        Scroll to make sure the cursor position is visible and that we maintain
        the requested scroll offset.

        Set `self.horizontal_scroll/vertical_scroll`.
        """
        cursor_position = ui_content.cursor_position or Point(0, 0)
        self.vertical_scroll_2 = 0
        if ui_content.line_count == 0:
            self.vertical_scroll = 0
            self.horizontal_scroll = 0
            return
        current_line_text = token_list_to_text(ui_content.get_line(cursor_position.y))

        def do_scroll(current_scroll, scroll_offset_start, scroll_offset_end, cursor_pos, window_size, content_size):
            scroll_offset_start = int(min(scroll_offset_start, window_size / 2, cursor_pos))
            scroll_offset_end = int(min(scroll_offset_end, window_size / 2, content_size - 1 - cursor_pos))
            if current_scroll < 0:
                current_scroll = 0
            if not self.allow_scroll_beyond_bottom(cli):
                if current_scroll > content_size - window_size:
                    current_scroll = max(0, content_size - window_size)
            if current_scroll > cursor_pos - scroll_offset_start:
                current_scroll = max(0, cursor_pos - scroll_offset_start)
            if current_scroll < cursor_pos + 1 - window_size + scroll_offset_end:
                current_scroll = cursor_pos + 1 - window_size + scroll_offset_end
            return current_scroll

        if self.get_vertical_scroll:
            self.vertical_scroll = self.get_vertical_scroll(self)
            if not isinstance(self.vertical_scroll, int):
                raise AssertionError
        if self.get_horizontal_scroll:
            self.horizontal_scroll = self.get_horizontal_scroll(self)
            if not isinstance(self.horizontal_scroll, int):
                raise AssertionError
        offsets = self.scroll_offsets
        self.vertical_scroll = do_scroll(current_scroll=(self.vertical_scroll),
          scroll_offset_start=(offsets.top),
          scroll_offset_end=(offsets.bottom),
          cursor_pos=(ui_content.cursor_position.y),
          window_size=height,
          content_size=(ui_content.line_count))
        self.horizontal_scroll = do_scroll(current_scroll=(self.horizontal_scroll),
          scroll_offset_start=(offsets.left),
          scroll_offset_end=(offsets.right),
          cursor_pos=(get_cwidth(current_line_text[:ui_content.cursor_position.x])),
          window_size=width,
          content_size=(max(get_cwidth(current_line_text), self.horizontal_scroll + width)))

    def _mouse_handler(self, cli, mouse_event):
        """
        Mouse handler. Called when the UI control doesn't handle this
        particular event.
        """
        if mouse_event.event_type == MouseEventType.SCROLL_DOWN:
            self._scroll_down(cli)
        elif mouse_event.event_type == MouseEventType.SCROLL_UP:
            self._scroll_up(cli)

    def _scroll_down(self, cli):
        """ Scroll window down. """
        info = self.render_info
        if self.vertical_scroll < info.content_height - info.window_height:
            if info.cursor_position.y <= info.configured_scroll_offsets.top:
                self.content.move_cursor_down(cli)
            self.vertical_scroll += 1

    def _scroll_up(self, cli):
        """ Scroll window up. """
        info = self.render_info
        if info.vertical_scroll > 0:
            if info.cursor_position.y >= info.window_height - 1 - info.configured_scroll_offsets.bottom:
                self.content.move_cursor_up(cli)
            self.vertical_scroll -= 1

    def walk(self, cli):
        yield self


class ConditionalContainer(Container):
    __doc__ = '\n    Wrapper around any other container that can change the visibility. The\n    received `filter` determines whether the given container should be\n    displayed or not.\n\n    :param content: :class:`.Container` instance.\n    :param filter: :class:`~prompt_tool_kit.filters.CLIFilter` instance.\n    '

    def __init__(self, content, filter):
        assert isinstance(content, Container)
        self.content = content
        self.filter = to_cli_filter(filter)

    def __repr__(self):
        return 'ConditionalContainer(%r, filter=%r)' % (self.content, self.filter)

    def reset(self):
        self.content.reset()

    def preferred_width(self, cli, max_available_width):
        if self.filter(cli):
            return self.content.preferred_width(cli, max_available_width)
        else:
            return LayoutDimension.exact(0)

    def preferred_height(self, cli, width, max_available_height):
        if self.filter(cli):
            return self.content.preferred_height(cli, width, max_available_height)
        else:
            return LayoutDimension.exact(0)

    def write_to_screen(self, cli, screen, mouse_handlers, write_position):
        if self.filter(cli):
            return self.content.write_to_screen(cli, screen, mouse_handlers, write_position)

    def walk(self, cli):
        return self.content.walk(cli)


Layout = Container