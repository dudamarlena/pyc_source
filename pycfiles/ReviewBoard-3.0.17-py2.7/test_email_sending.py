# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/notifications/tests/test_email_sending.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import logging
from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import clear_url_caches, reverse
from django.test.utils import override_settings
from django.utils import six
from django.utils.datastructures import MultiValueDict
from django.utils.six.moves import range
from djblets.mail.testing import DmarcDnsTestsMixin
from djblets.mail.utils import build_email_address, build_email_address_for_user
from djblets.siteconfig.models import SiteConfiguration
from djblets.testing.decorators import add_fixtures
from kgb import SpyAgency
from reviewboard.accounts.models import ReviewRequestVisit
from reviewboard.admin.server import build_server_url, get_server_url
from reviewboard.admin.siteconfig import load_site_config, settings_map
from reviewboard.diffviewer.models import FileDiff
from reviewboard.notifications.email.message import prepare_base_review_request_mail
from reviewboard.notifications.email.utils import get_email_addresses_for_group, send_email
from reviewboard.reviews.models import Group, Review, ReviewRequest, ReviewRequestDraft
from reviewboard.scmtools.core import PRE_CREATION
from reviewboard.site.models import LocalSite
from reviewboard.testing import TestCase
from reviewboard.webapi.models import WebAPIToken
_CONSOLE_EMAIL_BACKEND = b'django.core.mail.backends.console.EmailBackend'
urlpatterns = [
 url(b'^site-root/', include(b'reviewboard.urls'))]

class SiteRootURLTestsMixin(object):
    """A mixin for TestCases that helps test URLs generated with site roots.

    This mixin provides some settings for unit tests to help ensure that URLs
    generated in e-mails are done so correctly and to test that the site root
    is only present in those e-mails once.

    .. seealso:: `Bug 4612`_

    .. _Bug 4612: https://reviews.reviewboard.org/r/9448/bugs/4612/
    """
    CUSTOM_SITE_ROOT = b'/site-root/'
    BAD_SITE_ROOT = b'/site-root//site-root/'
    CUSTOM_SITE_ROOT_SETTINGS = {b'SITE_ROOT': b'/site-root/', 
       b'ROOT_URLCONF': b'reviewboard.notifications.tests.test_email_sending'}

    @classmethod
    def setUpClass(cls):
        super(SiteRootURLTestsMixin, cls).setUpClass()
        clear_url_caches()

    def tearDown(self):
        super(SiteRootURLTestsMixin, self).tearDown()
        clear_url_caches()


class EmailTestHelper(object):
    email_siteconfig_settings = {}

    def setUp(self):
        super(EmailTestHelper, self).setUp()
        mail.outbox = []
        self.sender = b'noreply@example.com'
        self._old_email_settings = {}
        if self.email_siteconfig_settings:
            siteconfig = SiteConfiguration.objects.get_current()
            needs_reload = False
            for key, value in six.iteritems(self.email_siteconfig_settings):
                old_value = siteconfig.get(key)
                if old_value != value:
                    self._old_email_settings[key] = old_value
                    siteconfig.set(key, value)
                    if key in settings_map:
                        needs_reload = True

            if self._old_email_settings:
                siteconfig.save()
                if needs_reload:
                    load_site_config()

    def tearDown(self):
        super(EmailTestHelper, self).tearDown()
        if self._old_email_settings:
            siteconfig = SiteConfiguration.objects.get_current()
            needs_reload = False
            for key, value in six.iteritems(self._old_email_settings):
                self._old_email_settings[key] = siteconfig.get(key)
                siteconfig.set(key, value)
                if key in settings_map:
                    needs_reload = True

            siteconfig.save()
            if needs_reload:
                load_site_config()

    def assertValidRecipients(self, user_list, group_list=[]):
        recipient_list = mail.outbox[0].to + mail.outbox[0].cc
        self.assertEqual(len(recipient_list), len(user_list) + len(group_list))
        for user in user_list:
            self.assertTrue(build_email_address_for_user(User.objects.get(username=user)) in recipient_list, b'user %s was not found in the recipient list' % user)

        groups = Group.objects.filter(name__in=group_list, local_site=None)
        for group in groups:
            for address in get_email_addresses_for_group(group):
                self.assertTrue(address in recipient_list, b'group %s was not found in the recipient list' % address)

        return


class UserEmailTestsMixin(EmailTestHelper):
    """A mixin for user-related e-mail tests."""
    email_siteconfig_settings = {b'mail_send_new_user_mail': True}

    def _register(self, username=b'NewUser', password1=b'password', password2=b'password', email=b'newuser@example.com', first_name=b'New', last_name=b'User'):
        fields = {b'username': username, 
           b'password1': password1, 
           b'password2': password2, 
           b'email': email, 
           b'first_name': first_name, 
           b'last_name': last_name}
        register_url = reverse(b'register')
        self.client.get(register_url)
        self.client.post(register_url, fields)


class UserEmailTests(UserEmailTestsMixin, TestCase):
    """User e-mail tests."""

    def test_new_user_email(self):
        """Testing sending an e-mail after a new user has successfully
        registered
        """
        self._register()
        siteconfig = SiteConfiguration.objects.get_current()
        admin_name = siteconfig.get(b'site_admin_name')
        admin_email_addr = siteconfig.get(b'site_admin_email')
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, b'New Review Board user registration for NewUser')
        self.assertEqual(email.from_email, self.sender)
        self.assertEqual(email.extra_headers[b'From'], settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(email.to[0], build_email_address(full_name=admin_name, email=admin_email_addr))


class UserEmailSiteRootURLTests(SiteRootURLTestsMixin, UserEmailTestsMixin, TestCase):
    """Tests for Bug 4612 related to user e-mails.

    User account e-mails do not include anything with a Local Site, so there
    is no reason to tests the Local Site case.
    """

    @override_settings(**SiteRootURLTestsMixin.CUSTOM_SITE_ROOT_SETTINGS)
    def test_new_user_email_site_root_custom(self):
        """Testing new user e-mail includes site root in e-mails only once with
        custom site root
        """
        self._register()
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertNotIn(self.BAD_SITE_ROOT, email.body)
        for alternative in email.alternatives:
            self.assertNotIn(self.BAD_SITE_ROOT, alternative[0])

    def test_new_user_email_site_root_default(self):
        """Testing new user e-mail includes site root in e-mails only once with
        default site root
        """
        self._register()
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertNotIn(b'example.com//', message.body)
        for alternative in message.alternatives:
            self.assertNotIn(b'example.com//', alternative[0])


class ReviewRequestEmailTestsMixin(EmailTestHelper):
    """A mixin for review request-related and review-related e-mail tests."""
    fixtures = [
     b'test_users']
    email_siteconfig_settings = {b'mail_send_review_mail': True, 
       b'mail_default_from': b'noreply@example.com', 
       b'mail_from_spoofing': b'smart'}


class ReviewRequestEmailTests(ReviewRequestEmailTestsMixin, DmarcDnsTestsMixin, SpyAgency, TestCase):
    """Tests for review and review request e-mails."""

    def test_new_review_request_email(self):
        """Testing sending an e-mail when creating a new review request"""
        review_request = self.create_review_request(summary=b'My test review request')
        review_request.target_people.add(User.objects.get(username=b'grumpy'))
        review_request.target_people.add(User.objects.get(username=b'doc'))
        review_request.publish(review_request.submitter)
        from_email = build_email_address_for_user(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, self.sender)
        self.assertEqual(mail.outbox[0].extra_headers[b'From'], from_email)
        self.assertEqual(mail.outbox[0].subject, b'Review Request %s: My test review request' % review_request.pk)
        self.assertValidRecipients([b'grumpy', b'doc'])
        message = mail.outbox[0].message()
        self.assertEqual(message[b'Sender'], self._get_sender(review_request.submitter))

    def test_new_review_request_with_from_spoofing_always(self):
        """Testing sending an e-mail when creating a new review request with
        mail_from_spoofing=always
        """
        self.dmarc_txt_records[b'_dmarc.example.com'] = b'v=DMARC1; p=reject;'
        review_request = self.create_review_request(summary=b'My test review request')
        review_request.target_people.add(*User.objects.filter(username__in=('doc',
                                                                            'grumpy')))
        settings = {b'mail_from_spoofing': b'always'}
        with self.siteconfig_settings(settings):
            review_request.publish(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, self.sender)
        self.assertEqual(mail.outbox[0].extra_headers[b'From'], b'Doc Dwarf <doc@example.com>')
        self.assertEqual(mail.outbox[0].subject, b'Review Request %s: My test review request' % review_request.pk)
        self.assertValidRecipients([b'grumpy', b'doc'])
        message = mail.outbox[0].message()
        self.assertEqual(message[b'Sender'], self._get_sender(review_request.submitter))

    def test_new_review_request_with_from_spoofing_never(self):
        """Testing sending an e-mail when creating a new review request with
        mail_from_spoofing=never
        """
        review_request = self.create_review_request(summary=b'My test review request')
        review_request.target_people.add(*User.objects.filter(username__in=('doc',
                                                                            'grumpy')))
        settings = {b'mail_from_spoofing': b'never'}
        with self.siteconfig_settings(settings):
            review_request.publish(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, self.sender)
        self.assertEqual(mail.outbox[0].extra_headers[b'From'], b'Doc Dwarf via Review Board <noreply@example.com>')
        self.assertEqual(mail.outbox[0].subject, b'Review Request %s: My test review request' % review_request.pk)
        self.assertValidRecipients([b'grumpy', b'doc'])
        message = mail.outbox[0].message()
        self.assertEqual(message[b'Sender'], self._get_sender(review_request.submitter))

    def test_new_review_request_email_with_from_spoofing_auto(self):
        """Testing sending an e-mail when creating a new review request with
        mail_from_spoofing=auto and allowed by DMARC
        """
        self.dmarc_txt_records[b'_dmarc.example.com'] = b'v=DMARC1; p=none;'
        review_request = self.create_review_request(summary=b'My test review request')
        review_request.target_people.add(*User.objects.filter(username__in=('doc',
                                                                            'grumpy')))
        review_request.publish(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, self.sender)
        self.assertEqual(mail.outbox[0].extra_headers[b'From'], b'Doc Dwarf <doc@example.com>')
        self.assertEqual(mail.outbox[0].subject, b'Review Request %s: My test review request' % review_request.pk)
        self.assertValidRecipients([b'grumpy', b'doc'])
        message = mail.outbox[0].message()
        self.assertEqual(message[b'Sender'], self._get_sender(review_request.submitter))

    def test_new_review_request_email_with_from_spoofing_auto_dmarc_deny(self):
        """Testing sending an e-mail when creating a new review request with
        mail_from_spoofing=auto and denied by DMARC
        """
        self.dmarc_txt_records[b'_dmarc.example.com'] = b'v=DMARC1; p=reject;'
        review_request = self.create_review_request(summary=b'My test review request')
        review_request.target_people.add(*User.objects.filter(username__in=('doc',
                                                                            'grumpy')))
        review_request.publish(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, self.sender)
        self.assertEqual(mail.outbox[0].extra_headers[b'From'], b'Doc Dwarf via Review Board <noreply@example.com>')
        self.assertEqual(mail.outbox[0].subject, b'Review Request %s: My test review request' % review_request.pk)
        self.assertValidRecipients([b'grumpy', b'doc'])
        message = mail.outbox[0].message()
        self.assertEqual(message[b'Sender'], self._get_sender(review_request.submitter))

    def test_review_request_email_local_site_group(self):
        """Testing sending email when a group member is part of a Local Site"""
        local_site = LocalSite.objects.create(name=self.local_site_name)
        group = self.create_review_group()
        user = User.objects.get(username=b'grumpy')
        local_site.users.add(user)
        local_site.admins.add(user)
        local_site.save()
        group.users.add(user)
        group.save()
        review_request = self.create_review_request()
        review_request.target_groups.add(group)
        review_request.publish(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        self.assertValidRecipients([b'doc', b'grumpy'])

    def test_review_email(self):
        """Testing sending an e-mail when replying to a review request"""
        review_request = self.create_review_request(summary=b'My test review request')
        review_request.target_people.add(User.objects.get(username=b'grumpy'))
        review_request.target_people.add(User.objects.get(username=b'doc'))
        review_request.publish(review_request.submitter)
        mail.outbox = []
        review = self.create_review(review_request=review_request)
        review.publish()
        from_email = build_email_address_for_user(review.user)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.from_email, self.sender)
        self.assertEqual(email.extra_headers[b'From'], from_email)
        self.assertEqual(email._headers[b'X-ReviewBoard-URL'], b'http://example.com/')
        self.assertEqual(email._headers[b'X-ReviewRequest-URL'], b'http://example.com/r/%s/' % review_request.display_id)
        self.assertEqual(email.subject, b'Re: Review Request %s: My test review request' % review_request.display_id)
        self.assertValidRecipients([
         review_request.submitter.username,
         b'grumpy',
         b'doc'])
        message = email.message()
        self.assertEqual(message[b'Sender'], self._get_sender(review.user))

    def test_review_email_with_from_spoofing_always(self):
        """Testing sending an e-mail when replying to a review request with
        mail_from_spoofing=always
        """
        self.dmarc_txt_records[b'_dmarc.example.com'] = b'v=DMARC1; p=reject;'
        review_request = self.create_review_request(summary=b'My test review request')
        review_request.target_people.add(*User.objects.filter(username__in=('doc',
                                                                            'grumpy')))
        review_request.publish(review_request.submitter)
        review = self.create_review(review_request=review_request)
        mail.outbox = []
        settings = {b'mail_from_spoofing': b'always'}
        with self.siteconfig_settings(settings):
            review.publish()
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.from_email, self.sender)
        self.assertEqual(email.extra_headers[b'From'], b'Dopey Dwarf <dopey@example.com>')
        self.assertEqual(email._headers[b'X-ReviewBoard-URL'], b'http://example.com/')
        self.assertEqual(email._headers[b'X-ReviewRequest-URL'], b'http://example.com/r/%s/' % review_request.display_id)
        self.assertEqual(email.subject, b'Re: Review Request %s: My test review request' % review_request.display_id)
        self.assertValidRecipients([
         review_request.submitter.username,
         b'grumpy',
         b'doc'])
        message = email.message()
        self.assertEqual(message[b'Sender'], self._get_sender(review.user))

    def test_review_email_with_from_spoofing_never(self):
        """Testing sending an e-mail when replying to a review request with
        mail_from_spoofing=never
        """
        review_request = self.create_review_request(summary=b'My test review request')
        review_request.target_people.add(*User.objects.filter(username__in=('doc',
                                                                            'grumpy')))
        review_request.publish(review_request.submitter)
        review = self.create_review(review_request=review_request)
        mail.outbox = []
        settings = {b'mail_from_spoofing': b'never'}
        with self.siteconfig_settings(settings):
            review.publish()
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.from_email, self.sender)
        self.assertEqual(email.extra_headers[b'From'], b'Dopey Dwarf via Review Board <noreply@example.com>')
        self.assertEqual(email._headers[b'X-ReviewBoard-URL'], b'http://example.com/')
        self.assertEqual(email._headers[b'X-ReviewRequest-URL'], b'http://example.com/r/%s/' % review_request.display_id)
        self.assertEqual(email.subject, b'Re: Review Request %s: My test review request' % review_request.display_id)
        self.assertValidRecipients([
         review_request.submitter.username,
         b'grumpy',
         b'doc'])
        message = email.message()
        self.assertEqual(message[b'Sender'], self._get_sender(review.user))

    def test_review_email_with_from_spoofing_auto(self):
        """Testing sending an e-mail when replying to a review request with
        mail_from_spoofing=auto and allowed by DMARC
        """
        self.dmarc_txt_records[b'_dmarc.example.com'] = b'v=DMARC1; p=none;'
        review_request = self.create_review_request(summary=b'My test review request')
        review_request.target_people.add(*User.objects.filter(username__in=('doc',
                                                                            'grumpy')))
        review_request.publish(review_request.submitter)
        mail.outbox = []
        review = self.create_review(review_request=review_request)
        review.publish()
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.from_email, self.sender)
        self.assertEqual(email.extra_headers[b'From'], b'Dopey Dwarf <dopey@example.com>')
        self.assertEqual(email._headers[b'X-ReviewBoard-URL'], b'http://example.com/')
        self.assertEqual(email._headers[b'X-ReviewRequest-URL'], b'http://example.com/r/%s/' % review_request.display_id)
        self.assertEqual(email.subject, b'Re: Review Request %s: My test review request' % review_request.display_id)
        self.assertValidRecipients([
         review_request.submitter.username,
         b'grumpy',
         b'doc'])
        message = email.message()
        self.assertEqual(message[b'Sender'], self._get_sender(review.user))

    def test_review_email_with_from_spoofing_auto_dmarc_deny(self):
        """Testing sending an e-mail when replying to a review request with
        mail_from_spoofing=auto and denied by DMARC
        """
        self.dmarc_txt_records[b'_dmarc.example.com'] = b'v=DMARC1; p=reject;'
        review_request = self.create_review_request(summary=b'My test review request')
        review_request.target_people.add(*User.objects.filter(username__in=('doc',
                                                                            'grumpy')))
        review_request.publish(review_request.submitter)
        mail.outbox = []
        review = self.create_review(review_request=review_request)
        review.publish()
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.from_email, self.sender)
        self.assertEqual(email.extra_headers[b'From'], b'Dopey Dwarf via Review Board <noreply@example.com>')
        self.assertEqual(email._headers[b'X-ReviewBoard-URL'], b'http://example.com/')
        self.assertEqual(email._headers[b'X-ReviewRequest-URL'], b'http://example.com/r/%s/' % review_request.display_id)
        self.assertEqual(email.subject, b'Re: Review Request %s: My test review request' % review_request.display_id)
        self.assertValidRecipients([
         review_request.submitter.username,
         b'grumpy',
         b'doc'])
        message = email.message()
        self.assertEqual(message[b'Sender'], self._get_sender(review.user))

    @add_fixtures([b'test_site'])
    def test_review_email_with_site(self):
        """Testing sending an e-mail when replying to a review request
        on a Local Site
        """
        review_request = self.create_review_request(summary=b'My test review request', with_local_site=True)
        review_request.target_people.add(User.objects.get(username=b'grumpy'))
        review_request.target_people.add(User.objects.get(username=b'doc'))
        review_request.publish(review_request.submitter)
        site = review_request.local_site
        site.users.add(*list(review_request.target_people.all()))
        mail.outbox = []
        review = self.create_review(review_request=review_request)
        review.publish()
        from_email = build_email_address_for_user(review.user)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.from_email, self.sender)
        self.assertEqual(email.extra_headers[b'From'], from_email)
        self.assertEqual(email._headers[b'X-ReviewBoard-URL'], b'http://example.com/s/local-site-1/')
        self.assertEqual(email._headers[b'X-ReviewRequest-URL'], b'http://example.com/s/local-site-1/r/%s/' % review_request.display_id)
        self.assertEqual(email.subject, b'Re: Review Request %s: My test review request' % review_request.display_id)
        self.assertValidRecipients([
         review_request.submitter.username,
         b'grumpy',
         b'doc'])
        message = email.message()
        self.assertEqual(message[b'Sender'], self._get_sender(review.user))

    def test_profile_should_send_email_setting(self):
        """Testing the Profile.should_send_email setting"""
        grumpy = User.objects.get(username=b'grumpy')
        profile = grumpy.get_profile()
        profile.should_send_email = False
        profile.save(update_fields=('should_send_email', ))
        review_request = self.create_review_request(summary=b'My test review request')
        review_request.target_people.add(grumpy)
        review_request.target_people.add(User.objects.get(username=b'doc'))
        review_request.publish(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        self.assertValidRecipients([b'doc'])

    def test_review_request_closed_no_email(self):
        """Tests e-mail is not generated when a review request is closed and
        e-mail setting is False
        """
        review_request = self.create_review_request()
        review_request.publish(review_request.submitter)
        mail.outbox = []
        review_request.close(ReviewRequest.SUBMITTED, review_request.submitter)
        self.assertEqual(len(mail.outbox), 0)

    def test_review_request_closed_with_email(self):
        """Tests e-mail is generated when a review request is closed and
        e-mail setting is True
        """
        with self.siteconfig_settings({b'mail_send_review_close_mail': True}, reload_settings=False):
            review_request = self.create_review_request()
            review_request.publish(review_request.submitter)
            mail.outbox = []
            review_request.close(ReviewRequest.SUBMITTED, review_request.submitter)
            from_email = build_email_address_for_user(review_request.submitter)
            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].from_email, self.sender)
            self.assertEqual(mail.outbox[0].extra_headers[b'From'], from_email)
            message = mail.outbox[0].message()
            self.assertTrue(b'This change has been marked as submitted' in message.as_string())

    def test_review_request_close_with_email_and_dmarc_deny(self):
        """Tests e-mail is generated when a review request is closed and
        e-mail setting is True and From spoofing blocked by DMARC
        """
        self.dmarc_txt_records[b'_dmarc.example.com'] = b'v=DMARC1; p=reject;'
        with self.siteconfig_settings({b'mail_send_review_close_mail': True}, reload_settings=False):
            review_request = self.create_review_request()
            review_request.publish(review_request.submitter)
            mail.outbox = []
            review_request.close(ReviewRequest.SUBMITTED, review_request.submitter)
            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].from_email, self.sender)
            self.assertEqual(mail.outbox[0].extra_headers[b'From'], b'Doc Dwarf via Review Board <noreply@example.com>')
            message = mail.outbox[0].message()
            self.assertTrue(b'This change has been marked as submitted' in message.as_string())

    def test_review_to_owner_only(self):
        """Test that e-mails from reviews published to the submitter only will
        only go to the submitter and the reviewer
        """
        review_request = self.create_review_request(public=True, publish=False)
        review_request.target_people.add(User.objects.get(username=b'grumpy'))
        review = self.create_review(review_request=review_request, publish=False)
        with self.siteconfig_settings({b'mail_send_review_mail': True}, reload_settings=False):
            review.publish(to_owner_only=True)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.cc, [])
        self.assertEqual(len(message.to), 2)
        self.assertEqual(set(message.to), set([build_email_address_for_user(review.user),
         build_email_address_for_user(review_request.submitter)]))

    def test_review_reply_email(self):
        """Testing sending an e-mail when replying to a review"""
        review_request = self.create_review_request(summary=b'My test review request')
        review_request.publish(review_request.submitter)
        base_review = self.create_review(review_request=review_request)
        base_review.publish()
        mail.outbox = []
        reply = self.create_reply(base_review)
        reply.publish()
        from_email = build_email_address_for_user(reply.user)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, self.sender)
        self.assertEqual(mail.outbox[0].extra_headers[b'From'], from_email)
        self.assertEqual(mail.outbox[0].subject, b'Re: Review Request %s: My test review request' % review_request.pk)
        self.assertValidRecipients([
         review_request.submitter.username,
         base_review.user.username,
         reply.user.username])
        message = mail.outbox[0].message()
        self.assertEqual(message[b'Sender'], self._get_sender(reply.user))

    def test_review_reply_email_with_dmarc_deny(self):
        """Testing sending an e-mail when replying to a review with From
        spoofing blocked by DMARC
        """
        self.dmarc_txt_records[b'_dmarc.example.com'] = b'v=DMARC1; p=reject;'
        review_request = self.create_review_request(summary=b'My test review request')
        review_request.publish(review_request.submitter)
        base_review = self.create_review(review_request=review_request)
        base_review.publish()
        mail.outbox = []
        reply = self.create_reply(base_review)
        reply.publish()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, self.sender)
        self.assertEqual(mail.outbox[0].extra_headers[b'From'], b'Grumpy Dwarf via Review Board <noreply@example.com>')
        self.assertEqual(mail.outbox[0].subject, b'Re: Review Request %s: My test review request' % review_request.pk)
        self.assertValidRecipients([
         review_request.submitter.username,
         base_review.user.username,
         reply.user.username])
        message = mail.outbox[0].message()
        self.assertEqual(message[b'Sender'], self._get_sender(reply.user))

    def test_update_review_request_email(self):
        """Testing sending an e-mail when updating a review request"""
        group = Group.objects.create(name=b'devgroup', mailing_list=b'devgroup@example.com')
        review_request = self.create_review_request(summary=b'My test review request')
        review_request.target_groups.add(group)
        review_request.email_message_id = b'junk'
        review_request.publish(review_request.submitter)
        from_email = build_email_address_for_user(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, self.sender)
        self.assertEqual(mail.outbox[0].extra_headers[b'From'], from_email)
        self.assertEqual(mail.outbox[0].subject, b'Re: Review Request %s: My test review request' % review_request.pk)
        self.assertValidRecipients([review_request.submitter.username], [
         b'devgroup'])
        message = mail.outbox[0].message()
        self.assertEqual(message[b'Sender'], self._get_sender(review_request.submitter))

    def test_update_review_request_email_with_dmarc_deny(self):
        """Testing sending an e-mail when updating a review request with
        From spoofing blocked by DMARC
        """
        self.dmarc_txt_records[b'_dmarc.example.com'] = b'v=DMARC1; p=reject;'
        group = Group.objects.create(name=b'devgroup', mailing_list=b'devgroup@example.com')
        review_request = self.create_review_request(summary=b'My test review request')
        review_request.target_groups.add(group)
        review_request.email_message_id = b'junk'
        review_request.publish(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, self.sender)
        self.assertEqual(mail.outbox[0].extra_headers[b'From'], b'Doc Dwarf via Review Board <noreply@example.com>')
        self.assertEqual(mail.outbox[0].subject, b'Re: Review Request %s: My test review request' % review_request.pk)
        self.assertValidRecipients([review_request.submitter.username], [
         b'devgroup'])
        message = mail.outbox[0].message()
        self.assertEqual(message[b'Sender'], self._get_sender(review_request.submitter))

    def test_add_reviewer_review_request_email(self):
        """Testing limited e-mail recipients
        when adding a reviewer to an existing review request
        """
        review_request = self.create_review_request(summary=b'My test review request', public=True)
        review_request.email_message_id = b'junk'
        review_request.target_people.add(User.objects.get(username=b'dopey'))
        review_request.save()
        draft = ReviewRequestDraft.create(review_request)
        draft.target_people.add(User.objects.get(username=b'grumpy'))
        draft.publish(user=review_request.submitter)
        from_email = build_email_address_for_user(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, self.sender)
        self.assertEqual(mail.outbox[0].extra_headers[b'From'], from_email)
        self.assertEqual(mail.outbox[0].subject, b'Re: Review Request %s: My test review request' % review_request.pk)
        self.assertValidRecipients([review_request.submitter.username,
         b'grumpy'])
        message = mail.outbox[0].message()
        self.assertEqual(message[b'Sender'], self._get_sender(review_request.submitter))

    def test_add_group_review_request_email(self):
        """Testing limited e-mail recipients
        when adding a group to an existing review request
        """
        existing_group = Group.objects.create(name=b'existing', mailing_list=b'existing@example.com')
        review_request = self.create_review_request(summary=b'My test review request', public=True)
        review_request.email_message_id = b'junk'
        review_request.target_groups.add(existing_group)
        review_request.target_people.add(User.objects.get(username=b'dopey'))
        review_request.save()
        new_group = Group.objects.create(name=b'devgroup', mailing_list=b'devgroup@example.com')
        draft = ReviewRequestDraft.create(review_request)
        draft.target_groups.add(new_group)
        draft.publish(user=review_request.submitter)
        from_email = build_email_address_for_user(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, self.sender)
        self.assertEqual(mail.outbox[0].extra_headers[b'From'], from_email)
        self.assertEqual(mail.outbox[0].subject, b'Re: Review Request %s: My test review request' % review_request.pk)
        self.assertValidRecipients([review_request.submitter.username], [
         b'devgroup'])
        message = mail.outbox[0].message()
        self.assertEqual(message[b'Sender'], self._get_sender(review_request.submitter))

    def test_limited_recipients_other_fields(self):
        """Testing that recipient limiting only happens when adding reviewers
        """
        review_request = self.create_review_request(summary=b'My test review request', public=True)
        review_request.email_message_id = b'junk'
        review_request.target_people.add(User.objects.get(username=b'dopey'))
        review_request.save()
        draft = ReviewRequestDraft.create(review_request)
        draft.summary = b'Changed summary'
        draft.target_people.add(User.objects.get(username=b'grumpy'))
        draft.publish(user=review_request.submitter)
        from_email = build_email_address_for_user(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, self.sender)
        self.assertEqual(mail.outbox[0].extra_headers[b'From'], from_email)
        self.assertEqual(mail.outbox[0].subject, b'Re: Review Request %s: Changed summary' % review_request.pk)
        self.assertValidRecipients([review_request.submitter.username,
         b'dopey', b'grumpy'])
        message = mail.outbox[0].message()
        self.assertEqual(message[b'Sender'], self._get_sender(review_request.submitter))

    def test_recipients_with_muted_review_requests(self):
        """Testing e-mail recipients when users mute a review request"""
        dopey = User.objects.get(username=b'dopey')
        admin = User.objects.get(username=b'admin')
        group = Group.objects.create(name=b'group')
        group.users.add(admin)
        group.save()
        review_request = self.create_review_request(summary=b'My test review request', public=True)
        review_request.target_people.add(dopey)
        review_request.target_people.add(User.objects.get(username=b'grumpy'))
        review_request.target_groups.add(group)
        review_request.save()
        visit = self.create_visit(review_request, ReviewRequestVisit.MUTED, dopey)
        visit.save()
        visit = self.create_visit(review_request, ReviewRequestVisit.MUTED, admin)
        visit.save()
        draft = ReviewRequestDraft.create(review_request)
        draft.summary = b'Summary changed'
        draft.publish(user=review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        self.assertValidRecipients([b'doc', b'grumpy'])

    def test_group_member_not_receive_email(self):
        """Testing sending review e-mails and filtering out the review
        submitter when they are part of a review group assigned to the request
        """
        submitter = User.objects.get(username=b'doc')
        profile = submitter.get_profile()
        profile.should_send_own_updates = False
        profile.save(update_fields=('should_send_own_updates', ))
        reviewer = User.objects.get(username=b'dopey')
        group = self.create_review_group()
        group.users.add(submitter)
        review_request = self.create_review_request(public=True)
        review_request.target_groups.add(group)
        review_request.target_people.add(reviewer)
        review_request.save()
        review = self.create_review(review_request, user=submitter)
        review.publish()
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertListEqual(msg.to, [
         build_email_address_for_user(reviewer)])
        self.assertListEqual(msg.cc, [])

    def test_local_site_user_filters(self):
        """Testing sending e-mails and filtering out users not on a local site
        """
        test_site = LocalSite.objects.create(name=self.local_site_name)
        site_user1 = User.objects.create_user(username=b'site_user1', email=b'site_user1@example.com')
        site_user2 = User.objects.create_user(username=b'site_user2', email=b'site_user2@example.com')
        site_user3 = User.objects.create_user(username=b'site_user3', email=b'site_user3@example.com')
        site_user4 = User.objects.create_user(username=b'site_user4', email=b'site_user4@example.com')
        site_user5 = User.objects.create_user(username=b'site_user5', email=b'site_user5@example.com')
        non_site_user1 = User.objects.create_user(username=b'non_site_user1', email=b'non_site_user1@example.com')
        non_site_user2 = User.objects.create_user(username=b'non_site_user2', email=b'non_site_user2@example.com')
        non_site_user3 = User.objects.create_user(username=b'non_site_user3', email=b'non_site_user3@example.com')
        test_site.admins.add(site_user1)
        test_site.users.add(site_user2)
        test_site.users.add(site_user3)
        test_site.users.add(site_user4)
        test_site.users.add(site_user5)
        group = Group.objects.create(name=b'my-group', display_name=b'My Group', local_site=test_site)
        group.users.add(site_user5)
        group.users.add(non_site_user3)
        review_request = self.create_review_request(with_local_site=True, local_id=123)
        review_request.email_message_id = b'junk'
        review_request.target_people = [site_user1, site_user2, site_user3,
         non_site_user1]
        review_request.target_groups = [group]
        review = Review.objects.create(review_request=review_request, user=site_user4)
        review.publish()
        review = Review.objects.create(review_request=review_request, user=non_site_user2)
        review.publish()
        from_email = build_email_address_for_user(review_request.submitter)
        mail.outbox = []
        review_request.publish(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, self.sender)
        self.assertEqual(mail.outbox[0].extra_headers[b'From'], from_email)
        self.assertValidRecipients([
         b'site_user1', b'site_user2', b'site_user3', b'site_user4',
         b'site_user5', review_request.submitter.username], [])
        message = mail.outbox[0].message()
        self.assertEqual(message[b'Sender'], self._get_sender(review_request.submitter))

    def test_review_request_email_with_unicode_summary(self):
        """Testing sending a review request e-mail with a unicode subject"""
        self.spy_on(logging.exception)
        with self.settings(EMAIL_BACKEND=_CONSOLE_EMAIL_BACKEND):
            review_request = self.create_review_request()
            review_request.summary = b'😄'
            review_request.target_people.add(User.objects.get(username=b'grumpy'))
            review_request.target_people.add(User.objects.get(username=b'doc'))
            review_request.publish(review_request.submitter)
        self.assertIsNotNone(review_request.email_message_id)
        self.assertFalse(logging.exception.spy.called)

    def test_review_request_email_with_unicode_description(self):
        """Testing sending a review request e-mail with a unicode
        description
        """
        self.spy_on(logging.exception)
        with self.settings(EMAIL_BACKEND=_CONSOLE_EMAIL_BACKEND):
            review_request = self.create_review_request()
            review_request.description = b'😄'
            review_request.target_people.add(User.objects.get(username=b'grumpy'))
            review_request.target_people.add(User.objects.get(username=b'doc'))
            review_request.publish(review_request.submitter)
        self.assertIsNotNone(review_request.email_message_id)
        self.assertFalse(logging.exception.spy.called)

    @add_fixtures([b'test_scmtools'])
    def test_review_request_email_with_added_file(self):
        """Testing sending a review request e-mail with added files in the
        diffset
        """
        repository = self.create_repository(tool_name=b'Test')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request)
        filediff = self.create_filediff(diffset=diffset, source_file=b'/dev/null', source_revision=PRE_CREATION)
        review_request.publish(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertTrue(b'X-ReviewBoard-Diff-For' in message._headers)
        diff_headers = message._headers.getlist(b'X-ReviewBoard-Diff-For')
        self.assertEqual(len(diff_headers), 1)
        self.assertFalse(filediff.source_file in diff_headers)
        self.assertTrue(filediff.dest_file in diff_headers)

    @add_fixtures([b'test_scmtools'])
    def test_review_request_email_with_added_files_over_header_limit(self):
        """Testing sending a review request e-mail with added files in the
        diffset such that the filename headers take up more than 8192
        characters
        """
        self.spy_on(logging.warning)
        self.maxDiff = None
        repository = self.create_repository(tool_name=b'Test')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request)
        prefix = b'X' * 97
        filediffs = []
        for i in range(70):
            filename = b'%s%#03d' % (prefix, i)
            self.assertEqual(len(filename), 100)
            filediffs.append(self.create_filediff(diffset=diffset, source_file=filename, dest_file=filename, source_revision=PRE_CREATION, diff=b'', save=False))

        FileDiff.objects.bulk_create(filediffs)
        review_request.publish(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertIn(b'X-ReviewBoard-Diff-For', message._headers)
        diff_headers = message._headers.getlist(b'X-ReviewBoard-Diff-For')
        self.assertEqual(len(logging.warning.spy.calls), 1)
        self.assertEqual(len(diff_headers), 65)
        self.assertEqual(logging.warning.spy.calls[0].args, ('Unable to store all filenames in the X-ReviewBoard-Diff-For headers when sending e-mail for review request %s: The header size exceeds the limit of %s. Remaining headers have been omitted.',
                                                             1, 8192))
        return

    @add_fixtures([b'test_scmtools'])
    def test_review_request_email_with_deleted_file(self):
        """Testing sending a review request e-mail with deleted files in the
        diffset
        """
        repository = self.create_repository(tool_name=b'Test')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request)
        filediff = self.create_filediff(diffset=diffset, dest_file=b'/dev/null', status=FileDiff.DELETED)
        review_request.publish(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertTrue(b'X-ReviewBoard-Diff-For' in message._headers)
        diff_headers = message._headers.getlist(b'X-ReviewBoard-Diff-For')
        self.assertEqual(len(diff_headers), 1)
        self.assertTrue(filediff.source_file in diff_headers)
        self.assertFalse(filediff.dest_file in diff_headers)

    @add_fixtures([b'test_scmtools'])
    def test_review_request_email_with_moved_file(self):
        """Testing sending a review request e-mail with moved files in the
        diffset
        """
        repository = self.create_repository(tool_name=b'Test')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request)
        filediff = self.create_filediff(diffset=diffset, source_file=b'foo', dest_file=b'bar', status=FileDiff.MOVED)
        review_request.publish(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertTrue(b'X-ReviewBoard-Diff-For' in message._headers)
        diff_headers = message._headers.getlist(b'X-ReviewBoard-Diff-For')
        self.assertEqual(len(diff_headers), 2)
        self.assertTrue(filediff.source_file in diff_headers)
        self.assertTrue(filediff.dest_file in diff_headers)

    @add_fixtures([b'test_scmtools'])
    def test_review_request_email_with_copied_file(self):
        """Testing sending a review request e-mail with copied files in the
        diffset
        """
        repository = self.create_repository(tool_name=b'Test')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request)
        filediff = self.create_filediff(diffset=diffset, source_file=b'foo', dest_file=b'bar', status=FileDiff.COPIED)
        review_request.publish(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertTrue(b'X-ReviewBoard-Diff-For' in message._headers)
        diff_headers = message._headers.getlist(b'X-ReviewBoard-Diff-For')
        self.assertEqual(len(diff_headers), 2)
        self.assertTrue(filediff.source_file in diff_headers)
        self.assertTrue(filediff.dest_file in diff_headers)

    @add_fixtures([b'test_scmtools'])
    def test_review_request_email_with_modified_file(self):
        """Testing sending a review request e-mail with modified files in
        the diffset
        """
        repository = self.create_repository(tool_name=b'Test')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request)
        filediff = self.create_filediff(diffset=diffset, source_file=b'foo', dest_file=b'bar', status=FileDiff.MODIFIED)
        review_request.publish(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertIn(b'X-ReviewBoard-Diff-For', message._headers)
        diff_headers = message._headers.getlist(b'X-ReviewBoard-Diff-For')
        self.assertEqual(len(diff_headers), 2)
        self.assertIn(filediff.source_file, diff_headers)
        self.assertIn(filediff.dest_file, diff_headers)

    @add_fixtures([b'test_scmtools'])
    def test_review_request_email_with_multiple_files(self):
        """Testing sending a review request e-mail with multiple files in the
        diffset
        """
        repository = self.create_repository(tool_name=b'Test')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request)
        filediffs = [
         self.create_filediff(diffset=diffset, source_file=b'foo', dest_file=b'bar', status=FileDiff.MOVED),
         self.create_filediff(diffset=diffset, source_file=b'baz', dest_file=b'/dev/null', status=FileDiff.DELETED)]
        review_request.publish(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertTrue(b'X-ReviewBoard-Diff-For' in message._headers)
        diff_headers = message._headers.getlist(b'X-ReviewBoard-Diff-For')
        self.assertEqual(set(diff_headers), {
         filediffs[0].source_file,
         filediffs[0].dest_file,
         filediffs[1].source_file})

    def test_extra_headers_dict(self):
        """Testing sending extra headers as a dict with an e-mail message"""
        review_request = self.create_review_request()
        submitter = review_request.submitter
        send_email(prepare_base_review_request_mail, user=submitter, review_request=review_request, subject=b'Foo', in_reply_to=None, to_field=[
         submitter], cc_field=[], template_name_base=b'notifications/review_request_email', extra_headers={b'X-Foo': b'Bar'})
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertIn(b'X-Foo', message._headers)
        self.assertEqual(message._headers[b'X-Foo'], b'Bar')
        return

    def test_extra_headers_multivalue_dict(self):
        """Testing sending extra headers as a MultiValueDict with an e-mail
        message
        """
        header_values = [
         b'Bar', b'Baz']
        review_request = self.create_review_request()
        submitter = review_request.submitter
        send_email(prepare_base_review_request_mail, user=review_request.submitter, review_request=review_request, subject=b'Foo', in_reply_to=None, to_field=[
         submitter], cc_field=[], template_name_base=b'notifications/review_request_email', extra_headers=MultiValueDict({b'X-Foo': header_values}))
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertIn(b'X-Foo', message._headers)
        self.assertEqual(set(message._headers.getlist(b'X-Foo')), set(header_values))
        return

    def test_review_no_shipit_headers(self):
        """Testing sending a review e-mail without a 'Ship It!'"""
        review_request = self.create_review_request(public=True)
        self.create_review(review_request, body_top=Review.SHIP_IT_TEXT, body_bottom=b'', publish=True)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertNotIn(b'X-ReviewBoard-ShipIt', message._headers)
        self.assertNotIn(b'X-ReviewBoard-ShipIt-Only', message._headers)
        self.assertFalse(Review.FIX_IT_THEN_SHIP_IT_TEXT in message.message().as_string())

    def test_review_shipit_only_headers(self):
        """Testing sending a review e-mail with only a 'Ship It!'"""
        review_request = self.create_review_request(public=True)
        self.create_review(review_request, body_top=Review.SHIP_IT_TEXT, body_bottom=b'', ship_it=True, publish=True)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertIn(b'X-ReviewBoard-ShipIt', message._headers)
        self.assertIn(b'X-ReviewBoard-ShipIt-Only', message._headers)
        self.assertFalse(Review.FIX_IT_THEN_SHIP_IT_TEXT in message.message().as_string())

    def test_review_shipit_only_headers_no_text(self):
        """Testing sending a review e-mail with only a 'Ship It!' and no text
        """
        review_request = self.create_review_request(public=True)
        self.create_review(review_request, body_top=b'', body_bottom=b'', ship_it=True, publish=True)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertIn(b'X-ReviewBoard-ShipIt', message._headers)
        self.assertIn(b'X-ReviewBoard-ShipIt-Only', message._headers)
        self.assertFalse(Review.FIX_IT_THEN_SHIP_IT_TEXT in message.message().as_string())

    def test_review_shipit_headers_custom_top_text(self):
        """Testing sending a review e-mail with a 'Ship It' and custom top text
        """
        review_request = self.create_review_request(public=True)
        self.create_review(review_request, body_top=b'Some general information.', body_bottom=b'', ship_it=True, publish=True)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertIn(b'X-ReviewBoard-ShipIt', message._headers)
        self.assertNotIn(b'X-ReviewBoard-ShipIt-Only', message._headers)
        self.assertFalse(Review.FIX_IT_THEN_SHIP_IT_TEXT in message.message().as_string())

    def test_review_shipit_headers_bottom_text(self):
        """Testing sending a review e-mail with a 'Ship It' and bottom text"""
        review_request = self.create_review_request(public=True)
        self.create_review(review_request, body_top=Review.SHIP_IT_TEXT, body_bottom=b'Some comments', ship_it=True, publish=True)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertIn(b'X-ReviewBoard-ShipIt', message._headers)
        self.assertNotIn(b'X-ReviewBoard-ShipIt-Only', message._headers)
        self.assertFalse(Review.FIX_IT_THEN_SHIP_IT_TEXT in message.message().as_string())

    @add_fixtures([b'test_scmtools'])
    def test_review_shipit_headers_comments(self):
        """Testing sending a review e-mail with a 'Ship It' and diff comments
        """
        repository = self.create_repository(tool_name=b'Test')
        review_request = self.create_review_request(repository=repository, public=True)
        diffset = self.create_diffset(review_request)
        filediff = self.create_filediff(diffset)
        review = self.create_review(review_request, body_top=Review.SHIP_IT_TEXT, body_bottom=b'', ship_it=True, publish=False)
        self.create_diff_comment(review, filediff)
        review.publish()
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertIn(b'X-ReviewBoard-ShipIt', message._headers)
        self.assertNotIn(b'X-ReviewBoard-ShipIt-Only', message._headers)
        self.assertFalse(Review.FIX_IT_THEN_SHIP_IT_TEXT in message.message().as_string())

    @add_fixtures([b'test_scmtools'])
    def test_review_shipit_headers_comments_opened_issue(self):
        """Testing sending a review e-mail with a 'Ship It' and diff comments
        with opened issue
        """
        repository = self.create_repository(tool_name=b'Test')
        review_request = self.create_review_request(repository=repository, public=True)
        diffset = self.create_diffset(review_request)
        filediff = self.create_filediff(diffset)
        review = self.create_review(review_request, body_top=Review.SHIP_IT_TEXT, body_bottom=b'', ship_it=True, publish=False)
        self.create_diff_comment(review, filediff, issue_opened=True)
        review.publish()
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertIn(b'X-ReviewBoard-ShipIt', message._headers)
        self.assertNotIn(b'X-ReviewBoard-ShipIt-Only', message._headers)
        self.assertTrue(Review.FIX_IT_THEN_SHIP_IT_TEXT in message.message().as_string())

    def test_review_shipit_headers_attachment_comments(self):
        """Testing sending a review e-mail with a 'Ship It' and file attachment
        comments
        """
        review_request = self.create_review_request(public=True)
        file_attachment = self.create_file_attachment(review_request)
        review = self.create_review(review_request, body_top=Review.SHIP_IT_TEXT, body_bottom=b'', ship_it=True, publish=False)
        self.create_file_attachment_comment(review, file_attachment)
        review.publish()
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertIn(b'X-ReviewBoard-ShipIt', message._headers)
        self.assertNotIn(b'X-ReviewBoard-ShipIt-Only', message._headers)
        self.assertFalse(Review.FIX_IT_THEN_SHIP_IT_TEXT in message.message().as_string())

    def test_review_shipit_headers_attachment_comments_opened_issue(self):
        """Testing sending a review e-mail with a 'Ship It' and file attachment
        comments with opened issue
        """
        review_request = self.create_review_request(public=True)
        file_attachment = self.create_file_attachment(review_request)
        review = self.create_review(review_request, body_top=Review.SHIP_IT_TEXT, body_bottom=b'', ship_it=True, publish=False)
        self.create_file_attachment_comment(review, file_attachment, issue_opened=True)
        review.publish()
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertIn(b'X-ReviewBoard-ShipIt', message._headers)
        self.assertNotIn(b'X-ReviewBoard-ShipIt-Only', message._headers)
        self.assertTrue(Review.FIX_IT_THEN_SHIP_IT_TEXT in message.message().as_string())

    def test_review_shipit_headers_screenshot_comments(self):
        """Testing sending a review e-mail with a 'Ship It' and screenshot
        comments
        """
        review_request = self.create_review_request(public=True)
        screenshot = self.create_screenshot(review_request)
        review = self.create_review(review_request, body_top=Review.SHIP_IT_TEXT, body_bottom=b'', ship_it=True, publish=False)
        self.create_screenshot_comment(review, screenshot)
        review.publish()
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertIn(b'X-ReviewBoard-ShipIt', message._headers)
        self.assertNotIn(b'X-ReviewBoard-ShipIt-Only', message._headers)
        self.assertFalse(Review.FIX_IT_THEN_SHIP_IT_TEXT in message.message().as_string())

    def test_review_shipit_headers_screenshot_comments_opened_issue(self):
        """Testing sending a review e-mail with a 'Ship It' and screenshot
        comments with opened issue
        """
        review_request = self.create_review_request(public=True)
        screenshot = self.create_screenshot(review_request)
        review = self.create_review(review_request, body_top=Review.SHIP_IT_TEXT, body_bottom=b'', ship_it=True, publish=False)
        self.create_screenshot_comment(review, screenshot, issue_opened=True)
        review.publish()
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertIn(b'X-ReviewBoard-ShipIt', message._headers)
        self.assertNotIn(b'X-ReviewBoard-ShipIt-Only', message._headers)
        self.assertTrue(Review.FIX_IT_THEN_SHIP_IT_TEXT in message.message().as_string())

    def test_review_shipit_headers_general_comments(self):
        """Testing sending a review e-mail with a 'Ship It' and general
        comments
        """
        review_request = self.create_review_request(public=True)
        review = self.create_review(review_request, body_top=Review.SHIP_IT_TEXT, body_bottom=b'', ship_it=True, publish=False)
        self.create_general_comment(review)
        review.publish()
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertIn(b'X-ReviewBoard-ShipIt', message._headers)
        self.assertNotIn(b'X-ReviewBoard-ShipIt-Only', message._headers)
        self.assertFalse(Review.FIX_IT_THEN_SHIP_IT_TEXT in message.message().as_string())

    def test_review_shipit_headers_general_comments_opened_issue(self):
        """Testing sending a review e-mail with a 'Ship It' and general
        comments with opened issue
        """
        review_request = self.create_review_request(public=True)
        review = self.create_review(review_request, body_top=Review.SHIP_IT_TEXT, body_bottom=b'', ship_it=True, publish=False)
        self.create_general_comment(review, issue_opened=True)
        review.publish()
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertIn(b'X-ReviewBoard-ShipIt', message._headers)
        self.assertNotIn(b'X-ReviewBoard-ShipIt-Only', message._headers)
        self.assertTrue(Review.FIX_IT_THEN_SHIP_IT_TEXT in message.message().as_string())

    def test_change_ownership_email(self):
        """Testing sending a review request e-mail when the owner is being
        changed
        """
        admin_user = User.objects.get(username=b'admin')
        admin_email = build_email_address_for_user(admin_user)
        review_request = self.create_review_request(public=True)
        submitter = review_request.submitter
        submitter_email = build_email_address_for_user(submitter)
        draft = ReviewRequestDraft.create(review_request)
        draft.target_people = [submitter, admin_user]
        draft.owner = admin_user
        draft.save()
        review_request.publish(submitter)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.extra_headers[b'From'], submitter_email)
        self.assertSetEqual(set(message.to), {
         admin_email, submitter_email})

    def test_change_ownership_email_not_submitter(self):
        """Testing sending a review request e-mail when the owner is being
        changed by someone else
        """
        admin_user = User.objects.get(username=b'admin')
        admin_email = build_email_address_for_user(admin_user)
        review_request = self.create_review_request(public=True)
        submitter = review_request.submitter
        submitter_email = build_email_address_for_user(submitter)
        draft = ReviewRequestDraft.create(review_request)
        draft.target_people = [
         admin_user, submitter]
        draft.owner = admin_user
        draft.save()
        review_request.publish(admin_user)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.extra_headers[b'From'], admin_email)
        self.assertSetEqual(set(message.to), {
         admin_email, submitter_email})

    def _get_sender(self, user):
        return build_email_address(full_name=user.get_full_name(), email=self.sender)


class ReviewRequestSiteRootURLTests(SiteRootURLTestsMixin, ReviewRequestEmailTestsMixin, TestCase):
    """Tests for Bug 4612 related to review request and review e-mails."""

    @override_settings(**SiteRootURLTestsMixin.CUSTOM_SITE_ROOT_SETTINGS)
    def test_review_request_email_site_root_custom(self):
        """Testing review request e-mail includes site root only once with
        custom site root
        """
        review_request = self.create_review_request()
        review_request.publish(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        absolute_url = review_request.get_absolute_url()
        review_request_url = build_server_url(absolute_url)
        bad_review_request_url = b'%s%s' % (get_server_url(), absolute_url)
        self.assertNotIn(self.BAD_SITE_ROOT, review_request_url)
        self.assertIn(self.BAD_SITE_ROOT, bad_review_request_url)
        self.assertIn(review_request_url, message.body)
        self.assertNotIn(bad_review_request_url, message.body)
        for alternative in message.alternatives:
            self.assertNotIn(bad_review_request_url, alternative)

    def test_review_request_email_site_root_default(self):
        """Testing review request e-mail includes site root only once with
        default site root
        """
        review_request = self.create_review_request()
        review_request.publish(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertNotIn(b'example.com//', message.body)
        for alternative in message.alternatives:
            self.assertNotIn(b'example.com//', alternative[0])

    @add_fixtures([b'test_site'])
    @override_settings(**SiteRootURLTestsMixin.CUSTOM_SITE_ROOT_SETTINGS)
    def test_review_request_email_site_root_custom_with_localsite(self):
        """Testing review request e-mail includes site root only once with
        custom site root and a LocalSite
        """
        review_request = self.create_review_request(with_local_site=True)
        with self.settings(SITE_ROOT=b'/foo/'):
            review_request.publish(review_request.submitter)
            absolute_url = review_request.get_absolute_url()
            bad_review_request_url = b'%s%s' % (get_server_url(), absolute_url)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        review_request_url = build_server_url(absolute_url)
        self.assertNotIn(self.BAD_SITE_ROOT, review_request_url)
        self.assertIn(self.BAD_SITE_ROOT, bad_review_request_url)
        self.assertIn(review_request_url, message.body)
        self.assertNotIn(bad_review_request_url, message.body)
        for alternative in message.alternatives:
            self.assertNotIn(bad_review_request_url, alternative[0])

    @add_fixtures([b'test_site'])
    def test_review_request_email_site_root_default_with_localsite(self):
        """Testing review request e-mail includes site root only once with
        default site root and a LocalSite
        """
        review_request = self.create_review_request()
        review_request.publish(review_request.submitter)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertNotIn(b'example.com//', message.body)
        for alternative in message.alternatives:
            self.assertNotIn(b'example.com//', alternative[0])

    @override_settings(**SiteRootURLTestsMixin.CUSTOM_SITE_ROOT_SETTINGS)
    def test_review_email_site_root_custom(self):
        """Testing review  e-mail includes site root only once with custom site
        root
        """
        review_request = self.create_review_request(public=True)
        review = self.create_review(review_request=review_request)
        review.publish(review.user)
        review_url = build_server_url(review.get_absolute_url())
        bad_review_url = b'%s%s' % (get_server_url(), review.get_absolute_url())
        self.assertNotIn(self.BAD_SITE_ROOT, review_url)
        self.assertIn(self.BAD_SITE_ROOT, bad_review_url)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertNotIn(bad_review_url, message.body)
        for alternative in message.alternatives:
            self.assertNotIn(bad_review_url, alternative[0])

    def test_review_email_site_root_default(self):
        """Testing review e-mail includes site root only once with default site
        root
        """
        review_request = self.create_review_request(public=True)
        review = self.create_review(review_request=review_request)
        review.publish(review.user)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertNotIn(b'example.com//', message.body)
        for alternative in message.alternatives:
            self.assertNotIn(b'example.com//', alternative[0])

    @add_fixtures([b'test_site'])
    @override_settings(**SiteRootURLTestsMixin.CUSTOM_SITE_ROOT_SETTINGS)
    def test_review_email_site_root_custom_with_localsite(self):
        """Testing review  e-mail includes site root only once with custom site
        root and a LocalSite
        """
        review_request = self.create_review_request(public=True, with_local_site=True)
        review = self.create_review(review_request=review_request)
        review.publish(review.user)
        review_url = build_server_url(review.get_absolute_url())
        bad_review_url = b'%s%s' % (get_server_url(), review.get_absolute_url())
        self.assertNotIn(self.BAD_SITE_ROOT, review_url)
        self.assertIn(self.BAD_SITE_ROOT, bad_review_url)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertNotIn(bad_review_url, message.body)
        for alternative in message.alternatives:
            self.assertNotIn(bad_review_url, alternative[0])

    @add_fixtures([b'test_site'])
    def test_review_email_site_root_default_with_localsite(self):
        """Testing review e-mail includes site root only once with default site
        root and a LocalSite
        """
        review_request = self.create_review_request(public=True, with_local_site=True)
        review = self.create_review(review_request=review_request)
        review.publish(review.user)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertNotIn(b'example.com//', message.body)
        for alternative in message.alternatives:
            self.assertNotIn(b'example.com//', alternative[0])


class WebAPITokenEmailTestsMixin(EmailTestHelper):
    """A mixin for web hook-related e-mail tests."""
    email_siteconfig_settings = {b'mail_send_new_user_mail': False}

    def setUp(self):
        super(WebAPITokenEmailTestsMixin, self).setUp()
        self.user = User.objects.create_user(username=b'test-user', first_name=b'Sample', last_name=b'User', email=b'test-user@example.com')
        self.assertEqual(len(mail.outbox), 0)


class WebAPITokenEmailTests(WebAPITokenEmailTestsMixin, TestCase):
    """Unit tests for WebAPIToken creation e-mails."""

    def test_create_token(self):
        """Testing sending e-mail when a new API Token is created"""
        webapi_token = WebAPIToken.objects.generate_token(user=self.user, note=b'Test', policy={})
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        html_body = email.alternatives[0][0]
        partial_token = b'%s...' % webapi_token.token[:10]
        self.assertEqual(email.subject, b'New Review Board API token created')
        self.assertEqual(email.from_email, self.sender)
        self.assertEqual(email.extra_headers[b'From'], settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(email.to[0], build_email_address_for_user(self.user))
        self.assertNotIn(webapi_token.token, email.body)
        self.assertNotIn(webapi_token.token, html_body)
        self.assertIn(partial_token, email.body)
        self.assertIn(partial_token, html_body)
        self.assertIn(b'A new API token has been added', email.body)
        self.assertIn(b'A new API token has been added', html_body)

    def test_create_token_no_email(self):
        """Testing WebAPIToken.objects.generate_token does not send e-mail
        when auto_generated is True
        """
        WebAPIToken.objects.generate_token(user=self.user, note=b'Test', policy={}, auto_generated=True)
        self.assertEqual(len(mail.outbox), 0)

    def test_update_token(self):
        """Testing sending e-mail when an existing API Token is updated"""
        webapi_token = WebAPIToken.objects.generate_token(user=self.user, note=b'Test', policy={})
        mail.outbox = []
        webapi_token.save()
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        html_body = email.alternatives[0][0]
        partial_token = b'%s...' % webapi_token.token[:10]
        self.assertEqual(email.subject, b'Review Board API token updated')
        self.assertEqual(email.from_email, self.sender)
        self.assertEqual(email.extra_headers[b'From'], settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(email.to[0], build_email_address_for_user(self.user))
        self.assertNotIn(webapi_token.token, email.body)
        self.assertNotIn(webapi_token.token, html_body)
        self.assertIn(partial_token, email.body)
        self.assertIn(partial_token, html_body)
        self.assertIn(b'One of your API tokens has been updated', email.body)
        self.assertIn(b'One of your API tokens has been updated', html_body)

    def test_delete_token(self):
        """Testing sending e-mail when an existing API Token is deleted"""
        webapi_token = WebAPIToken.objects.generate_token(user=self.user, note=b'Test', policy={})
        mail.outbox = []
        webapi_token.delete()
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        html_body = email.alternatives[0][0]
        self.assertEqual(email.subject, b'Review Board API token deleted')
        self.assertEqual(email.from_email, self.sender)
        self.assertEqual(email.extra_headers[b'From'], settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(email.to[0], build_email_address_for_user(self.user))
        self.assertIn(webapi_token.token, email.body)
        self.assertIn(webapi_token.token, html_body)
        self.assertIn(b'One of your API tokens has been deleted', email.body)
        self.assertIn(b'One of your API tokens has been deleted', html_body)


class WebAPITokenSiteRootURLTests(SiteRootURLTestsMixin, WebAPITokenEmailTestsMixin, TestCase):
    """Tests for Bug 4612 related to web API token e-mails."""

    @override_settings(**SiteRootURLTestsMixin.CUSTOM_SITE_ROOT_SETTINGS)
    def test_create_token_site_root_custom(self):
        """Testing WebAPI Token e-mails include site root only once with custom
        site root
        """
        WebAPIToken.objects.generate_token(user=self.user, note=b'Test', policy={})
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertNotIn(self.BAD_SITE_ROOT, message.body)
        for alternative in message.alternatives:
            self.assertNotIn(self.BAD_SITE_ROOT, alternative[0])

    def test_create_token_site_root_default(self):
        """Testing WebAPI Token e-mails include site root only once with
        default site root
        """
        WebAPIToken.objects.generate_token(user=self.user, note=b'Test', policy={})
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertNotIn(b'example.com//', message.body)
        for alternative in message.alternatives:
            self.assertNotIn(b'example.com//', alternative[0])

    @add_fixtures([b'test_site'])
    @override_settings(**SiteRootURLTestsMixin.CUSTOM_SITE_ROOT_SETTINGS)
    def test_create_token_site_root_custom_with_localsite(self):
        """Testing WebAPI Token e-mails include site root only once with custom
        site root and a LocalSite
        """
        local_site = LocalSite.objects.get(pk=1)
        WebAPIToken.objects.generate_token(user=self.user, note=b'Test', policy={}, local_site=local_site)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertNotIn(self.BAD_SITE_ROOT, message.body)
        for alternative in message.alternatives:
            self.assertNotIn(self.BAD_SITE_ROOT, alternative[0])

    @add_fixtures([b'test_site'])
    def test_create_token_site_root_default_with_localsite(self):
        """Testing WebAPI Token e-mails include site root only once with
        default site root and a LocalSite
        """
        local_site = LocalSite.objects.get(pk=1)
        WebAPIToken.objects.generate_token(user=self.user, note=b'Test', policy={}, local_site=local_site)
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertNotIn(b'example.com//', message.body)
        for alternative in message.alternatives:
            self.assertNotIn(b'example.com//', alternative[0])