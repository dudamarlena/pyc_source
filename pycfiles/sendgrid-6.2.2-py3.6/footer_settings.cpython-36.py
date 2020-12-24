# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/footer_settings.py
# Compiled at: 2020-04-15 16:00:33
# Size of source mod 2**32: 2390 bytes


class FooterSettings(object):
    __doc__ = 'The default footer that you would like included on every email.'

    def __init__(self, enable=None, text=None, html=None):
        """Create a default footer.

        :param enable: Whether this footer should be applied.
        :type enable: boolean, optional
        :param text: Text content of this footer
        :type text: FooterText, optional
        :param html: HTML content of this footer
        :type html: FooterHtml, optional
        """
        self._enable = None
        self._text = None
        self._html = None
        if enable is not None:
            self.enable = enable
        if text is not None:
            self.text = text
        if html is not None:
            self.html = html

    @property
    def enable(self):
        """Indicates if this setting is enabled.

        :rtype: boolean
        """
        return self._enable

    @enable.setter
    def enable(self, value):
        """Indicates if this setting is enabled.

        :param value: Indicates if this setting is enabled.
        :type value: boolean
        """
        self._enable = value

    @property
    def text(self):
        """The plain text content of your footer.

        :rtype: string
        """
        return self._text

    @text.setter
    def text(self, value):
        """The plain text content of your footer.

        :param value: The plain text content of your footer.
        :type value: string
        """
        self._text = value

    @property
    def html(self):
        """The HTML content of your footer.

        :rtype: string
        """
        return self._html

    @html.setter
    def html(self, value):
        """The HTML content of your footer.

        :param value: The HTML content of your footer.
        :type value: string
        """
        self._html = value

    def get(self):
        """
        Get a JSON-ready representation of this FooterSettings.

        :returns: This FooterSettings, ready for use in a request body.
        :rtype: dict
        """
        footer_settings = {}
        if self.enable is not None:
            footer_settings['enable'] = self.enable
        if self.text is not None:
            footer_settings['text'] = self.text.get()
        if self.html is not None:
            footer_settings['html'] = self.html.get()
        return footer_settings