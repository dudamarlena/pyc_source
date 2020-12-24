# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/privacy/consent/common.py
# Compiled at: 2019-06-12 01:17:17
"""Common consent requirements for use in applications.

This provides some basic definitions with standard requirement IDs that can be
further customized by applications needing to offer consent for services.
"""
from __future__ import unicode_literals
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _, ugettext
from djblets.privacy.consent.base import BaseConsentRequirement

class BaseGravatarConsentRequirement(BaseConsentRequirement):
    """Base consent requirement for Gravatar usage.

    This supplies a requirement ID, name, default summary, and default data
    use description for Gravatar consent requirements. Subclasses should
    provide their own intent and data use descriptions.
    """
    requirement_id = b'gravatar'
    name = _(b'Gravatar')
    summary = _(b"We'd like to use Gravatar.com for your avatars")
    data_use_description = _(b"Gravatar will receive a one-way hashed version of your e-mail address. This is not personally identifiable, but could potentially be used to track you across multiple sites that use Gravatar. Gravatar only has an avatar for you if you've set one with their service.")


class BaseIntercomConsentRequirement(BaseConsentRequirement):
    """Base consent requirement for Intercom usage.

    This supplies a requirement ID, name, and default summary for Intercom
    consent requirements. Subclasses should provide their own intent and
    data use descriptions.
    """
    requirement_id = b'intercom'
    name = b'Intercom'
    summary = _(b"We'd like to support and track activity using Intercom")


class PolicyConsentRequirement(BaseConsentRequirement):
    """A consent requirement for asking users to acknowledge policies."""
    requirement_id = b'policies'
    allow_text = _(b'Accept')
    allowed_text = _(b'Accepted')
    block_text = _(b'Reject')
    blocked_text = _(b'Rejected')

    def __init__(self, privacy_policy_url, terms_of_service_url, site_admin_email=None, reject_instructions=None):
        """Initialize the consent requirement.

        Args:
            privacy_policy_url (unicode):
                The URL to the privacy policy, if applicable.

            terms_of_service (unicode):
                The URL to the terms of service, if applicable.

            site_admin_email (unicode, optional):
                The e-mail address of the site admin. This is only used if
                ``reject_instructions`` is provided.

            reject_instructions (unicode, optional):
                Instructions for how the user should proceed if they do not
                accept the policies.

        """
        if site_admin_email is None and reject_instructions is None:
            raise ValueError(b'Either reject_instructions or site_admin_email must be provided.')
        self.privacy_policy_url = privacy_policy_url
        self.terms_of_service_url = terms_of_service_url
        self.site_admin_email = site_admin_email
        self.reject_instructions = reject_instructions
        return

    @property
    def name(self):
        """The name of the requirement."""
        if self.privacy_policy_url and self.terms_of_service_url:
            return ugettext(b'Privacy Policy and Terms of Service')
        if self.privacy_policy_url:
            return ugettext(b'Privacy Policy')
        if self.terms_of_service_url:
            return ugettext(b'Terms of Service')

    @property
    def summary(self):
        """A brief summary of the requirement."""
        if self.privacy_policy_url and self.terms_of_service_url:
            return ugettext(b'Accept the Privacy Policy and Terms of Service')
        if self.privacy_policy_url:
            return ugettext(b'Accept the Privacy Policy')
        if self.terms_of_service_url:
            return ugettext(b'Accept the Terms of Service')

    @property
    def intent_description(self):
        """A short description of why the requirement is needed."""
        if self.reject_instructions:
            reject_instructions = self.reject_instructions
        else:
            reject_instructions = ugettext(b'You will not be able to use the service without accepting this. If you disagree, please <a href="mailto:%s">contact</a> your server administrator.') % self.site_admin_email
        if self.privacy_policy_url and self.terms_of_service_url:
            return mark_safe(ugettext(b'You must accept the <a href="%s">Privacy Policy</a> and <a href="%s">Terms of Service</a>. %s') % (
             self.privacy_policy_url, self.terms_of_service_url,
             reject_instructions))
        if self.privacy_policy_url:
            return mark_safe(ugettext(b'You must accept the <a href="%s">Privacy Policy</a>. %s') % (
             self.privacy_policy_url, reject_instructions))
        if self.terms_of_service_url:
            return mark_safe(ugettext(b'You must accept the <a href="%s">Terms of Service</a>. %s') % (
             self.terms_of_service_url, reject_instructions))