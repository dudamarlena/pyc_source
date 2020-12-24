# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/future/backports/email/mime/application.py
# Compiled at: 2016-10-27 16:05:38
# Size of source mod 2**32: 1401 bytes
"""Class representing application/* type MIME documents."""
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future.backports.email import encoders
from future.backports.email.mime.nonmultipart import MIMENonMultipart
__all__ = [
 'MIMEApplication']

class MIMEApplication(MIMENonMultipart):
    __doc__ = 'Class for generating application/* MIME documents.'

    def __init__(self, _data, _subtype='octet-stream', _encoder=encoders.encode_base64, **_params):
        """Create an application/* type MIME document.

        _data is a string containing the raw application data.

        _subtype is the MIME content type subtype, defaulting to
        'octet-stream'.

        _encoder is a function which will perform the actual encoding for
        transport of the application data, defaulting to base64 encoding.

        Any additional keyword arguments are passed to the base class
        constructor, which turns them into parameters on the Content-Type
        header.
        """
        if _subtype is None:
            raise TypeError('Invalid application MIME subtype')
        MIMENonMultipart.__init__(self, 'application', _subtype, **_params)
        self.set_payload(_data)
        _encoder(self)