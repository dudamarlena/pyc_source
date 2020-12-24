# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/features.py
# Compiled at: 2020-02-11 04:03:56
"""Feature definitions for reviews."""
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from djblets.features import Feature, FeatureLevel

class ClassBasedActionsFeature(Feature):
    """A feature for class-based actions.

    With this enabled, extensions may use the new class-based action classes
    instead of the old-style dict actions.
    """
    feature_id = b'reviews.class_based_actions'
    name = _(b'Class-Based Actions')
    level = FeatureLevel.UNAVAILABLE
    summary = _(b'Allow using class-based actions with extension hooks.')


class GeneralCommentsFeature(Feature):
    """A feature for general comments.

    General comments allow comments to be created directly on a review request
    without accompanying file attachment or diff. These can be used to raise
    issues with the review request itself, such as its summary or description,
    or general implementation issues.
    """
    feature_id = b'reviews.general_comments'
    name = _(b'General Comments')
    level = FeatureLevel.STABLE
    summary = _(b'Allow comments on review requests without an associated file attachment or diff.')


class IssueVerificationFeature(Feature):
    """A feature for issue verification.

    Issue verification allows reviewers to mark that an issue requires
    verification before closing. In this case, the author of the change will be
    able to mark the issue as "Fixed", but then the original author of the
    comment will need to verify it before the issue is closed.
    """
    feature_id = b'reviews.issue_verification'
    name = _(b'Issue Verification')
    level = FeatureLevel.STABLE
    summary = _(b'Allow comment authors to require that issues be verified by them before being closed')


class StatusUpdatesFeature(Feature):
    """A feature for status updates.

    A status update is a way for third-party tools to provide feedback on a
    review request. In the past, this was done just as a normal review. Status
    updates allow those tools (via some integration like Review Bot) to mark
    their state (such as pending, success, failure, or error) and then
    associate that with a review.
    """
    feature_id = b'reviews.status_updates'
    name = _(b'Status Updates')
    level = FeatureLevel.STABLE
    summary = _(b'A way for external tools to do checks on a review request and report the results of those checks.')


class_based_actions_feature = ClassBasedActionsFeature()
general_comments_feature = GeneralCommentsFeature()
issue_verification_feature = IssueVerificationFeature()
status_updates_feature = StatusUpdatesFeature()