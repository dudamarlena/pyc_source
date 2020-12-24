# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/future/backports/email/mime/nonmultipart.py
# Compiled at: 2016-10-27 16:05:38
# Size of source mod 2**32: 832 bytes
"""Base class for MIME type messages that are not multipart."""
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
__all__ = [
 'MIMENonMultipart']
from future.backports.email import errors
from future.backports.email.mime.base import MIMEBase

class MIMENonMultipart(MIMEBase):
    __doc__ = 'Base class for MIME multipart/* type messages.'

    def attach(self, payload):
        raise errors.MultipartConversionError('Cannot attach additional subparts to non-multipart/*')