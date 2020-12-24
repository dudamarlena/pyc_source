# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/tests/test_emails.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 1174 bytes
from django.test import TestCase
from django.test.utils import override_settings
from django.core import mail
import ovp_core.emails

class TestBaseMail(TestCase):

    def test_email_trigger(self):
        """Assert that email is sent to outbox"""
        bm = ovp_core.emails.BaseMail('a@b.c')
        bm.sendEmail('base', '', {})
        self.assertTrue(len(mail.outbox) > 0)

    def test_async_email_trigger(self):
        """Assert that async emails are sent to outbox"""
        bm = ovp_core.emails.BaseMail('a@b.c', async_mail=True)
        bm.sendEmail('base', '', {}).join()
        self.assertTrue(len(mail.outbox) > 0)

    @override_settings(OVP_EMAILS={'base': {'disabled': True}})
    def test_email_can_be_disabled(self):
        """Assert that email can be disabled"""
        bm = ovp_core.emails.BaseMail('a@b.c')
        bm.sendEmail('base', '', {})
        self.assertTrue(len(mail.outbox) == 0)

    @override_settings(OVP_EMAILS={'base': {'subject': 'overriden'}})
    def test_email_subject_can_be_overridden(self):
        """Assert that email subject can be overridden"""
        bm = ovp_core.emails.BaseMail('a@b.c')
        bm.sendEmail('base', 'test', {})
        self.assertTrue(mail.outbox[0].subject == 'overriden')