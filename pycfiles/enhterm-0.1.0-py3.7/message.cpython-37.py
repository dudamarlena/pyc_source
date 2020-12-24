# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\enhterm\message.py
# Compiled at: 2019-11-09 02:45:51
# Size of source mod 2**32: 2738 bytes
"""
"""
from __future__ import unicode_literals
from __future__ import print_function
import logging
from .lang import _
logger = logging.getLogger('enhterm')

class MessagesMixin(object):
    __doc__ = '\n    Support for printing user messages.\n\n    The class expects a self.stdout from the implementation.\n    '

    def __init__(self, *args, **kwargs):
        (super(MessagesMixin, self).__init__)(*args, **kwargs)
        self.error_count = 0
        self.warning_count = 0
        self.print_mode = 'console'
        self.buffer = ''

    def print_message(self, text):
        """ Last stage of message printing. """
        if self.print_mode == 'console':
            self.stdout.write(text)
        else:
            if self.print_mode == 'buffer':
                self.buffer = self.buffer + text
            else:
                raise ValueError('Invalid print mode')

    def error(self, message, description=''):
        """Print an error message."""
        self.error_count = self.error_count + 1
        self.print_message(_('ERROR!!! '))
        self.print_message(message)
        self.print_message('\n')
        if len(description):
            if isinstance(description, str):
                description = description.split('\n')
            for ddd in description:
                self.print_message('  ')
                self.print_message(ddd)
                self.print_message('\n')

    def warning(self, message, description=''):
        """Print an warning message."""
        self.warning_count = self.warning_count + 1
        self.print_message(_('Warning! '))
        self.print_message(message)
        self.print_message('\n')
        if len(description):
            if isinstance(description, str):
                description = description.split('\n')
            for ddd in description:
                self.print_message(ddd)
                self.print_message('\n')

    def info(self, message):
        """Print an informative message."""
        self.print_message(message)
        self.print_message('\n')

    def info_start(self, message):
        """The beginning of an informative."""
        self.print_message(message)
        self.print_message('\n')

    def info_line(self, message):
        """An informative line."""
        self.print_message(message)
        self.print_message('\n')

    def info_end(self, message):
        """The end of an informative."""
        self.print_message(message)
        self.print_message('\n')

    def default(self, line):
        """Called on an input line when the command prefix is not recognized.
        """
        self.error('*** Unknown syntax: %s' % line)