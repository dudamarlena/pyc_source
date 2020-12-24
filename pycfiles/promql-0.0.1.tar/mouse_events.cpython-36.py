# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/mouse_events.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 1381 bytes
__doc__ = '\nMouse events.\n\n\nHow it works\n------------\n\nThe renderer has a 2 dimensional grid of mouse event handlers.\n(`prompt_tool_kit.layout.MouseHandlers`.) When the layout is rendered, the\n`Window` class will make sure that this grid will also be filled with\ncallbacks. For vt100 terminals, mouse events are received through stdin, just\nlike any other key press. There is a handler among the key bindings that\ncatches these events and forwards them to such a mouse event handler. It passes\nthrough the `Window` class where the coordinates are translated from absolute\ncoordinates to coordinates relative to the user control, and there\n`UIControl.mouse_handler` is called.\n'
from __future__ import unicode_literals
__all__ = ('MouseEventType', 'MouseEvent')

class MouseEventType:
    MOUSE_UP = 'MOUSE_UP'
    MOUSE_DOWN = 'MOUSE_DOWN'
    SCROLL_UP = 'SCROLL_UP'
    SCROLL_DOWN = 'SCROLL_DOWN'


MouseEventTypes = MouseEventType

class MouseEvent(object):
    """MouseEvent"""

    def __init__(self, position, event_type):
        self.position = position
        self.event_type = event_type

    def __repr__(self):
        return 'MouseEvent(%r, %r)' % (self.position, self.event_type)