# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/log/colored_log.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 2937 bytes
"""
Class responsible for colouring logs based on log level.
"""
import sys
from colorlog import TTYColoredFormatter
from termcolor import colored
ARGS = {'attrs': ['bold']}
DEFAULT_COLORS = {'DEBUG':'red', 
 'INFO':'', 
 'WARNING':'yellow', 
 'ERROR':'red', 
 'CRITICAL':'red'}

class CustomTTYColoredFormatter(TTYColoredFormatter):
    __doc__ = '\n    Custom log formatter which extends `colored.TTYColoredFormatter`\n    by adding attributes to message arguments and coloring error\n    traceback.\n    '

    def __init__(self, *args, **kwargs):
        kwargs['stream'] = sys.stdout or kwargs.get('stream')
        kwargs['log_colors'] = DEFAULT_COLORS
        (super(CustomTTYColoredFormatter, self).__init__)(*args, **kwargs)

    @staticmethod
    def _color_arg(arg):
        if isinstance(arg, (int, float)):
            return arg
        else:
            return colored((str(arg)), **ARGS)

    def _color_record_args(self, record):
        if isinstance(record.args, (tuple, list)):
            record.args = tuple(self._color_arg(arg) for arg in record.args)
        else:
            if isinstance(record.args, dict):
                record.args = {key:self._color_arg(value) for key, value in record.args.items()}
            else:
                if isinstance(record.args, str):
                    record.args = self._color_arg(record.args)
        return record

    def _color_record_traceback(self, record):
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
            if record.exc_text:
                record.exc_text = colored(record.exc_text, DEFAULT_COLORS['ERROR'])
        return record

    def format(self, record):
        record = self._color_record_args(record)
        record = self._color_record_traceback(record)
        return super(CustomTTYColoredFormatter, self).format(record)