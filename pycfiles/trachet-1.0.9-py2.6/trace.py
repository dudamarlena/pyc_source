# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/trachet/trace.py
# Compiled at: 2014-07-01 10:29:06
import codecs, time, logging, sys
from tffstub import tff
import template
try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

import esc, csi, ss2, ss3, char, cstr
from iomode import IOMode

class MockController(object):
    pass


class SwitchOnOffTrait(object):
    """
    >>> controller = MockController
    >>> output_file = StringIO()
    >>> handler = TraceHandler(output_file, "utf-8", controller)
    >>> handler.is_disabled()
    False
    >>> handler.set_disabled()
    >>> handler.is_disabled()
    True
    >>> handler.set_enabled()
    >>> handler.is_disabled()
    False
    """
    _disabled = False

    def is_disabled(self):
        return self._disabled

    def set_disabled(self):
        self._disabled = True

    def set_enabled(self):
        self._disabled = False


class TraceHandler(tff.DefaultHandler, SwitchOnOffTrait):
    _io_mode = None
    _xterm_mouse_buffer = None
    _xterm_mouse_counter = 0

    def __init__(self, output_file, termenc, controller):
        if isinstance(output_file, str):
            output_file = open(output_file, 'w')
        self._buffer = codecs.getwriter(termenc)(StringIO())
        self._output = output_file
        self.__bufferring = False
        self._controller = controller
        self._io_mode = IOMode()

    def set_output(self):
        if self.is_disabled():
            return
        if self._io_mode.is_input():
            if self.__bufferring:
                self._buffer.write('\n')
                self.__bufferring = False
            self._io_mode.set_output()

    def set_input(self):
        if self.is_disabled():
            return
        if self._io_mode.is_output():
            if self.__bufferring:
                self._buffer.write('\n')
                self.__bufferring = False
            self._io_mode.set_input()

    def handle_esc(self, context, intermediate, final):
        if self._xterm_mouse_buffer is not None and self._io_mode.is_input():
            seq = self._xterm_mouse_buffer
            self._xterm_mouse_buffer = None
            self.handle_invalid(context, seq)
        prompt = self._io_mode.get_prompt()
        formatted = esc.format_seq(intermediate, final, self._io_mode.is_input(), self, self._controller)
        if not formatted:
            return True
        else:
            if self.is_disabled():
                return False
            if self.__bufferring:
                self._buffer.write('\n')
                self.__bufferring = False
            self._buffer.write('%s  %s\n' % (prompt, formatted))
            return False

    def handle_csi(self, context, parameter, intermediate, final):
        if self._xterm_mouse_buffer is not None and self._io_mode.is_input():
            seq = self._xterm_mouse_buffer
            self._xterm_mouse_buffer = None
            self.handle_invalid(context, seq)
        prompt = self._io_mode.get_prompt()
        formatted = csi.format_seq(parameter, intermediate, final, self._io_mode.is_input(), self, self._controller)
        if self._io_mode.is_input():
            if not parameter and not intermediate:
                if final == 77:
                    self._xterm_mouse_counter = 3
                    self._xterm_mouse_buffer = [27, 91, final]
                    return False
                if final == 116:
                    self._xterm_mouse_counter = 2
                    self._xterm_mouse_buffer = [27, 91, final]
                    return False
                if final == 84:
                    self._xterm_mouse_counter = 6
                    self._xterm_mouse_buffer = [27, 91, final]
                    return False
        if not formatted:
            return True
        else:
            if self.is_disabled():
                return False
            if self.__bufferring:
                self._buffer.write('\n')
                self.__bufferring = False
            self._buffer.write('%s  %s\n' % (prompt, formatted))
            return False

    def handle_ss2(self, context, final):
        if self._xterm_mouse_buffer is not None and self._io_mode.is_input():
            seq = self._xterm_mouse_buffer
            self._xterm_mouse_buffer = None
            self.handle_invalid(context, seq)
        prompt = self._io_mode.get_prompt()
        formatted = ss2.format_seq(final, self._io_mode.is_input(), self, self._controller)
        if not formatted:
            return True
        else:
            if self.is_disabled():
                return False
            if self.__bufferring:
                self._buffer.write('\n')
                self.__bufferring = False
            self._buffer.write('%s  %s\n' % (prompt, formatted))
            return False

    def handle_ss3(self, context, final):
        if self._xterm_mouse_buffer is not None and self._io_mode.is_input():
            seq = self._xterm_mouse_buffer
            self._xterm_mouse_buffer = None
            self.handle_invalid(context, seq)
        prompt = self._io_mode.get_prompt()
        formatted = ss3.format_seq(final, self._io_mode.is_input(), self, self._controller)
        if not formatted:
            return True
        else:
            if self.is_disabled():
                return False
            if self.__bufferring:
                self._buffer.write('\n')
                self.__bufferring = False
            self._buffer.write('%s  %s\n' % (prompt, formatted))
            return False

    def handle_control_string(self, context, prefix, value):
        if self._xterm_mouse_buffer is not None and self._io_mode.is_input():
            seq = self._xterm_mouse_buffer
            self._xterm_mouse_buffer = None
            self.handle_invalid(context, seq)
        if self.is_disabled():
            return False
        else:
            if self.__bufferring:
                self._buffer.write('\n')
                self.__bufferring = False
            prompt = self._io_mode.get_prompt()
            formatted = cstr.format_seq(prefix, value, self._io_mode.is_input(), self, self._controller)
            if not formatted:
                return True
            self._buffer.write('%s  %s\n' % (prompt, formatted))
            return False

    def handle_char(self, context, c):
        if self._xterm_mouse_buffer is not None and self._io_mode.is_input():
            buf = self._xterm_mouse_buffer
            buf.append(c)
            self._xterm_mouse_counter -= 1
            if self._xterm_mouse_counter == 0:
                self._xterm_mouse_buffer = None
                self.handle_xterm_mouse(context, buf)
            return False
        else:
            (mnemonic, handled) = char.format_seq(c, self._io_mode.is_input(), self, self._controller)
            if not mnemonic:
                return True
            if self.is_disabled():
                return False
            if not self.__bufferring:
                self.__bufferring = True
                prompt = self._io_mode.get_prompt()
                self._buffer.write('%s  ' % prompt)
            if handled:
                self.__bufferring = False
                self._buffer.write(mnemonic)
                self._buffer.write('\n')
            else:
                self._buffer.write(mnemonic)
            return False

    def handle_invalid(self, context, seq):
        if self._xterm_mouse_buffer is not None and self._io_mode.is_input():
            seq = self._xterm_mouse_buffer
            self._xterm_mouse_buffer = None
            self.handle_invalid(context, seq)
        if self.is_disabled():
            return False
        else:
            if self.__bufferring:
                self._buffer.write('\n')
                self.__bufferring = False
            prompt = self._io_mode.get_prompt()
            value = str([ hex(c) for c in seq ])
            template_invalid = template.getinvalid()
            self._buffer.write(template_invalid % (prompt, value))
            return

    def handle_xterm_mouse(self, context, seq):
        if self.is_disabled():
            return False
        if self.__bufferring:
            self._buffer.write('\n')
            self.__bufferring = False
        prompt = self._io_mode.get_prompt()
        if seq[2] == 77:
            info = (
             seq[3] - 32, seq[4] - 32, seq[5] - 32)
            value = 'xterm normal mouse: button=%d, x=%d, y=%d' % info
            params = (prompt, seq[3], seq[4], seq[5], value)
            self._buffer.write(unicode(template.getmouse()) % params)
        elif seq[2] == 116:
            info = (
             seq[3] - 32, seq[4] - 32)
            value = 'xterm highlight mouse: x=%d, y=%d' % info
            params = (prompt, seq[3], seq[4], value)
            self._buffer.write(unicode(template.gethighlightmouseinitial()) % params)
        elif seq[2] == 84:
            info = (
             seq[3] - 32, seq[4] - 32, seq[5] - 32,
             seq[6] - 32, seq[7] - 32, seq[8] - 32)
            value = 'xterm highlight mouse: startx=%d starty=%d, endx=%d, endy=%d, mousex=%d, mousey=%d' % info
            params = (prompt, seq[3], seq[4], seq[5],
             seq[6], seq[7], seq[8], value)
            self._buffer.write(unicode(template.gethighlightmouse()) % params)

    def handle_resize(self, context, row, col):
        if self.is_disabled():
            return False
        if self.__bufferring:
            self._buffer.write('\n')
            self.__bufferring = False
        prompt = '==='
        self._buffer.write(template.getresize() % (prompt, row, col))

    def handle_draw(self, context):
        try:
            self._output.write(self._buffer.getvalue())
        except IOError:
            e = sys.exc_info()[1]
            logging.exception(e)
            time.sleep(0.1)
            self._output.write(self._buffer.getvalue())

        try:
            self._output.flush()
        except IOError:
            e = sys.exc_info()[1]
            logging.exception(e)
            time.sleep(0.1)
            self._output.flush()

        self._buffer.truncate(0)


def _test():
    pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()