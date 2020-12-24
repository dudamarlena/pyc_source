# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.1-i386/egg/email/errors.py
# Compiled at: 2007-04-25 15:29:36
"""email package exception classes."""

class MessageError(Exception):
    """Base class for errors in the email package."""
    __module__ = __name__


class MessageParseError(MessageError):
    """Base class for message parsing errors."""
    __module__ = __name__


class HeaderParseError(MessageParseError):
    """Error while parsing headers."""
    __module__ = __name__


class BoundaryError(MessageParseError):
    """Couldn't find terminating boundary."""
    __module__ = __name__


class MultipartConversionError(MessageError, TypeError):
    """Conversion to a multipart is prohibited."""
    __module__ = __name__


class CharsetError(MessageError):
    """An illegal charset was given."""
    __module__ = __name__


class MessageDefect:
    """Base class for a message defect."""
    __module__ = __name__

    def __init__(self, line=None):
        self.line = line


class NoBoundaryInMultipartDefect(MessageDefect):
    """A message claimed to be a multipart but had no boundary parameter."""
    __module__ = __name__


class StartBoundaryNotFoundDefect(MessageDefect):
    """The claimed start boundary was never found."""
    __module__ = __name__


class FirstHeaderLineIsContinuationDefect(MessageDefect):
    """A message had a continuation line as its first header line."""
    __module__ = __name__


class MisplacedEnvelopeHeaderDefect(MessageDefect):
    """A 'Unix-from' header was found in the middle of a header block."""
    __module__ = __name__


class MalformedHeaderDefect(MessageDefect):
    """Found a header that was missing a colon, or was otherwise malformed."""
    __module__ = __name__


class MultipartInvariantViolationDefect(MessageDefect):
    """A message claimed to be a multipart but no subparts were found."""
    __module__ = __name__