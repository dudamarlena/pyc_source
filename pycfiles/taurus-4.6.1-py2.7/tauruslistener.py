# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/tauruslistener.py
# Compiled at: 2019-08-19 15:09:29
"""This module contains the taurus base listeners classes"""
from __future__ import print_function
from builtins import object
from .util.log import Logger
__all__ = [
 'TaurusListener', 'TaurusExceptionListener']
__docformat__ = 'restructuredtext'

class TaurusListener(Logger):
    """ TaurusListener Interface"""

    def __init__(self, name='', parent=None):
        self.call__init__(Logger, name, parent)

    def eventReceived(self, src, type, evt_value):
        """ Method to implement the event notification"""
        pass

    def attributeList(self):
        """ Method to return the attributes of the widget"""
        return []


class TaurusExceptionListener(object):
    """Class for handling ConnectionFailed, DevFailed and TaurusException exceptions."""

    def connectionFailed(self, exception):
        msg = 'Deprecation warning: please note that the "connectionFailed" ' + 'method is deprecated. Scheme-specific exceptions should be ' + 'implemented in each model and be transformed into taurus ' + 'exceptions according Sep3 specifications'
        self.info(msg)
        self._printException(exception)

    def devFailed(self, exception):
        msg = 'Deprecation warning: please note that the "devFailed" ' + 'method is deprecated. Scheme-specific exceptions should be ' + 'implemented in each model and be transformed into taurus ' + 'exception according Sep3 specifications'
        self.info(msg)
        self._printException(exception)

    def exceptionReceived(self, exception):
        self._printException(exception)

    def _printException(self, exception):
        print(self.__class__.__name__, 'received', exception.__class__.__name__, str(exception))