# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/transmart/api/v2/widgets/shared.py
# Compiled at: 2019-03-27 06:02:14
# Size of source mod 2**32: 804 bytes
"""
* Copyright (c) 2015-2017 The Hyve B.V.
* This code is licensed under the GNU General Public License,
* version 3.
"""
import ipywidgets

def widget_on(widget):
    widget.disabled = False
    widget.layout.visibility = 'initial'
    widget.layout.max_height = None


def widget_off(widget):
    widget.layout.visibility = 'hidden'
    widget.layout.max_height = '0'


def toggle_visibility(widget):
    if widget.layout.max_height == '0':
        widget_on(widget)
    else:
        widget_off(widget)


def create_toggle(widget, out):

    def toggle(btn):
        btn.description = 'Show' if btn.description == 'Hide' else 'Hide'
        with out:
            toggle_visibility(widget)

    toggle_btn = ipywidgets.Button(description='Hide')
    toggle_btn.on_click(toggle)
    return toggle_btn