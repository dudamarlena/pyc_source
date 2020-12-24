# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/ip_pool_name.py
# Compiled at: 2020-04-15 16:00:33
# Size of source mod 2**32: 1159 bytes


class IpPoolName(object):
    __doc__ = 'The IP Pool that you would like to send this email from.'

    def __init__(self, ip_pool_name=None):
        """Create a IpPoolName object

        :param ip_pool_name: The IP Pool that you would like to send this
                             email from.
        :type ip_pool_name: string, optional
        """
        self._ip_pool_name = None
        if ip_pool_name is not None:
            self.ip_pool_name = ip_pool_name

    @property
    def ip_pool_name(self):
        """The IP Pool that you would like to send this email from.

        :rtype: string
        """
        return self._ip_pool_name

    @ip_pool_name.setter
    def ip_pool_name(self, value):
        """The IP Pool that you would like to send this email from.

        :param value: The IP Pool that you would like to send this email from.
        :type value: string
        """
        self._ip_pool_name = value

    def get(self):
        """
        Get a JSON-ready representation of this IpPoolName.

        :returns: This IpPoolName, ready for use in a request body.
        :rtype: string
        """
        return self.ip_pool_name