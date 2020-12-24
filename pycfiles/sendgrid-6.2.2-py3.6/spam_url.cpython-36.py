# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/spam_url.py
# Compiled at: 2020-04-15 16:00:33
# Size of source mod 2**32: 1377 bytes


class SpamUrl(object):
    __doc__ = 'An Inbound Parse URL that you would like a copy of your email\n       along with the spam report to be sent to.'

    def __init__(self, spam_url=None):
        """Create a SpamUrl object

        :param spam_url: An Inbound Parse URL that you would like a copy of
                         your email along with the spam report to be sent to.
        :type spam_url: string, optional
        """
        self._spam_url = None
        if spam_url is not None:
            self.spam_url = spam_url

    @property
    def spam_url(self):
        """An Inbound Parse URL that you would like a copy of your email
           along with the spam report to be sent to.

        :rtype: string
        """
        return self._spam_url

    @spam_url.setter
    def spam_url(self, value):
        """An Inbound Parse URL that you would like a copy of your email
           along with the spam report to be sent to.

        :param value: An Inbound Parse URL that you would like a copy of your
                      email along with the spam report to be sent to.
        :type value: string
        """
        self._spam_url = value

    def get(self):
        """
        Get a JSON-ready representation of this SpamUrl.

        :returns: This SpamUrl, ready for use in a request body.
        :rtype: string
        """
        return self.spam_url