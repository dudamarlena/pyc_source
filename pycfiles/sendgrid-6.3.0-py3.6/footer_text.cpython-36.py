# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/footer_text.py
# Compiled at: 2020-04-29 15:57:11
# Size of source mod 2**32: 1011 bytes


class FooterText(object):
    __doc__ = 'The text in an Footer.'

    def __init__(self, footer_text=None):
        """Create a FooterText object

        :param footer_text: The plain text content of your footer.
        :type footer_text: string, optional
        """
        self._footer_text = None
        if footer_text is not None:
            self.footer_text = footer_text

    @property
    def footer_text(self):
        """The plain text content of your footer.

        :rtype: string
        """
        return self._footer_text

    @footer_text.setter
    def footer_text(self, value):
        """The plain text content of your footer.

        :param value: The plain text content of your footer.
        :type value: string
        """
        self._footer_text = value

    def get(self):
        """
        Get a JSON-ready representation of this FooterText.

        :returns: This FooterText, ready for use in a request body.
        :rtype: string
        """
        return self.footer_text