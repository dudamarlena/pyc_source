# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/bypass_list_management.py
# Compiled at: 2020-04-29 15:57:11
# Size of source mod 2**32: 1401 bytes


class BypassListManagement(object):
    __doc__ = 'Setting for Bypass List Management\n\n    Allows you to bypass all unsubscribe groups and suppressions to ensure that\n    the email is delivered to every single recipient. This should only be used\n    in emergencies when it is absolutely necessary that every recipient\n    receives your email.\n    '

    def __init__(self, enable=None):
        """Create a BypassListManagement.

        :param enable: Whether emails should bypass list management.
        :type enable: boolean, optional
        """
        self._enable = None
        if enable is not None:
            self.enable = enable

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

    def get(self):
        """
        Get a JSON-ready representation of this BypassListManagement.

        :returns: This BypassListManagement, ready for use in a request body.
        :rtype: dict
        """
        bypass_list_management = {}
        if self.enable is not None:
            bypass_list_management['enable'] = self.enable
        return bypass_list_management