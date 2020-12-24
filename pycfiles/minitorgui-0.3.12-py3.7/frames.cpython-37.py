# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vincent/Projects/PythonMinitor/minitorgui/minitorgui/frames.py
# Compiled at: 2020-02-21 15:28:43
# Size of source mod 2**32: 8183 bytes
"""
Main code for frame.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import tkinter as tk
from tkinter import ttk
__author__ = 'Vincent Schouten <inquiry@intoreflection.co>'
__docformat__ = 'google'
__date__ = '06-12-2019'
__copyright__ = 'Copyright 2019, Vincent Schouten'
__credits__ = ['Vincent Schouten']
__license__ = 'MIT'
__maintainer__ = 'Vincent Schouten'
__email__ = '<inquiry@intoreflection.co>'
__status__ = 'Development'
BACKGROUND_CANVAS = '#232729'

class InnerWindow(tk.Frame):
    __doc__ = '______________.'

    def __init__(self, parent, scale, *args, **kwargs):
        """____________."""
        (tk.Frame.__init__)(self, parent, *args, **kwargs)
        self.parent = parent
        self.canvas_window = CanvasWindow(self, scale)
        self.log_window = LogWindow(self, scale)
        self.canvas_window.pack(fill='both', expand=True)
        self.log_window.pack(fill='both', expand=True)


class CanvasWindow(tk.Frame):
    __doc__ = 'Construct a canvas widget for the shapes and the canvas for animation of connection.'

    def __init__(self, parent, scale):
        """_____________."""
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.scale = scale
        self.canvas = self._canvas()
        self.status = self._status()
        self._scrollbar()
        self._scroll_bind()

    def _canvas(self):
        canvas = tk.Canvas(master=self, background=BACKGROUND_CANVAS,
          height=(140 * self.scale),
          borderwidth=0,
          highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        return canvas

    def _status(self):
        status = tk.Canvas(master=self, background=BACKGROUND_CANVAS,
          height=(40 * self.scale),
          borderwidth=0,
          highlightthickness=0)
        status.pack(fill='both', expand=True)
        return status

    def _scrollbar(self):
        scrollbar = ttk.Scrollbar(master=self, orient=(tk.HORIZONTAL),
          command=(self.canvas.xview))
        scrollbar.pack(fill='x', expand=False)
        self.canvas.config(xscrollcommand=(scrollbar.set))

    def _scroll_bind(self):
        self.canvas.bind('<ButtonPress-1>', self._scroll_start)
        self.status.bind('<ButtonPress-1>', self._scroll_start)
        self.canvas.bind('<B1-Motion>', self._scroll_move)
        self.status.bind('<B1-Motion>', self._scroll_move)

    def _scroll_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def _scroll_move(self, event):
        self.canvas.scan_dragto((event.x), (event.y), gain=1)


class LogWindow(tk.Frame):
    __doc__ = '______________________.'

    def __init__(self, parent, scale):
        """____________."""
        tk.Frame.__init__(self, parent)
        self.scale = scale
        self.text = self._widget()

    def _widget(self):
        """____________."""
        text = tk.Text(master=self, width=1,
          height=1,
          background='white',
          foreground='black')
        text.pack(side='left', fill='both', expand=True)
        text.config(wrap='word')
        scrollbar = ttk.Scrollbar(master=self, orient=(tk.VERTICAL),
          command=(text.yview))
        scrollbar.pack(side='right', fill='y', expand=False)
        text.config(yscrollcommand=(scrollbar.set))
        return text

    def insert_log_line(self, line):
        """____________."""
        self.text.insert('end', line + '\n')
        self.text.see('end')


class SubCommandWindow(tk.Frame):
    __doc__ = '______________.'

    def __init__(self, parent, *args, **kwargs):
        """____________."""
        (tk.Frame.__init__)(self, parent, *args, **kwargs)
        self.parent = parent
        self.command_entry = CommandEntry(self.parent)
        self.command_response = CommandResponse(self.parent)
        self.command_entry.pack(fill='both', expand=False)
        self.command_response.pack(fill='both', expand=True)


class CommandEntry(tk.Frame):
    __doc__ = '______________.'

    def __init__(self, parent):
        """____________."""
        tk.Frame.__init__(self, parent)
        self._label()
        self.entry = self._entry()

    def _label(self):
        label = tk.Label(self, text='Input')
        label.pack(fill='x', expand=False)

    def _entry(self):
        entry = tk.Entry(self, justify='left')
        entry.pack(fill='x', expand=False)
        entry.focus_set()
        return entry


class CommandResponse(tk.Frame):
    __doc__ = '______________.'

    def __init__(self, parent):
        """____________."""
        tk.Frame.__init__(self, parent)
        self._label()
        self.text = self._text()

    def _label(self):
        label = tk.Label(self, text='Output')
        label.pack(fill='x', expand=False)

    def _text(self):
        text = tk.Text(self, width=1,
          height=1)
        text.config(wrap='word')
        text.tag_config('warning_style', foreground='red')
        text.insert(tk.END, "the interface does not support shell meta characters \nsuch as pipe and it's not possible to interact with \nprograms that need a response. hit control-c to quit \n", 'warning_style')
        text.pack(fill='both', expand=True)
        return text