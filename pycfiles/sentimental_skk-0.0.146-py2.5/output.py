# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sskk/output.py
# Compiled at: 2014-03-11 11:41:30
from canossa import tff
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class OutputHandler(tff.DefaultHandler):

    def __init__(self, screen, mode_handler):
        """
        >>> mode_handler = tff.DefaultHandler()
        >>> from canossa import Screen, termprop
        >>> termprop = termprop.MockTermprop()
        >>> screen = Screen(24, 80, 0, 0, "utf-8", termprop)
        >>> output_handler = OutputHandler(screen, mode_handler)
        >>> output_handler.dirty_flag
        False
        """
        self._output = StringIO()
        self._screen = screen
        self._mode_handler = mode_handler
        self.dirty_flag = False

    def handle_esc(self, context, intermediate, final):
        return self._mode_handler.handle_esc(context, intermediate, final)

    def handle_csi(self, context, parameter, intermediate, final):
        """
        >>> mode_handler = tff.DefaultHandler()
        >>> from canossa import MockScreenWithWindows, termprop
        >>> termprop = termprop.MockTermprop()
        >>> screen = MockScreenWithWindows()
        >>> output_handler = OutputHandler(screen, mode_handler)
        >>> context = tff.MockParseContext()
        >>> output_handler.dirty_flag
        False
        >>> output_handler.handle_csi(context, (), (), 0x4c)
        False
        >>> output_handler.dirty_flag
        True
        """
        if self._mode_handler.handle_csi(context, parameter, intermediate, final):
            return True
        if final in (76, 77, 83, 84):
            if not intermediate:
                if self._screen.has_visible_windows():
                    self.dirty_flag = True
        return False

    def handle_char(self, context, c):
        """
        >>> mode_handler = tff.DefaultHandler()
        >>> from canossa import MockScreenWithWindows, termprop
        >>> termprop = termprop.MockTermprop()
        >>> screen = MockScreenWithWindows()
        >>> output_handler = OutputHandler(screen, mode_handler)
        >>> context = tff.MockParseContext()
        >>> output_handler.dirty_flag
        False
        >>> output_handler.handle_char(context, 0x0b)
        False
        >>> output_handler.dirty_flag
        False
        >>> screen.cursor.row = screen.scroll_bottom - 1
        >>> output_handler.handle_char(context, 0x0a)
        False
        >>> output_handler.dirty_flag
        True
        """
        if c == 10:
            screen = self._screen
            if screen.cursor.row == screen.scroll_bottom - 1:
                if screen.has_visible_windows():
                    self.dirty_flag = True
        return False

    def handle_draw(self, context):
        """
        >>> mode_handler = tff.DefaultHandler()
        >>> from canossa import MockScreenWithWindows, termprop
        >>> termprop = termprop.MockTermprop()
        >>> screen = MockScreenWithWindows()
        >>> output_handler = OutputHandler(screen, mode_handler)
        >>> context = tff.MockParseContext()
        >>> output_handler.dirty_flag
        False
        >>> output_handler.handle_csi(context, (), (), 0x4c)
        False
        >>> output_handler.dirty_flag
        True
        >>> output_handler.handle_draw(context)
        False
        >>> output_handler.dirty_flag
        False
        """
        screen = self._screen
        output = self._output
        screen.cursor.attr.draw(output)
        context.puts(output.getvalue())
        output.truncate(0)
        if self.dirty_flag:
            self.dirty_flag = False
            (y, x) = screen.getyx()
            screen.drawall(context)
            screen.drawwindows(context)
            context.puts('\x1b[%d;%dH' % (y + 1, x + 1))
        return False


def test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    test()