# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/user_error.py
# Compiled at: 2013-04-04 15:36:36
from muntjac.terminal.error_message import IErrorMessage
from muntjac.terminal.gwt.server.abstract_application_servlet import AbstractApplicationServlet

class UserError(IErrorMessage):
    """C{UserError} is a controlled error occurred in application. User
    errors are occur in normal usage of the application and guide the user.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """
    CONTENT_TEXT = 0
    CONTENT_PREFORMATTED = 1
    CONTENT_UIDL = 2
    CONTENT_XHTML = 3

    def __init__(self, message, contentMode=None, errorLevel=None):
        """Creates a error message with level and content mode.

        @param message:
                   the error message.
        @param contentMode:
                   the content Mode.
        @param errorLevel:
                   the level of error (defaults to Error).
        """
        self._mode = self.CONTENT_TEXT
        self._msg = message
        self._level = IErrorMessage.ERROR
        if contentMode is not None:
            if contentMode < 0 or contentMode > 2:
                raise ValueError, 'Unsupported content mode: ' + contentMode
            self._mode = contentMode
            self._level = errorLevel
        return

    def getErrorLevel(self):
        return self._level

    def addListener(self, listener, iface=None):
        pass

    def addCallback(self, callback, eventType=None, *args):
        pass

    def removeListener(self, listener, iface=None):
        pass

    def removeCallback(self, callback, eventType=None):
        pass

    def requestRepaint(self):
        pass

    def paint(self, target):
        target.startTag('error')
        if self._level >= IErrorMessage.SYSTEMERROR:
            target.addAttribute('level', 'system')
        elif self._level >= IErrorMessage.CRITICAL:
            target.addAttribute('level', 'critical')
        elif self._level >= IErrorMessage.ERROR:
            target.addAttribute('level', 'error')
        elif self._level >= IErrorMessage.WARNING:
            target.addAttribute('level', 'warning')
        else:
            target.addAttribute('level', 'info')
        if self._mode == self.CONTENT_TEXT:
            escaped = AbstractApplicationServlet.safeEscapeForHtml(self._msg)
            target.addText(escaped)
        elif self._mode == self.CONTENT_UIDL:
            target.addUIDL('<pre>' + AbstractApplicationServlet.safeEscapeForHtml(self._msg) + '</pre>')
        elif self._mode == self.CONTENT_PREFORMATTED:
            target.startTag('pre')
            target.addText(self._msg)
            target.endTag('pre')
        target.endTag('error')

    def requestRepaintRequests(self):
        pass

    def __str__(self):
        return self._msg

    def getDebugId(self):
        return

    def setDebugId(self, idd):
        raise NotImplementedError, 'Setting testing id for this Paintable is not implemented'