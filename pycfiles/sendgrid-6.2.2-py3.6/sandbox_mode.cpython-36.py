# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/sandbox_mode.py
# Compiled at: 2020-04-15 16:00:33
# Size of source mod 2**32: 1187 bytes


class SandBoxMode(object):
    __doc__ = 'Setting for sandbox mode.\n    This allows you to send a test email to ensure that your request body is\n    valid and formatted correctly.\n    '

    def __init__(self, enable=None):
        """Create an enabled or disabled SandBoxMode.

        :param enable: Whether this is a test request.
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
        Get a JSON-ready representation of this SandBoxMode.

        :returns: This SandBoxMode, ready for use in a request body.
        :rtype: dict
        """
        sandbox_mode = {}
        if self.enable is not None:
            sandbox_mode['enable'] = self.enable
        return sandbox_mode