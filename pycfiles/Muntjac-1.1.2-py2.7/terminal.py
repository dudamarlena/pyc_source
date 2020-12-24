# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/terminal.py
# Compiled at: 2013-04-04 15:36:36
"""Defines an interface that provides information about the user's terminal.
"""

class ITerminal(object):
    """An interface that provides information about the user's terminal.
    Implementors typically provide additional information using methods
    not in this interface.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def getDefaultTheme(self):
        """Gets the name of the default theme for this terminal.

        @return: the name of the theme that is used by default by this
                terminal.
        """
        raise NotImplementedError

    def getScreenWidth(self):
        """Gets the width of the terminal screen in pixels. This is the
        width of the screen and not the width available for the application.

        Note that the screen width is typically not available in the
        L{Application.init} method as this is called before the browser has
        a chance to report the screen size to the server.

        @return: the width of the terminal screen.
        """
        raise NotImplementedError

    def getScreenHeight(self):
        """Gets the height of the terminal screen in pixels. This is the
        height of the screen and not the height available for the application.

        Note that the screen height is typically not available in the
        L{Application.init} method as this is called before the browser has
        a chance to report the screen size to the server.

        @return: the height of the terminal screen.
        """
        raise NotImplementedError


class IErrorEvent(object):
    """An error event implementation for ITerminal."""

    def getThrowable(self):
        """Gets the contained throwable, the cause of the error."""
        pass


class IErrorListener(object):
    """Interface for listening to ITerminal errors."""

    def terminalError(self, event):
        """Invoked when a terminal error occurs.

        @param event:
                   the fired event.
        """
        pass