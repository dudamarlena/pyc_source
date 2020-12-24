# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/opentea/opentea/gui_forms/wincanvas.py
# Compiled at: 2019-07-18 11:38:44
# Size of source mod 2**32: 879 bytes
"""Opentea module for wincanvas."""

def redirect_canvas_items(schema, root_frame, name):
    """Redirect to wincanvas widgets.

    The schema attributes trigger which string widget will be in use.

    Inputs :
    --------
    schema :  a schema object
    root_frame :  a Tk object were the widget will be grafted
    name : name of the element

    Outputs :
    --------
    none
    """
    if 'ot_canvas_type' not in schema:
        raise RuntimeError('ot_canvas_type attribute is compulsory')
    elif schema['ot_canvas_type'] == 'image':
        out = WinCanvasImage(schema, root_frame, name)
    else:
        raise NotImplementedError(schema['ot_canvas_type'] + ' not implemented')


class WinCanvasImage:
    __doc__ = 'Class for Image handling in dynamic canvases'

    def __init__(self, schema, root_frame, name):
        """Startup class"""
        pass