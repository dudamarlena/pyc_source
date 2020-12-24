# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/of/tools/setup/lib/frame_plugin.py
# Compiled at: 2016-11-15 18:02:59
# Size of source mod 2**32: 1748 bytes
"""
Created on Feb 5, 2014

@author: Nicklas Boerjesson
"""
from tkinter import IntVar, StringVar, ttk, BooleanVar
from tkinter.constants import LEFT, X, RIGHT
from of.tools.setup.lib.frame_list import FrameCustomItem
__author__ = 'nibo'

def empty_when_none(_string=None):
    """If _string if None, return an empty string, otherwise return string.
    """
    if _string is None:
        return ''
    else:
        return str(_string)


class FramePlugin(FrameCustomItem):
    __doc__ = 'Holds and visualizes a Map between two columns of different datasets'
    row_index = None
    description = None
    plugins = None

    def __init__(self, _master, _name=None, _plugin=None):
        super(FramePlugin, self).__init__(_master)
        self.name = _name
        self.description = StringVar()
        self.init_widgets()
        self.plugin = _plugin
        if _plugin is not None:
            self.plugin_to_gui()

    def plugin_to_gui(self):
        if 'description' in self.plugin:
            self.description.set(str(empty_when_none(self.plugin['description'])))
        else:
            if 'url' in self.plugin:
                self.description.set(self.plugin['url'] + ' (Not installed)')
            else:
                raise Exception('Plugin does not have an URL property!')

    def gui_to_plugin(self):
        self.plugin['description'] = self.description.get()
        return self.plugin

    def init_widgets(self):
        """Init all widgets"""
        self.l_description = ttk.Label(self, textvariable=self.description)
        self.l_description.pack(side=LEFT)
        self.l_description['background'] = '#000000'