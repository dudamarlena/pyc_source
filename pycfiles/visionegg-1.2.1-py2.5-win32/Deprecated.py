# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\Deprecated.py
# Compiled at: 2009-07-07 11:29:42
"""
Bits of code which will be removed in the future.

"""
import VisionEgg, sys, os, logging

class Message:
    """DEPRECATED Handles message/warning/error printing, exception raising."""
    TRIVIAL = 0
    NAG = 1
    INFO = 2
    DEPRECATION = 3
    WARNING = 4
    ERROR = 5
    FATAL = 6

    def __init__(self):
        self.pid = os.getpid()

    def add(self, message, level=INFO, preserve_formatting=0, no_sys_stderr=0):
        level_translate = {Message.TRIVIAL: logging.DEBUG, 
           Message.NAG: logging.DEBUG, 
           Message.INFO: logging.INFO, 
           Message.DEPRECATION: logging.WARNING, 
           Message.WARNING: logging.WARNING, 
           Message.ERROR: logging.ERROR, 
           Message.FATAL: logging.CRITICAL}
        new_level = level_translate[level]
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger('VisionEgg.Deprecated')
        self.logger.log(new_level, message + '\n(sent using deprecated VisionEgg.Core.Message class)')

    def format_string(self, in_str):
        min_line_length = 70
        in_list = in_str.split()
        out_str = ''
        cur_line = ''
        for word in in_list:
            cur_line = cur_line + word + ' '
            if len(cur_line) > min_line_length:
                out_str = out_str + cur_line[:-1] + '\n'
                cur_line = '    '

        if cur_line.strip():
            out_str = out_str + cur_line + '\n'
        return out_str

    def handle(self):
        if not self._sent_initial_newline:
            self.output_stream.write('\n', _no_sys_stderr=1)
            self.output_stream.flush()
            self._sent_initial_newline = 1
        while len(self.message_queue) > 0:
            my_str = ''
            (level, text, preserve_formatting, date_str, no_sys_stderr) = self.message_queue.pop(0)
            if level >= self.print_level:
                my_str = my_str + date_str + ' '
                if self.pid:
                    my_str += '(%d) ' % (self.pid,)
                if level == Message.TRIVIAL:
                    my_str = my_str + 'trivial'
                elif level == Message.INFO:
                    my_str = my_str + 'info'
                elif level == Message.NAG:
                    my_str = my_str + 'nag'
                elif level == Message.DEPRECATION:
                    my_str = my_str + 'DEPRECATION WARNING'
                elif level == Message.WARNING:
                    my_str = my_str + 'WARNING'
                elif level == Message.ERROR:
                    my_str = my_str + 'ERROR'
                elif level == Message.FATAL:
                    my_str = my_str + 'FATAL'
                my_str += ': '
                my_str += text
                if not preserve_formatting:
                    my_str = self.format_string(my_str)
                self.output_stream.write(my_str, _no_sys_stderr=no_sys_stderr)
                self.output_stream.flush()
            if level >= self.exception_level:
                raise RuntimeError(text)
            if level == Message.FATAL:
                sys.exit(-1)