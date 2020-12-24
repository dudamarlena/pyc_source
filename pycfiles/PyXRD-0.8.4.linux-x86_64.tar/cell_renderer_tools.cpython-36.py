# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/views/cell_renderer_tools.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 2357 bytes
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
renderer_map = {'text':Gtk.CellRendererText, 
 'accel':Gtk.CellRendererAccel, 
 'combo':Gtk.CellRendererCombo, 
 'spin':Gtk.CellRendererSpin, 
 'pixbuf':Gtk.CellRendererPixbuf, 
 'progress':Gtk.CellRendererProgress, 
 'spinner':Gtk.CellRendererSpinner, 
 'toggle':Gtk.CellRendererToggle}

def get_default_renderer(type, **kwargs):
    """
        Creates a CellRendere of type 'type' and sets any attributes passed with
        the key-word arguments. Underscores in variable names are replaced with
        dashes in the proces.
    """
    rend = renderer_map.get(type, type)()
    for key, val in kwargs.items():
        rend.set_property(key.replace('_', '-'), val)

    return rend


def parse_callback(callback, reduce=True):
    """
        Parses callbacks for CellRenderers: it splits the 
        callback from its arguments if present. Additionally this method will 
        not create singleton argument lists, but pass them as a single argument.
        
        Returns the callback and its argument(s) (or an empty tuple)
    """
    args = tuple()
    try:
        callback, args = callback
    except TypeError as ValueError:
        pass

    if reduce:
        if len(args) == 1:
            args = args[0]
    return (
     callback, args)


def parse_kwargs(**kwargs):
    """
        Parses key-word arguments.
        It checks for the presence of key-words ending with '_col', these are
        popped and stored in a seperate dictionary, as they are to be passed
        to the constructor of the actual column or combobox (attribute mappings)
        In addition it sets a number of default attributes for the CellRenderer.
        
        Returns a tuple containing a dict with the CellRenderer attributes and a
        dict with the TreeViewColumn attribute mappings
    """
    kwargs['xalign'] = kwargs.get('xalign', 0.5)
    kwargs['yalign'] = kwargs.get('yalign', 0.5)
    col_attrs = dict()
    for key, value in dict(kwargs).items():
        if key.endswith('_col'):
            col_attrs[key[:-4]] = value
            kwargs.pop(key)

    return (
     kwargs, col_attrs)