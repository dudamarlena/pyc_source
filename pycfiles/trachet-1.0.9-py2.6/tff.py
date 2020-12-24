# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/trachet/tff/tff.py
# Compiled at: 2014-07-01 10:29:06
__author__ = 'Hayaki Saito (user@zuse.jp)'
__version__ = '0.2.10'
__license__ = 'MIT'
signature = 'b87c36758a4c3d666c74490b383f483b'
import sys, os, termios, pty, signal, fcntl, struct, select, errno, codecs, threading, logging
_BUFFER_SIZE = 8192
_ESC_TIMEOUT = 0.5

class NotHandledException(Exception):
    """ thrown when an unknown seqnence is detected """

    def __init__(self, value):
        """
        >>> e = NotHandledException("test1")
        >>> e.value
        'test1'
        """
        self.value = value

    def __str__(self):
        """
        >>> e = NotHandledException("test2")
        >>> e.value
        'test2'
        """
        return repr(self.value)


class ParseException(Exception):
    """ thrown when a parse error is detected """

    def __init__(self, value):
        """
        >>> e = ParseException("test2")
        >>> e.value
        'test2'
        """
        self.value = value

    def __str__(self):
        """
        >>> e = ParseException("test2")
        >>> e.value
        'test2'
        """
        return repr(self.value)


class EventObserver():
    """ adapt to event driven ECMA-35/48 parser model """

    def handle_start(self, context):
        raise NotImplementedError('EventObserver::handle_start')

    def handle_end(self, context):
        raise NotImplementedError('EventObserver::handle_end')

    def handle_csi(self, context, params, intermediate, final):
        raise NotImplementedError('EventObserver::handle_csi')

    def handle_esc(self, context, prefix, final):
        raise NotImplementedError('EventObserver::handle_esc')

    def handle_ss2(self, context, final):
        raise NotImplementedError('EventObserver::handle_ss2')

    def handle_ss3(self, context, final):
        raise NotImplementedError('EventObserver::handle_ss3')

    def handle_control_string(self, context, prefix, value):
        raise NotImplementedError('EventObserver::handle_control_string')

    def handle_char(self, context, c):
        raise NotImplementedError('EventObserver::handle_char')

    def handle_invalid(self, context, seq):
        raise NotImplementedError('EventObserver::handle_invalid')

    def handle_draw(self, context):
        raise NotImplementedError('EventObserver::handle_draw')

    def handle_resize(self, context, row, col):
        raise NotImplementedError('EventObserver::handle_resize')


class Scanner():
    """ forward input iterator """

    def __iter__(self):
        raise NotImplementedError('Scanner::__iter__')

    def assign(self, value, termenc):
        raise NotImplementedError('Scanner::assign')

    def continuous_assign(self, value, termenc):
        raise NotImplementedError('Scanner::continuous_assign')


class OutputStream():
    """ abstruct TTY output stream """

    def write(self, c):
        raise NotImplementedError('OutputStream::write')

    def flush(self):
        raise NotImplementedError('OutputStream::flush')


class EventDispatcher():
    """ Dispatch interface of terminal sequence event oriented parser """

    def dispatch_esc(self, prefix, final):
        raise NotImplementedError('EventDispatcher::dispatch_esc')

    def dispatch_csi(self, prefix, params, final):
        raise NotImplementedError('EventDispatcher::dispatch_csi')

    def dispatch_control_string(self, prefix, value):
        raise NotImplementedError('EventDispatcher::dispatch_control_string')

    def dispatch_char(self, c):
        raise NotImplementedError('EventDispatcher::dispatch_char')


class Parser():
    """ abstruct Parser """

    def parse(self, context):
        raise NotImplementedError('Parser::parse')


class PTY():
    """ abstruct PTY device """

    def fitsize(self):
        raise NotImplementedError('PTY::fitsize')

    def resize(self, height, width):
        raise NotImplementedError('PTY::resize')

    def read(self):
        raise NotImplementedError('PTY::read')

    def write(self, data):
        raise NotImplementedError('PTY::write')

    def xon(self):
        raise NotImplementedError('PTY::xon')

    def xoff(self):
        raise NotImplementedError('PTY::xoff')

    def drive(self):
        raise NotImplementedError('PTY::drive')


class SimpleParser(Parser):
    """ simple parser, don't parse ESC/CSI/string seqneces """

    class _MockContext:

        def __init__(self):
            self.output = []

        def __iter__(self):
            for i in [1, 2, 3, 4, 5]:
                yield i

        def dispatch_char(self, c):
            self.output.append(c)

    def parse(self, context):
        """
        >>> parser = SimpleParser()
        >>> context = SimpleParser._MockContext()
        >>> parser.parse(context)
        >>> context.output
        [1, 2, 3, 4, 5]
        """
        for c in context:
            context.dispatch_char(c)


_STATE_GROUND = 0
_STATE_ESC = 1
_STATE_ESC_INTERMEDIATE = 2
_STATE_CSI_PARAMETER = 3
_STATE_CSI_INTERMEDIATE = 4
_STATE_SS2 = 6
_STATE_SS3 = 7
_STATE_OSC = 8
_STATE_OSC_ESC = 9
_STATE_STR = 10
_STATE_STR_ESC = 11

class _MockHandler():

    def handle_csi(self, context, parameter, intermediate, final):
        print (
         parameter, intermediate, final)

    def handle_esc(self, context, intermediate, final):
        print (
         intermediate, final)

    def handle_control_string(self, context, prefix, value):
        print (
         prefix, value)

    def handle_char(self, context, c):
        print c


class DefaultParser(Parser):
    """ parse ESC/CSI/string seqneces """

    def __init__(self):
        self.reset()

    def init(self, context):
        self.__context = context

    def state_is_esc(self):
        return self.__state != _STATE_GROUND

    def flush(self):
        pbytes = self.__pbytes
        ibytes = self.__ibytes
        state = self.__state
        context = self.__context
        if state == _STATE_ESC:
            context.dispatch_char(27)
        elif state == _STATE_ESC_INTERMEDIATE:
            context.dispatch_invalid([27] + ibytes)
        elif state == _STATE_CSI_INTERMEDIATE:
            context.dispatch_invalid([27, 91] + ibytes)
        elif state == _STATE_CSI_PARAMETER:
            context.dispatch_invalid([27, 91] + ibytes + pbytes)

    def reset(self):
        self.__state = _STATE_GROUND
        self.__pbytes = []
        self.__ibytes = []

    def parse(self, data):
        context = self.__context
        context.assign(data)
        pbytes = self.__pbytes
        ibytes = self.__ibytes
        state = self.__state
        for c in context:
            if state == _STATE_GROUND:
                if c == 27:
                    ibytes = []
                    state = _STATE_ESC
                else:
                    context.dispatch_char(c)
            elif state == _STATE_ESC:
                if c == 91:
                    pbytes = []
                    state = _STATE_CSI_PARAMETER
                elif c == 93:
                    pbytes = [
                     c]
                    state = _STATE_OSC
                elif c == 78:
                    state = _STATE_SS2
                elif c == 79:
                    state = _STATE_SS3
                elif c == 80 or c == 88 or c == 94 or c == 95:
                    pbytes = [c]
                    state = _STATE_STR
                elif c < 32:
                    if c == 27:
                        seq = [
                         27]
                        context.dispatch_invalid(seq)
                        ibytes = []
                        state = _STATE_ESC
                    elif c == 24 or c == 26:
                        seq = [
                         27]
                        context.dispatch_invalid(seq)
                        context.dispatch_char(c)
                        state = _STATE_GROUND
                    else:
                        context.dispatch_char(c)
                elif c <= 47:
                    ibytes.append(c)
                    state = _STATE_ESC_INTERMEDIATE
                elif c <= 126:
                    context.dispatch_esc(ibytes, c)
                    state = _STATE_GROUND
                elif c == 127:
                    context.dispatch_char(c)
                else:
                    seq = [
                     27, c]
                    context.dispatch_invalid(seq)
                    state = _STATE_GROUND
            elif state == _STATE_CSI_PARAMETER:
                if c > 126:
                    if c == 127:
                        context.dispatch_char(c)
                    else:
                        seq = [
                         27, 91] + pbytes
                        context.dispatch_invalid(seq)
                        state = _STATE_GROUND
                elif c > 63:
                    context.dispatch_csi(pbytes, ibytes, c)
                    state = _STATE_GROUND
                elif c > 47:
                    pbytes.append(c)
                elif c > 31:
                    ibytes.append(c)
                    state = _STATE_CSI_INTERMEDIATE
                elif c == 27:
                    seq = [
                     27, 91] + pbytes
                    context.dispatch_invalid(seq)
                    ibytes = []
                    state = _STATE_ESC
                elif c == 24 or c == 26:
                    seq = [
                     27, 91] + pbytes
                    context.dispatch_invalid(seq)
                    context.dispatch_char(c)
                    state = _STATE_GROUND
                else:
                    context.dispatch_char(c)
            elif state == _STATE_CSI_INTERMEDIATE:
                if c > 126:
                    if c == 127:
                        context.dispatch_char(c)
                    else:
                        seq = [
                         27, 91] + pbytes + ibytes
                        context.dispatch_invalid(seq)
                        state = _STATE_GROUND
                elif c > 63:
                    context.dispatch_csi(pbytes, ibytes, c)
                    state = _STATE_GROUND
                elif c > 47:
                    seq = [
                     27, 91] + pbytes + ibytes + [c]
                    context.dispatch_invalid(seq)
                    state = _STATE_GROUND
                elif c > 31:
                    ibytes.append(c)
                    state = _STATE_CSI_INTERMEDIATE
                elif c == 27:
                    seq = [
                     27, 91] + pbytes + ibytes
                    context.dispatch_invalid(seq)
                    ibytes = []
                    state = _STATE_ESC
                elif c == 24 or c == 26:
                    seq = [
                     27, 91] + pbytes + ibytes
                    context.dispatch_invalid(seq)
                    context.dispatch_char(c)
                    state = _STATE_GROUND
                else:
                    context.dispatch_char(c)
            elif state == _STATE_ESC_INTERMEDIATE:
                if c > 126:
                    if c == 127:
                        context.dispatch_char(c)
                    else:
                        seq = [
                         27] + ibytes + [c]
                        context.dispatch_invalid(seq)
                        state = _STATE_GROUND
                elif c > 47:
                    context.dispatch_esc(ibytes, c)
                    state = _STATE_GROUND
                elif c > 31:
                    ibytes.append(c)
                    state = _STATE_ESC_INTERMEDIATE
                elif c == 27:
                    seq = [
                     27] + ibytes
                    context.dispatch_invalid(seq)
                    ibytes = []
                    state = _STATE_ESC
                elif c == 24 or c == 26:
                    seq = [
                     27] + ibytes
                    context.dispatch_invalid(seq)
                    context.dispatch_char(c)
                    state = _STATE_GROUND
                else:
                    context.dispatch_char(c)
            elif state == _STATE_OSC:
                if c == 7:
                    context.dispatch_control_string(pbytes[0], ibytes)
                    state = _STATE_GROUND
                elif c < 8:
                    seq = [
                     27] + pbytes + ibytes + [c]
                    context.dispatch_invalid(seq)
                    state = _STATE_GROUND
                elif c < 14:
                    ibytes.append(c)
                elif c == 27:
                    state = _STATE_OSC_ESC
                elif c < 32:
                    seq = [
                     27] + pbytes + ibytes + [c]
                    context.dispatch_invalid(seq)
                    state = _STATE_GROUND
                else:
                    ibytes.append(c)
            elif state == _STATE_STR:
                if c < 8:
                    seq = [
                     27] + pbytes + ibytes + [c]
                    context.dispatch_invalid(seq)
                    state = _STATE_GROUND
                elif c < 14:
                    ibytes.append(c)
                elif c == 27:
                    state = _STATE_STR_ESC
                elif c < 32:
                    seq = [
                     27] + pbytes + ibytes + [c]
                    context.dispatch_invalid(seq)
                    state = _STATE_GROUND
                else:
                    ibytes.append(c)
            elif state == _STATE_OSC_ESC:
                if c == 92:
                    context.dispatch_control_string(pbytes[0], ibytes)
                    state = _STATE_GROUND
                else:
                    seq = [
                     27] + pbytes + ibytes + [27, c]
                    context.dispatch_invalid(seq)
                    state = _STATE_GROUND
            elif state == _STATE_STR_ESC:
                if c == 92:
                    context.dispatch_control_string(pbytes[0], ibytes)
                    state = _STATE_GROUND
                else:
                    seq = [
                     27] + pbytes + ibytes + [27, c]
                    context.dispatch_invalid(seq)
                    state = _STATE_GROUND
            elif state == _STATE_SS3:
                if c < 32:
                    if c == 27:
                        seq = [
                         27, 79]
                        context.dispatch_invalid(seq)
                        ibytes = []
                        state = _STATE_ESC
                    elif c == 24 or c == 26:
                        seq = [
                         27, 79]
                        context.dispatch_invalid(seq)
                        context.dispatch_char(c)
                        state = _STATE_GROUND
                    else:
                        context.dispatch_char(c)
                elif c < 127:
                    context.dispatch_ss3(c)
                    state = _STATE_GROUND
                else:
                    seq = [
                     27, 79]
                    context.dispatch_invalid(seq)
                    context.dispatch_char(c)
            elif state == _STATE_SS2:
                if c < 32:
                    if c == 27:
                        seq = [
                         27, 78]
                        context.dispatch_invalid(seq)
                        ibytes = []
                        state = _STATE_ESC
                    elif c == 24 or c == 26:
                        seq = [
                         27, 78]
                        context.dispatch_invalid(seq)
                        context.dispatch_char(c)
                        state = _STATE_GROUND
                    else:
                        context.dispatch_char(c)
                elif c < 127:
                    context.dispatch_ss2(c)
                    state = _STATE_GROUND
                else:
                    seq = [
                     27, 79]
                    context.dispatch_invalid(seq)
                    context.dispatch_char(c)

        self.__pbytes = pbytes
        self.__ibytes = ibytes
        self.__state = state


class DefaultScanner(Scanner):
    """ scan input stream and iterate UCS code points """

    def __init__(self, ucs4=True, termenc=None):
        """
        >>> scanner = DefaultScanner()
        >>> scanner._ucs4
        True
        """
        self._data = None
        self._ucs4 = ucs4
        if termenc:
            self._decoder = codecs.getincrementaldecoder(termenc)(errors='replace')
            self._termenc = termenc
        else:
            self._decoder = None
            self._termenc = None
        return

    def assign(self, value, termenc):
        """
        >>> scanner = DefaultScanner()
        >>> scanner.assign("01234", "ascii")
        >>> scanner._data
        u'01234'
        """
        if self._termenc != termenc:
            self._decoder = codecs.getincrementaldecoder(termenc)(errors='replace')
            self._termenc = termenc
        self._data = self._decoder.decode(value)

    def continuous_assign(self, value):
        """
        >>> scanner = DefaultScanner(termenc="utf-8")
        >>> scanner.continuous_assign("01234")
        >>> scanner._data
        u'01234'
        """
        self._data = self._decoder.decode(value)

    def __iter__(self):
        """
        >>> scanner = DefaultScanner()
        >>> scanner.assign("abcde", "UTF-8")
        >>> print [ c for c in scanner ]
        [97, 98, 99, 100, 101]
        """
        if self._ucs4:
            c1 = 0
            for x in self._data:
                c = ord(x)
                if c >= 55296 and c <= 56319:
                    c1 = c - 55296
                    continue
                elif c1 != 0 and c >= 56320 and c <= 57343:
                    c = 65536 + (c1 << 10 | c - 56320)
                    c1 = 0
                yield c

        for x in self._data:
            yield ord(x)


class DefaultHandler(EventObserver):
    """ default handler, pass through all ESC/CSI/string seqnceses """

    def __init__(self):
        pass

    def handle_start(self, context):
        pass

    def handle_end(self, context):
        pass

    def handle_esc(self, context, intermediate, final):
        return False

    def handle_csi(self, context, parameter, intermediate, final):
        return False

    def handle_ss2(self, context, final):
        return False

    def handle_ss3(self, context, final):
        return False

    def handle_control_string(self, context, prefix, value):
        return False

    def handle_char(self, context, c):
        return False

    def handle_invalid(self, context, seq):
        return False

    def handle_draw(self, context):
        pass

    def handle_resize(self, context, row, col):
        pass


class FilterMultiplexer(EventObserver):

    def __init__(self, lhs, rhs):
        self.__lhs = lhs
        self.__rhs = rhs

    def get_lhs(self):
        return self.__lhs

    def get_rhs(self):
        return self.__rhs

    def handle_start(self, context):
        handled_lhs = self.__lhs.handle_start(context)
        handled_rhs = self.__rhs.handle_start(context)
        return handled_lhs and handled_rhs

    def handle_end(self, context):
        handled_lhs = self.__lhs.handle_end(context)
        handled_rhs = self.__rhs.handle_end(context)
        return handled_lhs and handled_rhs

    def handle_flush(self, context):
        handled_lhs = self.__lhs.handle_flush(context)
        handled_rhs = self.__rhs.handle_flush(context)
        return handled_lhs and handled_rhs

    def handle_csi(self, context, params, intermediate, final):
        handled_lhs = self.__lhs.handle_csi(context, params, intermediate, final)
        handled_rhs = self.__rhs.handle_csi(context, params, intermediate, final)
        return handled_lhs and handled_rhs

    def handle_esc(self, context, intermediate, final):
        handled_lhs = self.__lhs.handle_esc(context, intermediate, final)
        handled_rhs = self.__rhs.handle_esc(context, intermediate, final)
        return handled_lhs and handled_rhs

    def handle_ss2(self, context, final):
        handled_lhs = self.__lhs.handle_ss2(context, final)
        handled_rhs = self.__rhs.handle_ss2(context, final)
        return handled_lhs and handled_rhs

    def handle_ss3(self, context, final):
        handled_lhs = self.__lhs.handle_ss3(context, final)
        handled_rhs = self.__rhs.handle_ss3(context, final)
        return handled_lhs and handled_rhs

    def handle_control_string(self, context, prefix, value):
        handled_lhs = self.__lhs.handle_control_string(context, prefix, value)
        handled_rhs = self.__rhs.handle_control_string(context, prefix, value)
        return handled_lhs and handled_rhs

    def handle_char(self, context, c):
        handled_lhs = self.__lhs.handle_char(context, c)
        handled_rhs = self.__rhs.handle_char(context, c)
        return handled_lhs and handled_rhs

    def handle_invalid(self, context, seq):
        handled_lhs = self.__lhs.handle_invalid(context, seq)
        handled_rhs = self.__rhs.handle_invalid(context, seq)
        return handled_lhs and handled_rhs

    def handle_draw(self, context):
        handled_lhs = self.__lhs.handle_draw(context)
        handled_rhs = self.__rhs.handle_draw(context)
        return handled_lhs and handled_rhs

    def handle_resize(self, context, row, col):
        handled_lhs = self.__lhs.handle_resize(context, row, col)
        handled_rhs = self.__rhs.handle_resize(context, row, col)
        return handled_lhs and handled_rhs


class ParseContext(OutputStream, EventDispatcher):

    def __init__(self, output, termenc='UTF-8', scanner=DefaultScanner(), handler=DefaultHandler(), buffering=False):
        self.__termenc = termenc
        self.__scanner = scanner
        self.__handler = handler
        self._c1 = 0
        if buffering:
            try:
                from cStringIO import StringIO
                self._output = codecs.getwriter(termenc)(StringIO())
            except ImportError:
                try:
                    from StringIO import StringIO
                    self._output = codecs.getwriter(termenc)(StringIO())
                except ImportError:
                    from io import StringIO
                    self._output = codecs.getwriter(termenc)(StringIO())

        else:
            self._output = codecs.getwriter(termenc)(output)
        self._target_output = output
        self._buffering = buffering

    def __iter__(self):
        return self.__scanner.__iter__()

    def assign(self, data):
        self.__scanner.assign(data, self.__termenc)
        if self._buffering:
            self._output.truncate(0)

    def sethandler(self, handler):
        self.__handler = handler

    def putu(self, data):
        self._output.write(data)

    def puts(self, data):
        self._target_output.write(data)

    def put(self, c):
        if c < 128:
            self._output.write(chr(c))
        elif c < 55296:
            self._output.write(unichr(c))
        elif c < 56320:
            self._c1 = c
        elif c < 57344:
            self._output.write(unichr(self._c1) + unichr(c))
        elif c < 65536:
            self._output.write(unichr(c))
        else:
            c -= 65536
            c1 = (c >> 10) + 55296
            c2 = (c & 1023) + 56320
            self._output.write(unichr(c1) + unichr(c2))

    def writestring(self, data):
        try:
            self._target_output.write(data)
        except Exception:
            self._output.write(data)

    def write(self, c):
        self.put(c)

    def flush(self):
        if self._buffering:
            self._target_output.write(self._output)
        try:
            self._target_output.flush()
        except IOError:
            pass

    def dispatch_esc(self, intermediate, final):
        if not self.__handler.handle_esc(self, intermediate, final):
            self.put(27)
            for c in intermediate:
                self.put(c)

            self.put(final)

    def dispatch_csi(self, parameter, intermediate, final):
        if not self.__handler.handle_csi(self, parameter, intermediate, final):
            self.put(27)
            self.put(91)
            for c in parameter:
                self.put(c)

            for c in intermediate:
                self.put(c)

            self.put(final)

    def dispatch_ss2(self, final):
        if not self.__handler.handle_ss2(self, final):
            self.put(27)
            self.put(78)
            self.put(final)

    def dispatch_ss3(self, final):
        if not self.__handler.handle_ss3(self, final):
            self.put(27)
            self.put(79)
            self.put(final)

    def dispatch_control_string(self, prefix, value):
        if not self.__handler.handle_control_string(self, prefix, value):
            self.put(27)
            self.put(prefix)
            for c in value:
                self.put(c)

            self.put(27)
            self.put(92)

    def dispatch_char(self, c):
        if not self.__handler.handle_char(self, c):
            self.put(c)

    def dispatch_invalid(self, seq):
        if not self.__handler.handle_invalid(self, seq):
            for c in seq:
                self.put(c)


class DefaultPTY(PTY):

    def __init__(self, term, lang, command, stdin, row=None, col=None):
        self._stdin_fileno = stdin.fileno()
        backup = termios.tcgetattr(self._stdin_fileno)
        self._backup_termios = backup
        (pid, master) = pty.fork()
        if not pid:
            os.environ['TERM'] = term
            os.environ['LANG'] = lang
            os.execlp('/bin/sh', '/bin/sh', '-c', 'exec %s' % command)
        self.__setupterm(self._stdin_fileno)
        self.pid = pid
        self._master = master
        if row and col:
            self.resize(row, col)

    def close(self):
        try:
            os.close(self._master)
        except OSError, e:
            logging.exception(e)
            logging.info('DefaultPTY.close: master=%d' % self._master)

    def restore_term(self):
        termios.tcsetattr(self._stdin_fileno, termios.TCSANOW, self._backup_termios)

    def __setupterm(self, fd):
        term = termios.tcgetattr(fd)
        term[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK | termios.ISTRIP | termios.INLCR | termios.IGNCR | termios.ICRNL | termios.IXON)
        term[1] &= ~(termios.OPOST | termios.ONLCR)
        c_cflag = term[2]
        c_cflag &= ~(termios.CSIZE | termios.PARENB)
        c_cflag |= termios.CS8
        term[2] = c_cflag
        c_lflag = term[3]
        c_lflag &= ~(termios.ECHO | termios.ECHONL | termios.ICANON | termios.ISIG | termios.IEXTEN)
        term[3] = c_lflag
        vdisable = os.fpathconf(self._stdin_fileno, 'PC_VDISABLE')
        VDSUSP = 11
        c_cc = term[6]
        c_cc[termios.VEOF] = vdisable
        c_cc[termios.VINTR] = vdisable
        c_cc[termios.VREPRINT] = vdisable
        c_cc[termios.VSTART] = vdisable
        c_cc[termios.VSTOP] = vdisable
        c_cc[termios.VLNEXT] = vdisable
        c_cc[termios.VWERASE] = vdisable
        c_cc[termios.VKILL] = vdisable
        c_cc[termios.VSUSP] = vdisable
        c_cc[termios.VQUIT] = vdisable
        c_cc[VDSUSP] = vdisable
        termios.tcsetattr(fd, termios.TCSANOW, term)

    def __resize_impl(self, winsize):
        fcntl.ioctl(self._master, termios.TIOCSWINSZ, winsize)
        os.kill(self.pid, signal.SIGWINCH)

    def fitsize(self):
        winsize = fcntl.ioctl(self._stdin_fileno, termios.TIOCGWINSZ, 'hhhh')
        (height, width) = struct.unpack('hh', winsize)
        self.__resize_impl(winsize)
        return (height, width)

    def resize(self, height, width):
        winsize = struct.pack('HHHH', height, width, 0, 0)
        self.__resize_impl(winsize)
        return (height, width)

    def fileno(self):
        return self._master

    def stdin_fileno(self):
        return self._stdin_fileno

    def read(self):
        return os.read(self._master, _BUFFER_SIZE)

    def write(self, data):
        os.write(self._master, data)

    def flush(self):
        pass

    def xoff(self):
        termios.tcflow(self._master, termios.TCOOFF)

    def xon(self):
        termios.tcflow(self._master, termios.TCOON)


class MockParseContext(ParseContext):

    def __init__(self):
        from StringIO import StringIO
        output = StringIO()
        ParseContext.__init__(self, output)


class Process():
    _tty = None
    _esc_timer = None

    def __init__(self, tty):
        self._tty = tty

    def start(self, termenc, inputhandler, outputhandler, inputparser, outputparser, inputscanner, outputscanner, buffering=False, stdout=sys.stdout):
        inputcontext = ParseContext(output=self._tty, termenc=termenc, scanner=inputscanner, handler=inputhandler, buffering=buffering)
        outputcontext = ParseContext(output=stdout, termenc=termenc, scanner=outputscanner, handler=outputhandler, buffering=buffering)
        inputparser.init(inputcontext)
        outputparser.init(outputcontext)
        self._inputhandler = inputhandler
        self._outputhandler = outputhandler
        self._inputparser = inputparser
        self._outputparser = outputparser
        self._inputcontext = inputcontext
        self._outputcontext = outputcontext
        inputhandler.handle_start(outputcontext)
        outputhandler.handle_start(outputcontext)

    def getpid(self):
        return self._tty.pid

    def is_alive(self):
        return self._tty is not None

    def fileno(self):
        return self._tty.fileno()

    def stdin_fileno(self):
        return self._tty.stdin_fileno()

    def read(self):
        return self._tty.read()

    def write(self, data):
        self._tty.write(data)

    def close(self):
        tty = self._tty
        if tty is not None:
            tty.close()
            self._tty = None
        return

    def end(self):
        self._inputhandler.handle_end(self._outputcontext)
        self._outputhandler.handle_end(self._outputcontext)

    def resize(self, row, col):
        self._tty.resize(row, col)

    def fitsize(self):
        return self._tty.fitsize()

    def on_write(self, data):
        self._inputparser.parse(data)

    def process_start(self):
        self._inputhandler.handle_start(self._inputcontext)
        self._outputhandler.handle_start(self._outputcontext)
        self._inputhandler.handle_draw(self._outputcontext)
        self._outputhandler.handle_draw(self._outputcontext)
        self._outputcontext.flush()

    def process_end(self):
        self._inputhandler.handle_end(self._inputcontext)
        self._outputhandler.handle_end(self._outputcontext)

    def process_resize(self, row, col):
        try:
            self._inputhandler.handle_resize(self._inputcontext, row, col)
            self._outputhandler.handle_resize(self._outputcontext, row, col)
        finally:
            self._resized = False

    def process_input(self, data):
        if self._esc_timer is not None:
            self._esc_timer.cancel()
            self._esc_timer = None
        self._inputparser.parse(data)
        if not self._inputparser.state_is_esc():
            self._inputhandler.handle_draw(self._outputcontext)
            self._outputhandler.handle_draw(self._outputcontext)
            self._outputcontext.flush()
        else:

            def dispatch_esc():
                self._inputparser.flush()
                self._inputparser.reset()
                self._inputhandler.handle_draw(self._outputcontext)
                self._outputhandler.handle_draw(self._outputcontext)
                self._outputcontext.flush()

            self._esc_timer = threading.Timer(_ESC_TIMEOUT, dispatch_esc)
            self._esc_timer.start()
        return

    def process_output(self, data):
        self._outputparser.parse(data)
        if not self._outputparser.state_is_esc():
            self._inputhandler.handle_draw(self._outputcontext)
            self._outputhandler.handle_draw(self._outputcontext)
            self._outputcontext.flush()

    def on_read(self, data):
        self._outputparser.parse(data)

    def drain(self):
        self._inputparser.reset()
        self._inputcontext.assign('')


class Session():

    def __init__(self, tty):
        self._alive = True
        self._mainprocess = Process(tty)
        self._input_target = self._mainprocess
        stdin_fileno = self._mainprocess.stdin_fileno()
        self._rfds = [stdin_fileno]
        self._xfds = [stdin_fileno]
        self._resized = False
        self._process_map = {}

    def add_subtty(self, term, lang, command, row, col, termenc, inputhandler=DefaultHandler(), outputhandler=DefaultHandler()):
        return self.create_process(term, lang, command, row, col, termenc, inputhandler, outputhandler)

    def create_process(self, term, lang, command, row, col, termenc, inputhandler=DefaultHandler(), outputhandler=DefaultHandler(), inputparser=DefaultParser(), outputparser=DefaultParser(), inputscanner=DefaultScanner(), outputscanner=DefaultScanner(), buffering=False):
        tty = DefaultPTY(term, lang, command, sys.stdin, row, col)
        process = Process(tty)
        self._init_process(process, termenc, inputhandler, outputhandler, inputparser, outputparser, inputscanner, outputscanner, buffering=buffering)
        return process

    def getactiveprocess(self):
        return self._input_target

    def process_is_active(self, process):
        return self._input_target == process

    def focus_process(self, process):
        if process.is_alive():
            logging.info('Switching focus: fileno=%d' % process.fileno())
            self._input_target.drain()
            self._input_target = process

    def blur_process(self):
        process = self._mainprocess
        if process.is_alive():
            template = 'Switching focus: fileno=%d (main process)'
            logging.info(template % process.fileno())
            self._input_target.drain()
            self._input_target = process

    def destruct_process(self, process):
        fd = process.fileno()
        if fd in self._rfds:
            self._rfds.remove(fd)
        if fd in self._xfds:
            self._xfds.remove(fd)
        process.end()
        process.close()
        del self._process_map[fd]
        self.focus_process(self._mainprocess)
        self._mainprocess.process_output('')

    def drive--- This code section failed: ---

 L.1274         0  LOAD_CLOSURE          0  'self'
                6  LOAD_CODE                <code_object onresize>
                9  MAKE_CLOSURE_0        0  None
               12  STORE_FAST            1  'onresize'

 L.1278        15  SETUP_EXCEPT         23  'to 41'

 L.1279        18  LOAD_GLOBAL           0  'signal'
               21  LOAD_ATTR             0  'signal'
               24  LOAD_GLOBAL           0  'signal'
               27  LOAD_ATTR             1  'SIGWINCH'
               30  LOAD_FAST             1  'onresize'
               33  CALL_FUNCTION_2       2  None
               36  POP_TOP          
               37  POP_BLOCK        
               38  JUMP_FORWARD         19  'to 60'
             41_0  COME_FROM            15  '15'

 L.1280        41  DUP_TOP          
               42  LOAD_GLOBAL           2  'ValueError'
               45  COMPARE_OP           10  exception-match
               48  JUMP_IF_FALSE         7  'to 58'
               51  POP_TOP          
               52  POP_TOP          
               53  POP_TOP          
               54  POP_TOP          

 L.1281        55  JUMP_FORWARD          2  'to 60'
               58  POP_TOP          
               59  END_FINALLY      
             60_0  COME_FROM            55  '55'
             60_1  COME_FROM            38  '38'

 L.1283        60  LOAD_DEREF            0  'self'
               63  LOAD_ATTR             3  '_mainprocess'
               66  LOAD_ATTR             4  'stdin_fileno'
               69  CALL_FUNCTION_0       0  None
               72  STORE_FAST            2  'stdin_fileno'

 L.1284        75  SETUP_FINALLY       777  'to 855'
               78  SETUP_EXCEPT        689  'to 770'

 L.1285        81  SETUP_LOOP          682  'to 766'
               84  LOAD_DEREF            0  'self'
               87  LOAD_ATTR             5  '_alive'
               90  JUMP_IF_FALSE       671  'to 764'
               93  POP_TOP          

 L.1286        94  SETUP_EXCEPT        460  'to 557'

 L.1287        97  LOAD_GLOBAL           6  'select'
              100  LOAD_ATTR             6  'select'
              103  LOAD_DEREF            0  'self'
              106  LOAD_ATTR             7  '_rfds'
              109  BUILD_LIST_0          0 
              112  LOAD_DEREF            0  'self'
              115  LOAD_ATTR             8  '_xfds'
              118  LOAD_CONST               0.6
              121  CALL_FUNCTION_4       4  None
              124  UNPACK_SEQUENCE_3     3 
              127  STORE_FAST            3  'rfd'
              130  STORE_FAST            4  'wfd'
              133  STORE_FAST            5  'xfd'

 L.1288       136  LOAD_FAST             5  'xfd'
              139  JUMP_IF_FALSE        70  'to 212'
            142_0  THEN                     213
              142  POP_TOP          

 L.1289       143  SETUP_LOOP           67  'to 213'
              146  LOAD_FAST             5  'xfd'
              149  GET_ITER         
              150  FOR_ITER             55  'to 208'
              153  STORE_FAST            6  'fd'

 L.1290       156  LOAD_FAST             6  'fd'
              159  LOAD_DEREF            0  'self'
              162  LOAD_ATTR             9  '_process_map'
              165  COMPARE_OP            6  in
              168  JUMP_IF_FALSE        33  'to 204'
              171  POP_TOP          

 L.1291       172  LOAD_DEREF            0  'self'
              175  LOAD_ATTR             9  '_process_map'
              178  LOAD_FAST             6  'fd'
              181  BINARY_SUBSCR    
              182  STORE_FAST            7  'process'

 L.1292       185  LOAD_DEREF            0  'self'
              188  LOAD_ATTR            10  'destruct_process'
              191  LOAD_FAST             7  'process'
              194  CALL_FUNCTION_1       1  None
              197  POP_TOP          

 L.1293       198  CONTINUE            150  'to 150'
              201  JUMP_BACK           150  'to 150'
            204_0  COME_FROM           168  '168'
              204  POP_TOP          
              205  JUMP_BACK           150  'to 150'
              208  POP_BLOCK        
              209  JUMP_FORWARD          1  'to 213'
            212_0  COME_FROM           139  '139'
              212  POP_TOP          
            213_0  COME_FROM           143  '143'

 L.1294       213  LOAD_DEREF            0  'self'
              216  LOAD_ATTR            11  '_resized'
              219  JUMP_IF_FALSE        53  'to 275'
            222_0  THEN                     276
              222  POP_TOP          

 L.1295       223  LOAD_GLOBAL          12  'False'
              226  LOAD_DEREF            0  'self'
              229  STORE_ATTR           11  '_resized'

 L.1296       232  LOAD_DEREF            0  'self'
              235  LOAD_ATTR             3  '_mainprocess'
              238  LOAD_ATTR            13  'fitsize'
              241  CALL_FUNCTION_0       0  None
              244  UNPACK_SEQUENCE_2     2 
              247  STORE_FAST            8  'row'
              250  STORE_FAST            9  'col'

 L.1297       253  LOAD_DEREF            0  'self'
              256  LOAD_ATTR             3  '_mainprocess'
              259  LOAD_ATTR            14  'process_resize'
              262  LOAD_FAST             8  'row'
              265  LOAD_FAST             9  'col'
              268  CALL_FUNCTION_2       2  None
              271  POP_TOP          
              272  JUMP_FORWARD          1  'to 276'
            275_0  COME_FROM           219  '219'
              275  POP_TOP          
            276_0  COME_FROM           272  '272'

 L.1298       276  LOAD_FAST             3  'rfd'
              279  JUMP_IF_FALSE       270  'to 552'
              282  POP_TOP          

 L.1299       283  SETUP_LOOP          267  'to 553'
              286  LOAD_FAST             3  'rfd'
              289  GET_ITER         
              290  FOR_ITER            255  'to 548'
              293  STORE_FAST            6  'fd'

 L.1300       296  LOAD_FAST             6  'fd'
              299  LOAD_FAST             2  'stdin_fileno'
              302  COMPARE_OP            2  ==
              305  JUMP_IF_FALSE        99  'to 407'
              308  POP_TOP          

 L.1301       309  LOAD_GLOBAL          15  'os'
              312  LOAD_ATTR            16  'read'
              315  LOAD_FAST             2  'stdin_fileno'
              318  LOAD_GLOBAL          17  '_BUFFER_SIZE'
              321  CALL_FUNCTION_2       2  None
              324  STORE_FAST           10  'data'

 L.1302       327  LOAD_DEREF            0  'self'
              330  LOAD_ATTR            18  '_input_target'
              333  LOAD_ATTR            19  'is_alive'
              336  CALL_FUNCTION_0       0  None
              339  JUMP_IF_FALSE        61  'to 403'
              342  POP_TOP          

 L.1303       343  LOAD_DEREF            0  'self'
              346  LOAD_ATTR            18  '_input_target'
              349  LOAD_ATTR            20  'fileno'
              352  CALL_FUNCTION_0       0  None
              355  STORE_FAST           11  'target_fd'

 L.1304       358  LOAD_DEREF            0  'self'
              361  LOAD_ATTR             9  '_process_map'
              364  LOAD_FAST            11  'target_fd'
              367  BINARY_SUBSCR    
              368  STORE_FAST            7  'process'

 L.1305       371  LOAD_FAST             7  'process'
              374  LOAD_ATTR            21  'process_input'
              377  LOAD_FAST            10  'data'
              380  CALL_FUNCTION_1       1  None
              383  POP_TOP          

 L.1306       384  LOAD_DEREF            0  'self'
              387  LOAD_ATTR             3  '_mainprocess'
              390  LOAD_ATTR            21  'process_input'
              393  LOAD_CONST               ''
              396  CALL_FUNCTION_1       1  None
              399  POP_TOP          
              400  JUMP_ABSOLUTE       545  'to 545'
            403_0  COME_FROM           339  '339'
              403  POP_TOP          
              404  JUMP_BACK           290  'to 290'
            407_0  COME_FROM           305  '305'
              407  POP_TOP          

 L.1307       408  LOAD_DEREF            0  'self'
              411  LOAD_ATTR             9  '_process_map'
              414  JUMP_IF_FALSE       127  'to 544'
              417  POP_TOP          

 L.1308       418  LOAD_DEREF            0  'self'
              421  LOAD_ATTR             9  '_process_map'
              424  STORE_FAST           12  'process_map'

 L.1309       427  LOAD_FAST             6  'fd'
              430  LOAD_FAST            12  'process_map'
              433  COMPARE_OP            6  in
              436  JUMP_IF_FALSE       101  'to 540'
              439  POP_TOP          

 L.1310       440  LOAD_FAST            12  'process_map'
              443  LOAD_FAST             6  'fd'
              446  BINARY_SUBSCR    
              447  STORE_FAST            7  'process'

 L.1311       450  LOAD_DEREF            0  'self'
              453  LOAD_ATTR            18  '_input_target'
              456  LOAD_ATTR            19  'is_alive'
              459  CALL_FUNCTION_0       0  None
              462  JUMP_IF_FALSE        71  'to 536'
              465  POP_TOP          

 L.1312       466  LOAD_FAST             6  'fd'
              469  LOAD_DEREF            0  'self'
              472  LOAD_ATTR            18  '_input_target'
              475  LOAD_ATTR            20  'fileno'
              478  CALL_FUNCTION_0       0  None
              481  COMPARE_OP            2  ==
              484  JUMP_IF_FALSE        45  'to 532'
              487  POP_TOP          

 L.1313       488  LOAD_FAST             7  'process'
              491  LOAD_ATTR            16  'read'
              494  CALL_FUNCTION_0       0  None
              497  STORE_FAST           10  'data'

 L.1314       500  LOAD_FAST             7  'process'
              503  LOAD_ATTR            22  'on_read'
              506  LOAD_FAST            10  'data'
              509  CALL_FUNCTION_1       1  None
              512  POP_TOP          

 L.1315       513  LOAD_DEREF            0  'self'
              516  LOAD_ATTR             3  '_mainprocess'
              519  LOAD_ATTR            23  'process_output'
              522  LOAD_CONST               ''
              525  CALL_FUNCTION_1       1  None
              528  POP_TOP          
              529  JUMP_ABSOLUTE       537  'to 537'
            532_0  COME_FROM           484  '484'
              532  POP_TOP          
              533  JUMP_ABSOLUTE       541  'to 541'
            536_0  COME_FROM           462  '462'
              536  POP_TOP          
              537  JUMP_ABSOLUTE       545  'to 545'
            540_0  COME_FROM           436  '436'
              540  POP_TOP          
              541  JUMP_BACK           290  'to 290'
            544_0  COME_FROM           414  '414'
              544  POP_TOP          
              545  JUMP_BACK           290  'to 290'
              548  POP_BLOCK        
              549  JUMP_FORWARD          1  'to 553'
            552_0  COME_FROM           279  '279'
              552  POP_TOP          
            553_0  COME_FROM           283  '283'

 L.1317       553  POP_BLOCK        
              554  JUMP_BACK            84  'to 84'
            557_0  COME_FROM            94  '94'

 L.1318       557  DUP_TOP          
              558  LOAD_GLOBAL           6  'select'
              561  LOAD_ATTR            24  'error'
              564  COMPARE_OP           10  exception-match
              567  JUMP_IF_FALSE       122  'to 692'
              570  POP_TOP          
              571  POP_TOP          
              572  STORE_FAST           13  'e'
              575  POP_TOP          

 L.1319       576  LOAD_FAST            13  'e'
              579  UNPACK_SEQUENCE_2     2 
              582  STORE_FAST           14  'no'
              585  STORE_FAST           15  'msg'

 L.1320       588  LOAD_FAST            14  'no'
              591  LOAD_GLOBAL          25  'errno'
              594  LOAD_ATTR            26  'EINTR'
              597  COMPARE_OP            2  ==
              600  JUMP_IF_FALSE        13  'to 616'
              603  POP_TOP          

 L.1322       604  LOAD_GLOBAL          27  'True'
              607  LOAD_DEREF            0  'self'
              610  STORE_ATTR           11  '_resized'
              613  JUMP_ABSOLUTE       761  'to 761'
            616_0  COME_FROM           600  '600'
              616  POP_TOP          

 L.1323       617  LOAD_FAST            14  'no'
              620  LOAD_GLOBAL          25  'errno'
              623  LOAD_ATTR            28  'EBADF'
              626  COMPARE_OP            2  ==
              629  JUMP_IF_FALSE        50  'to 682'
              632  POP_TOP          

 L.1324       633  SETUP_LOOP           53  'to 689'
              636  LOAD_DEREF            0  'self'
              639  LOAD_ATTR             9  '_process_map'
              642  GET_ITER         
              643  FOR_ITER             32  'to 678'
              646  STORE_FAST            6  'fd'

 L.1325       649  LOAD_DEREF            0  'self'
              652  LOAD_ATTR             9  '_process_map'
              655  LOAD_FAST             6  'fd'
              658  BINARY_SUBSCR    
              659  STORE_FAST            7  'process'

 L.1326       662  LOAD_DEREF            0  'self'
              665  LOAD_ATTR            10  'destruct_process'
              668  LOAD_FAST             7  'process'
              671  CALL_FUNCTION_1       1  None
              674  POP_TOP          
              675  JUMP_BACK           643  'to 643'
              678  POP_BLOCK        
              679  JUMP_ABSOLUTE       761  'to 761'
            682_0  COME_FROM           629  '629'
              682  POP_TOP          

 L.1328       683  LOAD_FAST            13  'e'
              686  RAISE_VARARGS_1       1  None
            689_0  COME_FROM           633  '633'
              689  JUMP_BACK            84  'to 84'
              692  POP_TOP          

 L.1329       693  DUP_TOP          
              694  LOAD_GLOBAL          29  'OSError'
              697  COMPARE_OP           10  exception-match
              700  JUMP_IF_FALSE        56  'to 759'
              703  POP_TOP          
              704  POP_TOP          
              705  STORE_FAST           13  'e'
              708  POP_TOP          

 L.1330       709  LOAD_FAST            13  'e'
              712  UNPACK_SEQUENCE_2     2 
              715  STORE_FAST           14  'no'
              718  STORE_FAST           15  'msg'

 L.1331       721  LOAD_FAST            14  'no'
              724  LOAD_GLOBAL          25  'errno'
              727  LOAD_ATTR            26  'EINTR'
              730  COMPARE_OP            2  ==
              733  JUMP_IF_FALSE        13  'to 749'
              736  POP_TOP          

 L.1333       737  LOAD_GLOBAL          27  'True'
              740  LOAD_DEREF            0  'self'
              743  STORE_ATTR           11  '_resized'
              746  JUMP_ABSOLUTE       761  'to 761'
            749_0  COME_FROM           733  '733'
              749  POP_TOP          

 L.1335       750  LOAD_FAST            13  'e'
              753  RAISE_VARARGS_1       1  None
              756  JUMP_BACK            84  'to 84'
            759_0  COME_FROM           700  '700'
              759  POP_TOP          
              760  END_FINALLY      
              761  JUMP_BACK            84  'to 84'
              764  POP_TOP          
              765  POP_BLOCK        
            766_0  COME_FROM            81  '81'
              766  POP_BLOCK        
              767  JUMP_FORWARD         81  'to 851'
            770_0  COME_FROM            78  '78'

 L.1336       770  DUP_TOP          
              771  LOAD_GLOBAL          29  'OSError'
              774  COMPARE_OP           10  exception-match
              777  JUMP_IF_FALSE        69  'to 849'
              780  POP_TOP          
              781  POP_TOP          
              782  STORE_FAST           13  'e'
              785  POP_TOP          

 L.1337       786  LOAD_FAST            13  'e'
              789  UNPACK_SEQUENCE_2     2 
              792  STORE_FAST           14  'no'
              795  STORE_FAST           15  'msg'

 L.1338       798  LOAD_FAST            14  'no'
              801  LOAD_GLOBAL          25  'errno'
              804  LOAD_ATTR            30  'EIO'
              807  COMPARE_OP            2  ==
              810  JUMP_IF_FALSE         5  'to 818'
            813_0  THEN                     818
              813  POP_TOP          

 L.1339       814  LOAD_CONST               None
              817  RETURN_END_IF    
              818  POP_TOP          

 L.1340       819  LOAD_FAST            14  'no'
              822  LOAD_GLOBAL          25  'errno'
              825  LOAD_ATTR            28  'EBADF'
              828  COMPARE_OP            2  ==
              831  JUMP_IF_FALSE         5  'to 839'
            834_0  THEN                     839
              834  POP_TOP          

 L.1341       835  LOAD_CONST               None
              838  RETURN_END_IF    
              839  POP_TOP          

 L.1343       840  LOAD_FAST            13  'e'
              843  RAISE_VARARGS_1       1  None
              846  JUMP_FORWARD          2  'to 851'
              849  POP_TOP          
              850  END_FINALLY      
            851_0  COME_FROM           846  '846'
            851_1  COME_FROM           767  '767'
              851  POP_BLOCK        
              852  LOAD_CONST               None
            855_0  COME_FROM            75  '75'

 L.1345       855  SETUP_FINALLY        17  'to 875'

 L.1346       858  LOAD_DEREF            0  'self'
              861  LOAD_ATTR             3  '_mainprocess'
              864  LOAD_ATTR            31  'process_end'
              867  CALL_FUNCTION_0       0  None
              870  POP_TOP          
              871  POP_BLOCK        
              872  LOAD_CONST               None
            875_0  COME_FROM           855  '855'

 L.1348       875  SETUP_LOOP           50  'to 928'
              878  LOAD_DEREF            0  'self'
              881  LOAD_ATTR             9  '_process_map'
              884  GET_ITER         
              885  FOR_ITER             39  'to 927'
              888  STORE_FAST            6  'fd'

 L.1349       891  LOAD_DEREF            0  'self'
              894  LOAD_ATTR             9  '_process_map'
              897  LOAD_FAST             6  'fd'
              900  BINARY_SUBSCR    
              901  STORE_FAST            7  'process'

 L.1350       904  LOAD_FAST             7  'process'
              907  LOAD_ATTR            32  'end'
              910  CALL_FUNCTION_0       0  None
              913  POP_TOP          

 L.1351       914  LOAD_FAST             7  'process'
              917  LOAD_ATTR            33  'close'
              920  CALL_FUNCTION_0       0  None
              923  POP_TOP          
              924  JUMP_BACK           885  'to 885'
              927  POP_BLOCK        
            928_0  COME_FROM           875  '875'
              928  END_FINALLY      
              929  END_FINALLY      

Parse error at or near `COME_FROM' instruction at offset 689_0

    def start(self, termenc, stdin=sys.stdin, stdout=sys.stdout, inputscanner=DefaultScanner(), inputparser=DefaultParser(), inputhandler=DefaultHandler(), outputscanner=DefaultScanner(), outputparser=DefaultParser(), outputhandler=DefaultHandler(), buffering=False):
        mainprocess = self._mainprocess
        self._init_process(mainprocess, termenc, inputhandler, outputhandler, inputparser, outputparser, inputscanner, outputscanner, buffering)
        self._resized = False

        def onclose(no, frame):
            (pid, status) = os.wait()
            if not mainprocess.is_alive():
                self._alive = False
            elif pid == mainprocess.getpid():
                self._alive = False
            else:
                self.focus_process(mainprocess)

        signal.signal(signal.SIGCHLD, onclose)
        self.drive()

    def _init_process(self, process, termenc, inputhandler, outputhandler, inputparser, outputparser, inputscanner, outputscanner, buffering):
        fd = process.fileno()
        self._rfds.append(fd)
        self._xfds.append(fd)
        self._process_map[fd] = process
        process.start(termenc, inputhandler, outputhandler, inputparser, outputparser, inputscanner, outputscanner, buffering)
        self.focus_process(process)


def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    import inspect, hashlib, sys
    thismodule = sys.modules[__name__]
    md5 = hashlib.md5()
    specs = []
    for (name, member) in inspect.getmembers(thismodule):
        if inspect.isclass(member):
            if name[0] != '_':
                classname = name
                for (name, member) in inspect.getmembers(member):
                    if inspect.ismethod(member):
                        if name.startswith('__') or name[0] != '_':
                            argspec = inspect.getargspec(member)
                            (args, varargs, keywords, defaultvalue) = argspec
                            specstr = '%s.%s.%s' % (classname, name, args)
                            specs.append(specstr)

    specs.sort()
    md5.update(('').join(specs))
    sys.stdout.write(md5.hexdigest())