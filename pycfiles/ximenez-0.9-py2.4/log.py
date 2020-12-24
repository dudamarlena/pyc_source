# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.11.1-i386/egg/ximenez/actions/misc/log.py
# Compiled at: 2007-11-26 12:53:57
"""Define ``Log``, a plug-in which simply logs items of a given
sequence.

$Id: log.py 31 2007-11-26 17:53:56Z damien.baty $
"""
import logging
from ximenez.actions.action import Action

def getInstance():
    """Return an instance of ``Log``."""
    return Log()


class Log(Action):
    """A very simple action, which logs each item returned by the
    collector.
    """
    __module__ = __name__
    _input_info = ()

    def execute(self, sequence):
        """Log each item of ``sequence``."""
        for item in sequence:
            logging.info(str(item))