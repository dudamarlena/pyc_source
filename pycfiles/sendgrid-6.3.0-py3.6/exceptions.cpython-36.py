# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/exceptions.py
# Compiled at: 2020-04-29 15:57:11
# Size of source mod 2**32: 1831 bytes


class SendGridException(Exception):
    __doc__ = 'Wrapper/default SendGrid-related exception'


class ApiKeyIncludedException(SendGridException):
    __doc__ = 'Exception raised for when Twilio SendGrid API Key included in message text'

    def __init__(self, expression='Email body', message='Twilio SendGrid API Key detected'):
        """Create an exception for when Twilio SendGrid API Key included in message text

            :param expression: Input expression in which the error occurred
            :type expression: string
            :param message: Explanation of the error
            :type message: string
        """
        self._expression = None
        self._message = None
        if expression is not None:
            self.expression = expression
        if message is not None:
            self.message = message

    @property
    def expression(self):
        """Input expression in which the error occurred

        :rtype: string
        """
        return self._expression

    @expression.setter
    def expression(self, value):
        """Input expression in which the error occurred

        :param value: Input expression in which the error occurred
        :type value: string
        """
        self._expression = value

    @property
    def message(self):
        """Explanation of the error

        :rtype: string
        """
        return self._message

    @message.setter
    def message(self, value):
        """Explanation of the error

        :param value: Explanation of the error
        :type value: string
        """
        self._message = value