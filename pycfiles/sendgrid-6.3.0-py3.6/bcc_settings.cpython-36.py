# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/bcc_settings.py
# Compiled at: 2020-04-29 15:57:11
# Size of source mod 2**32: 1929 bytes


class BccSettings(object):
    __doc__ = 'Settings object for automatic BCC.\n\n    This allows you to have a blind carbon copy automatically sent to the\n    specified email address for every email that is sent.\n    '

    def __init__(self, enable=None, email=None):
        """Create a BCCSettings.

        :param enable: Whether this BCCSettings is applied to sent emails.
        :type enable: boolean, optional
        :param email: Who should be BCCed.
        :type email: BccSettingEmail, optional
        """
        self._enable = None
        self._email = None
        if enable is not None:
            self.enable = enable
        if email is not None:
            self.email = email

    @property
    def enable(self):
        """Indicates if this setting is enabled.

        :rtype: boolean
        """
        return self._enable

    @enable.setter
    def enable(self, value):
        """Indicates if this setting is enabled.

        :type param: Indicates if this setting is enabled.
        :type value: boolean
        """
        self._enable = value

    @property
    def email(self):
        """The email address that you would like to receive the BCC.

        :rtype: string
        """
        return self._email

    @email.setter
    def email(self, value):
        """The email address that you would like to receive the BCC.

        :param value: The email address that you would like to receive the BCC.
        :type value: string
        """
        self._email = value

    def get(self):
        """
        Get a JSON-ready representation of this BCCSettings.

        :returns: This BCCSettings, ready for use in a request body.
        :rtype: dict
        """
        bcc_settings = {}
        if self.enable is not None:
            bcc_settings['enable'] = self.enable
        if self.email is not None:
            bcc_settings['email'] = self.email.get()
        return bcc_settings