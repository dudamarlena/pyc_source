# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/key_binding/bindings/scroll.py
# Compiled at: 2019-08-15 23:53:39
# Size of source mod 2**32: 5709 bytes
"""
Key bindings, for scrolling up and down through pages.

This are separate bindings, because GNU readline doesn't have them, but
they are very useful for navigating through long multiline buffers, like in
Vi, Emacs, etc...
"""
from __future__ import unicode_literals
from prompt_tool_kit.layout.utils import find_window_for_buffer_name
from six.moves import range
__all__ = ('scroll_forward', 'scroll_backward', 'scroll_half_page_up', 'scroll_half_page_down',
           'scroll_one_line_up', 'scroll_one_line_down')

def _current_window_for_event(event):
    """
    Return the `Window` for the currently focussed Buffer.
    """
    return find_window_for_buffer_name(event.cli, event.cli.current_buffer_name)


def scroll_forward(event, half=False):
    """
    Scroll window down.
    """
    w = _current_window_for_event(event)
    b = event.cli.current_buffer
    if w:
        if w.render_info:
            info = w.render_info
            ui_content = info.ui_content
            scroll_height = info.window_height
            if half:
                scroll_height //= 2
            y = b.document.cursor_position_row + 1
            height = 0
            while y < ui_content.line_count:
                line_height = info.get_height_for_line(y)
                if height + line_height < scroll_height:
                    height += line_height
                    y += 1
                else:
                    break

            b.cursor_position = b.document.translate_row_col_to_index(y, 0)


def scroll_backward(event, half=False):
    """
    Scroll window up.
    """
    w = _current_window_for_event(event)
    b = event.cli.current_buffer
    if w:
        if w.render_info:
            info = w.render_info
            scroll_height = info.window_height
            if half:
                scroll_height //= 2
            y = max(0, b.document.cursor_position_row - 1)
            height = 0
            while y > 0:
                line_height = info.get_height_for_line(y)
                if height + line_height < scroll_height:
                    height += line_height
                    y -= 1
                else:
                    break

            b.cursor_position = b.document.translate_row_col_to_index(y, 0)


def scroll_half_page_down(event):
    """
    Same as ControlF, but only scroll half a page.
    """
    scroll_forward(event, half=True)


def scroll_half_page_up(event):
    """
    Same as ControlB, but only scroll half a page.
    """
    scroll_backward(event, half=True)


def scroll_one_line_down(event):
    """
    scroll_offset += 1
    """
    w = find_window_for_buffer_name(event.cli, event.cli.current_buffer_name)
    b = event.cli.current_buffer
    if w:
        if w.render_info:
            info = w.render_info
            if w.vertical_scroll < info.content_height - info.window_height:
                if info.cursor_position.y <= info.configured_scroll_offsets.top:
                    b.cursor_position += b.document.get_cursor_down_position()
                w.vertical_scroll += 1


def scroll_one_line_up(event):
    """
    scroll_offset -= 1
    """
    w = find_window_for_buffer_name(event.cli, event.cli.current_buffer_name)
    b = event.cli.current_buffer
    if w:
        if w.render_info:
            info = w.render_info
            if w.vertical_scroll > 0:
                first_line_height = info.get_height_for_line(info.first_visible_line())
                cursor_up = info.cursor_position.y - (info.window_height - 1 - first_line_height - info.configured_scroll_offsets.bottom)
                for _ in range(max(0, cursor_up)):
                    b.cursor_position += b.document.get_cursor_up_position()

                w.vertical_scroll -= 1


def scroll_page_down(event):
    """
    Scroll page down. (Prefer the cursor at the top of the page, after scrolling.)
    """
    w = _current_window_for_event(event)
    b = event.cli.current_buffer
    if w:
        if w.render_info:
            line_index = max(w.render_info.last_visible_line(), w.vertical_scroll + 1)
            w.vertical_scroll = line_index
            b.cursor_position = b.document.translate_row_col_to_index(line_index, 0)
            b.cursor_position += b.document.get_start_of_line_position(after_whitespace=True)


def scroll_page_up(event):
    """
    Scroll page up. (Prefer the cursor at the bottom of the page, after scrolling.)
    """
    w = _current_window_for_event(event)
    b = event.cli.current_buffer
    if w:
        if w.render_info:
            line_index = max(0, min(w.render_info.first_visible_line(), b.document.cursor_position_row - 1))
            b.cursor_position = b.document.translate_row_col_to_index(line_index, 0)
            b.cursor_position += b.document.get_start_of_line_position(after_whitespace=True)
            w.vertical_scroll = 0