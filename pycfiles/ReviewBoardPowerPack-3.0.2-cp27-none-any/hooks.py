# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/extension/hooks.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from django.utils import six
from django.utils.translation import ugettext_lazy as _, ungettext
from djblets.extensions.hooks import ExtensionHook, ExtensionHookPoint
from djblets.webapi.errors import PERMISSION_DENIED
from reviewboard.extensions.hooks import TemplateHook
from reviewboard.reviews.models import ReviewRequest
from reviewboard.webapi.resources import resources
try:
    from reviewboard.reviews.forms import NewReviewRequestForm
except ImportError:
    NewReviewRequestForm = None

from rbpowerpack.extension.errors import CannotPostReviewRequestError

class CanPostReviewRequestHook(ExtensionHook):
    """Allows blocking the posting of review requests against a repository.

    This monkey patches the Review Request API posting and Review Request
    object creation to allow a hosting service or SCMTool to block the posting
    of a review request for a user.

    In the future, when Review Board gains native functionality for this,
    we'll be able to detect that and only perform these operations on older
    versions.
    """
    __metaclass__ = ExtensionHookPoint

    def __init__(self, extension):
        super(CanPostReviewRequestHook, self).__init__(extension)
        self._orig_api_create_review_request = resources.review_request.create
        resources.review_request.create = self._api_create_review_request
        self._orig_create_review_request = ReviewRequest.objects.create
        ReviewRequest.objects.create = self._create_review_request

    def shutdown(self):
        super(CanPostReviewRequestHook, self).shutdown()
        ReviewRequest.objects.create = self._orig_create_review_request
        resources.review_request.create = self._orig_api_create_review_request

    def _create_review_request(self, user, repository, *args, **kwargs):
        if repository:
            if repository.hosting_account and repository.hosting_account.service:
                service = repository.hosting_account.service
                if hasattr(service, b'can_user_post') and not service.can_user_post(user, repository):
                    raise CannotPostReviewRequestError(service.name)
            else:
                tool = repository.tool
                if hasattr(tool.get_scmtool_class(), b'can_user_post') and not repository.get_scmtool().can_user_post(user):
                    raise CannotPostReviewRequestError(tool.name)
        return self._orig_create_review_request(user, repository, *args, **kwargs)

    def _api_create_review_request(self, *args, **kwargs):
        try:
            return self._orig_api_create_review_request(*args, **kwargs)
        except CannotPostReviewRequestError as e:
            return PERMISSION_DENIED.with_message(six.text_type(e))

    def _form_create(self, form, *args, **kwargs):
        try:
            return self._orig_form_create(form, *args, **kwargs)
        except CannotPostReviewRequestError as e:
            form.errors[b'repository'] = six.text_type(e)
            raise


class LicenseBannerTemplateHook(TemplateHook):
    """A template hook which shows a banner to admins about the license."""

    def __init__(self, extension):
        super(LicenseBannerTemplateHook, self).__init__(extension, b'base-after-navbar', b'powerpack/license-banner.html')

    def get_extra_context(self, request, context):
        """Return extra context for the hook.

        Args:
            request (django.http.HttpRequest):
                The HTTP request.

            context (dict):
                Existing context for the template.

        Returns:
            dict:
            Extra context to add when rendering the template.
        """
        license = self.extension.license
        if license and not license.unlicensed:
            days_left = license.time_left.days
            if license.trial and license.expired:
                state = b'trial-expired'
                title = _(b'Your Power Pack trial has expired.')
            elif license.trial and days_left < 7:
                state = b'trial-expiring'
                title = ungettext(b'Your Power Pack trial is expiring in %s day', b'Your Power Pack trial is expiring in %s days', days_left) % days_left
            elif not license.trial and license.expired:
                state = b'paid-expired'
                title = _(b'Your Power Pack license has expired.')
            elif not license.trial and days_left < 30:
                state = b'paid-expiring'
                title = ungettext(b'Your Power Pack license is expiring in %s day', b'Your Power Pack license is expiring in %s days', days_left) % days_left
            else:
                state = b'valid'
                title = None
        else:
            days_left = None
            state = b'no-license'
            title = _(b'Start your 30-day Power Pack trial.')
        show_banner = request.user.is_staff or state in ('trial-expired', 'paid-expired')
        return {b'days_left': days_left, 
           b'is_staff': request.user.is_staff, 
           b'show_banner': show_banner, 
           b'state': state, 
           b'title': title, 
           b'trial_url': self.extension.get_trial_url(request)}