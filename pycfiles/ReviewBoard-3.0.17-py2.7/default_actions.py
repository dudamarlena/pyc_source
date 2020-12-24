# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/default_actions.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from reviewboard.reviews.actions import BaseReviewRequestAction, BaseReviewRequestMenuAction
from reviewboard.reviews.features import general_comments_feature
from reviewboard.reviews.models import ReviewRequest
from reviewboard.site.urlresolvers import local_site_reverse
from reviewboard.urls import diffviewer_url_names

class CloseMenuAction(BaseReviewRequestMenuAction):
    """A menu action for closing the corresponding review request."""
    action_id = b'close-review-request-action'
    label = _(b'Close')

    def should_render(self, context):
        review_request = context[b'review_request']
        return review_request.status == ReviewRequest.PENDING_REVIEW and (context[b'request'].user.pk == review_request.submitter_id or context[b'perms'][b'reviews'][b'can_change_status'] and review_request.public)


class SubmitAction(BaseReviewRequestAction):
    """An action for submitting the review request."""
    action_id = b'submit-review-request-action'
    label = _(b'Submitted')

    def should_render(self, context):
        return context[b'review_request'].public


class DiscardAction(BaseReviewRequestAction):
    """An action for discarding the review request."""
    action_id = b'discard-review-request-action'
    label = _(b'Discarded')


class DeleteAction(BaseReviewRequestAction):
    """An action for permanently deleting the review request."""
    action_id = b'delete-review-request-action'
    label = _(b'Delete Permanently')

    def should_render(self, context):
        return context[b'perms'][b'reviews'][b'delete_reviewrequest']


class UpdateMenuAction(BaseReviewRequestMenuAction):
    """A menu action for updating the corresponding review request."""
    action_id = b'update-review-request-action'
    label = _(b'Update')

    def should_render(self, context):
        review_request = context[b'review_request']
        return review_request.status == ReviewRequest.PENDING_REVIEW and (context[b'request'].user.pk == review_request.submitter_id or context[b'perms'][b'reviews'][b'can_edit_reviewrequest'])


class UploadDiffAction(BaseReviewRequestAction):
    """An action for updating/uploading a diff for the review request."""
    action_id = b'upload-diff-action'

    def get_label(self, context):
        """Return this action's label.

        The label will change depending on whether or not the corresponding
        review request already has a diff.

        Args:
            context (django.template.Context):
                The collection of key-value pairs from the template.

        Returns:
            unicode: The label that displays this action to the user.
        """
        review_request = context[b'review_request']
        draft = review_request.get_draft(context[b'request'].user)
        if draft and draft.diffset or review_request.get_diffsets():
            return _(b'Update Diff')
        return _(b'Upload Diff')

    def should_render(self, context):
        """Return whether or not this action should render.

        If the corresponding review request has a repository, then an upload
        diff form exists, so we should render this UploadDiffAction.

        Args:
            context (django.template.Context):
                The collection of key-value pairs available in the template
                just before this action is to be rendered.

        Returns:
            bool: Determines if this action should render.
        """
        return context[b'review_request'].repository_id is not None


class UploadFileAction(BaseReviewRequestAction):
    """An action for uploading a file for the review request."""
    action_id = b'upload-file-action'
    label = _(b'Add File')


class DownloadDiffAction(BaseReviewRequestAction):
    """An action for downloading a diff from the review request."""
    action_id = b'download-diff-action'
    label = _(b'Download Diff')

    def get_url(self, context):
        """Return this action's URL.

        Args:
            context (django.template.Context):
                The collection of key-value pairs from the template.

        Returns:
            unicode: The URL to invoke if this action is clicked.
        """
        match = context[b'request'].resolver_match
        if match.url_name in diffviewer_url_names:
            return b'raw/'
        return local_site_reverse(b'raw-diff', context[b'request'], kwargs={b'review_request_id': context[b'review_request'].display_id})

    def get_hidden(self, context):
        """Return whether this action should be initially hidden to the user.

        Args:
            context (django.template.Context):
                The collection of key-value pairs from the template.

        Returns:
            bool: Whether this action should be initially hidden to the user.
        """
        match = context[b'request'].resolver_match
        if match.url_name in diffviewer_url_names:
            return match.url_name == b'view-interdiff'
        return super(DownloadDiffAction, self).get_hidden(context)

    def should_render(self, context):
        """Return whether or not this action should render.

        Args:
            context (django.template.Context):
                The collection of key-value pairs available in the template
                just before this action is to be rendered.

        Returns:
            bool: Determines if this action should render.
        """
        review_request = context[b'review_request']
        request = context[b'request']
        match = request.resolver_match
        if match.url_name in diffviewer_url_names:
            return True
        else:
            return review_request.repository_id is not None


class EditReviewAction(BaseReviewRequestAction):
    """An action for editing a review intended for the review request."""
    action_id = b'review-action'
    label = _(b'Review')

    def should_render(self, context):
        return context[b'request'].user.is_authenticated()


class AddGeneralCommentAction(BaseReviewRequestAction):
    """An action for adding a new general comment to a review."""
    action_id = b'general-comment-action'
    label = _(b'Add General Comment')

    def should_render(self, context):
        request = context[b'request']
        return request.user.is_authenticated() and general_comments_feature.is_enabled(request=request)


class ShipItAction(BaseReviewRequestAction):
    """An action for quickly approving the review request without comments."""
    action_id = b'ship-it-action'
    label = _(b'Ship It!')

    def should_render(self, context):
        return context[b'request'].user.is_authenticated()


def get_default_actions():
    """Return a copy of all the default actions.

    Returns:
        list of BaseReviewRequestAction: A copy of all the default actions.
    """
    return [
     CloseMenuAction([
      SubmitAction(),
      DiscardAction(),
      DeleteAction()]),
     UpdateMenuAction([
      UploadDiffAction(),
      UploadFileAction()]),
     DownloadDiffAction(),
     EditReviewAction(),
     AddGeneralCommentAction(),
     ShipItAction()]