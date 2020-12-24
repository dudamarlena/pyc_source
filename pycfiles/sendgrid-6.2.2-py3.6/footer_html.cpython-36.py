# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/footer_html.py
# Compiled at: 2020-04-15 16:00:33
# Size of source mod 2**32: 982 bytes


class FooterHtml(object):
    __doc__ = 'The HTML in a Footer.'

    def __init__(self, footer_html=None):
        """Create a FooterHtml object

        :param footer_html: The html content of your footer.
        :type footer_html: string, optional
        """
        self._footer_html = None
        if footer_html is not None:
            self.footer_html = footer_html

    @property
    def footer_html(self):
        """The html content of your footer.

        :rtype: string
        """
        return self._footer_html

    @footer_html.setter
    def footer_html(self, html):
        """The html content of your footer.

        :param html: The html content of your footer.
        :type html: string
        """
        self._footer_html = html

    def get(self):
        """
        Get a JSON-ready representation of this FooterHtml.

        :returns: This FooterHtml, ready for use in a request body.
        :rtype: string
        """
        return self.footer_html