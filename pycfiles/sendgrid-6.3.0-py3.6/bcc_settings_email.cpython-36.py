# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/bcc_settings_email.py
# Compiled at: 2020-04-29 15:57:11
# Size of source mod 2**32: 1249 bytes


class BccSettingsEmail(object):
    __doc__ = 'The BccSettingsEmail of an Attachment.'

    def __init__(self, bcc_settings_email=None):
        """Create a BccSettingsEmail object

        :param bcc_settings_email: The email address that you would like to
                                   receive the BCC
        :type bcc_settings_email: string, optional
        """
        self._bcc_settings_email = None
        if bcc_settings_email is not None:
            self.bcc_settings_email = bcc_settings_email

    @property
    def bcc_settings_email(self):
        """The email address that you would like to receive the BCC

        :rtype: string
        """
        return self._bcc_settings_email

    @bcc_settings_email.setter
    def bcc_settings_email(self, value):
        """The email address that you would like to receive the BCC

        :param value: The email address that you would like to receive the BCC
        :type value: string
        """
        self._bcc_settings_email = value

    def get(self):
        """
        Get a JSON-ready representation of this BccSettingsEmail.

        :returns: This BccSettingsEmail, ready for use in a request body.
        :rtype: string
        """
        return self.bcc_settings_email