# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/botcore/util/logging_tool.py
# Compiled at: 2018-04-01 06:36:57
# Size of source mod 2**32: 4609 bytes
"""

    Python logging tuned to extreme.

"""
__author__ = 'Mikko Ohtamaa <mikko@opensourcehacker.com>'
__license__ = 'MIT'
import logging
from logutils.colorize import ColorizingStreamHandler

class LoggingHandler(ColorizingStreamHandler):
    __doc__ = ' A colorful logging handler optimized for terminal debugging aestetichs.\n\n    - Designed for diagnosis and debug mode output - not for disk logs\n\n    - Highlight the content of logging message in more readable manner\n\n    - Show function and line, so you can trace where your logging messages\n      are coming from\n\n    - Keep timestamp compact\n\n    - Extra module/function output for traceability\n\n    The class provide few options as member variables you\n    would might want to customize after instiating the handler.\n    '
    level_map = {logging.DEBUG: (None, 'cyan', False), 
     logging.INFO: (None, 'white', False), 
     logging.WARNING: (None, 'yellow', True), 
     logging.ERROR: (None, 'red', True), 
     logging.CRITICAL: ('red', 'white', True)}
    date_format = '%H:%m:%S'
    who_padding = 22
    show_name = True

    def get_color(self, fg=None, bg=None, bold=False):
        """
        Construct a terminal color code

        :param fg: Symbolic name of foreground color

        :param bg: Symbolic name of background color

        :param bold: Brightness bit
        """
        params = []
        if bg in self.color_map:
            params.append(str(self.color_map[bg] + 40))
        if fg in self.color_map:
            params.append(str(self.color_map[fg] + 30))
        if bold:
            params.append('1')
        color_code = ''.join((self.csi, ';'.join(params), 'm'))
        return color_code

    def colorize(self, record):
        """
        Get a special format string with ASCII color codes.
        """
        if record.levelno in self.level_map:
            fg, bg, bold = self.level_map[record.levelno]
        else:
            bg = None
            fg = 'white'
            bold = False
        template = [
         '[',
         self.get_color('black', None, True),
         '%(asctime)s',
         self.reset,
         '] ',
         self.get_color('white', None, True) if self.show_name else '',
         '%(name)s ' if self.show_name else '',
         '%(padded_who)s',
         self.reset,
         ' ',
         self.get_color(bg, fg, bold),
         '%(message)s',
         self.reset]
        format = ''.join(template)
        who = [
         self.get_color('green'),
         getattr(record, 'funcName', ''),
         '()',
         self.get_color('black', None, True),
         ':',
         self.get_color('cyan'),
         str(getattr(record, 'lineno', 0))]
        who = ''.join(who)
        unformatted_who = getattr(record, 'funcName', '') + '()' + ':' + str(getattr(record, 'lineno', 0))
        if len(unformatted_who) < self.who_padding:
            spaces = ' ' * (self.who_padding - len(unformatted_who))
        else:
            spaces = ''
        record.padded_who = who + spaces
        formatter = logging.Formatter(format, self.date_format)
        self.colorize_traceback(formatter, record)
        output = formatter.format(record)
        record.ext_text = None
        return output

    def colorize_traceback(self, formatter, record):
        """
        Turn traceback text to red.
        """
        if record.exc_info:
            record.exc_text = ''.join([
             self.get_color('red'),
             formatter.formatException(record.exc_info),
             self.reset])

    def format(self, record):
        """
        Formats a record for output.

        Takes a custom formatting path on a terminal.
        """
        if self.is_tty:
            message = self.colorize(record)
        else:
            message = logging.StreamHandler.format(self, record)
        return message