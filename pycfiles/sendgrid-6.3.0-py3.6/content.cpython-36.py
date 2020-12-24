# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/content.py
# Compiled at: 2020-04-29 15:57:11
# Size of source mod 2**32: 2250 bytes
from .validators import ValidateApiKey

class Content(object):
    __doc__ = 'Content to be included in your email.\n\n    You must specify at least one mime type in the Contents of your email.\n    '

    def __init__(self, mime_type, content):
        """Create a Content with the specified MIME type and content.

        :param mime_type: MIME type of this Content (e.g. "text/plain").
        :type mime_type: string
        :param content: The actual content.
        :type content: string
        """
        self._mime_type = None
        self._content = None
        self._validator = ValidateApiKey()
        if mime_type is not None:
            self.mime_type = mime_type
        if content is not None:
            self.content = content

    @property
    def mime_type(self):
        """The MIME type of the content you are including in your email.
        For example, "text/plain" or "text/html".

        :rtype: string
        """
        return self._mime_type

    @mime_type.setter
    def mime_type(self, value):
        """The MIME type of the content you are including in your email.
        For example, "text/plain" or "text/html".

        :param value: The MIME type of the content you are including in your
                      email.
        For example, "text/plain" or "text/html".
        :type value: string
        """
        self._mime_type = value

    @property
    def content(self):
        """The actual content (of the specified mime type).

        :rtype: string
        """
        return self._content

    @content.setter
    def content(self, value):
        """The actual content (of the specified mime type).

        :param value: The actual content (of the specified mime type).
        :type value: string
        """
        self._validator.validate_message_dict(value)
        self._content = value

    def get(self):
        """
        Get a JSON-ready representation of this Content.

        :returns: This Content, ready for use in a request body.
        :rtype: dict
        """
        content = {}
        if self.mime_type is not None:
            content['type'] = self.mime_type
        if self.content is not None:
            content['value'] = self.content
        return content