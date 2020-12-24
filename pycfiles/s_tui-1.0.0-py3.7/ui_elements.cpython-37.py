# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/s_tui/sturwid/ui_elements.py
# Compiled at: 2019-12-27 09:31:39
# Size of source mod 2**32: 4556 bytes
import urwid
DEFAULT_PALETTE = [
 ('body', 'default', 'default', 'standout'),
 ('header', 'default', 'dark red'),
 ('screen edge', 'light blue', 'brown'),
 ('main shadow', 'dark gray', 'black'),
 ('line', 'default', 'light gray', 'standout'),
 ('menu button', 'light gray', 'black'),
 ('bg background', 'default', 'default'),
 ('overheat dark', 'white', 'light red', 'standout'),
 ('bold text', 'default,bold', 'default', 'bold'),
 ('under text', 'default,underline', 'default', 'underline'),
 ('util light', 'default', 'light green'),
 ('util light smooth', 'light green', 'default'),
 ('util dark', 'default', 'dark green'),
 ('util dark smooth', 'dark green', 'default'),
 ('high temp dark', 'default', 'dark red'),
 ('high temp dark smooth', 'dark red', 'default'),
 ('high temp light', 'default', 'light red'),
 ('high temp light smooth', 'light red', 'default'),
 ('power dark', 'default', 'light gray', 'standout'),
 ('power dark smooth', 'light gray', 'default'),
 ('power light', 'default', 'white', 'standout'),
 ('power light smooth', 'white', 'default'),
 ('temp dark', 'default', 'dark cyan', 'standout'),
 ('temp dark smooth', 'dark cyan', 'default'),
 ('temp light', 'default', 'light cyan', 'standout'),
 ('temp light smooth', 'light cyan', 'default'),
 ('freq dark', 'default', 'dark magenta', 'standout'),
 ('freq dark smooth', 'dark magenta', 'default'),
 ('freq light', 'default', 'light magenta', 'standout'),
 ('freq light smooth', 'light magenta', 'default'),
 ('fan dark', 'default', 'dark blue', 'standout'),
 ('fan dark smooth', 'dark blue', 'default'),
 ('fan light', 'default', 'light blue', 'standout'),
 ('fan light smooth', 'light blue', 'default'),
 ('button normal', 'dark green', 'default', 'standout'),
 ('button select', 'white', 'dark green'),
 ('line', 'default', 'default', 'standout'),
 ('pg normal', 'white', 'default', 'standout'),
 ('pg complete', 'white', 'dark magenta'),
 ('high temp txt', 'light red', 'default'),
 ('pg smooth', 'dark magenta', 'default')]

class ViListBox(urwid.ListBox):

    def keypress(self, size, key):
        if key == 'j':
            key = 'down'
        else:
            if key == 'k':
                key = 'up'
            else:
                if key == 'h':
                    key = 'left'
                else:
                    if key == 'l':
                        key = 'right'
                    else:
                        if key == 'G':
                            key = 'page down'
                        else:
                            if key == 'g':
                                key = 'page up'
                            else:
                                if key == 'x':
                                    key = 'enter'
                                else:
                                    if key == 'q':
                                        key = 'q'
        return super(ViListBox, self).keypress(size, key)


def radio_button(g, l, fn):
    """ Inheriting radio button of urwid """
    w = urwid.RadioButton(g, l, False, on_state_change=fn)
    w = urwid.AttrWrap(w, 'button normal', 'button select')
    return w


def button(t, fn, data=None):
    w = urwid.Button(t, fn, data)
    w = urwid.AttrWrap(w, 'button normal', 'button select')
    return w