# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/subscription_text.py
# Compiled at: 2020-04-15 16:00:33
# Size of source mod 2**32: 1617 bytes


class SubscriptionText(object):
    __doc__ = 'The text of an SubscriptionTracking.'

    def __init__(self, subscription_text=None):
        """Create a SubscriptionText object

        :param subscription_text: Text to be appended to the email, with the
                                  subscription tracking link. You may control
                                  where the link is by using the tag <% %>
        :type subscription_text: string, optional
        """
        self._subscription_text = None
        if subscription_text is not None:
            self.subscription_text = subscription_text

    @property
    def subscription_text(self):
        """Text to be appended to the email, with the subscription tracking link.
           You may control where the link is by using the tag <% %>

        :rtype: string
        """
        return self._subscription_text

    @subscription_text.setter
    def subscription_text(self, value):
        """Text to be appended to the email, with the subscription tracking link.
           You may control where the link is by using the tag <% %>

        :param value: Text to be appended to the email, with the subscription
                      tracking link. You may control where the link is by using
                      the tag <% %>
        :type value: string
        """
        self._subscription_text = value

    def get(self):
        """
        Get a JSON-ready representation of this SubscriptionText.

        :returns: This SubscriptionText, ready for use in a request body.
        :rtype: string
        """
        return self.subscription_text