# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/logging_system.py
# Compiled at: 2020-04-22 01:04:47
# Size of source mod 2**32: 1895 bytes
""" Create a logging system using Python's built-in module. 

Each module within pyEQL has its own logger, with a StreamHandler attached to it that
directs formatted messages to standard output. This is intended to facilitate the use
of pyEQL as an interactive console program, at the expense of some flexibility when
using it as a true library in another application.

The default logging levels are mapped to pyEQL events as follows:
 
DEBUG       -   detailed messages about function execution including methods used, data sources,
                temperature adjustments, etc.
INFO        -   Messages indicating calculation steps, function calls, etc.
WARNING     -   assumptions or limitations of module output
ERROR       -   Module could not complete a task due to invalid input or other problem
CRITICAL    -   not used

:copyright: 2013-2020 by Ryan S. Kingsbury
:license: LGPL, see LICENSE for more details.

"""
import logging

class Unique(logging.Filter):
    __doc__ = "Messages are allowed through just once.\n    The 'message' includes substitutions, but is not formatted by the \n    handler. If it were, then practically all messages would be unique!\n    "

    def __init__(self, name=''):
        logging.Filter.__init__(self, name)
        self.reset()

    def reset(self):
        """Act as if nothing has happened."""
        self._Unique__logged = {}

    def filter(self, rec):
        """logging.Filter.filter performs an extra filter on the name."""
        return logging.Filter.filter(self, rec) and self._Unique__is_first_time(rec)

    def __is_first_time(self, rec):
        """Emit a message only once."""
        msg = rec.msg % rec.args
        if msg in self._Unique__logged:
            self._Unique__logged[msg] += 1
            return False
        self._Unique__logged[msg] = 1
        return True