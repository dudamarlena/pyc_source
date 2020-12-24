# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/logging_system.py
# Compiled at: 2020-04-22 01:04:47
# Size of source mod 2**32: 1895 bytes
__doc__ = " Create a logging system using Python's built-in module. \n\nEach module within pyEQL has its own logger, with a StreamHandler attached to it that\ndirects formatted messages to standard output. This is intended to facilitate the use\nof pyEQL as an interactive console program, at the expense of some flexibility when\nusing it as a true library in another application.\n\nThe default logging levels are mapped to pyEQL events as follows:\n \nDEBUG       -   detailed messages about function execution including methods used, data sources,\n                temperature adjustments, etc.\nINFO        -   Messages indicating calculation steps, function calls, etc.\nWARNING     -   assumptions or limitations of module output\nERROR       -   Module could not complete a task due to invalid input or other problem\nCRITICAL    -   not used\n\n:copyright: 2013-2020 by Ryan S. Kingsbury\n:license: LGPL, see LICENSE for more details.\n\n"
import logging

class Unique(logging.Filter):
    """Unique"""

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