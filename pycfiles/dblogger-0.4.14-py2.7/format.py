# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dblogger/format.py
# Compiled at: 2015-04-26 18:06:04
"""Formatters for :mod:`logging`.

.. This software is released under an MIT/X11 open source license.
   Copyright 2013-2014 Diffeo, Inc.

"""
import logging, sys

class FixedWidthFormatter(logging.Formatter):
    """Formats log messages in fixed columns.

    This adds format string properties
    ``%(fixed_width_filename_lineno)s`` containing the file name and
    line number in a 17-character-wide field, and
    ``%(fixed_width_levelname`` containing the log level padded out to
    an 8-character-wide field.

    """
    filename_width = 17
    levelname_width = 8

    def format(self, record):
        max_filename_width = self.filename_width - 3 - len(str(record.lineno))
        filename = record.filename
        if len(record.filename) > max_filename_width:
            filename = record.filename[:max_filename_width]
        a = '%s:%s' % (filename, record.lineno)
        record.fixed_width_filename_lineno = a.ljust(self.filename_width)
        levelname = record.levelname
        levelname_padding = ' ' * (self.levelname_width - len(levelname))
        record.fixed_width_levelname = levelname + levelname_padding
        if sys.hexversion > 34013184:
            return super(FixedWidthFormatter, self).format(record)
        else:
            return logging.Formatter.format(self, record)