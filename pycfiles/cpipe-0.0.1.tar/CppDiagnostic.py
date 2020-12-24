# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/core/CppDiagnostic.py
# Compiled at: 2017-10-03 13:07:16
__doc__ = 'Describes how a preprocessor class behaves under abnormal conditions.'
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import logging
from cpip import ExceptionCpip

class ExceptionCppDiagnostic(ExceptionCpip):
    """Exception class for representing CppDiagnostic."""


class ExceptionCppDiagnosticUndefined(ExceptionCppDiagnostic):
    """Exception class for representing undefined behaviour."""


class ExceptionCppDiagnosticPartialTokenStream(ExceptionCppDiagnostic):
    """Exception class for representing partial remaining tokens."""


class PreprocessDiagnosticStd(object):
    """Describes how a preprocessor class behaves under abnormal conditions."""

    def __init__(self):
        """Constructor."""
        self._cntrUndefined = 0
        self._cntrImplDefined = 0
        self._cntrError = 0
        self._cntrWarning = 0
        self._cntrUnspecified = 0
        self._cntrPartialTokenStream = 0
        self._isWellFormed = True
        self._eventList = []

    def clear(self):
        self._eventList = []

    @property
    def isWellFormed(self):
        return self._isWellFormed

    @property
    def eventList(self):
        """A list of events in the order that they appear.
        An event is a pair of strings: ``(type, message)``"""
        return self._eventList

    def _prepareMsg(self, event, msg, theLoc):
        """Prepares a message.
        
        *event*
            The event e.g. 'error', if None it is not accumulated
        
        *msg*
            The main message, a string.
        
        *theLoc*
            The file locator e.g. :py:class:`FileLocation.FileLineCol`.
            If present it must have: ``(fileId, lineNum colNum)`` attributes."""
        if theLoc is None:
            myMsg = msg
        else:
            myMsg = '%s at line=%s, col=%s of file "%s"' % (
             msg.rstrip(),
             theLoc.lineNum,
             theLoc.colNum,
             theLoc.fileId)
        if event is not None:
            self._eventList.append((event, myMsg))
        return myMsg

    def undefined(self, msg, theLoc=None):
        """Reports when an *undefined* event happens.
        
        *msg*
            The main message, a string.
        
        *theLoc*
            The file locator e.g. :py:class:`FileLocation.FileLineCol`.
            If present it must have: ``(fileId, lineNum colNum)`` attributes."""
        self._cntrUndefined += 1
        self._isWellFormed = False
        raise ExceptionCppDiagnosticUndefined(self._prepareMsg('undefined', msg, theLoc))

    def partialTokenStream(self, msg, theLoc=None):
        """Reports when an partial token stream exists (e.g. an unclosed comment).
        
        *msg*
            The main message, a string.
        
        *theLoc*
            The file locator e.g. :py:class:`FileLocation.FileLineCol`.
            If present it must have: ``(fileId, lineNum colNum)`` attributes."""
        self._cntrPartialTokenStream += 1
        self._isWellFormed = False
        raise ExceptionCppDiagnosticPartialTokenStream(self._prepareMsg('partial token stream', msg, theLoc))

    def implementationDefined(self, msg, theLoc=None):
        """Reports when an *implementation defined* event happens.
        
        *msg*
            The main message, a string.
        
        *theLoc*
            The file locator e.g. :py:class:`FileLocation.FileLineCol`.
            If present it must have: ``(fileId, lineNum colNum)`` attributes."""
        self._cntrImplDefined += 1
        logging.warning(self._prepareMsg('implementation defined', msg, theLoc))

    def error(self, msg, theLoc=None):
        """Reports when an error event happens.
        
        *msg*
            The main message, a string.
        
        *theLoc*
            The file locator e.g. :py:class:`FileLocation.FileLineCol`.
            If present it must have: ``(fileId, lineNum colNum)`` attributes."""
        self._cntrError += 1
        logging.error(self._prepareMsg('error', msg, theLoc))

    def warning(self, msg, theLoc=None):
        """Reports when an warning event happens.
        
        *msg*
            The main message, a string.
        
        *theLoc*
            The file locator e.g. :py:class:`FileLocation.FileLineCol`.
            If present it must have: ``(fileId, lineNum colNum)`` attributes."""
        self._cntrWarning += 1
        logging.warning(self._prepareMsg('warning', msg, theLoc))

    def handleUnclosedComment(self, msg, theLoc=None):
        """Reports when an unclosed comment is seen at EOF.
        
        *msg*
            The main message, a string.
        
        *theLoc*
            The file locator e.g. :py:class:`FileLocation.FileLineCol`.
            If present it must have: ``(fileId, lineNum colNum)`` attributes."""
        self.partialTokenStream(msg, theLoc)

    def unspecified(self, msg, theLoc=None):
        """Reports when unspecified behaviour is happening.
        For example order of evaluation of ``'#'`` and ``'##'``.
        
        *msg*
            The main message, a string.
        
        *theLoc*
            The file locator e.g. :py:class:`FileLocation.FileLineCol`.
            If present it must have: ``(fileId, lineNum colNum)`` attributes."""
        self._cntrUnspecified += 1
        logging.info(self._prepareMsg('unspecified', msg, theLoc))

    @property
    def isDebug(self):
        """Whether a call to debug() will result in any log output."""
        return logging.getLogger().getEffectiveLevel() <= logging.DEBUG

    def debug(self, msg, theLoc=None):
        """Reports a debug message.
        
        *msg*
            The main message, a string.
        
        *theLoc*
            The file locator e.g. :py:class:`FileLocation.FileLineCol`.
            If present it must have: ``(fileId, lineNum colNum)`` attributes."""
        logging.debug(self._prepareMsg(None, msg, theLoc))
        return


class PreprocessDiagnosticKeepGoing(PreprocessDiagnosticStd):
    """Sub-class that does not raise exceptions."""

    def undefined(self, msg, theLoc=None):
        """Reports when an *undefined* event happens.
        
        *msg*
            The main message, a string.
        
        *theLoc*
            The file locator e.g. :py:class:`FileLocation.FileLineCol`.
            If present it must have: ``(fileId, lineNum colNum)`` attributes."""
        try:
            super(PreprocessDiagnosticKeepGoing, self).undefined(msg, theLoc)
        except ExceptionCppDiagnostic as err:
            self.warning('Undefined behaviour: %s' % str(err), theLoc)

    def partialTokenStream(self, msg, theLoc=None):
        """Reports when an partial token stream exists (e.g. an unclosed comment).
        
        *msg*
            The main message, a string.
        
        *theLoc*
            The file locator e.g. :py:class:`FileLocation.FileLineCol`.
            If present it must have: ``(fileId, lineNum colNum)`` attributes."""
        try:
            super(PreprocessDiagnosticKeepGoing, self).partialTokenStream(msg, theLoc)
        except ExceptionCppDiagnostic as err:
            self.warning('Undefined behaviour: %s' % str(err), theLoc)


class PreprocessDiagnosticRaiseOnError(PreprocessDiagnosticStd):
    """Sub-class that raises an exception on a ``#error`` directive."""

    def error(self, msg, theLoc=None):
        """Reports when an error event happens.

        *msg*
            The main message, a string.
        
        *theLoc*
            The file locator e.g. :py:class:`FileLocation.FileLineCol`.
            If present it must have: ``(fileId, lineNum colNum)`` attributes."""
        try:
            super(PreprocessDiagnosticRaiseOnError, self).error(msg, theLoc)
        except ExceptionCppDiagnostic:
            pass

        raise ExceptionCppDiagnostic(self._prepareMsg('error', msg, theLoc))