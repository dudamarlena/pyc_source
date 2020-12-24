# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/robots/helpers/ansistrm.py
# Compiled at: 2015-01-26 11:58:05
__doc__ = " An ANSI-based colored console log handler, based on\nhttps://gist.github.com/758430, and with a few special features\nto make sure it works well in pyRobots' concurrent environment.\n"
import logging, os, threading
from collections import deque
import time, weakref, robots.concurrency
if os.name == 'nt':
    import ctypes, re

class ConcurrentColorizingStreamHandler(logging.StreamHandler):
    """
    A log handler that:

    - (tries to) guarantee strong thread-safety: the threads generating log
      message can be interrupted at *any* time without causing dead-locks (which
      is not the case with a regular ``StreamHandler``: the calling thread may
      be interrupted while it owns a lock on stdout)
    - propagate pyRobots signals (ActionCancelled, ActionPaused)
    - colors the output (nice!)

    """
    color_map = {'black': 0, 
       'red': 1, 
       'green': 2, 
       'yellow': 3, 
       'blue': 4, 
       'magenta': 5, 
       'cyan': 6, 
       'white': 7}
    bright_scheme = {logging.DEBUG: (
                     None, 'blue', False, False), 
       logging.INFO: (
                    None, 'white', False, False), 
       logging.WARNING: (
                       None, 'yellow', False, False), 
       logging.ERROR: (
                     None, 'red', False, False), 
       logging.CRITICAL: (
                        'red', 'white', True, False)}
    dark_scheme = {logging.DEBUG: (
                     None, 'blue', False, False), 
       logging.INFO: (
                    None, 'black', False, False), 
       logging.WARNING: (
                       None, 'yellow', False, False), 
       logging.ERROR: (
                     None, 'red', False, False), 
       logging.CRITICAL: (
                        'red', 'black', True, False)}
    mono_scheme = {logging.DEBUG: (
                     None, None, False, False), 
       logging.INFO: (
                    None, None, False, False), 
       logging.WARNING: (
                       None, None, False, False), 
       logging.ERROR: (
                     None, None, False, False), 
       logging.CRITICAL: (
                        None, None, False, False)}
    xmas_scheme = {logging.DEBUG: (
                     'red', 'yellow', False, True), 
       logging.INFO: (
                    'red', 'white', False, True), 
       logging.WARNING: (
                       'red', 'yellow', False, True), 
       logging.ERROR: (
                     'red', 'yellow', False, True), 
       logging.CRITICAL: (
                        'red', 'white', False, True)}
    csi = '\x1b['
    reset = '\x1b[0m'

    def __init__(self, scheme=None):
        logging.StreamHandler.__init__(self)
        self.msgs = deque()
        if scheme == 'xmas':
            self.level_map = self.xmas_scheme
        elif scheme == 'dark':
            self.level_map = self.dark_scheme
        elif scheme == 'mono':
            self.level_map = self.mono_scheme
        else:
            self.level_map = self.bright_scheme
        self.main_thread = threading.current_thread()
        self.thread = threading.Thread(target=ConcurrentColorizingStreamHandler.run, name='pyRobots logger', args=(
         weakref.proxy(self),))
        self.thread.start()

    def __del__(self):
        self.thread.join()

    @property
    def is_tty(self):
        isatty = getattr(self.stream, 'isatty', None)
        return isatty and isatty()

    def handle(self, record):
        """
        Override the default handle method to *remove locking*, because Python logging, while thread-safe according to the doc,
        does not play well with us raising signals (ie exception) at anytime (including while the logging system is locking the output stream).
        """
        rv = self.filter(record)
        if rv:
            self.msgs.append(record)
        return rv

    def run(self):
        while self.main_thread.is_alive() or len(self.msgs) > 0:
            try:
                record = self.msgs.popleft()
                self.emit(record)
            except IndexError:
                time.sleep(0.01)

    def emit(self, record):
        try:
            message = self.format(record)
            if message is None:
                return
            stream = self.stream
            if not self.is_tty:
                stream.write(message)
            else:
                self.output_colorized(message)
            stream.write(getattr(self, 'terminator', '\n'))
            self.flush()
        except (KeyboardInterrupt, SystemExit, robots.concurrency.ActionCancelled, robots.concurrency.ActionPaused):
            raise
        except:
            self.handleError(record)

        return

    if os.name != 'nt':

        def output_colorized(self, message):
            self.stream.write(message)

    else:
        ansi_esc = re.compile('\\x1b\\[((?:\\d+)(?:;(?:\\d+))*)m')
        nt_color_map = {0: 0, 
           1: 4, 
           2: 2, 
           3: 6, 
           4: 1, 
           5: 5, 
           6: 3, 
           7: 7}

        def output_colorized(self, message):
            parts = self.ansi_esc.split(message)
            write = self.stream.write
            h = None
            fd = getattr(self.stream, 'fileno', None)
            if fd is not None:
                fd = fd()
                if fd in (1, 2):
                    h = ctypes.windll.kernel32.GetStdHandle(-10 - fd)
            while parts:
                text = parts.pop(0)
                if text:
                    write(text)
                if parts:
                    params = parts.pop(0)
                    if h is not None:
                        params = [ int(p) for p in params.split(';') ]
                        color = 0
                        for p in params:
                            if 40 <= p <= 47:
                                color |= self.nt_color_map[(p - 40)] << 4
                            elif 30 <= p <= 37:
                                color |= self.nt_color_map[(p - 30)]
                            elif p == 1:
                                color |= 8
                            elif p == 0:
                                color = 7

                        ctypes.windll.kernel32.SetConsoleTextAttribute(h, color)

            return

    def colorize(self, message, record):
        if record.levelno in self.level_map:
            bg, fg, bold, blink = self.level_map[record.levelno]
            params = []
            if bg in self.color_map:
                params.append(str(self.color_map[bg] + 40))
            if fg in self.color_map:
                params.append(str(self.color_map[fg] + 30))
            if bold:
                params.append('1')
            elif blink:
                params.append('5')
            if params:
                message = ('').join((self.csi, (';').join(params),
                 'm', message, self.reset))
        return message

    def format(self, record):
        try:
            message = logging.StreamHandler.format(self, record)
        except AttributeError:
            return

        if self.is_tty:
            message = self.colorize(message, record)
        return message


def main():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(ConcurrentColorizingStreamHandler())
    logging.debug('DEBUG')
    logging.info('INFO')
    logging.warning('WARNING')
    logging.error('ERROR')
    logging.critical('CRITICAL')


if __name__ == '__main__':
    main()