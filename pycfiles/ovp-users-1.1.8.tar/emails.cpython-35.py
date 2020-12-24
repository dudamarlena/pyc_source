# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/emails.py
# Compiled at: 2017-05-15 11:01:22
# Size of source mod 2**32: 776 bytes
from ovp_core.emails import BaseMail

class UserMail(BaseMail):
    __doc__ = '\n  This class is responsible for firing emails for Users\n  '

    def __init__(self, user, async_mail=None):
        super(UserMail, self).__init__(user.email, async_mail, user.locale)

    def sendWelcome(self, context={}):
        """
    Sent when user registers
    """
        return self.sendEmail('welcome', 'Welcome', context)

    def sendRecoveryToken(self, context):
        """
    Sent when volunteer requests recovery token
    """
        return self.sendEmail('recoveryToken', 'Password recovery', context)

    def sendMessageToAnotherVolunteer(self, context):
        """
    Sent when volunteer make contact with another volunteer
    """
        return self.sendEmail('messageToVolunteer', 'Volunteer Message', context)