# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/notification/service.py
# Compiled at: 2009-02-23 05:30:01
from types import GeneratorType
import smtplib
from notification import errors

class NotificationService(object):
    swallowSMTPErrors = False
    emailFromAddress = None

    def __init__(self, smtpHost, emailFromAddress=None, swallowSMTPErrors=None):
        self.smtpHost = smtpHost
        if emailFromAddress is not None:
            self.emailFromAddress = emailFromAddress
        if swallowSMTPErrors is not None:
            self.swallowSMTPErrors = swallowSMTPErrors
        return

    def sendEmail(self, toAddresses, msg, fromAddress=None, swallowErrors=None):
        """
        Send an email to one or more recipients.
        """
        if not isinstance(toAddresses, (list, tuple, GeneratorType)):
            toAddresses = [
             toAddresses]
        if swallowErrors is None:
            swallowErrors = self.swallowSMTPErrors
        if fromAddress is None:
            fromAddress = self.emailFromAddress
        try:
            server = smtplib.SMTP(self.smtpHost)
            r = server.sendmail(fromAddress, toAddresses, str(msg))
        except smtplib.SMTPException, e:
            if not swallowErrors:
                raise errors.MailNotificationError(str(e.value))

        return r

    def buildEmailFromTemplate(self, templateName, templateArgs, headers):
        raise NotImplementedError('buildEmailFromTemplate must be implemented by a subclass')