# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/ttkwidgets/linklabel.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 4376 bytes
"""
Author: RedFantom
License: GNU GPLv3
Source: This repository
"""
from noval import GetApp
try:
    import Tkinter as tk, ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk

import tkinter.font as tk_font, webbrowser

class LinkLabel(ttk.Label):
    __doc__ = '\n    A :class:`ttk.Label` that can be clicked to open a link with a default blue color, a purple color when clicked and a bright\n    blue color when hovering over the Label.\n    '

    def __init__(self, master=None, **kwargs):
        """
        Create a LinkLabel.
        
        :param master: master widget
        :param link: link to be opened
        :type link: str
        :param normal_color: text color when widget is created
        :type normal_color: str
        :param hover_color: text color when hovering over the widget
        :type hover_color: str
        :param clicked_color: text color when link is clicked
        :type clicked_color: str
        :param kwargs: options to be passed on to the :class:`ttk.Label` initializer
        """
        link_label_font = (
         tk_font.Font(name='LinkLabelFont', family=GetApp().GetDefaultEditorFamily(), underline=True),)
        self._cursor = kwargs.pop('cursor', 'hand2')
        self._link = kwargs.pop('link', '')
        self._normal_color = kwargs.pop('normal_color', '#0563c1')
        self._hover_color = kwargs.pop('hover_color', '#057bc1')
        self._clicked_color = kwargs.pop('clicked_color', '#954f72')
        ttk.Label.__init__(self, master, font='LinkLabelFont', **kwargs)
        self.config(foreground=self._normal_color)
        self._LinkLabel__clicked = False
        self.bind('<Button-1>', self.open_link)
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)

    def __getitem__(self, key):
        return self.cget(key)

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def _on_enter(self, *args):
        """Set the text color to the hover color."""
        self.config(foreground=self._hover_color, cursor=self._cursor)

    def _on_leave(self, *args):
        """Set the text color to either the normal color when not clicked or the clicked color when clicked."""
        if self._LinkLabel__clicked:
            self.config(foreground=self._clicked_color)
        else:
            self.config(foreground=self._normal_color)
        self.config(cursor='')

    def reset(self):
        """Reset Label to unclicked status if previously clicked."""
        self._LinkLabel__clicked = False
        self._on_leave()

    def open_link(self, *args):
        """Open the link in the web browser."""
        if 'disabled' not in self.state():
            webbrowser.open(self._link)
            self._LinkLabel__clicked = True
            self._on_leave()

    def cget(self, key):
        """
        Query widget option.

        :param key: option name
        :type key: str
        :return: value of the option

        To get the list of options for this widget, call the method :meth:`~LinkLabel.keys`.
        """
        if key is 'link':
            return self._link
        else:
            if key is 'hover_color':
                return self._hover_color
            if key is 'normal_color':
                return self._normal_color
            if key is 'clicked_color':
                return self._clicked_color
            return ttk.Label.cget(self, key)

    def configure(self, **kwargs):
        """
        Configure resources of the widget.

        To get the list of options for this widget, call the method :meth:`~LinkLabel.keys`.
        See :meth:`~LinkLabel.__init__` for a description of the widget specific option.
        """
        self._link = kwargs.pop('link', self._link)
        self._hover_color = kwargs.pop('hover_color', self._hover_color)
        self._normal_color = kwargs.pop('normal_color', self._normal_color)
        self._clicked_color = kwargs.pop('clicked_color', self._clicked_color)
        ttk.Label.configure(self, **kwargs)
        self._on_leave()

    def keys(self):
        """Return a list of all resource names of this widget."""
        keys = ttk.Label.keys(self)
        keys.extend(['link', 'normal_color', 'hover_color', 'clicked_color'])
        return keys