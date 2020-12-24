# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/utm_medium.py
# Compiled at: 2020-04-29 15:57:11
# Size of source mod 2**32: 1028 bytes


class UtmMedium(object):
    __doc__ = 'The utm medium of an Ganalytics object.'

    def __init__(self, utm_medium=None):
        """Create a UtmMedium object

        :param utm_medium: Name of the marketing medium. (e.g. Email)

        :type utm_medium: string, optional
        """
        self._utm_medium = None
        if utm_medium is not None:
            self.utm_medium = utm_medium

    @property
    def utm_medium(self):
        """Name of the marketing medium. (e.g. Email)

        :rtype: string
        """
        return self._utm_medium

    @utm_medium.setter
    def utm_medium(self, value):
        """Name of the marketing medium. (e.g. Email)

        :param value: Name of the marketing medium. (e.g. Email)
        :type value: string
        """
        self._utm_medium = value

    def get(self):
        """
        Get a JSON-ready representation of this UtmMedium.

        :returns: This UtmMedium, ready for use in a request body.
        :rtype: string
        """
        return self.utm_medium