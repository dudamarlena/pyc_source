# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.1-i386/egg/email/mime/text.py
# Compiled at: 2007-04-25 15:29:36
"""Class representing text/* type MIME documents."""
__all__ = [
 'MIMEText']
from email.encoders import encode_7or8bit
from email.mime.nonmultipart import MIMENonMultipart

class MIMEText(MIMENonMultipart):
    """Class for generating text/* type MIME documents."""
    __module__ = __name__

    def __init__(self, _text, _subtype='plain', _charset='us-ascii'):
        """Create a text/* type MIME document.

        _text is the string for this message object.

        _subtype is the MIME sub content type, defaulting to "plain".

        _charset is the character set parameter added to the Content-Type
        header.  This defaults to "us-ascii".  Note that as a side-effect, the
        Content-Transfer-Encoding header will also be set.
        """
        MIMENonMultipart.__init__(self, 'text', _subtype, **{'charset': _charset})
        self.set_payload(_text, _charset)