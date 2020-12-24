# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.1-i386/egg/email/mime/multipart.py
# Compiled at: 2007-04-25 15:29:36
"""Base class for MIME multipart/* type messages."""
__all__ = [
 'MIMEMultipart']
from email.mime.base import MIMEBase

class MIMEMultipart(MIMEBase):
    """Base class for MIME multipart/* type messages."""
    __module__ = __name__

    def __init__(self, _subtype='mixed', boundary=None, _subparts=None, **_params):
        """Creates a multipart/* type message.

        By default, creates a multipart/mixed message, with proper
        Content-Type and MIME-Version headers.

        _subtype is the subtype of the multipart content type, defaulting to
        `mixed'.

        boundary is the multipart boundary string.  By default it is
        calculated as needed.

        _subparts is a sequence of initial subparts for the payload.  It
        must be an iterable object, such as a list.  You can always
        attach new subparts to the message by using the attach() method.

        Additional parameters for the Content-Type header are taken from the
        keyword arguments (or passed into the _params argument).
        """
        MIMEBase.__init__(self, 'multipart', _subtype, **_params)
        if _subparts:
            for p in _subparts:
                self.attach(p)

        if boundary:
            self.set_boundary(boundary)