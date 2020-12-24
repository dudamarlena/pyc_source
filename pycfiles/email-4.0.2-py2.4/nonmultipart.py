# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.1-i386/egg/email/mime/nonmultipart.py
# Compiled at: 2007-04-25 15:29:36
"""Base class for MIME type messages that are not multipart."""
__all__ = [
 'MIMENonMultipart']
from email import errors
from email.mime.base import MIMEBase

class MIMENonMultipart(MIMEBase):
    """Base class for MIME multipart/* type messages."""
    __module__ = __name__
    __pychecker__ = 'unusednames=payload'

    def attach(self, payload):
        raise errors.MultipartConversionError('Cannot attach additional subparts to non-multipart/*')

    del __pychecker__