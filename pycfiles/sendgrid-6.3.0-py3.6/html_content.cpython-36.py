# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/html_content.py
# Compiled at: 2020-04-29 15:57:11
# Size of source mod 2**32: 1434 bytes
from .content import Content
from .validators import ValidateApiKey

class HtmlContent(Content):
    __doc__ = 'HTML content to be included in your email.'

    def __init__(self, content):
        """Create an HtmlContent with the specified MIME type and content.

        :param content: The HTML content.
        :type content: string
        """
        self._content = None
        self._validator = ValidateApiKey()
        if content is not None:
            self.content = content

    @property
    def mime_type(self):
        """The MIME type for HTML content.

        :rtype: string
        """
        return 'text/html'

    @property
    def content(self):
        """The actual HTML content.

        :rtype: string
        """
        return self._content

    @content.setter
    def content(self, value):
        """The actual HTML content.

        :param value: The actual HTML content.
        :type value: string
        """
        self._validator.validate_message_dict(value)
        self._content = value

    def get(self):
        """
        Get a JSON-ready representation of this HtmlContent.

        :returns: This HtmlContent, ready for use in a request body.
        :rtype: dict
        """
        content = {}
        if self.mime_type is not None:
            content['type'] = self.mime_type
        if self.content is not None:
            content['value'] = self.content
        return content