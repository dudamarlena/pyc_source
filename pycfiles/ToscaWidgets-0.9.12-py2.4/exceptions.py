# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tw\core\exceptions.py
# Compiled at: 2011-07-14 11:57:01
"""ToscaWidget exceptions."""

class WidgetException(RuntimeError):
    __module__ = __name__
    msg = 'Widget error'

    def __init__(self, msg=None):
        self.msg = msg or self.msg

    def __str__(self):
        return self.msg


class WidgetUnlocked(WidgetException, AttributeError):
    __module__ = __name__
    msg = 'The widget is not locked. This method needs to wait until the widget is fully locked in order to function properly'


class WidgetLocked(WidgetException, AttributeError):
    __module__ = __name__
    msg = "The widget is locked. It's unthread-safe to alter its attributes after initialization."


class WidgetInitialized(WidgetException, AttributeError):
    __module__ = __name__
    msg = 'The widget is already initialized, try doing it at the constructor.'


class WidgetUninitialized(WidgetException, AttributeError):
    __module__ = __name__
    msg = 'The widget is uninitialized.'