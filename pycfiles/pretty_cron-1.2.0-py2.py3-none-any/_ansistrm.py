# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pretty_bad_protocol/_ansistrm.py
# Compiled at: 2018-07-06 15:24:49
import ctypes, logging, os

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
        level_map = {logging.DEBUG: (None, 'blue', True), logging.INFO: (
                        None, 'green', False), 
           logging.WARNING: (
                           None, 'yellow', True), 
           logging.ERROR: (
                         None, 'red', True), 
           logging.CRITICAL: (
                            'red', 'white', True)}
    else:
        level_map = {logging.DEBUG: (None, 'blue', False), logging.INFO: (
                        None, 'green', False), 
           logging.WARNING: (
                           None, 'yellow', False), 
           logging.ERROR: (
                         None, 'red', False), 
           logging.CRITICAL: (
                            'red', 'white', True)}
    csi = '\x1b['
    reset = '\x1b[0m'

    @property
    def is_tty(self):
        isatty = getattr(self.stream, 'isatty', None)
        return isatty and isatty()

    def emit(self, record):
        try:
            message = self.format(record)
            stream = self.stream
            if not self.is_tty:
                stream.write(message)
            else:
                self.output_colorized(message)
            stream.write(getattr(self, 'terminator', '\n'))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    if os.name != 'nt':

        def output_colorized(self, message):
            self.stream.write(message)

    else:
        import re
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
            bg, fg, bold = self.level_map[record.levelno]
            params = []
            if bg in self.color_map:
                params.append(str(self.color_map[bg] + 40))
            if fg in self.color_map:
                params.append(str(self.color_map[fg] + 30))
            if bold:
                params.append('1')
            if params:
                message = ('').join((self.csi, (';').join(params),
                 'm', message, self.reset))
        return message

    def format(self, record):
        message = logging.StreamHandler.format(self, record)
        if self.is_tty:
            parts = message.split('\n', 1)
            parts[0] = self.colorize(parts[0], record)
            message = ('\n').join(parts)
        return message


def main():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(ColorizingStreamHandler())
    logging.debug('DEBUG')
    logging.info('INFO')
    logging.warning('WARNING')
    logging.error('ERROR')
    logging.critical('CRITICAL')


if __name__ == '__main__':
    main()