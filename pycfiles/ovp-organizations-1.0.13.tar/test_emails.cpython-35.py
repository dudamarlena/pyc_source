# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-organizations/ovp_organizations/tests/test_emails.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 1551 bytes
from django.test import TestCase
from django.core import mail
from ovp_core.helpers import get_email_subject, is_email_enabled
from ovp_users.models import User
from ovp_organizations.models import Organization

class TestEmailTriggers(TestCase):

    def setUp(self):
        user = User.objects.create_user(email='test_project@project.com', password='test_project')
        user.save()
        mail.outbox = []
        organization = Organization(name='test organization', type=0, owner=user)
        organization.save()
        self.organization = organization

    def test_organization_creation_trigger_email(self):
        """Assert that email is triggered when creating an organization"""
        if is_email_enabled('organizationCreated'):
            self.assertTrue(len(mail.outbox) == 1)
            self.assertTrue(mail.outbox[0].subject == get_email_subject('organizationCreated', 'Your organization was created'))
        else:
            self.assertTrue(len(mail.outbox) == 0)

    def test_organization_publishing_trigger_email(self):
        """Assert that email is triggered when publishing an organization"""
        mail.outbox = []
        self.organization.published = True
        self.organization.save()
        if is_email_enabled('organizationPublished'):
            self.assertTrue(len(mail.outbox) == 1)
            self.assertTrue(mail.outbox[0].subject == get_email_subject('organizationPublished', 'Your organization was published'))
        else:
            self.assertTrue(len(mail.outbox) == 0)