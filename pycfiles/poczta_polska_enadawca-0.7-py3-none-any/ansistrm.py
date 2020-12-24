# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/thirdparty/ansistrm/ansistrm.py
# Compiled at: 2018-11-28 03:20:09
import logging, os, re
from pocsuite.lib.core.convert import stdoutencode

class ColorizingStreamHandler(logging.StreamHandler):
    color_map = {'black': 0, 
       'red': 1, 
       'green': 2, 
       'yellow': 3, 
       'blue': 4, 
       'magenta': 5, 
       'cyan': 6, 
       'white': 7}
    if os.name == 'nt':
        level_map = {logging.DEBUG: (None, 'blue', False), logging.INFO: (
                        None, 'green', False), 
           logging.WARNING: (
                           None, 'yellow', False), 
           logging.ERROR: (
                         None, 'red', False), 
           logging.CRITICAL: (
                            'red', 'white', False)}
    else:
        level_map = {logging.DEBUG: (None, 'blue', False), logging.INFO: (
                        None, 'green', False), 
           logging.WARNING: (
                           None, 'yellow', False), 
           logging.ERROR: (
                         None, 'red', False), 
           logging.CRITICAL: (
                            'red', 'white', False)}
    csi = '\x1b['
    reset = '\x1b[0m'
    disable_coloring = False

    @property
    def is_tty(self):
        isatty = getattr(self.stream, 'isatty', None)
        return isatty and isatty() and not self.disable_coloring

    def emit(self, record):
        try:
            message = stdoutencode(self.format(record))
            stream = self.stream
            if not self.is_tty:
                if message and message[0] == '\r':
                    message = message[1:]
                stream.write(message)
            else:
                self.output_colorized(message)
            stream.write(getattr(self, 'terminator', '\n'))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except IOError:
            pass
        except:
            self.handleError(record)

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
            import ctypes
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
        if record.levelno in self.level_map and self.is_tty:
            bg, fg, bold = self.level_map[record.levelno]
            params = []
            if bg in self.color_map:
                params.append(str(self.color_map[bg] + 40))
            if fg in self.color_map:
                params.append(str(self.color_map[fg] + 30))
            if bold:
                params.append('1')
            if params and message:
                if message.lstrip() != message:
                    prefix = re.search('\\s+', message).group(0)
                    message = message[len(prefix):]
                else:
                    prefix = ''
                message = '%s%s' % (prefix,
                 ('').join((self.csi, (';').join(params),
                  'm', message, self.reset)))
        return message

    def format(self, record):
        message = logging.StreamHandler.format(self, record)
        return self.colorize(message, record)