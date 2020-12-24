# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/future/backports/email/mime/image.py
# Compiled at: 2016-10-27 16:05:38
# Size of source mod 2**32: 1907 bytes
"""Class representing image/* type MIME documents."""
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
__all__ = [
 'MIMEImage']
import imghdr
from future.backports.email import encoders
from future.backports.email.mime.nonmultipart import MIMENonMultipart

class MIMEImage(MIMENonMultipart):
    __doc__ = 'Class for generating image/* type MIME documents.'

    def __init__(self, _imagedata, _subtype=None, _encoder=encoders.encode_base64, **_params):
        """Create an image/* type MIME document.

        _imagedata is a string containing the raw image data.  If this data
        can be decoded by the standard Python `imghdr' module, then the
        subtype will be automatically included in the Content-Type header.
        Otherwise, you can specify the specific image subtype via the _subtype
        parameter.

        _encoder is a function which will perform the actual encoding for
        transport of the image data.  It takes one argument, which is this
        Image instance.  It should use get_payload() and set_payload() to
        change the payload to the encoded form.  It should also add any
        Content-Transfer-Encoding or other headers to the message as
        necessary.  The default encoding is Base64.

        Any additional keyword arguments are passed to the base class
        constructor, which turns them into parameters on the Content-Type
        header.
        """
        if _subtype is None:
            _subtype = imghdr.what(None, _imagedata)
        if _subtype is None:
            raise TypeError('Could not guess image MIME subtype')
        MIMENonMultipart.__init__(self, 'image', _subtype, **_params)
        self.set_payload(_imagedata)
        _encoder(self)