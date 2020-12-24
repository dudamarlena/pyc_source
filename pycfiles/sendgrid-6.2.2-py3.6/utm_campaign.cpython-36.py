# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/utm_campaign.py
# Compiled at: 2020-04-15 16:00:33
# Size of source mod 2**32: 992 bytes


class UtmCampaign(object):
    __doc__ = 'The utm campaign of an Ganalytics object.'

    def __init__(self, utm_campaign=None):
        """Create a UtmCampaign object

        :param utm_campaign: The name of the campaign

        :type utm_campaign: string, optional
        """
        self._utm_campaign = None
        if utm_campaign is not None:
            self.utm_campaign = utm_campaign

    @property
    def utm_campaign(self):
        """The name of the campaign

        :rtype: string
        """
        return self._utm_campaign

    @utm_campaign.setter
    def utm_campaign(self, value):
        """The name of the campaign

        :param value: The name of the campaign
        :type value: string
        """
        self._utm_campaign = value

    def get(self):
        """
        Get a JSON-ready representation of this UtmCampaign.

        :returns: This UtmCampaign, ready for use in a request body.
        :rtype: string
        """
        return self.utm_campaign