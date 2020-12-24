# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/HaufeWingDBG/ZopeLogFile.py
# Compiled at: 2012-12-06 03:42:07
"""File-like object which writes to Zope eventlog facility

All written information is collected until a newline is written after which the
collected line will be sent to the logging module.

"""
import logging

class ZopeLogFile:
    """File-like object that sends all data written to it to the Zope eventlog
    (which Zope will have handlers configured for).
    
    Data is collected and logged as summary lines whenever a newline is 
    encountered. On creation, set the subsystem under which the lines should be 
    logged. By default the INFO severity is used, unless a different severity
    is specified on creation of the class.
    
    """
    severity = logging.INFO
    subsystem = ''
    _data = ''

    def __init__(self, subsystem, severity=logging.INFO):
        self.subsystem = subsystem
        self.severity = severity

    def write(self, text):
        self._data += text
        while '\n' in self._data:
            line, self._data = self._data.split('\n', 1)
            logger = logging.getLogger(self.subsystem)
            logger.log(self.severity, line)