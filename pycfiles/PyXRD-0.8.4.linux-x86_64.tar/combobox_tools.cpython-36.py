# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/views/combobox_tools.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 827 bytes
from .cell_renderer_tools import get_default_renderer, parse_callback, parse_kwargs

def add_renderer_with_attrs(combo, col_attrs, rend):
    combo.pack_start(rend, True)
    for attr, val in col_attrs.items():
        combo.add_attribute(rend, attr, val)


def add_combo_text_column(combo, data_func=None, **kwargs):
    kwargs['xalign'] = kwargs.get('xalign', 0.0)
    kwargs, col_attrs = parse_kwargs(**kwargs)
    rend = get_default_renderer(*('text', ), **kwargs)
    add_renderer_with_attrs(combo, col_attrs, rend)
    if data_func != None:
        callback, args = parse_callback(data_func)
        combo.set_cell_data_func(rend, callback, args)
    return rend