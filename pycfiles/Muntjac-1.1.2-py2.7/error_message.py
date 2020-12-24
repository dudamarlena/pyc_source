# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/error_message.py
# Compiled at: 2013-04-04 15:36:36
"""Interface for rendering error messages to terminal."""
from muntjac.terminal.paintable import IPaintable

class IErrorMessage(IPaintable):
    """Interface for rendering error messages to terminal. All the
    visible errors shown to user must implement this interface.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """
    SYSTEMERROR = 5000
    CRITICAL = 4000
    ERROR = 3000
    WARNING = 2000
    INFORMATION = 1000

    def getErrorLevel(self):
        """Gets the errors level.

        @return: the level of error as an integer.
        """
        raise NotImplementedError

    def addListener(self, listener, iface=None):
        """Error messages are unmodifiable and thus listeners are not needed.
        This method should be implemented as empty.

        @param listener:
                   the listener to be added.
        @see: L{IPaintable.addListener}
        """
        raise NotImplementedError

    def addCallback(self, callback, eventType=None, *args):
        raise NotImplementedError

    def removeListener(self, listener, iface=None):
        """Error messages are inmodifiable and thus listeners are not needed.
        This method should be implemented as empty.

        @param listener:
                   the listener to be removed.
        @see: L{IPaintable.removeListener}
        """
        raise NotImplementedError

    def removeCallback(self, callback, eventType=None):
        raise NotImplementedError

    def requestRepaint(self):
        """Error messages are inmodifiable and thus listeners are not needed.
        This method should be implemented as empty.

        @see: L{IPaintable.requestRepaint}
        """
        raise NotImplementedError