# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/saltstack/utils.py
# Compiled at: 2016-09-28 02:05:53
from django.core.mail import send_mail

def sms_user_password(user):
    if not user.phone:
        return
    options = user.tenant.service_project_link.service.settings.options or {}
    sender = options.get('sms_email_from')
    recipient = options.get('sms_email_rcpt')
    if sender and recipient and '{phone}' in recipient:
        send_mail('', 'Your OTP is: %s' % user.password, sender, [
         recipient.format(phone=user.phone)], fail_silently=True)