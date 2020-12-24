# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/thirdparty/ansistrm/ansistrm.py
# Compiled at: 2019-03-15 03:35:12
# Size of source mod 2**32: 7287 bytes
import logging, re, sys
from pocsuite3.lib.core.convert import stdout_encode
if sys.platform == 'win32':
    import ctypes, ctypes.wintypes
    ctypes.windll.kernel32.SetConsoleTextAttribute.argtypes = [
     ctypes.wintypes.HANDLE, ctypes.wintypes.WORD]
    ctypes.windll.kernel32.SetConsoleTextAttribute.restype = ctypes.wintypes.BOOL

class ColorizingStreamHandler(logging.StreamHandler):
    color_map = {'black':0, 
     'red':1, 
     'green':2, 
     'yellow':3, 
     'blue':4, 
     'magenta':5, 
     'cyan':6, 
     'white':7}
    level_map = {logging.DEBUG: (None, 'blue', False), 
     logging.INFO: (None, 'green', False), 
     logging.WARNING: (None, 'yellow', False), 
     logging.ERROR: (None, 'red', False), 
     logging.CRITICAL: ('red', 'white', False)}
    csi = '\x1b['
    reset = '\x1b[0m'
    bold = '\x1b[1m'
    disable_coloring = False

    @property
    def is_tty(self):
        isatty = getattr(self.stream, 'isatty', None)
        return isatty and isatty() and not self.disable_coloring

    def emit(self, record):
        try:
            message = stdout_encode(self.format(record))
            message = message.decode()
            stream = self.stream
            if not self.is_tty:
                if message:
                    if message[0] == '\r':
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

    if not sys.platform == 'win32':

        def output_colorized(self, message):
            self.stream.write(message)

    else:
        ansi_esc = re.compile('\\x1b\\[((?:\\d+)(?:;(?:\\d+))*)m')
        nt_color_map = {0:0, 
         1:4, 
         2:2, 
         3:6, 
         4:1, 
         5:5, 
         6:3, 
         7:7}

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
                        params = [int(p) for p in params.split(';')]
                        color = 0
                        for p in params:
                            if 40 <= p <= 47:
                                color |= self.nt_color_map[(p - 40)] << 4
                            elif 30 <= p <= 37:
                                color |= self.nt_color_map[(p - 30)]
                            else:
                                if p == 1:
                                    color |= 8

                        ctypes.windll.kernel32.SetConsoleTextAttribute(h, color)

    def colorize(self, message, levelno):
        if levelno in self.level_map and self.is_tty:
            bg, fg, bold = self.level_map[levelno]
            params = []
            if bg in self.color_map:
                params.append(str(self.color_map[bg] + 40))
            if fg in self.color_map:
                params.append(str(self.color_map[fg] + 30))
            if bold:
                params.append('1')
            if params and message:
                match = re.search('\\A(\\s+)', message)
                prefix = match.group(1) if match else ''
                match = re.search('\\[([A-Z ]+)\\]', message)
                if match:
                    level = match.group(1)
                    if message.startswith(self.bold):
                        message = message.replace(self.bold, '')
                        reset = self.reset + self.bold
                        params.append('1')
                    else:
                        reset = self.reset
                    message = message.replace(level, ''.join((self.csi, ';'.join(params), 'm', level, reset)), 1)
                    match = re.search('\\A\\s*\\[([\\d:]+)\\]', message)
                    if match:
                        time = match.group(1)
                        if not message.endswith(self.reset):
                            reset = self.reset
                        else:
                            if self.bold in message:
                                reset = self.reset + self.bold
                            else:
                                reset = self.reset
                        message = message.replace(time, ''.join((self.csi, str(self.color_map['cyan'] + 30), 'm', time, reset)), 1)
                    match = re.search('\\[(#\\d+)\\]', message)
                    if match:
                        counter = match.group(1)
                        if not message.endswith(self.reset):
                            reset = self.reset
                        else:
                            if self.bold in message:
                                reset = self.reset + self.bold
                            else:
                                reset = self.reset
                        message = message.replace(counter, ''.join((self.csi, str(self.color_map['yellow'] + 30), 'm', counter, reset)), 1)
                    if level != 'PAYLOAD':
                        for match in re.finditer("[^\\w]'([^']+)'", message):
                            string = match.group(1)
                            if not message.endswith(self.reset):
                                reset = self.reset
                            else:
                                if self.bold in message:
                                    reset = self.reset + self.bold
                                else:
                                    reset = self.reset
                            message = message.replace("'%s'" % string, "'%s'" % ''.join((self.csi, str(self.color_map['white'] + 30), 'm', string, reset)), 1)

        else:
            message = ''.join((self.csi, ';'.join(params), 'm', message, self.reset))
        if prefix:
            message = '%s%s' % (prefix, message)
        return message

    def format(self, record):
        message = logging.StreamHandler.format(self, record)
        return self.colorize(message, record.levelno)